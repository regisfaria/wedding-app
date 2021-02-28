import os
import json
import pathlib

from datetime import datetime as dt
from helpers.isTokenExpired import isTokenExpired
from dotenv import load_dotenv
from providers.hashProvider import HashProvider
from uuid import uuid4
from flask import Flask, request as flaskRequest, jsonify
from flask_cors import CORS
from flask_restful import Api, Resource
from database.index import Database
from aws.S3 import S3

# models imports
from models.Users import Users, EmbeddedUsers
from models.Posts import Posts
from models.Comments import Comments
from models.Tokens import Tokens

# config
load_dotenv()
app = Flask(__name__)
CORS(app)
api = Api(app)
database = Database(app)

bucketURL = os.getenv('AWS_BUCKET_URL')
rootDir = os.getenv('ROOT_DIR')

def isAuthenticated(token):
  validToken = Tokens.objects(token=token).first()

  if not validToken:
    return False, None
  if isTokenExpired(validToken['createdAt']):
    return False, None

  return True, validToken['user']

########## POST REQUESTS ##########

@app.route('/users', methods=['POST'])
def create_user():
  request = json.loads(flaskRequest.data)

  userExists = Users.objects(username=request['username']).first()

  if userExists:
    return 'Username already in use', 400

  hashProvider = HashProvider()

  encryptedPassword = hashProvider.encrypt(request['password'])

  user = Users(name=request['name'],
              username=request['username'],
              password=encryptedPassword,
              privileges=request['privileges'],
              imageUrl=f'{bucketURL}/avatars/standard-picture.jpg',
              imageKey='standard')

  user.save()

  return jsonify({"data": user})

@app.route('/posts', methods=['POST'])
def create_post():
  userAuthenticated, user = isAuthenticated(flaskRequest.headers['authorization'])

  if userAuthenticated:
    description = flaskRequest.form.get('description')
    title = flaskRequest.form.get('title')

    # save img tmp
    image = flaskRequest.files['image']
    hashedImageName = f'{uuid4()}-{image.filename.replace(" ", "").replace("(", "").replace(")", "")}'
    imageKey = f'gallery/{hashedImageName}'
    tmpPath = f'{rootDir}/tmp/{hashedImageName}'
    image.save(tmpPath)

    # upload
    s3 = S3()
    s3.uploadFile(tmpPath, f'gallery/{hashedImageName}')
    os.remove(tmpPath)

    post = Posts(imageUrl=f'{bucketURL}/gallery/{hashedImageName}',
                imageKey=imageKey,
                author=user['id'],
                description=description,
                title=title)

    post.save()

    return jsonify({"data": post})
  else:
    return "Token not found or expired. Please login again.", 403

@app.route('/comments', methods=['POST'])
def create_comment():
  userAuthenticated, user = isAuthenticated(flaskRequest.headers['authorization'])

  if userAuthenticated:
    request = json.loads(flaskRequest.data)

    post = Posts.objects(id=request['postId']).first()

    if not post:
      return 'No post was found with this id', 400

    comment = Comments(content=request['content'], author=user['id'], identifier=f'{uuid4()}', authorName=user['name'], imageUrl=user['imageUrl'])

    post['comments'].append(comment)
    post.save()

    return jsonify({"data": post})
  else:
    return "Token missing or expired. Please login again.", 403

@app.route('/auth', methods=['POST'])
def authenticate():
  request = json.loads(flaskRequest.data)

  user = Users.objects(username=request['username']).first()

  if not user:
    return 'Wrong username. Try again.',  400

  hashProvider = HashProvider()
  passwordMatch = hashProvider.compareHashs(request['password'], user['password'])

  if not passwordMatch:
    return 'Wrong password. Try again.', 400

  tokenExists = Tokens.objects(user=user['id']).first()

  if (tokenExists):
    tokenExists.delete()

  token = Tokens(token=f'{uuid4()}', createdAt=f'{dt.now()}', user=user['id'])
  token.save()

  return jsonify({"token": token["token"], "user": user})

########## GET REQUESTS ##########

@app.route('/posts/<int:isActive>', methods=['GET'])
def getPosts(isActive):
  userAuthenticated, user = isAuthenticated(flaskRequest.headers['authorization'])

  if userAuthenticated:
    active = True if isActive == 1 else False

    posts = Posts.objects(active=active)
    

    for post in posts:  
      author = Users.objects(id=post['author']['id']).first()
      authorData = EmbeddedUsers(name=author['name'], imageUrl=author['imageUrl'])
      post["authorData"] = authorData
      post.save()

    return jsonify({"data": posts})
  else:
    return "Token missing or expired. Please login again.", 403

########## PATCH REQUESTS ##########

@app.route('/posts', methods=['PATCH'])
def changePostActiveStatus():
  userAuthenticated, user = isAuthenticated(flaskRequest.headers['authorization'])

  if userAuthenticated:
    request = json.loads(flaskRequest.data)

    post = Posts.objects(id=request["id"]).first()

    if not post:
      return "No post was found with that ID.", 400

    post['active'] = request['active']
    post.save()

    return jsonify({"data": post})
  else:
    return "Token missing or expired. Please login again.", 403

@app.route('/posts/like/<string:postId>', methods=['PATCH'])
def postLike(postId):
  userAuthenticated, user = isAuthenticated(flaskRequest.headers['authorization'])

  if userAuthenticated:
    post = Posts.objects(id=postId).first()
    if not post:
      return "No post was found with that ID.", 400

    post['likes'] += 1
    post.save()

    return jsonify({"data": post})
  else:
    return "Token missing or expired. Please login again.", 403

@app.route('/posts/dislike/<string:postId>', methods=['PATCH'])
def postDislike(postId):
  userAuthenticated, user = isAuthenticated(flaskRequest.headers['authorization'])

  if userAuthenticated:
    post = Posts.objects(id=postId).first()
    if not post:
      return "No post was found with that ID.", 400

    if post['likes'] > 0:
      post['likes'] -= 1
      post.save()

    return jsonify({"data": post})
  else:
    return "Token missing or expired. Please login again.", 403

@app.route('/users', methods=['PATCH'])
def uploadUserPicture():
  userAuthenticated, userData = isAuthenticated(flaskRequest.headers['authorization'])

  if userAuthenticated:
    user = Users.objects(id=userData['id']).first()

    if not user:
      return "No user was found with that ID.", 400

    s3 = S3()
    if user['imageKey'] != 'standard':
      print(user["imageKey"])
      print(type(user["imageKey"]))
      s3.deleteFile(user["imageKey"])

    image = flaskRequest.files['image']
    hashedImageName = f'{uuid4()}-{image.filename.replace(" ", "").replace("(", "").replace(")", "")}'
    imageKey = f'avatars/{hashedImageName}'
    tmpPath = f'{rootDir}/tmp/{hashedImageName}'
    image.save(tmpPath)

    s3.uploadFile(tmpPath, f'avatars/{hashedImageName}')
    os.remove(tmpPath)

    user['imageKey'] = imageKey
    user['imageUrl'] = f'{bucketURL}/avatars/{hashedImageName}'

    user.save()

    return jsonify({"data": user})
  else:
    return "Token missing or expired. Please login again.", 403
  
########## DELETE REQUESTS ##########
@app.route('/posts/<string:postId>', methods=['DELETE'])
def deletePost(postId):
  token = flaskRequest.headers['authorization']
  userAuthenticated, user = isAuthenticated(token)

  if userAuthenticated:
    post = Posts.objects(id=postId).first()

    if not post:
      return "Can't delete an unexisting post", 400

    if post['author']['id'] != user['id']:
      return "Only the author of that post can delete it.", 400

    s3 = S3()
    s3.deleteFile(post['imageKey'])

    post.delete()

    return "Deleted", 204
  else:
    return "Token missing or expired. Please login again.", 403

if __name__ == '__main__':
  # [] remove debug later when production
  app.run(debug=True)
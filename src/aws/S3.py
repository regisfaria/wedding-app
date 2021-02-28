import boto3
import os

from dotenv import load_dotenv
from uuid import uuid4

load_dotenv()

class S3():
  def __init__(self):
    awsKey = os.getenv('AWS_ACCESS_KEY_ID')
    secret = os.getenv('AWS_SECRET_ACCESS_KEY')

    self.client = boto3.client('s3', aws_access_key_id=awsKey, aws_secret_access_key=secret, region_name='us-east-1')


  def uploadFile(self, filePath, fileKey):
    # Upload the file
    bucket = os.getenv('AWS_BUCKET_NAME')
    try:
        response = self.client.upload_file(filePath, bucket, fileKey, ExtraArgs={'ACL':'public-read', 'ContentType':'image/jpeg', 'ContentDisposition':'inline; filename=filename.jpg'})
        return True
    except Exception as e:
        return False

  def deleteFile(self, fileKey):
    bucket = os.getenv('AWS_BUCKET_NAME')
    try:
        response = self.client.delete_object(Bucket=bucket, Key=fileKey)
        return True
    except Exception as e:
        return False
  


# Route Documentation
Here you will find documentation to be able to make requests for this API.

# Summary
1. [Auth](#auth)
2. [Find Posts](#findPost)
3. [Create User](#createUser)
4. [Create Post](#createPost)
5. [Create Comment](#createComment)
6. [Update Post Active Status](#updateActivePost)
7. [Update User Avatar](#updateUserAvatar)
8. [Like Post](#like)
9. [Delete Post](#deletePost)


## **POST** Auth - {{ _.baseURL }}/auth <a id="auth"></a>
### BODY PARAMS
| Parameter | Required |
| ------ | ----------- |
| username   | true |
| password   | true |

```typescript
interface Body {
  username: string;
  password: string;
}
```

### Example
```json
// request.body
{
	"username": "gsfp",
	"password": "1234567"
}

// response
{
  "token": "df8835a5-350e-41a3-b8f3-255056de699a",
  "user": {
    "_id": {
      "$oid": "603aeb956ee34adba1e0ada9"
    },
    "imageKey": "standard",
    "imageUrl": "https://wedding-app-anchor-loans-test.s3.amazonaws.com/avatars/standard-picture.jpg",
    "name": "Giorgio",
    "password": "1234567",
    "privileges": "user",
    "username": "gsfp"
  }
}
```

## **GET** Find Posts - {{ _.baseURL }}/posts/:active <a id="findPost"></a>
### AUTH REQUIRED
To use auth, the request must contain the following header:

**"authorization": "token"**

Token is an uuid generated throught the auth route. 

### ROUTE PARAMS
| Parameter | Required |
| ------ | ----------- |
| active   | true |

The url would look like:
- {baseurl}/posts/:active

Where active is our required param and accept the following values:

| Parameter | Value |
| ------ | ----------- |
| active   | 1 OR 0 |

### Example
```json
// url
"{{ _.baseURL }}/posts/1"

// response
{
  "data": [
    {
      "_id": {
        "$oid": "603aebfb6ee34adba1e0adac"
      },
      "active": true,
      "author": {
        "$oid": "603aeb7b6ee34adba1e0ada8"
      },
      "comments": [
        {
          "author": {
            "$oid": "603aeb956ee34adba1e0ada9"
          },
          "content": "Concordo demais!",
          "identifier": "4bde31ec-3a87-4496-9a6a-57e8ad8c4b02"
        }
      ],
      "description": "Must be in a place like this!",
      "imageKey": "gallery/Wedding-2.jpg",
      "imageUrl": "https://wedding-app-anchor-loans-test.s3.amazonaws.com/gallery/7fbc3a13-4542-457b-b460-39f87b59c2bd-Wedding-2.jpg",
      "likes": 1,
      "title": "Nice place"
    }
  ]
}
```

## **POST** Create User - {{ _.baseURL }}/users <a id="createUser"></a>
### BODY PARAMS
| Parameter | Required |
| ------ | ----------- |
| name   | true |
| username   | true |
| password   | true |
| privileges   | true |

```typescript
interface Body {
  name: string;
  username: string;
  password: string;
  privileges: 'user' | 'admin';
}
```

### Example
```json
// request.body
{
	"name": "Giorgio",
	"username": "gsfp",
	"password": "1234567",
	"privileges": "user"
}

// response
{
  "data": {
    "_id": {
      "$oid": "603aeb956ee34adba1e0ada9"
    },
    "imageKey": "standard",
    "imageUrl": "https://wedding-app-anchor-loans-test.s3.amazonaws.com/avatars/standard-picture.jpg",
    "name": "Giorgio",
    "password": "1234567",
    "privileges": "user",
    "username": "gsfp"
  }
}
```

## **POST** Create Post - {{ _.baseURL }}/posts <a id="createPost"></a>
### AUTH REQUIRED
To use auth, the request must contain the following header:

**"authorization": "token"**

Token is an uuid generated throught the auth route. 


### MULTIPART FORM
| Parameter | Required |
| ------ | ----------- |
| image   | true |
| description   | true |
| title   | true |

- **image**: must be an image file;
- **description**: string;
- **title**: string;

### Example
```json
// Multipart form request
{
	"image": IMG_FILE.JPG,
	"description": "Must be in a place like this!",
	"title": "Nice place"
}

// response
{
  "data": {
    "_id": {
      "$oid": "603aebfb6ee34adba1e0adac"
    },
    "active": false,
    "author": {
      "$oid": "603aeb7b6ee34adba1e0ada8"
    },
    "comments": [],
    "description": "Must be in a place like this!",
    "imageKey": "gallery/IMG_FILE.jpg",
    "imageUrl": "https://wedding-app-anchor-loans-test.s3.amazonaws.com/gallery/7fbc3a13-4542-457b-b460-39f87b59c2bd-IMG_FILE.jpg",
    "likes": 0,
    "title": "Nice place"
  }
}
```

## **POST** Create Comment - {{ _.baseURL }}/comments <a id="createComment"></a>
### AUTH REQUIRED
To use auth, the request must contain the following header:

**"authorization": "token"**

Token is an uuid generated throught the auth route. 

### BODY PARAMS
| Parameter | Required |
| ------ | ----------- |
| postId   | true |
| content   | true |

```typescript
interface Body {
  postId: string;
  content: string;
}
```

### Example
```json
// request.body
{
	"postId": "603aebfb6ee34adba1e0adac",
	"content": "Concordo demais!"
}

// response
{
  "data": {
    "author": {
      "$oid": "603aeb956ee34adba1e0ada9"
    },
    "content": "Concordo demais!",
    "identifier": "4bde31ec-3a87-4496-9a6a-57e8ad8c4b02"
  }
}
```

## **PATCH** Update Post Active Status - {{ _.baseURL }}/posts <a id="updateActivePost"></a>
### AUTH REQUIRED
To use auth, the request must contain the following header:

**"authorization": "token"**

Token is an uuid generated throught the auth route. 

### ROUTE PARAMS
| Parameter | Required |
| ------ | ----------- |
| id   | true |
| active   | true |

```typescript
interface Body {
  id: string;
  active: boolean;
}
```

### Example
```json
// request body
{
	"id": "603aebfb6ee34adba1e0adac",
	"active": true
}

// response
{
  "data": {
    "_id": {
      "$oid": "603aebfb6ee34adba1e0adac"
    },
    "active": true,
    "author": {
      "$oid": "603aeb7b6ee34adba1e0ada8"
    },
    "comments": [
      {
        "author": {
          "$oid": "603aeb956ee34adba1e0ada9"
        },
        "content": "Concordo demais!",
        "identifier": "4bde31ec-3a87-4496-9a6a-57e8ad8c4b02"
      }
    ],
    "description": "Must be in a place like this!",
    "imageKey": "gallery/Wedding-2.jpg",
    "imageUrl": "https://wedding-app-anchor-loans-test.s3.amazonaws.com/gallery/7fbc3a13-4542-457b-b460-39f87b59c2bd-Wedding-2.jpg",
    "likes": 1,
    "title": "Nice place"
  }
}
```

## **PATCH** Update User Avatar - {{ _.baseURL }}/users <a id="updateUserAvatar"></a>
### AUTH REQUIRED
To use auth, the request must contain the following header:

**"authorization": "token"**

Token is an uuid generated throught the auth route. 

### MULTIPART FORM
| Parameter | Required |
| ------ | ----------- |
| image   | true |

The url would look like:
- **image**: image file to be uploaded

### Example
```json
// multipart form
{
  "image": file:some_img.png
}

// response
{
  "data": {
    "_id": {
      "$oid": "603aeb956ee34adba1e0ada9"
    },
    "imageKey": "avatars/regis4.jpg",
    "imageUrl": "https://wedding-app-anchor-loans-test.s3.amazonaws.com/avatars/bec96031-c71a-40f4-8aa6-a454196bf7dd-regis4.jpg",
    "name": "Giorgio",
    "password": "1234567",
    "privileges": "user",
    "username": "gsfp"
  }
}
```

## **PATCH** Like Post - {{ _.baseURL }}/posts/:postId <a id="like"></a>
### AUTH REQUIRED
To use auth, the request must contain the following header:

**"authorization": "token"**

Token is an uuid generated throught the auth route. 

### ROUTE PARAMS
| Parameter | Required |
| ------ | ----------- |
| postId   | true |

The url would look like:
- {baseurl}/posts/:postId

Where postId is our required param and accept the following values:

| Parameter | Value |
| ------ | ----------- |
| postId   | string |


### Example
```json
// PATCH request to
"{{ _.baseURL }}/posts/603aebfb6ee34adba1e0adac"

// response
{
  "data": {
    "_id": {
      "$oid": "603aebfb6ee34adba1e0adac"
    },
    "active": false,
    "author": {
      "$oid": "603aeb7b6ee34adba1e0ada8"
    },
    "comments": [
      {
        "author": {
          "$oid": "603aeb956ee34adba1e0ada9"
        },
        "content": "Concordo demais!",
        "identifier": "4bde31ec-3a87-4496-9a6a-57e8ad8c4b02"
      }
    ],
    "description": "Must be in a place like this!",
    "imageKey": "gallery/Wedding-2.jpg",
    "imageUrl": "https://wedding-app-anchor-loans-test.s3.amazonaws.com/gallery/7fbc3a13-4542-457b-b460-39f87b59c2bd-Wedding-2.jpg",
    "likes": 1,
    "title": "Nice place"
  }
}
```

## **DELETE** Delete Post - {{ _.baseURL }}/posts/:postId <a id="deletePost"></a>
### AUTH REQUIRED
To use auth, the request must contain the following header:

**"authorization": "token"**

Token is an uuid generated throught the auth route. 

### ROUTE PARAMS
| Parameter | Required |
| ------ | ----------- |
| postId   | true |

The url would look like:
- {baseurl}/posts/:postId

Where postId is our required param and accept the following values:

| Parameter | Value |
| ------ | ----------- |
| postId   | string |


### Example
```json
// DELETE request to
"{{ _.baseURL }}/posts/603aebfb6ee34adba1e0adac"

// response
RESPONSE STATUS 204
```

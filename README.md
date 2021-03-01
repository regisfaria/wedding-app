# Wedding App

## Overview
This app is born by the following problem: 
A friend wants a web app for all his friends to send pictures, like and comment to gather photos for his wedding.

This is the backend of the app, done in Python3, using the flask restful framework.
The app uses mongodb as database and it have connection with AWS S3 service, to store photos from post and from users.
## Installation
Make sure you have python3 and pip3 installed, as well mongodb.

After that, you just need to run(from the root folder):
```shell
pip3 install -r requirements.txt
```
This will download all of this app dependencies.

Alternativily you can install mongodb with docker, this can be done by running the following:
```shell
docker run --name mongodb -p 27017:27017 -d -t mongo
```

With the database & py reqs installed, now is needed to configure a .env file in your project root folder
for that, I've added a file called ".env.example" that shows how your .env should look like.

With all this setup, you are good to go, just run:
```shell
python3 src/main.py
```

The server will run on http://localhost:5000, make sure you have this port available.


## Contact
Email: regisprogramming@gmail.com

[LinkedIn](https://www.linkedin.com/in/regissfaria/), [GitHub](https://github.com/regisfaria) and [GitLab](https://gitlab.com/regisfaria) profiles
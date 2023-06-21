from flask import Flask, request, jsonify
from flasgger import APISpec, Swagger
from flask_restx import Api, Resource
from apispec_webframeworks.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin

from database import session, engine, init_db
import models

application = Flask(__name__)
api = Api(application)


spec = APISpec(
    title='UserList',
    version='1.0.0',
    openapi_version='2.0',
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin(),
    ]
)


@application.before_request
def before_request():
    init_db()
    user = models.User(
        name='Andrey',
        api_key='test',
        followers=[],
        tweets=[1])
    tweet = models.Tweet(user_id=1, tweet_data='Test', tweet_media_ids=[])
    session.add(user)
    session.flush()
    session.add(tweet)
    session.commit()


@api.route('/api/users/me')
class Me(Resource):
    def get(self):
        """
        Endpoint to get user info.
        ---
        tags:
          - users
        responses:
          200:
            description: User data
        """
        if True:
            user = session.query(models.User).filter(models.User.id == 1).one()
            info = user.get_info()
            info['following'] = []
            return jsonify(result='true', user=info)


@api.route('/api/users/<id>')
class User(Resource):
    def get(self):
        """
        Endpoint to get info about user by Id.
        ---
        tags:
          - users
        """


@api.route('/api/tweets')
class TweetsList(Resource):
    def get(self):
        """
        Endpoint to get tweets info.
        ---
        tags:
         - tweets
        responses:
         200:
           description: Tweets data
        """
        return {
            "result": "true",
            "tweets": [
                {
                    "id": 1,
                    "content": "test",
                    "attachments": [],
                    "author": {
                        "id": 1,
                        "name": "Andrey"
                    },
                    "likes": []
                }
            ]
        }

    def post(self):
        """
        Endpoint to send new tweet.
        ---
        tags:
         - tweets
        responses:
         200:
           description: Tweets data
        """
        pass


@api.route('/api/medias')
class Media(Resource):
    def get(self):
        """
        Endpoint to get medias from tweet.
        ---
        tags:
          - medias
        """
        pass

@api.route('/api/tweets/<id>')
class DeleteTweet(Resource):
    def delete(self):
        """
        Endpoint to delete the tweet.
        ---
        tags:
         - tweets
        responses:
         200:
           description: Tweets data
        """
        pass


@api.route('/api/tweets/<id>/likes')
class Likes(Resource):
    def post(self):
        """
        Endpoint to add like.
        ---
        tags:
          - likes
        """
        pass

    def delete(self):
        """
        Endpoint to delete like.
        ---
        tags:
          - likes
        """
        pass


@api.route('/api/users/<id>/follow')
class Following(Resource):
    def post(self):
        """
        Endpoint to follow user.
        ---
        tags:
          - users
        """
        pass

    def delete(self):
        """
        Endpoint to delete following user.
        ---
        tags:
          - users
        """
        pass


template = spec.to_flasgger(
    application,
)

swagger = Swagger(application, template=template)

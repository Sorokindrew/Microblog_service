import json

from flask import Flask, request, jsonify
from flasgger import APISpec, Swagger
from flask_restx import Api, Resource
from apispec_webframeworks.flask import FlaskPlugin
from apispec.ext.marshmallow import MarshmallowPlugin
from loguru import logger

from database import session, engine, init_db, get_user_by_id, \
    get_logged_user, get_all_tweets, add_like, add_tweet, unfollow_user, \
    delete_tweet, add_image
import models
from schemas import TweetSchema, UserSchema

application = Flask(__name__)
api = Api(application)

logger.add("./logs/log.log", level="DEBUG")

spec = APISpec(
    title='UserList',
    version='1.0.0',
    openapi_version='2.0',
    plugins=[
        FlaskPlugin(),
        MarshmallowPlugin(),
    ]
)

with application.app_context():
    init_db()
    logger.info("DB created!")


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
        logger.info("Info about me!")
        user = get_logged_user(request)
        return jsonify(result='true', user=user.get_user_full_info())


@api.route('/api/users/<id>')
class User(Resource):
    def get(self, id):
        """
        Endpoint to get info about user by Id.
        ---
        tags:
          - users
        """
        user = get_user_by_id(id)
        return jsonify(result='true', user=user.get_user_full_info())


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
           schema:
             $ref: '#/definitions/Tweet'
        """
        tweets = get_all_tweets()
        return jsonify(result="true", tweets=tweets)

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
        user_posted_tweet = get_logged_user(request)
        tweet_id = add_tweet(request=request, user_id=user_posted_tweet.id)
        return {"result": "true",
                "tweet_id": tweet_id}


@api.route('/api/medias')
class Media(Resource):
    def post(self):
        """
        Endpoint to add medias of tweet.
        ---
        tags:
          - medias
        """
        id_of_added_image = add_image(request=request)

        return {
            "result": "true",
            "media_id": id_of_added_image
        }


@api.route('/api/tweets/<id>')
class DeleteTweet(Resource):
    def delete(self, id):
        """
        Endpoint to delete the tweet.
        ---
        tags:
         - tweets
        responses:
         200:
           description: Tweets data
        """
        user = get_logged_user(request=request)
        delete_tweet(tweet_id=id, user_id=user.id)
        return jsonify(result='true')


@api.route('/api/tweets/<id>/follow')
class Following(Resource):
    def delete(self, id):
        """
        Endpoint to delete the tweet.
        ---
        tags:
         - users
        responses:
         200:
           description: Tweets data
        """
        active_user = get_logged_user(request=request)
        unfollow_user(user_to_be_unfollowed=id, user_id=active_user.id)
        return jsonify(result='true')


@api.route('/api/tweets/<id>/likes')
class Likes(Resource):
    def post(self, id):
        """
        Endpoint to add like.
        ---
        tags:
          - likes
        """
        user_liked_tweet = get_logged_user(request)
        add_like(tweet_id=id, user_id=user_liked_tweet.id)
        return jsonify(result='true')

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

    def delete(self, id):
        """
        Endpoint to delete following user.
        ---
        tags:
          - users
        """
        active_user = get_logged_user(request=request)
        unfollow_user(user_to_be_unfollowed=id, user_id=active_user.id)
        return jsonify(result='true')


template = spec.to_flasgger(
    application,
    definitions=[TweetSchema, UserSchema]
)

swagger = Swagger(application, template=template)

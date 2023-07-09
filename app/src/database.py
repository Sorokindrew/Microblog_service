import json
from typing import List

import flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from models import User, Tweet, Like, Image, Base
from flask import Request

engine = create_engine('postgresql+psycopg2://admin:admin@postgres')
Session = sessionmaker(bind=engine)
session = Session()


def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    user = User(
        name='Andrey',
        api_key='test',
    )
    user1 = User(
        name='Artem',
        api_key='test1',
    )
    user2 = User(
        name='Nina',
        api_key='test2',
    )
    tweet = Tweet(user_id=1, content='Test', attachments=[])
    session.add(user)
    session.add(user1)
    session.add(user2)
    session.flush()
    user.followers.append(user1)
    session.add(tweet)
    session.commit()


def get_user_by_id(id: str) -> User:
    return session.query(User).filter(User.id == id).one()


def get_logged_user(request: Request) -> User:
    api_key = request.headers['Api-Key']
    return session.query(User).filter(User.api_key == api_key).one()


def get_all_tweets() -> List:
    tweets = session.query(Tweet).all()
    tweets_list = []
    for tweet in tweets:
        tweet_likes = []
        for like in tweet.likes:
            user_id = like.user_id
            user_data = get_user_by_id(user_id)
            user_liked_tweet_info = user_data.get_user_id_and_name()
            tweet_likes.append(user_liked_tweet_info)
        tweets_list.append({
            "id": tweet.id,
            "content": tweet.content,
            "attachments": tweet.attachments,
            "author": {
                "id": tweet.user_id,
                "name": tweet.user.name
            },
            "likes": tweet_likes
        })
    return tweets_list


def add_tweet(request: Request, user_id):
    data = request.get_data(as_text=True)
    tweet_data = json.loads(data)
    tweet_to_add = Tweet(user_id=user_id,
                         content=tweet_data['tweet_data'],
                         attachments=tweet_data['tweet_media_ids'])
    session.add(tweet_to_add)
    session.flush()
    session.commit()
    return tweet_to_add.id


def add_like(tweet_id, user_id):
    if session.query(Like).filter(Like.tweet_id == tweet_id,
                                  Like.user_id == user_id).first() is None:
        like_to_add = Like(tweet_id=tweet_id, user_id=user_id)
        session.add(like_to_add)
        session.commit()
    else:
        session.query(Like).filter(Like.tweet_id == tweet_id,
                                   Like.user_id == user_id).delete()
        session.commit()

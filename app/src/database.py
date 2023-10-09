import json
import os
from typing import List

import flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from models import User, Tweet, Like, Image, Base
from flask import Request
from faker import Faker


engine = create_engine(
    f'postgresql+psycopg2://admin:admin@{os.environ["DB_URL"]}')
Session = sessionmaker(bind=engine)
session = Session()
fake = Faker()


def init_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    user = User(
        name='Andrey Sorokin',
        api_key='test',
    )
    user1 = User(
        name='Artem Sorokin',
        api_key='test1',
    )
    user2 = User(
        name='Nina Sorokina',
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
    for index in range(10):
        user = User(name=fake.name(), api_key=fake.word())
        session.add(user)
        session.commit()
    for _ in range(20):
        tweet1 = Tweet(user_id=fake.random_int(min=1, max=13),
                       content=fake.sentence(nb_words=10),
                       attachments=[])
        tweet2 = Tweet(user_id=fake.random_int(min=1, max=13),
                       content=fake.sentence(nb_words=10),
                       attachments=[])
        session.add(tweet1)
        session.add(tweet2)
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


def delete_tweet(tweet_id, user_id):
    tweet_to_delete = session.query(Tweet).filter(Tweet.id == tweet_id).one()
    if tweet_to_delete.user_id == user_id:
        session.query(Tweet).filter(Tweet.id == tweet_id).delete()


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


def unfollow_user(user_to_be_unfollowed, user_id):
    following = session.query(User).filter(
        User.id == user_to_be_unfollowed).one()
    follower = session.query(User).filter(
        User.id == user_id).one()
    if follower in following.followers:
        print('True')
        following.followers.remove(follower)
    else:
        following.followers.append(follower)
    session.commit()


def add_image(request: Request):
    file = request.files['file']
    number = len(session.query(Image).all()) + 1
    with open(f'/usr/share/nginx/html/images/{number}.png', 'wb') as f:
        f.write(file.read())
    image = Image(name=f'{number}.png')
    session.add(image)
    session.commit()
    return image.id

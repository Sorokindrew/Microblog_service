from sqlalchemy import Column, Sequence, String, JSON, ARRAY, \
    Integer, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,
                Sequence('users_id'),
                primary_key=True,
                nullable=False)
    name = Column(String(200), nullable=False)
    api_key = Column(String(200), nullable=False)
    followers = Column(ARRAY(Integer))
    tweets = Column(ARRAY(Integer))

    def get_info(self):
        return {"id": self.id,
                "name": self.name,
                "followers": self.followers,
                }


class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer,
                Sequence('tweets_id'),
                primary_key=True,
                nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    tweet_data = Column(String(200), default='')
    tweet_media_ids = Column(ARRAY(Integer))

    # user = relationship('User', backref='tweets')

    def get_info(self):
        return {'user': self.user.name,
                'tweet_data': self.tweet_data,
                'tweet_media_ids': self.tweet_media_ids
                }


class Likes(Base):
    __tablename__ = 'likes'

    id = Column(Integer,
                Sequence('likes_id'),
                primary_key=True)
    tweet_id = Column(Integer, ForeignKey('tweets.id'))
    user_id = Column(Integer, ForeignKey('users.id'))

    tweets = relationship(Tweet, backref='likes')
    users = relationship(User, backref='likes')


class Image(Base):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)

from sqlalchemy import Column, Sequence, String, JSON, ARRAY, \
    Integer, ForeignKey, Table
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

user_to_user = Table(
    "user_follows",
    Base.metadata,
    Column("followers_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("following_id", Integer, ForeignKey("users.id"), primary_key=True),
)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer,
                Sequence('users_id'),
                primary_key=True,
                nullable=False)
    name = Column(String(200), nullable=False)
    api_key = Column(String(200), nullable=False)

    followers = relationship(
        "User",
        secondary=user_to_user,
        primaryjoin=id == user_to_user.c.following_id,
        secondaryjoin=id == user_to_user.c.followers_id,
        back_populates="following",
    )
    following = relationship(
        "User",
        secondary=user_to_user,
        primaryjoin=id == user_to_user.c.followers_id,
        secondaryjoin=id == user_to_user.c.following_id,
        back_populates="followers",
    )

    def get_user_id_and_name(self):
        return {"id": self.id,
                "name": self.name
                }

    def get_user_full_info(self):
        info_about_followers = []
        info_about_following = []
        for follower in self.followers:
            follower_data = {
                'id': follower.id,
                'name': follower.name
            }
            info_about_followers.append(follower_data)
        for following in self.following:
            following_data = {
                'id': following.id,
                'name': following.name
            }
            info_about_following.append(following_data)
        return {"id": self.id,
                "name": self.name,
                "followers": info_about_followers,
                "following": info_about_following
                }


class Tweet(Base):
    __tablename__ = 'tweets'

    id = Column(Integer,
                Sequence('tweets_id'),
                primary_key=True,
                nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    content = Column(String(200), default='')
    attachments = Column(ARRAY(Integer))

    user = relationship('User', backref='tweets')


class Like(Base):
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
    name = Column(String(200), nullable=False)

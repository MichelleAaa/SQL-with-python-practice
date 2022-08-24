import datetime
from flask_sqlalchemy import SQLAlchemy

# create a database adapter object with the name of db by using the SQLAlchemy class:
db = SQLAlchemy()

# Create the User class as a subclass of SQLAlchemy's db.Model class

class User(db.Model):
    __tablename__ = 'users'
    # auto-increment-True (in other words, a SERIAL data type):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # 128 character limit below:
    username = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    tweets = db.relationship('Tweet', backref='user', cascade="all,delete")

#MANY-TO-MANY RELATIONSHIP (with User and Tweet)
likes_table = db.Table(
    'likes',
    db.Column(
        'user_id', db.Integer,
        db.ForeignKey('users.id'),
        primary_key=True
    ),

    db.Column(
        'tweet_id', db.Integer,
        db.ForeignKey('tweets.id'),
        primary_key=True
    ),

    db.Column(
        'created_at', db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
)


# MANY-TO-ONE RELATIONSHIP (WITH USER)
class Tweet(db.Model):
    __tablename__ = 'tweets'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(280), nullable=False)
    # We are using the datetime standard library for the created_at column default value. -- imported above.
    created_at = db.Column(
        db.DateTime,
        default=datetime.datetime.utcnow,
        nullable=False
    )
    #  db.ForeignKey() provided by Flask to use the id column of the users table for the user_id foreign key column for the tweets table. By setting nullable=False, we have made the user_id column non-nullable. This means that every record in the tweets table must have one and only one user_id linked to it.
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    liking_users = db.relationship(
        'User', secondary=likes_table,
        lazy='subquery',
        backref=db.backref('liked_tweets', lazy=True)
    )



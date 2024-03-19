from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

class USer(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    username = DB.Column(DB.String, nullable=False)
    
class Tweet(DB.Model):
    id = DB.Column(DB.BigInteger, primary_key=True, nullable=False)
    text = DB.Column(DB.Unicode(300), nullable=False)
    #Creating a relationship between Users and Tweets
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey('user.id'), nullable=False)
    #create a whole list of tweet to be attached to the User
    user = DB.relationship('User', backref=DB.backref('tweets'), lazy=True)
from flask import Flask, render_template
from.models import DB, User, Tweet

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLACHEMY_TRACK_MODIFICATION'] = 
    
    DB.init_app(app)

    @app.route('/')
    def root():

        users = User.query.all()

        return render_template('base.html', title='Home', user=users)
    
    @app.route('/')
    def reset():
        
        #resetting the database
        DB.drop_all()
        DB.create_all()

        #create some fake tweets and users
        ryan = User(id=1, username='ryanallred')
        moses = User(id=1, username='mosesadamu')


        tweet1 = Tweet(id=1, text='this is ryan\'s tweet', user=ryan)
        tweet2 = Tweet(id=1, text='this is ryan\'s tweet', user=moses)

        DB.session.add(ryan)
        DB.session.add(moses)
        DB.session.add(tweet1)
        DB.session.add(tweet2)

        DB.session.commit()

        return render_template('base.html', title='Reset')
    
    return app
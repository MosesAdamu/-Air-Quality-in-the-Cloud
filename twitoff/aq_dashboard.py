"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import openaq


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(app)

class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String)  # Storing datetime as string
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f'<Time {self.datetime} --- Value {self.value}>'

@app.route('/')
def root():
    """Base view."""
    risky_records = Record.query.filter(Record.value >= 18).all()
    risky_data = [(record.datetime, record.value) for record in risky_records]
    return str(risky_data)

if __name__ == "__main__":
    app.run()

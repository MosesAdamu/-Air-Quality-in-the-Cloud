"""OpenAQ Air Quality Dashboard with Flask."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import openaq

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
DB = SQLAlchemy(app)
api = openaq.OpenAQ()


class Record(DB.Model):
    id = DB.Column(DB.Integer, primary_key=True)
    datetime = DB.Column(DB.String(25))
    value = DB.Column(DB.Float, nullable=False)

    def __repr__(self):
        return f'< Time {self.datetime} --- Value {self.value} >'


@app.route('/')
def root():
    """Base view."""
    records = Record.query.filter(Record.value >= 18).all()
    return str(records)


@app.route('/refresh')
def refresh():
    """Pull fresh data from Open AQ and replace existing data."""
    DB.drop_all()
    DB.create_all()
    status, body = api.measurements(parameter='pm25')
    results = body['results']
    for result in results:
        datetime = result['date']['utc']
        value = result['value']
        record = Record(datetime=datetime, value=value)
        DB.session.add(record)
    DB.session.commit()
    return root()


def get_results():
    """Function to retrieve data from the API."""
    status, body = api.measurements(parameter='pm25')
    results = body['results']
    result_tuples = [
        (result['date']['utc'], result['value'])
        for result in results
    ]

    return result_tuples


if __name__ == '__main__':
    app.run(debug=True)

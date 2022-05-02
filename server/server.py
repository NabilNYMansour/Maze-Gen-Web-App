import urllib.request
import json
from datetime import datetime
from flask import Flask, send_file, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/mazes.db'
db = SQLAlchemy(app)

class Maze(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.LargeBinary, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.route('/New')
def main():
    url = 'http://127.0.0.1:5000/makeNew'
    data = {'size':25, 'password': 'testing'}
    data = json.dumps(data)
    data = str(data)
    data = data.encode('utf-8')
    req =  urllib.request.Request(url, data=data)

    contents = urllib.request.urlopen(req).read()
    new = Maze(img=contents)
    db.session.add(new)
    db.session.commit()

    response = make_response(contents)
    response.headers.set('Content-Type', 'image/jpeg')
    # response.headers.set('Content-Disposition', 'attachment', filename='test.jpg')

    return response
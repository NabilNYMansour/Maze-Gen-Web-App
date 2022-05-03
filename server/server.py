import urllib.request
import json
from datetime import datetime
from flask import Flask, send_file, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from io import BytesIO

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/mazes.db'
db = SQLAlchemy(app)

class Maze(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.LargeBinary, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@app.route('/New')
def new():
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
    response.headers.add('Access-Control-Allow-Origin', '*')
    # response.headers.set('Content-Disposition', 'attachment', filename='test.jpg')

    return response

@app.route('/GetImagesCount')
def getCount():
    count = db.session.query(Maze).count()
    response = make_response(jsonify({'count':count}))
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/Show/<int:id>')
def show(id):
    maze = Maze.query.get(id)

    if maze:
        response = make_response(maze.img)
        response.headers.set('Content-Type', 'image/jpeg')
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
        response = make_response(jsonify(None))
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
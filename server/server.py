import urllib.request
import json
from flask import Flask, make_response, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from oso import Oso, ForbiddenError

# Init
oso = Oso()
app = Flask(__name__)
app.secret_key = "super secret key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/mazes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.from_object(__name__)
db = SQLAlchemy(app)

# Models


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    role = db.Column(db.String(80), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class Maze(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    img = db.Column(db.LargeBinary, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


oso.register_class(User)
oso.register_class(Maze)
oso.load_files(["main.polar"])

# Renders


@app.route('/New')
def new():
    try:
        user = User(id=session["currentUser"][0], username=session["currentUser"][1], role=session["currentUser"][2])
        oso.authorize(user, "create", Maze())
        print("new", ">>>>>>>>>>>>>>", session["currentUser"])

        if (db.session.query(Maze).count() > 20):
            raise ForbiddenError

        # url = 'http://127.0.0.1:5000/makeNew'
        url = 'https://nabilmansour.com:5000/makeNew'
        data = {'size': 25, 'password': 'testing'}
        data = json.dumps(data)
        data = str(data)
        data = data.encode('utf-8')
        req = urllib.request.Request(url, data=data)

        contents = urllib.request.urlopen(req).read()
        new = Maze(img=contents)

        db.session.add(new)
        db.session.commit()

        response = make_response(contents)
        response.headers.set('Content-Type', 'image/jpeg')
        # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Origin', 'https://nabilmansour.com/MazeGen')
        response.headers.add('Access-Control-Allow-Credentials ', 'true')
        return response

    except ForbiddenError:
        response = make_response(jsonify({'complete': False, 'errormsg': 'Permission Denied'}))
        # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Origin', 'https://nabilmansour.com/MazeGen')
        response.headers.add('Access-Control-Allow-Credentials ', 'true')
        return response, 403
    except KeyError:
        response = make_response(jsonify({'complete': False, 'errormsg': 'No current User'}))
        # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Origin', 'https://nabilmansour.com/MazeGen')
        response.headers.add('Access-Control-Allow-Credentials ', 'true')
        return response, 404


@app.route('/GetImagesCount')
def getCount():
    try:
        user = User(id=session["currentUser"][0], username=session["currentUser"][1], role=session["currentUser"][2])
        oso.authorize(user, "read", Maze())

        count = db.session.query(Maze).count()
        response = make_response(jsonify({'count': count}))
        # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Origin', 'https://nabilmansour.com/MazeGen')
        response.headers.add('Access-Control-Allow-Credentials ', 'true')
        return response
    except KeyError:
        response = make_response(jsonify({'complete': False, 'errormsg': 'No current User'}))
        # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Origin', 'https://nabilmansour.com/MazeGen')
        response.headers.add('Access-Control-Allow-Credentials ', 'true')
        return response, 404



@app.route('/Show/<int:id>')
def show(id):
    try:
        user = User(id=session["currentUser"][0], username=session["currentUser"][1], role=session["currentUser"][2])
        oso.authorize(user, "read", Maze())

        maze = Maze.query.get(id)

        if maze:
            response = make_response(maze.img)
            response.headers.set('Content-Type', 'image/jpeg')
            # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
            response.headers.add('Access-Control-Allow-Origin', 'https://nabilmansour.com/MazeGen')
            response.headers.add('Access-Control-Allow-Credentials ', 'true')
            return response
        else:
            response = make_response(jsonify(None))
            # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
            response.headers.add('Access-Control-Allow-Origin', 'https://nabilmansour.com/MazeGen')
            response.headers.add('Access-Control-Allow-Credentials ', 'true')
            return response
    except KeyError:
        response = make_response(jsonify({'complete': False, 'errormsg': 'No current User'}))
        # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Origin', 'https://nabilmansour.com/MazeGen')
        response.headers.add('Access-Control-Allow-Credentials ', 'true')
        return response, 404


@app.route('/Delete/<int:id>')
def delete(id):
    try:
        user = User(id=session["currentUser"][0], username=session["currentUser"][1], role=session["currentUser"][2])
        oso.authorize(user, "delete", Maze())
        maze = Maze.query.get(id)

        if maze:
            response = make_response(jsonify({'complete': True, 'errormsg': None}))
            db.session.delete(maze)
            db.session.commit()
        else:
            response = make_response(
                jsonify({'complete': False, 'errormsg': 'no entry found'}))

        # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Origin', 'https://nabilmansour.com/MazeGen')
        response.headers.add('Access-Control-Allow-Credentials ', 'true')
        return response
    except ForbiddenError:
        response = make_response(jsonify({'complete': False, 'errormsg': 'Permission Denied'}))
        # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Origin', 'https://nabilmansour.com/MazeGen')
        response.headers.add('Access-Control-Allow-Credentials ', 'true')
        return response, 403
    except KeyError:
        response = make_response(jsonify({'complete': False, 'errormsg': 'No current User'}))
        # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Origin', 'https://nabilmansour.com/MazeGen')
        response.headers.add('Access-Control-Allow-Credentials ', 'true')
        return response, 404


@app.route('/login/<name>')
def login(name):
    user = User.query.filter_by(username=name.lower()).first()
    if not user:
        user = User(username=name.lower(), role="viewer")
    
    session['currentUser'] = [user.id, user.username, user.role]
    print("login", ">>>>>>>>>>>>>", session["currentUser"])
    response = make_response(jsonify({'login': True, 'name': name.lower(), 'role': user.role}))
    # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    response.headers.add('Access-Control-Allow-Origin', 'https://nabilmansour.com/MazeGen')
    response.headers.add('Access-Control-Allow-Credentials ', 'true')
    return response

@app.route('/currentUser')
def current():
    if 'currentUser' in list(session.keys()):
        return jsonify(session["currentUser"])
    else:
        return "No current User"

@app.route('/resetUser')
def reset():
    if 'currentUser' in list(session.keys()):
        del session["currentUser"]
        return "deleted"
    else:
        return "No current User"


@app.route('/GetImgList')
def imglist():
    try:
        user = User(id=session["currentUser"][0], username=session["currentUser"][1], role=session["currentUser"][2])
        oso.authorize(user, "read", Maze())
        print()
        response = make_response(jsonify([maze.id for maze in Maze.query.all()]))
        # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Origin', 'https://nabilmansour.com/MazeGen')
        response.headers.add('Access-Control-Allow-Credentials ', 'true')
        return response
    except KeyError:
        response = make_response(jsonify({'complete': False, 'errormsg': 'No current User'}))
        # response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Origin', 'https://nabilmansour.com/MazeGen')
        response.headers.add('Access-Control-Allow-Credentials ', 'true')
        return response, 404


if __name__ == "__main__":
    app.run(port=8000)
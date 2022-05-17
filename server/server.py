import urllib.request
import json
from flask import Flask, make_response, jsonify, send_file, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
from io import BytesIO
from PIL import Image, ImageDraw
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
        user = User(id=session["currentUser"][0],
                    username=session["currentUser"][1], role=session["currentUser"][2])
        oso.authorize(user, "create", Maze())
        print("new", ">>>>>>>>>>>>>>", session["currentUser"])

        if (db.session.query(Maze).count() > 20):
            raise ForbiddenError

        # url = 'http://127.0.0.1:5000/makeNew'
        # url = 'https://nabilmansour.com:5000/makeNew'
        # data = {'size': 25, 'password': 'testing'}
        # data = json.dumps(data)
        # data = str(data)
        # data = data.encode('utf-8')
        # req = urllib.request.Request(url, data=data)

        # contents = urllib.request.urlopen(req).read()
        contents = genImg(25).read()
        new = Maze(img=contents)

        db.session.add(new)
        db.session.commit()

        response = make_response(contents)
        response.headers.set('Content-Type', 'image/jpeg')
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        # response.headers.add('Access-Control-Allow-Origin', 'https://nabilmansour.com')
        response.headers.add('Access-Control-Allow-Credentials ', 'true')
        return response

    except ForbiddenError:
        response = make_response(
            jsonify({'complete': False, 'errormsg': 'Permission Denied'}))
        response.headers.add('Access-Control-Allow-Credentials ', 'true')
        return response, 403
    except KeyError:
        response = make_response(
            jsonify({'complete': False, 'errormsg': 'No current User'}))
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Credentials ', 'true')
        return response, 404


@app.route('/GetImagesCount')
def getCount():
    try:
        user = User(id=session["currentUser"][0],
                    username=session["currentUser"][1], role=session["currentUser"][2])
        oso.authorize(user, "read", Maze())

        count = db.session.query(Maze).count()
        response = make_response(jsonify({'count': count}))
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Credentials ', 'true')
        return response
    except KeyError:
        response = make_response(
            jsonify({'complete': False, 'errormsg': 'No current User'}))
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Credentials ', 'true')
        return response, 404


@app.route('/Show/<int:id>')
def show(id):
    try:
        user = User(id=session["currentUser"][0],
                    username=session["currentUser"][1], role=session["currentUser"][2])
        oso.authorize(user, "read", Maze())

        maze = Maze.query.get(id)

        if maze:
            response = make_response(maze.img)
            response.headers.set('Content-Type', 'image/jpeg')
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
            response.headers.add('Access-Control-Allow-Credentials ', 'true')
            return response
        else:
            response = make_response(jsonify(None))
            response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
            response.headers.add('Access-Control-Allow-Credentials ', 'true')
            return response
    except KeyError:
        response = make_response(
            jsonify({'complete': False, 'errormsg': 'No current User'}))
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Credentials ', 'true')
        return response, 404


@app.route('/Delete/<int:id>')
def delete(id):
    try:
        user = User(id=session["currentUser"][0],
                    username=session["currentUser"][1], role=session["currentUser"][2])
        oso.authorize(user, "delete", Maze())
        maze = Maze.query.get(id)

        if maze:
            response = make_response(
                jsonify({'complete': True, 'errormsg': None}))
            db.session.delete(maze)
            db.session.commit()
        else:
            response = make_response(
                jsonify({'complete': False, 'errormsg': 'no entry found'}))

        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Credentials ', 'true')
        return response
    except ForbiddenError:
        response = make_response(
            jsonify({'complete': False, 'errormsg': 'Permission Denied'}))
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Credentials ', 'true')
        return response, 403
    except KeyError:
        response = make_response(
            jsonify({'complete': False, 'errormsg': 'No current User'}))
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Credentials ', 'true')
        return response, 404


@app.route('/login/<name>')
def login(name):
    user = User.query.filter_by(username=name.lower()).first()
    if not user:
        user = User(username=name.lower(), role="viewer")

    session['currentUser'] = [user.id, user.username, user.role]
    print("login", ">>>>>>>>>>>>>", session["currentUser"])
    response = make_response(
        jsonify({'login': True, 'name': name.lower(), 'role': user.role}))
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
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
        user = User(id=session["currentUser"][0],
                    username=session["currentUser"][1], role=session["currentUser"][2])
        oso.authorize(user, "read", Maze())
        print()
        response = make_response(
            jsonify([maze.id for maze in Maze.query.all()]))
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Credentials ', 'true')
        return response
    except KeyError:
        response = make_response(
            jsonify({'complete': False, 'errormsg': 'No current User'}))
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Credentials ', 'true')
        return response, 404


# Utils:

def MakeVerticies_DrawEdges(size, draw):
    print("Making vertices and drawing the edges...")
    vertices = []
    edges = []
    for i in range(size):
        print("Progress: ", i, "/", size - 1, end="\r")
        draw.point((i, 0), "black")
        draw.point((i, size - 1), "black")
        if i % 2 == 1:
            edges.append((i, 0))
            edges.append((i, size - 1))
        for j in range(size):
            if j % 2 == 1:
                edges.append((0, j))
                edges.append((size - 1, j))
            if i % 2 == 0:
                draw.point((i, j), "black")
            if j % 2 == 0:
                draw.point((i, j), "black")
            elif i % 2 == 1 and j % 2 == 1:
                vertices.append((i, j))
    print()
    return vertices, edges


def MakeGraph(vertices, edges, size):
    print("Making graph...")
    graph = []
    for currentVertex in vertices:
        print("Progress: ", vertices.index(currentVertex),
              "/", len(vertices) - 1, end="\r")

        newRow = []
        if (currentVertex[0]+2, currentVertex[1]) in vertices:
            edge = (currentVertex[0]+1, currentVertex[1])
            index = vertices.index(currentVertex)+((size-1)//2)
            newRow.append((edge[0], edge[1], index))
            edges.append((edge[0], edge[1]))

        if (currentVertex[0]-2, currentVertex[1]) in vertices:
            edge = (currentVertex[0]-1, currentVertex[1])
            index = vertices.index(currentVertex)-((size-1)//2)
            newRow.append((edge[0], edge[1], index))
            edges.append((edge[0], edge[1]))

        if (currentVertex[0], currentVertex[1]+2) in vertices:
            edge = (currentVertex[0], currentVertex[1]+1)
            index = vertices.index(currentVertex)+1
            newRow.append((edge[0], edge[1], index))
            edges.append((edge[0], edge[1]))

        if (currentVertex[0], currentVertex[1]-2) in vertices:
            edge = (currentVertex[0], currentVertex[1]-1)
            index = vertices.index(currentVertex)-1
            newRow.append((edge[0], edge[1], index))
            edges.append((edge[0], edge[1]))
        graph.append(newRow)
    print()
    return graph


def DFS(graph, row, usedEdges, usedVertices, draw):
    random.shuffle(row)
    for edge in row:
        if edge not in usedEdges and edge[2] not in usedVertices:
            draw.point((edge[0], edge[1])[::-1], "white")
            if (edge[0], edge[1]) not in usedEdges:
                usedEdges.append((edge[0], edge[1]))
            if graph.index(row) not in usedVertices:
                usedVertices.append(graph.index(row))
            DFS(graph, graph[edge[2]], usedEdges, usedVertices, draw)
            break


def IsStuck(vertex, usedEdges):
    if (vertex[0]+1, vertex[1]) in usedEdges:
        if (vertex[0]-1, vertex[1]) in usedEdges:
            if (vertex[0], vertex[1]+1) in usedEdges:
                if (vertex[0], vertex[1]-1) in usedEdges:
                    return True
    return False


def Demolish(RIGHT, LEFT, UP, DOWN, vertices, vertex, usedEdges, usedVertices, draw, size):
    toReturn = False

    if vertex+1 in usedVertices and RIGHT:
        draw.point((vertices[vertex][0], vertices[vertex][1]+1)[::-1], "white")
        usedEdges.append((vertices[vertex][0], vertices[vertex][1]+1))
        if vertex not in usedVertices:
            usedVertices.append(vertex)
        toReturn = True

    elif vertex-1 in usedVertices and LEFT:
        draw.point((vertices[vertex][0], vertices[vertex][1]-1)[::-1], "white")
        usedEdges.append((vertices[vertex][0], vertices[vertex][1]-1))
        if vertex not in usedVertices:
            usedVertices.append(vertex)
        toReturn = True

    elif vertex-((size-1)//2) in usedVertices and UP:
        draw.point((vertices[vertex][0]-1, vertices[vertex][1])[::-1], "white")
        usedEdges.append((vertices[vertex][0]-1, vertices[vertex][1]))
        if vertex not in usedVertices:
            usedVertices.append(vertex)
        toReturn = True

    elif vertex+((size-1)//2) in usedVertices and DOWN:
        draw.point((vertices[vertex][0]+1, vertices[vertex][1])[::-1], "white")
        usedEdges.append((vertices[vertex][0]+1, vertices[vertex][1]))
        if vertex not in usedVertices:
            usedVertices.append(vertex)
        toReturn = True

    return toReturn


def DFSPathFinding(startingVertex, EndingVertex, vertices, usedEdges, graph, row, excludingEdge, draw, color):
    for edge in row:
        if edge[2] == vertices.index(EndingVertex) and edge[0:2] in usedEdges:
            draw.point(edge[0:2][::-1], color)
            draw.point(startingVertex[0:2][::-1], color)

            return True
        elif edge[0:2] in usedEdges and edge[0:2] != excludingEdge[0:2]:
            if DFSPathFinding(vertices[edge[2]], EndingVertex, vertices, usedEdges, graph, graph[edge[2]], edge, draw, color):
                draw.point(edge[0:2][::-1], color)
                draw.point(startingVertex[0:2][::-1], color)

                return True


def DrawPath(startingVertex, EndingVertex, vertices, edges, graph, usedEdges, draw, color):
    row = graph[vertices.index(startingVertex)]
    excludingEdge = (0, 0)
    DFSPathFinding(startingVertex, EndingVertex, vertices,
                   usedEdges, graph, row, excludingEdge, draw, color)
    draw.point(startingVertex[::-1], "yellow")
    draw.point(EndingVertex[::-1], "blue")


def getRow(vertex, size):
    return (vertex)//((size-1)//2)


def getColumn(row, vertex, size):
    return vertex - row * ((size-1)//2)


def genImg(size):
    img = Image.new("RGB", (size, size), "white")
    draw = ImageDraw.Draw(img)
    vertices, edges = MakeVerticies_DrawEdges(size, draw)
    graph = MakeGraph(vertices, edges, size)
    usedEdges = []
    usedVertices = []

    print("Performing DFS...")

    DFS(graph, graph[len(vertices)//2], usedEdges, usedVertices, draw)

    while len(usedVertices) < len(vertices):
        choices = [i+1 for i in usedVertices if i+1 not in usedVertices and i +
                   1 < len(vertices) and getColumn(getRow(i+1, size), i+1, size) != 0]
        choices.extend([i-1 for i in usedVertices if i-1 not in usedVertices and i -
                        1 not in choices and i-1 > 0 and getColumn(getRow(i-1, size), i-1, size) != ((size)//2)-1])
        choices.extend([i+((size-1)//2) for i in usedVertices if i+((size-1)//2)
                        not in usedVertices and i+((size-1)//2) not in choices and i+((size-1)//2) < len(vertices)])
        choices.extend([i-((size-1)//2) for i in usedVertices if i-((size-1)//2)
                        not in usedVertices and i-((size-1)//2) not in choices and i-((size-1)//2) > 0])
        choices = [i for i in choices if IsStuck(
            vertices[i], set(edges) - set(usedEdges))]

        if choices == []:
            for vertex in range(len(vertices)):
                if IsStuck(vertices[vertex], set(edges) - set(usedEdges)):
                    break
            if not IsStuck(vertices[vertex], set(edges) - set(usedEdges)):
                usedVertices = [i for i in range(len(vertices))]
                break
        else:
            vertex = choices[random.randint(0, len(choices)-1)]

        print("Progress: ", len(usedVertices),
              "/", len(vertices)-1, end="\r")

        row = getRow(vertex, size)
        column = getColumn(row, vertex, size)
        performDFS = False

        if row == 0 and column == 0:  # RIGHT and DOWN
            performDFS = Demolish(True, False, False, True, vertices, vertex,
                                  usedEdges, usedVertices, draw, size)

        elif row == 0 and column == ((size-1)//2)-1:  # LEFT and DOWN
            performDFS = Demolish(False, True, False, True, vertices, vertex,
                                  usedEdges, usedVertices, draw, size)

        elif row == ((size-1)//2)-1 and column == 0:  # RIGHT and UP
            performDFS = Demolish(True, False, True, False, vertices, vertex,
                                  usedEdges, usedVertices, draw, size)

        elif row == ((size-1)//2)-1 and column == ((size-1)//2)-1:  # LEFT and UP
            performDFS = Demolish(False, True, True, False, vertices, vertex,
                                  usedEdges, usedVertices, draw, size)

        elif row == 0:  # RIGHT, LEFT, and DOWN
            performDFS = Demolish(True, True, False, True, vertices, vertex,
                                  usedEdges, usedVertices, draw, size)

        elif column == 0:  # UP, DOWN, and RIGHT
            performDFS = Demolish(True, False, True, True, vertices, vertex,
                                  usedEdges, usedVertices, draw, size)

        elif row == ((size-1)//2)-1:  # RIGHT, LEFT, and UP
            performDFS = Demolish(True, True, True, False, vertices, vertex,
                                  usedEdges, usedVertices, draw, size)

        elif column == ((size-1)//2)-1:  # UP, DOWN, and LEFT
            performDFS = Demolish(False, True, True, True, vertices, vertex,
                                  usedEdges, usedVertices, draw, size)

        else:
            performDFS = Demolish(True, True, True, True, vertices, vertex,
                                  usedEdges, usedVertices, draw, size)

        if performDFS:
            DFS(graph, graph[vertex], usedEdges, usedVertices, draw)

    print("Progress: ", len(usedVertices)-1, "/", len(vertices)-1, end="\r")
    print("\nDONE: maze generation")

    # DrawPath(vertices[0], (1, vertices[-1][1]),
    #          vertices, edges, graph, usedEdges, draw, "tomato")
    # DrawPath(vertices[0], (vertices[-1][1], 1),
    #          vertices, edges, graph, usedEdges, draw, "purple")
    # DrawPath(vertices[0], vertices[-1], vertices,
    #          edges, graph, usedEdges, draw, "red")

    # print("DONE: path finding")

    # print("Resizing image...")
    # img = img.resize((size*10, size*10), Image.BOX)

    print("Sending image...")
    img_io = BytesIO()
    img.save(img_io, 'JPEG', quality=70)
    img_io.seek(0)

    return img_io


if __name__ == "__main__":
    app.run(port=8000)

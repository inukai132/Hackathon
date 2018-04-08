#!/usr/bin/python2
import flask
import ujson
import md5

def makeToken(name):
    m = md5.new()
    m.update(name)
    return m.digest().encode('hex')

users = {}
app = flask.Flask(__name__,static_folder='./static')

users = None
data = None
policy = None

with(open('../tables/users.json') as j):
    users = ujson.loads(j.read())['users']

with(open('../tables/data.json') as j):
    data = ujson.loads(j.read())

with(open('../tables/policy.json') as j):
    policy = ujson.loads(j.read())

@app.route('/<path:path>')
def get_file(path):
    return send_from_directory("./",path)

@app.route('/login')
def login():
    try:
        name = request.json["username"]
        user = None
        for u in users:
            if u['username'] is name:
                user = u
                break
        if user is None:
            flask.abort(401)
        users[makeToken(u['username'])] = u['UUID']
        return users[u['UUID']]
    except KeyError as e:
        flask.abort(401)

@app.route('/read')
def santaRead():
    try:
        RID = request.json["RID"]
        UUID = request.json["UUID"]
        user = users[RID]
        
    except KeyError as e:
        flask.abort(401)


@app.route('/write')
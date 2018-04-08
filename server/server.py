#!/usr/bin/python2
from flask import request, json, send_from_directory, Flask, abort, make_response
import ujson
import md5
import boto3

def makeToken(name):
    m = md5.new()
    m.update(name)
    return m.digest().encode('hex')

loggedIn = {} 
app = Flask(__name__,static_folder='./static')

users = None
data = None
policies = None

dynamodb = boto3.resource('dynamodb', 'us-east-2')


# with open('../tables/users.json') as j:
#     users = ujson.loads(j.read())['users']

# with(open('../tables/data.json') as j):
#     data = ujson.loads(j.read())

# with(open('../tables/policy.json') as j):
#     policies = ujson.loads(j.read())

@app.route('/<path:path>')
def get_file(path):
    return send_from_directory("./static/",path)

@app.route('/login', methods=['POST','GET'])
def login():
    try:
        name = request.json["username"]
        user = None
        for u in users:
            print str(u['username'])
            if u['username'] == name:
                user = u
                break
        if user is None:
            print 'nouser'
            abort(401)
        loggedIn[user['UUID']] = makeToken(user['username'])
        resp = make_response("<p>Good</p>",200)
        resp.set_cookie('userID',loggedIn[user['UUID']])
        return resp
    except KeyError as e:
        print 'badkey'
        abort(401)
    except TypeError as e:
        print 'badtype'
        abort(401)

# @app.route('/read')
# def santaRead():
#     try:
#         returned = None
#         RID = request.cookies.get('userID')
#         UUID = request.json["UUID"]
#         user = loggedIn[RID]
#         policy = policies[user['role']]
#         patient = data[UUID]
        
#     except KeyError as e:
#         abort(401)


# @app.route('/write')
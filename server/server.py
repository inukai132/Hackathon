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
app = Flask(__name__,static_folder='../web_services/')

users = None
data = None
policies = None
key = ""
skey = ""
with open("../../accessKeys.csv") as kf:
    key,skey = kf.read().split('/r/n')[1].split(',')

dynamodb = boto3.resource('dynamodb', 'us-east-2', aws_access_key_id=key, aws_secret_key_id=skey)


# with open('../tables/users.json') as j:
#     users = ujson.loads(j.read())['users']

# with(open('../tables/data.json') as j):
#     data = ujson.loads(j.read())

# with(open('../tables/policy.json') as j):
#     policies = ujson.loads(j.read())

@app.route('/<path:path>')
def get_file(path):
    return send_from_directory("../web_services",path)

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

@app.route('/read')
def santaRead():
    try:
        RID = request.cookies.get('userID')
        UUID = request.json["UUID"]
        readFunction(RID,UUID)
        abort(404)
    except KeyError as e:
        abort(401)


@app.route('/write')
def santaWrite():
    abort(404)
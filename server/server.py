#!/usr/bin/python2
from flask import request, json, send_from_directory, Flask, abort, make_response
import ujson
import md5
import boto3
import logging
import datetime

def makeToken(name):
    m = md5.new()
    m.update(name)
    return m.digest().encode('hex')

loggedIn = {} 
app = Flask(__name__,static_folder='../web_services/')

time = datetime.datetime.now().strftime("%Y-%m-%d.%H:%M:%S")
logging.basicConfig(filename="../"+time+".log", level=logging.DEBUG)

users = None
data = None
policies = None
key = ""
skey = ""
with open("../../accessKeys.csv") as kf:
    key,skey = kf.read().split('\r\n')[1].split(',')


dynamodb = boto3.resource('dynamodb', 'us-east-2', aws_access_key_id=key, aws_secret_key_id=skey)

@app.route('/<path:path>')
def get_file(path):
    return send_from_directory("../web_services",path)

@app.route('/api/login', methods=['POST','GET'])
def login():
    try:
        name = request.json["username"]
        user = None
        for u in users:
            print str(u['username'])
            if u['username']dynamodb == name:
                user = u
                break
        if user is None:
            print 'nouser'
            abort(401)
        loggedIn[makeToken(user['username'])] = user['UUID']
        resp = make_response("<p>Good</p>",200)
        resp.set_cookie('userID',loggedIn[user['UUID']])
        return resp
    except KeyError as e:
        print 'badkey'
        abort(401)
    except TypeError as e:
        print 'badtype'
        abort(401)

@app.route('/api/session/validate')
def validate():
    try:
        uid = request.cookies.get('userID')
        if uid is not None:
            # resp = make_response(ujson.dumps(loggedIn[uid]),200)
            resp = make_response("{'name':'Bob Stevens'}",200)
            return resp
    except Exception as e:
        abort(401)

@app.route('/api/read')
def santaRead():
    try:
        RID = request.cookies.get('userID')
        UUID = request.json["UUID"]
        readFunction(RID,UUID)
        abort(404)
    except KeyError as e:
        abort(401)


@app.route('/api/write')
def santaWrite():
    abort(404)
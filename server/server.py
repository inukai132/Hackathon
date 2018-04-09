#!/usr/bin/python2
from flask import request, json, send_from_directory, Flask, abort, make_response, current_app
import ujson
import md5
import boto3
import logging
import datetime
from functools import update_wrapper
from datetime import timedelta

def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, basestring):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, basestring):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers

            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

def makeToken(name):
    m = md5.new()
    m.update(name)
    return m.digest().encode('hex')

loggedIn = {} 
app = Flask(__name__,static_folder='../web_services/')

time = datetime.datetime.now().strftime("%Y-%m-%d.%H:%M:%S")
# logging.basicConfig(filename="../"+time+".log", level=logging.DEBUG)

users = None
data = None
policies = None
key = ""
skey = ""
with open("../../accessKeys.csv") as kf:
    key,skey = kf.read().split('\r\n')[1].split(',')


dynamodb = boto3.resource('dynamodb', 'us-east-2', aws_access_key_id=key, aws_secret_access_key=skey)

@app.route('/<path:path>')
def get_file(path):
    return send_from_directory("../web_services",path)

@crossdomain(origin='*')
@app.route('/api/login', methods=['POST','GET','OPTIONS'])
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

@crossdomain(origin='*')
@app.route('/api/session/validate')
def validate():
    print "DING"
    try:
        uid = request.cookies.get('userID')
        if uid is not None:
            # resp = make_response(ujson.dumps(loggedIn[uid]),200)
            resp = make_response("{'name':'Bob Stevens'}",200)
        resp = make_response("{'name':'Bob Stevens'}",200)
        return resp
    except Exception as e:
        resp = make_response("{'name':'error'}",200)

@crossdomain(origin='*')
@app.route('/api/read')
def santaRead():
    try:
        RID = request.cookies.get('userID')
        UUID = request.json["UUID"]
        readFunction(RID,UUID)
        abort(404)
    except KeyError as e:
        abort(401)

@crossdomain(origin='*')
@app.route('/api/write')
def santaWrite():
    abort(404)
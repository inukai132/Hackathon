#!/usr/bin/python2
import falcon, pymongo

class RequestMonitor:
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = "TEST COMPLETE"

app = falcon.API()
santa = RequestMonitor()
app.add_route('/test', santa)
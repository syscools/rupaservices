# Copyright 2015 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from flask import Flask, jsonify,request,redirect

import googlemaps
from datetime import datetime
from flask import Response
import json

API_KEY = 'AIzaSyCzpbgoECGhplawnFLBNgCVStWyMY30Ku8'

app = Flask(__name__)

@app.route('/')
def Welcome():
    return app.send_static_file('index.html')

@app.route('/places')
def places():
    location = (10.3099,123.893)
    val = request.args.get('q')
    if val:
        try:
            gmaps = googlemaps.Client(key = API_KEY)
            loc = gmaps.places(val,location = location,radius = 100);
        except:
            resp = Response("{'addresses':[],'timeout':'yes'}")
            resp.headers['Access-Control-Allow-Origin'] = '*'
            return resp

        def get_addresses(b):        # a is a string
            c = b["results"]
            e = []
            for x in c:
                # convert dict to string using json.dumps()
                d = json.dumps(x["formatted_address"])
                if len(d) > 2: # exclude empty stuff
                    e.append(x["formatted_address"])
            return json.dumps({"addresses":e})
 
        resp = Response(get_addresses(loc))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp
    return redirect("/")

@app.route('/directions')
def directions():
    a = request.args.get('a')
    b = request.args.get('b')
    if a and b:
        gmaps = googlemaps.Client(key = API_KEY)
        routes = gmaps.directions(a,b)
        return str(routes)

        def get_routes(b):        # a is a string
            return '{"routes":"test123"}'

        resp = Response(get_routes(routes))
        resp.headers['Access-Control-Allow-Origin'] = '*'
        return resp

    else:
        return "please specify from,to locations"

@app.route('/api/people/<name>')
def SayHello(name):
    message = {
        'message': 'Hello ' + name
    }
    return jsonify(results=message)

port = os.getenv('PORT', '5000')
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(port))

#!/usr/bin/env python

from __future__ import print_function
from future import standard_library
standard_library.install_aliases()
import urllib.request, urllib.parse, urllib.error
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    with open('data.json') as data_file:
        data = json.load(data_file)
    
    '''
    if req.get("result").get("action") == "_welcome":
        return data["greet"][0]
    '''
    
    if req.get("result").get("action") == "_search_major":
        degree = req.get("result").get("parameters").get("degree")
        language = req.get("result").get("parameters").get("language")
        
        if degree == "graduate":
            
            for major in data["grad"]:
                if language.lower() in major["major"].lower():
                    return {"speech":json.dumps(major)};
        
        if degree == "undergraduate":
            for major in data["undergrad"]:
                if language.lower() in major["major"].lower():
                    return {"speech":json.dumps(major)};
        
        return data["sorry"]
    
    '''
    if req.get("result").get("action") == "semester.search":
        return data["semester"]
    
    if req.get("result").get("action") == "employee.search":
        employee = req.get("result").get("parameters").get("employee")
        
        if employee == "azhar":
            return data["users"]["azhar"]
        if employee == "arathi":
            return data["users"]["arathi"]
        if employee == "mahesh":
            return data["users"]["mahesh"]
    '''
        
        
    return data["sorry"]

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

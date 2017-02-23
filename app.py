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

    for ctxt in req.get("result").get("contexts"):
        if req.get("result").get("action") == "_admission_req":
            if ctxt["name"] == "context_admission_requirement":
                degree = ctxt["parameters"]["degree"]
                language = ctxt["parameters"]["language"]
                
                for info in data[degree]:
                    if language.lower() in info["major"].lower():
                        return {"displayText": json.dumps(info["requirement"]["admission"]), "speech": info["requirement"]["admission"]["detail"]}
                return data["sorry"]
        if req.get("result").get("action") == "_more_info":
            if ctxt["name"] == "context_search_major":
                degree = ctxt["parameters"]["degree"]
                language = ctxt["parameters"]["language"]
                
                for info in data[degree]:
                    if language.lower() in info["major"].lower():
                        return {"displayText": json.dumps(info["desc"]), "speech": info["desc"]["detail"]}
                return data["sorry"]
        if req.get("result").get("action") == "_contact_info":
            if ctxt["name"] == "context_contact_info":
                degree = ctxt["parameters"]["degree"]
                language = ctxt["parameters"]["language"]
                
                for info in data[degree]:
                    if language.lower() in info["major"].lower():
                        return {"displayText": info["contact"], "speech": info["contact"]}
                return data["sorry"]
        
    if req.get("result").get("action") == "_search_major":
        degree = req.get("result").get("parameters").get("degree")
        language = req.get("result").get("parameters").get("language")
        
        for info in data[degree]:
            if language.lower() in info["major"].lower():
                
                obj = {
                    "major": info["major"],
                    "degree": info["degree"],
                    "location": info["location"],
                    "options": info["options"],
                    "college": info["college"],
                    "request":info["request"]
                }
                
                test = json.dumps(info)
                
                if "required courses" in test:
                    obj["required courses"] = info["required courses"]
                
                return {"displayText": json.dumps(obj), "speech": info["major"]}
        return data["sorry"]
    
    if req.get("result").get("action") == "_job_placement":
        return {"displayText": json.dumps(data["jobPlacement"]), "speech": data["jobPlacement"]}
    if req.get("result").get("action") == "_scholarship":
        return {"displayText": json.dumps(data["scholarship"]), "speech": data["scholarship"]}
    if req.get("result").get("action") == "_cost_of_program":
        return {"displayText": json.dumps(data["programCost"]), "speech": data["programCost"]}
    if req.get("result").get("action") == "_companies":
        return {"displayText": json.dumps(data["companies"]), "speech": data["companies"]}
    if req.get("result").get("action") == "_executive_program":
        return {"displayText": json.dumps(data["executiveProgram"]), "speech": data["executiveProgram"]}
    
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

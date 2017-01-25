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
    if req.get("result").get("action") == "greet":
        return {
            "speech": "Hi. Pleased to know. Hope you've a good time enjoying the app.",
            "displayText": "Hi. Pleased to know.",
            "source": "test-my-api-ai"
        }
    if req.get("result").get("action") == "course.search":
        return {
            "speech": "Here's the list of courses you wanted",
            "displayText": "EED 123, ABC 345, TTT 789",
            "source": "test-my-api-ai"
        }
    if req.get("result").get("action") == "semester.search":
        return {
            "speech": "Here's the list of Semesters you wanted",
            "displayText": "Fall, Spring, Summer",
            "source": "test-my-api-ai"
        }
    return {
        "speech": "Sorry, I don't think you've asked the right thing!",
        "displayText": "Sorry, I don't think you've asked the right thing!",
        "source": "test-my-api-ai"
    }

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

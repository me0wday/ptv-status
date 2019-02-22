import os
import slackweb
from flask import Flask, request
from utils import get_ptv_status
app = Flask(__name__)
slack = slackweb.Slack(url=os.environ.get('slackhook'))

import requests

@app.route('/')
def index():
	if (request.args.get('token') == os.environ.get('token')):
		status = get_ptv_status()
		return status
	else:
		return "Error"

@app.route('/hook', methods=['GET', 'POST'])
def hook():
	if (request.args.get('token') == os.environ.get('token')):
		status = get_ptv_status()
		slack.notify(text=status)
		print "nice"
		return "Success"
	else:
		return "Error"

if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5000)) 
        app.run(host='0.0.0.0', port=port)

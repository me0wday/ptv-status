from bs4 import BeautifulSoup
import os
from flask import Flask, request
app = Flask(__name__)

import requests

@app.route('/')
def index():
	if (request.args.get('token') == os.environ.get('token')):
		try:
			r  = requests.get("https://www.ptv.vic.gov.au/live-travel-updates/")

			if not r.status_code // 100 == 2:
				return "Error: Unexpected response"

			data = r.text
			soup = BeautifulSoup(data)
			final_string = "*Current status of Victorian train lines:* \n"
			for div in soup.find_all('div', class_='LineInfo'):
					line = div.find('div', class_='titleHolder')
					status = div.find('span', class_='bubbleType')
					more_info = soup.find(id=('article-' + div.get('data-id')))

					if ((line == None) or (status == None)):
						continue

					final_string += "*" +div.find('div', class_='titleHolder').text + "* | "
					if "Good" in status.text:
						final_string += ":green_heart: "
					elif "Major" in status.text:
						final_string += ":red_circle: "
					elif "Minor" in status.text:
						final_string += ":large_orange_diamond: "

					final_string += div.find('span', class_='bubbleType').text

					if not (more_info == None):
						final_string += " | " + soup.find(id=('article-' + div.get('data-id'))).text + "\n"
					else:
						final_string += "\n"
			return final_string
		except requests.exceptions.RequestException as e:
			#return "Error: {}".format(e)
			return "Error"
	else:
		return "Error"

if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5000)) 
        app.run(host='0.0.0.0', port=port)
	
    
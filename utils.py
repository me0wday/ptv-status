from bs4 import BeautifulSoup
import requests
import json

def get_ptv_status():
	final_string = "*Current status of Victorian train lines:* \n"
	try:
		r  = requests.get("https://www.ptv.vic.gov.au/plan/disruptions/")
		if not r.status_code // 100 == 2:
				return "Error: Unexpected response"
		data = r.text
		soup = BeautifulSoup(data, features="html.parser")
		test = soup.find("input", {"id": "fetch-key"})
		route_req = requests.get(u"https://www.ptv.vic.gov.au/lithe/routes?__tok=" + test.get('value'))
		routes = route_req.json()["routes"]
		dis_req = requests.get(u"https://www.ptv.vic.gov.au/lithe/disruptions?__tok=" + test.get('value'))
		disruptions = dis_req.json()["disruptions"]
		disruption_text = ""
		for line in routes:
			has_fault = True
			if line["route_type"] == 0:
				for disruption in disruptions:
					if disruption["display_status"] and disruption["route_ids"]:
						for id in disruption["route_ids"]:
							if id == line["id"]:
								if has_fault:
									kind = disruption["kind"]
									if "Good" in kind:
										final_string += ":green_heart: "
									elif "Major" in kind:
										final_string += ":red_circle: "
									elif "Minor" in kind:
										final_string += ":large_orange_diamond: "
									elif "Part" in kind:
										final_string += ":black_circle: "
									elif "Planned Works" in kind:
										final_string += ":construction: "
									final_string += "*" + line["short_label"] + "*" + "\n"
								final_string += "Disruption: " + disruption["label"] + "\n"
								has_fault = False

	except requests.exceptions.RequestException as e:
		#return "Error: {}".format(e)
		return "Error"

	return final_string

def get_ptv_status_html():
	final_string = "*Current status of Victorian train lines:* <br>"
	try:
		r  = requests.get("https://www.ptv.vic.gov.au/plan/disruptions/")
		if not r.status_code // 100 == 2:
				return "Error: Unexpected response"
		data = r.text
		soup = BeautifulSoup(data, features="html.parser")
		test = soup.find("input", {"id": "fetch-key"})
		route_req = requests.get(u"https://www.ptv.vic.gov.au/lithe/routes?__tok=" + test.get('value'))
		routes = route_req.json()["routes"]
		dis_req = requests.get(u"https://www.ptv.vic.gov.au/lithe/disruptions?__tok=" + test.get('value'))
		disruptions = dis_req.json()["disruptions"]
		disruption_text = ""
		counter = 0
		for line in routes:
			has_fault = True
			if line["route_type"] == 0:
				for disruption in disruptions:
					if disruption["display_status"] and disruption["route_ids"]:
						counter += 1
						for id in disruption["route_ids"]:
							if id == line["id"]:
								if has_fault:
									kind = disruption["kind"]
									if "Good" in kind:
										final_string += "(yes) "
									elif "Major" in kind:
										final_string += "(angry) "
									elif "Minor" in kind:
										final_string += "(worry) "
									elif "Part" in kind:
										final_string += "(swear) "
									elif "Planned Works" in kind:
										final_string += ":construction: "
									final_string += "*" + line["short_label"] + "*" + "<br>"
								final_string += "Disruption: " + disruption["label"] + "<br>"
								has_fault = False
		if counter	== 0:
			final_string = "*No current disruptions*"

	except requests.exceptions.RequestException as e:
		#return "Error: {}".format(e)
		return "Error"

	return final_string



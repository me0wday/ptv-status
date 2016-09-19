from bs4 import BeautifulSoup

def get_ptv_status():
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
				elif "Part" in status.text:
					final_string += ":black_circle: "

				final_string += div.find('span', class_='bubbleType').text

				if not (more_info == None):
					final_string += " | " + soup.find(id=('article-' + div.get('data-id'))).text + "\n"
				else:
					final_string += "\n"
		return final_string
	except requests.exceptions.RequestException as e:
		#return "Error: {}".format(e)
		return "Error"
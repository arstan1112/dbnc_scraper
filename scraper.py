import requests
import csv
import json

def _request(companyName, address1, city, state, postalzip):
	"""Helper function that makes actual http requests

	Makes post requests to check if submitted address is valid

	Returns a string of submitted address status

	"""

	URL = "https://tools.usps.com/tools/app/ziplookup/zipByAddress"
	referer = 'https://tools.usps.com/zip-code-lookup.htm?byaddress'
	headers = {
	    'Accept':'application/json, text/javascript, */*; q=0.01',
	    'Accept-Encoding':'gzip, deflate, br',
	    'Accept-Language':'en-US,en;q=0.8',
	    'Cache-Control':'max-age=0',
	    'Connection':'keep-alive',
	    'Content-Length':'110',
	    'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
	    'Origin':'https://tools.usps.com',
	    'Referer': referer,
	    'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36'
	}
	data = {
	    'companyName': companyName,
	    'address1': address1,
	    'address2': '',
	    'city': city,
	    'state': state,
	    'urbanCode': '',
	    'zip': postalzip
	}

	try:
		page = requests.post(URL, data=data, headers=headers)
	except requests.exceptions.RequestException as e:
		raise SystemExit(e)
	else:
		response_string = page.text
		response = json.loads(response_string)
		response_status = response['resultStatus']
		return response_status

def scrape(filename):
	"""Main function

	Receives a filename of a csv file as 'filename.csv'

	For each row of a csv file makes corresponding requests

	Request response is added to the end of each row

	"""

	file = filename
	with open(file,'r+') as f:
		reader = csv.reader(f)
		writer = csv.writer(f, lineterminator='\n')
		all = []
		row = next(reader)
		row.append('Address search status')
		all.append(row)

		for row in reader:
			response_status = _request(row[0], row[1], row[2], row[3], row[4])
			row.append(response_status)
			all.append(row)
		f.truncate(0)
		writer.writerows(all)

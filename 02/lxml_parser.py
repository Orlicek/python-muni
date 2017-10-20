import requests
from lxml import etree
from io import BytesIO

def get_xml(url=None):
	if not url:
		return None
	resp = requests.get(url)
	return resp.content

def main():
	url = 'https://aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&stationString=LKTB&hoursBeforeNow=2'
	xml = get_xml(url)
	tree = etree.fromstring(xml)
	for elem in tree.findall('.//data/METAR'):
		if temp < date(elem.find('./observation_time').text)
		time = elem.find('./observation_time').text
		temp = elem.find('./temp_c').text
		
		print('{} - {}'.format(time, temp))




if __name__ == '__main__':
	main()


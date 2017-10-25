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
        date_weather = None
        hottest = None
        low_index = 0
        for elem in tree.findall('.//data/METAR'):
            if not hottest:
                hottest = elem.find('./temp_c').text
                date_weather = date(elem.find('./observation_time').text)
            if hottest < elem.find('./temp_c').text:
                hottest = elem.find('./temp_c').text
                date_weather = date(elem.find('./observation_time').text)
        print('{} - {}'.format(date_weather, temp))




if __name__ == '__main__':
    main()


import csv
import json
import requests

from pprint import pprint

def fetch_geocodes(cities):
    d = {}
    url = 'http://maps.googleapis.com/maps/api/geocode/json'
    for city in cities:
        print 'fetching ' + city
        res = requests.get(url, params={
            'address': city,
            'sensor': 'false'
        })
        city = unicode(city.decode('utf8')).encode('utf8')
        d[city] = json.loads(res.content, encoding='utf8')
    return d

with open('ballots.csv', 'r') as f:
    c = csv.reader(f, delimiter=',', quotechar='"')
    data = [x for x in c]
    addresses = map(lambda x: '%s %s, %s' % (x[8], x[9], x[6]), data)
    addresses = list(set(addresses))
    city_data = fetch_geocodes(addresses)
    with open('ballots.json', 'w') as out:
        json.dump(city_data, out, indent=4, ensure_ascii=False)

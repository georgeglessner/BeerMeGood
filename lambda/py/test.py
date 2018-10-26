#!/usr/bin/env python3
import logging
import urllib.request
import urllib.parse
import json

from keys import api_key
from random import randint

# city = intent['slots']['city']['value']
city = 'grand rapids'
city = city.replace(' ', '+')


f = urllib.request.urlopen('http://beermapping.com/webservice/loccity/{}/{}&s=json'.format(api_key, city))

json_string = f.read()
parsed_json = json.loads(json_string)
totalCount = len(parsed_json)

breweries = []

if(totalCount>=1):
    for i in range(0, totalCount):
        if parsed_json[i]['status'] == 'Brewpub':
            breweries.append(parsed_json[i]['name'])

print(breweries[randint(0,len(breweries))])
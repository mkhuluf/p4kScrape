from bs4 import BeautifulSoup
import requests
from pprint import pprint
import time
import urllib3
import urllib
import json
import pandas as pd
from requests import Request, Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
import socket
import sys
from pymongo import MongoClient


DEFAULT_TIMEOUT = 120 # seconds

class TimeoutHTTPAdapter(HTTPAdapter):
    def __init__(self, *args, **kwargs):
        self.timeout = DEFAULT_TIMEOUT
        if "timeout" in kwargs:
            self.timeout = kwargs["timeout"]
            del kwargs["timeout"]
        super().__init__(*args, **kwargs)

    def send(self, request, **kwargs):
        timeout = kwargs.get("timeout")
        if timeout is None:
            kwargs["timeout"] = self.timeout
        return super().send(request, **kwargs)

headers = {
    "User-Agent": "insomnia/2020.5.2",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"
}

retries = Retry(total=5, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504], raise_on_status=False)

http = requests.Session()
http.mount("https://", TimeoutHTTPAdapter(max_retries=retries))
http.mount("http://", TimeoutHTTPAdapter(max_retries=retries))

# entry = {
#     'category': 'album_reviews',
#     'list': []
# }
# temp = {}
# count = 0
# page = 0
# url = 'https://pitchfork.com/api/v2/search/?types=reviews&hierarchy=sections%2Freviews%2Falbums%2Cchannels%2Freviews%2Falbums&sort=publishdate%20desc%2Cposition%20asc&size=200&start=' + str(count)
# baseUrl = 'https://pitchfork.com'
# response = http.get(url, headers=headers)
# info = json.loads(response.content)
# while len(info['results']['list']) != 0:
#     for result in info['results']['list']:
#         entry['list'].append(result)
#     count += 200
#     page += 1
#     print("Scraped page:", page)
#     # print("Time to sleep")
#     # time.sleep(120)
#     url = 'https://pitchfork.com/api/v2/search/?types=reviews&hierarchy=sections%2Freviews%2Falbums%2Cchannels%2Freviews%2Falbums&sort=publishdate%20desc%2Cposition%20asc&size=200&start=' + str(count)
#     baseUrl = 'https://pitchfork.com'
#     response = requests.get(url)
#     info = json.loads(response.content)



entry = {
    'category': 'track_reviews',
    'list': []
}
temp = {}
count = 0
page = 0
url = 'https://pitchfork.com/api/v2/search/?types=reviews&hierarchy=sections%2Freviews%2Ftracks%2Cchannels%2Freviews%2Ftracks&sort=publishdate%20desc%2Cposition%20asc&size=200&start=' + str(count)
baseUrl = 'https://pitchfork.com'
response = http.get(url, headers=headers)
info = json.loads(response.content)
while len(info['results']['list']) != 0:
    for result in info['results']['list']:
        entry['list'].append(result)
    count += 200
    page += 1
    print("Scraped page:", page)
    # print("Time to sleep")
    # time.sleep(120)
    url = 'https://pitchfork.com/api/v2/search/?types=reviews&hierarchy=sections%2Freviews%2Ftracks%2Cchannels%2Freviews%2Ftracks&sort=publishdate%20desc%2Cposition%20asc&size=200&start=' + str(count)    
    baseUrl = 'https://pitchfork.com'
    response = requests.get(url)
    info = json.loads(response.content)




with open('p4kForm_track_reviews.json', 'w') as outfile:
    json.dump(entry, outfile)
entry = json.dumps(entry)


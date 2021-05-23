from bs4 import BeautifulSoup
import requests
import urllib3
import urllib
import json
from requests import Request, Session
from requests.adapters import HTTPAdapter
from urllib3.util import Retry
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

def getAlbumReviews():
    entry = {
        'category': 'album_reviews',
        'results': []
    }

    count = 0
    page = 0

    url = 'https://pitchfork.com/api/v2/search/?types=reviews&hierarchy=sections%2Freviews%2Falbums%2Cchannels%2Freviews%2Falbums&sort=publishdate%20desc%2Cposition%20asc&size=200&start=' + str(count)
    response = http.get(url, headers=headers)
    info = json.loads(response.content)

    while len(info['results']['list']) != 0:
        for result in info['results']['list']:
            entry['results'].append(result)

        count += 200
        page += 1
        print("Scraped page:", page)

        url = 'https://pitchfork.com/api/v2/search/?types=reviews&hierarchy=sections%2Freviews%2Falbums%2Cchannels%2Freviews%2Falbums&sort=publishdate%20desc%2Cposition%20asc&size=200&start=' + str(count)
        response = requests.get(url)
        info = json.loads(response.content)
    
    return entry


def getTrackReviews():
    entry = {
        'category': 'track_reviews',
        'results': []
    }

    count = 0
    page = 0

    url = 'https://pitchfork.com/api/v2/search/?types=reviews&hierarchy=sections%2Freviews%2Ftracks%2Cchannels%2Freviews%2Ftracks&sort=publishdate%20desc%2Cposition%20asc&size=200&start=' + str(count)
    response = http.get(url, headers=headers)
    info = json.loads(response.content)

    while len(info['results']['list']) != 0:
        for result in info['results']['list']:
            entry['results'].append(result)

        count += 200
        page += 1
        print("Scraped page:", page)

        url = 'https://pitchfork.com/api/v2/search/?types=reviews&hierarchy=sections%2Freviews%2Ftracks%2Cchannels%2Freviews%2Ftracks&sort=publishdate%20desc%2Cposition%20asc&size=200&start=' + str(count)    
        response = requests.get(url)
        info = json.loads(response.content)

    return entry


headers = {
    "User-Agent": "insomnia/2020.5.2",
    "Accept-Encoding": "*",
    "Connection": "keep-alive"
}

retries = Retry(total=5, backoff_factor=2, status_forcelist=[429, 500, 502, 503, 504], raise_on_status=False)

http = requests.Session()
http.mount("https://", TimeoutHTTPAdapter(max_retries=retries))
http.mount("http://", TimeoutHTTPAdapter(max_retries=retries))

client = MongoClient('mongodb://localhost:27017/')
db = client.pitchfork
album_reviews = db['track_reviews_demo']

entry = getTrackReviews()

count = 0
for result in entry['results']:
    album_reviews.insert_one(result)
    count += 1
    print("Entries added: ", count)





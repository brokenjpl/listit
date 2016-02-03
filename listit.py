import requests
import json

r = requests.get(r'http://reddit.com/r/climbing/new/.json')
data = r.json();

for child in data['data']['children']:
    print "\t", "[", child['data']['id'] , "]", child['data']['title']


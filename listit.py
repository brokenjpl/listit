import requests
import requests.auth
import json
import argparse
from tabulate import tabulate

#################
## Helpers
################
def trimit(s, l):
    return s if len(s) <= l else s[0:l-3] + '...'

##########################
#Args
#########################
parser = argparse.ArgumentParser(description='CLI Reddit.')
parser.add_argument('--sr', '--subreddit', required=False, default=False, help="Enter the subreddit (no /r)")
parser.add_argument('--view', required=False, default=False, help="Pass the id of the post you want to view")
parser.add_argument('--comments', required=False, default=False, help="Pass the id of the post to view the comments")
args = parser.parse_args()

############################
## OAuth setup
###########################

client_auth = requests.auth.HTTPBasicAuth('X126Mp7itJXFgA', '0f_44ETrBetwOFANv9FznSleWn8')
post_data = {"grant_type": "password", "username": "levacjeep", "password": "hellobob33"}
headers = {"User-Agent": "ListItClient/0.1 by levacjeep"}
response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
jsonResponse = response.json()
access_token = jsonResponse['access_token']

#############
# Action
############
headers = {"Authorization": "bearer " + access_token, "User-Agent": "ListItClient/0.1 by levacjeep"}

uri = "https://oauth.reddit.com"
if args.sr :
    uri += "/r/" + args.sr
if args.view :
    uri += "/by_id/"+args.view
if args.comments :
    uri += "/comments/"+args.comments[3:]

response = requests.get(uri, headers=headers)

##Debug
f = open('ouput.txt', 'w')
f.write(response.text)
f.close()

data = response.json()

###################
# Parse and output
###################
if args.view:
    print "############################################"
    print data['data']['children'][0]['data']['title']
    print "############################################"
    print data['data']['children'][0]['data']['selftext']
    response = requests.get("https://oauth.reddit.com/comments/" + args.view[3:], headers=headers)
if args.comments:


if args.sr:
    list=[]
    for child in data['data']['children']:
        list.append(["[" + child['data']['name'] + "]", "["+ child['data']['domain']+"]", trimit(child['data']['title'], 150)])
        #print "\t [" + child['data']['id'] + "]" , "["+ child['data']['domain']+"]\t\t", trimit(child['data']['title'], 150)
    print tabulate(list)

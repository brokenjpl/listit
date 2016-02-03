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

response = requests.get(uri, headers=headers)

##Debug
f = open('ouput.txt', 'w')
f.write(response.json())
f.close()

data = response.json()

###################
# Parse and output
###################
list=[]
for child in data['data']['children']:
    list.append(["[" + child['data']['id'] + "]", "["+ child['data']['domain']+"]", trimit(child['data']['title'], 150)])
    #print "\t [" + child['data']['id'] + "]" , "["+ child['data']['domain']+"]\t\t", trimit(child['data']['title'], 150)
print tabulate(list)

import sys
import configparser
import requests
import requests.auth
import json
import argparse
import webbrowser
import os.path
from tabulate import tabulate
from colorama import init, Fore, Style

init()

#################
## Helpers
################
def trimit(s, l):
    return s if len(s) <= l else s[0:l-3] + '...'

##########################
# Configs
##########################
config = configparser.RawConfigParser()
config.read(os.path.expanduser('~') + '/.listit/listit.cfg')

##########################
#Args
#########################
parser = argparse.ArgumentParser(description='CLI Reddit.')
parser.add_argument('-sr', '-subreddit', required=False, default=False, help="Enter the subreddit (no /r)")
parser.add_argument('-view', required=False, default=False, help="Pass the id of the post you want to view")
parser.add_argument('-browser', required=False, default=False, help="Pass the id of the post you want to view in your browser")
parser.add_argument('-comments', required=False, default=False, help="Pass the id of the post to view the comments")
parser.add_argument('-ct', '-comment_tree', required=False, default=False, help="Pass the id of the comment to view the comment tree")
args = parser.parse_args()

############################
## OAuth setup
###########################
client_auth = requests.auth.HTTPBasicAuth(config.get('OAuth', 'key.private'), config.get('OAuth', 'key.public'))
post_data = {"grant_type": "password", "username": config.get('OAuth', 'reddit.username'), "password": config.get('OAuth', 'reddit.password')}
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
if args.view or args.browser :
    uri += "/by_id/" + (args.view if args.view else args.browser)
if args.comments :
    uri += "/comments/"+args.comments[3:]

response = requests.get(uri, headers=headers)

data = response.json()

##Debug
f = open('ouput.txt', 'w')
f.write(response.text)
f.close()
###################
# Parse and output
###################
if args.browser:
    webbrowser.open_new_tab('http://reddit.com' + data['data']['children'][0]['data']['permalink'])
    sys.exit()
if args.view:
    print("------------------------------------------------------------------------")
    print(data['data']['children'][0]['data']['title'])
    print("------------------------------------------------------------------------")
    print(data['data']['children'][0]['data']['selftext'])
if args.comments:
    response = requests.get("https://oauth.reddit.com/comments/" + args.comments[3:], headers=headers)
    list=[]
    print("-----------------------------------------------------------------------------------------------")
    for child in data[1]['data']['children'][:3]:
        print(Fore.YELLOW + "[" + child['data']['name'] + "] [score: " + str(child['data']['score']) + "] [replies: " + str(len(child['data']['replies'])) +"]" + Style.RESET_ALL)
        print(child['data']['body'])
        print("-----------------------------------------------------------------------------------------------")
    print("")
if args.sr or (not args.view and not args.comments):
    list=[]
    for child in data['data']['children']:
        list.append(["[" + child['data']['name'] + "]", "["+ child['data']['domain']+"]", trimit(child['data']['title'], 150)])
    print(tabulate(list))

class ListitAction(object):

    def __init__(self, view_id):
        ##########################
        # Configs
        ##########################
        config = configparser.RawConfigParser()
        config.read(os.path.expanduser('~') + '/.listit/listit.cfg')

        ############################
        ## OAuth setup
        ###########################
        client_auth = requests.auth.HTTPBasicAuth(config.get('OAuth', 'key.private'), config.get('OAuth', 'key.public'))
        post_data = {"grant_type": "password", "username": config.get('OAuth', 'reddit.username'), "password": config.get('OAuth', 'reddit.password')}
        headers = {"User-Agent": "ListItClient/0.1 by levacjeep"}
        response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
        jsonResponse = response.json()
        access_token = jsonResponse['access_token']

        #############
        # Action
        ############
        headers = {"Authorization": "bearer " + access_token, "User-Agent": "ListItClient/0.1 by levacjeep"}

    def build_uri():
        return "https://oauth.reddit.com"

    def fetch_response():
        uri = build_uri()
        response =  requests.get(uri, headers=headers)
        return response.json()

    def print(data):
        list=[]
        for child in data['data']['children']:
            list.append(["[" + child['data']['name'] + "]", "["+ child['data']['domain']+"]", trimit(child['data']['title'], 150)])
        print(tabulate(list))

    def execute():
        response = fetch_response()
        print(response)

class ViewAction(ListitAction):

    def __init__(self, view_id):
        this.view_id = view_id

    def build_uri():
        return super(ViewAction, self).build_url() + "/by_id/" + this.view 

class CommentsAction(ListitAction):

    def __init__(self, view_id):
        this.view_id = view_id

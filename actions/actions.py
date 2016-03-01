from tabulate import tabulate
import os.path
import json
import pprint
from tabulate import tabulate
import webbrowser
from colorama import init, Fore, Style
import requests.auth
import requests
import sys
import configparser

'''
    Base class for actions, handles the view of the front page
'''
class ListitAction(object):

    def __init__(self):
        init()
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

        #set the access_token for later use
        self.access_token = jsonResponse['access_token']

    def build_uri(self):
        return "https://oauth.reddit.com"

    def fetch_response(self):
        uri = self.build_uri()
        headers = {"Authorization": "bearer " + self.access_token, "User-Agent": "ListItClient/0.1 by levacjeep"}
        response =  requests.get(uri, headers=headers)
        return response.json()

    def output(self, data):
        list=[]
        for child in data['data']['children']:
            list.append(["[" + child['data']['name'] + "]", "["+ child['data']['domain']+"]", self.trimit(child['data']['title'], 150)])
        print(tabulate(list))

    def execute(self):
        response = self.fetch_response()
        self.output(response)

    #################
    ## Helpers
    ################
    def trimit(self, s, l):
        return s if len(s) <= l else s[0:l-3] + '...'


'''
    Handles the creation of a Comments action. Comments typically required the ID of the post (view_id)
'''
class CommentsAction(ListitAction):

    def __init__(self, view_id):
        super().__init__()
        self.view_id = view_id

    def build_uri(self):
        return super().build_uri() + "/comments/" + self.view_id[3:]

    def output(self, data):
        list=[]
        print("-----------------------------------------------------------------------------------------------")
        for child in data[1]['data']['children'][:5]:
            print(Fore.YELLOW + "[" + child['data']['name'] + "] [score: " + str(child['data']['score']) + "] [replies: " + str(len(child['data']['replies'])) +"]" + Style.RESET_ALL)
            print(child['data']['body'])
            print("-----------------------------------------------------------------------------------------------")
        print("")

class CommentTree(ListitAction):
    
    def __init__(self, comment_id):
        super().__init__()
        self.comment_id = comment_id

    def build_uri(self):
        return super().build_uri() + "/api/info.json?id" + self.comment_id 

    def output(self, data):
        pprint.pprint(data)
    

'''
    Handles the viewing of a post
'''
class ViewAction(ListitAction):

    def __init__(self, view_id):
        super().__init__()
        self.view_id = view_id

    def build_uri(self):
        return super().build_uri() + "/by_id/" + self.view_id 

    def output(self, data):
        #pprint.pprint(data)
        print("------------------------------------------------------------------------")
        print(data['data']['children'][0]['data']['title'])
        print("------------------------------------------------------------------------")
        print(data['data']['children'][0]['data']['selftext'])

    def execute(self):
        data = super().fetch_response()
        #if text only, output to CL
        if data['data']['children'][0]['data']['domain'].startswith('self.'):
            self.output(data)
        #open browser for anything else
        else:
            webbrowser.open(data['data']['children'][0]['data']['url'])


'''
    Handles explicitly opening a post in the browser
'''
class BrowserAction(ListitAction):

    def __init__(self, view_id):
        super().__init__()
        self.view_id = view_id

    def build_uri(self):
       return super().build_uri() + "/by_id/" + view_id

    def execute(self):
        data = self.fetch_response()
        webbrowser.open('http://reddit.com' + data['data']['children'][0]['data']['permalink'])

'''
    Handles viewing a specific subreddit
'''
class SubredditAction(ListitAction):

    def __init__(self, subreddit):
        super().__init__()
        self.subreddit = subreddit

    def build_uri(self):
        return super().build_uri() + "/r/" + self.subreddit

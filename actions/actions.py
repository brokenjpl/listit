from tabulate import tabulate
import configparser

'''
    Base class for actions
'''
class ListitAction(object):

    def __init__(self):
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

    def build_uri(self):
        return "https://oauth.reddit.com"

    def fetch_response(self):
        uri = build_uri()
        response =  requests.get(uri, headers=headers)
        return response.json()

    def print(self, data):
        list=[]
        for child in data['data']['children']:
            list.append(["[" + child['data']['name'] + "]", "["+ child['data']['domain']+"]", trimit(child['data']['title'], 150)])
        print(tabulate(list))

    def execute(self):
        response = fetch_response()
        print(response)

'''
    Handles the creation of a Comments action. Comments typically required the ID of the post (view_id)
'''
class CommentsAction(ListitAction):

    def __init__(self, view_id):
        this.view_id = view_id

'''
    Handles the viewing of a post
'''
class ViewAction(ListitAction):

    def __init__(self, view_id):
        super.__init__()
        self.view_id = view_id

    def build_uri(self):
        return super(ViewAction, self, view_id).build_url() + "/by_id/" + this.view 

    def print(self):
        data = super.fetch_response(self);
        print("------------------------------------------------------------------------")
        print(data['data']['children'][0]['data']['title'])
        print("------------------------------------------------------------------------")
        print(data['data']['children'][0]['data']['selftext'])

'''
    Handles explicitly opening a post in the browser
'''
class BrowserAction(ListitAction):

    def __init__(self, view_id):
        super.__init__(self)
	this.view_id = view_id

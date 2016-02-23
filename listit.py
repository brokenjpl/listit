import configparser
import argparse

from actions.actions import *

##########################
# Functions
##########################

##########################
#Args
##########################
parser = argparse.ArgumentParser(description='CLI Reddit: Listit')
parser.add_argument('-sr', '-subreddit',  help="Enter the subreddit (no /r)")
parser.add_argument('-view', '-v',  help="Pass the id of the post you want to view")
parser.add_argument('-browser', '-b',  help="Pass the id of the post you want to view in your browser")
parser.add_argument('-comments', '-c',  help="Pass the id of the post to view the comments")
parser.add_argument('-ct', '-comment_tree',  help="Pass the id of the comment to view the comment tree")

args = parser.parse_args()

action = None

if args.sr:
    action = SubredditAction(args.sr)
if args.view:
    action = ViewAction(args.view)
if args.browser:
    action = BrowserAction(args.browser)
if args.comments: 
    action = CommentsAction(args.comments)
if action == None:
    action = ListitAction()

action.execute()

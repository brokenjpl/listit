import configparser
import argparse

from actions.actions import *

##########################
#Args
#########################
parser = argparse.ArgumentParser(description='CLI Reddit.')
parser.add_argument('-sr', '-subreddit', required=False, default=False, help="Enter the subreddit (no /r)")
parser.add_argument('-view', '-v', required=False, default=False, help="Pass the id of the post you want to view")
parser.add_argument('-browser', '-b', required=False, default=False, help="Pass the id of the post you want to view in your browser")
parser.add_argument('-comments', '-c', required=False, default=False, help="Pass the id of the post to view the comments")
parser.add_argument('-ct', '-comment_tree', required=False, default=False, help="Pass the id of the comment to view the comment tree")
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
if not args.sr and not args.view and not args.browser and not args.comments:
    action = ListitAction()

action.execute()

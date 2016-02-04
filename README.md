#List it

This is a small simple personal project to learn a bit about python.  It is a python script which calls the reddit API and allows you to "read" reddit articles within your command line.

##Configuration

###Dependencies
Python3 is required to run this script.  You will also need to install **tabular** : 

> sudo pip3 install tabular

##OAuth##
Listit requries OAuth for reddit. To gain access //TODO

##User Configs##
Create a folder under your home directory called **.listit** and create a file called **listit.cfg**.

In the file enter the following:

>[OAuth]
>key.private=*your private Oauth key*
>key.public=*your public Oauth key*
>reddit.username=*your reddit username*
>reddit.password=*your reddit password*


##Running the script##
Simply run the script to get the front page posts of reddit: **python3 listit.py**


-Jeep

#!/usr/bin/env python

import facebook
import requests
import json
import webbrowser
import time

#get the code to perform the login
print("Hi! So you're trying to buy tickets from people selling them on Facebook Events, huh?")
print("Before doing this, create an app on https://developers.facebook.com/ so you have a client_id (App Id) and a client_secret (App Secret).")
print("Also don't forget to set a redirect uri pointing to https://www.facebook.com/connect/login_success.html (Settings > Advanced > Client Oauth Settings - Valid OAuth Redirect URIs)')")
client_id = raw_input("Once you're done, please enter your client_id:")
client_secret = raw_input("Okay, now our client_secret:")
print('QUICK! A browser tab is going to open in 10 seconds. Your browser URL will change right after your login is done. Copy the URL >before< it changes, so you can get the code. (look for "code=" and copy whats after it)')
time.sleep(10)
webbrowser.open('https://www.facebook.com/dialog/oauth?client_id='+ client_id +'&redirect_uri=https://www.facebook.com/connect/login_success.html')
code = raw_input('Enter code:')
if '#_=_' in code:
    code = code.replace('#_=_','')
r = requests.get('https://graph.facebook.com/v2.3/oauth/access_token?client_id='+client_id+'&redirect_uri=https://www.facebook.com/connect/login_success.html&client_secret='+client_secret+'&code='+code)
json = json.loads(r.text)
graph = facebook.GraphAPI(json['access_token'])

#get event using its ID
print("You're doing great! Now tell me the ID from the event you want me to look. It's the numbers after 'events/' in the URL when you open the event on the browser.")
event_id = raw_input("Event ID:")
event = graph.get_object(event_id)
print("Thanks! I'm going to look "+event['name']+" for you.")

print("Is your ticket for a gender only? If it is, type either 'fem' or 'masc'.")
gender = raw_input("If not, just type enter :)")

#creates file to use later
open('post_ids.txt', 'w+')

print(" I'll start my search. If you're tired of me, just cancel the execution.")
#runs forever till you cancel it
while 1==1:
    #get posts from event feed (put a high limit)
    posts = graph.get_connections(event['id'], 'feed', limit=150)['data']

    for post in posts:
        # false default
        sold = False

        #get posts selling and for the gender specified. (if no gender it's ok as well)
        if 'vendo' in post['message'].lower() and gender in post['message'].lower():
            
            # search if is already sold
            comments = graph.get_connections(post['id'], 'comments')['data']
            for comment in comments:
                #gets both 'vendi' and 'vendido' :P
                if 'vendi' in comment['message'].lower():
                    sold = True

            # if still selling, send inbox message to the author 
            #>>>>> API DISABLED THIS, so it opens a browser tab showing the post
            if not sold:
                #author_name = graph.get_connections(post['id'], '', fields='from')['from']

                #check if this post wasn't opened before
                f = open('post_ids.txt', 'r')
                data = f.read()
                f.close()
                permalink = post['id'].split('_')[1]

                #if first time this post shows up, opens it then write on the file
                if permalink not in data:
                    webbrowser.open("https://fb.com/events/"+event['id']+"/permalink/"+permalink)
                    f = open('post_ids.txt','a+')
                    f.write(permalink+'\n')
                    f.close()
                    print("Ticket found! But don't worry, I'm already looking for another.")
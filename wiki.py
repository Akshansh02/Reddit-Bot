import praw
import config
import time
import os
import wikipedia


def bot_login():
    r = praw.Reddit(username=config.username,
                password=config.password,
                client_id=config.client_id,
                client_secret=config.client_secret,
                user_agent="cipher's reddit bot"
                )
    return r


def get_saved_comments():
    if not os.path.isfile("comments_replied_to.txt"):
        comments_replied_to = []
    else:
        with open("comments_replied_to.txt","r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
           # comments_replied_to = filter(None,comments_replied_to)

    return comments_replied_to



def run_bot(r):
    for comment in r.subreddit('testingground4bots').comments(limit=25):
        if "!cipherWiki" in comment.body and comment.id not in comments_replied_to:

            #Split Comment 
            breakedComment = comment.body.split()

            #Word to get meaning of
            if len(breakedComment) <2:
                 print("No word")
                 
            else:
                search = comment.body.split(' ', 1)[1]
                
                try:
                   output =  wikipedia.summary(search, sentences=2)
                except:
                    print("not found")
                    output = "NOt Found"
                
                #Get Username
                username = comment.author
                
             
                #send Message with answer
                r.redditor(username.name).message("<===>\n  " + search,  output)
            
            comments_replied_to.append(comment.id)
            with open("comments_replied_to.txt","a") as f:
                f.write(comment.id + "\n")  
            
            



r = bot_login()
comments_replied_to = get_saved_comments()
while(True):
    run_bot(r)
    print("Going to sleep For 5 sec")
    time.sleep(5)


import praw
import config
import time
import os
from PyDictionary import PyDictionary
import json



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
        if "!cipherDict" in comment.body and comment.id not in comments_replied_to:

            #Split Comment 
            breakedComment = comment.body.split()

            #Word to get meaning of
            if len(breakedComment) <2:
                 print("No word")
                 
            else:
                word = breakedComment[breakedComment.index("!cipherDict") + 1]
                meaning = dictionary.meaning(word)

                #Format JSON
                output = ""
                for catg in meaning: 
                    output += "\n==>" + catg
                    for mean in meaning[catg]:
                        output += "\n\t" + "--" + mean 
 

                #Get Username
                username = comment.author
                #send Message with meaning
                r.redditor(username.name).message("Meaning of " + word, "\t" + output)
                print(word, output)
            
            comments_replied_to.append(comment.id)
            with open("comments_replied_to.txt","a") as f:
                f.write(comment.id + "\n")  
            
            


dictionary=PyDictionary()
r = bot_login()
comments_replied_to = get_saved_comments()
while(True):
    run_bot(r)
    print("Going to sleep For 10 sec")
    time.sleep(10)


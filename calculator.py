import praw
import config
import time
import os
import math

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
        if "!cipherCalc" in comment.body and comment.id not in comments_replied_to:

            #Split Comment 
            breakedComment = comment.body.split()

            #Word to get meaning of
            if len(breakedComment) <2:
                 print("No word")
                 
            else:
                equation = breakedComment[breakedComment.index("!cipherCalc") + 1]
                
               
                #Get Username
                username = comment.author
                
                #TODO: solve the math expression EQUATION
                search = comment.body.split(' ')
                
                if(search[1] == 'sqrt'):
                    output=math.sqrt(float(search[2]))
                    
                elif(search[1] == 'fact'):
                    output=math.factorial(int(search[2]))
                    
                    
                elif(search[1] == 'log'):
                    output=math.log(float(search[2])) 


                #send Message with answer
                r.redditor(username.name).message("Ans of the " +   equation,output)
                
            
            comments_replied_to.append(comment.id)
            with open("comments_replied_to.txt","a") as f:
                f.write(comment.id + "\n")  
            
            


r = bot_login()
comments_replied_to = get_saved_comments()
while(True):
    run_bot(r)
    print("Going to sleep For 5 sec")
    time.sleep(10)


import praw
import config
import time
import requests
import json
import os


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
        with open("comments_replied_to.txt", "r") as f:
            comments_replied_to = f.read()
            comments_replied_to = comments_replied_to.split("\n")
    return comments_replied_to


def run_bot(r):
    for comment in r.subreddit('testingground4bots').comments(limit=25):
        if "!cipherWeather" in comment.body and comment.id not in comments_replied_to:

            # Split Comment
            breakedComment = comment.body.split()

            # Word to get meaning of
            if len(breakedComment) < 2:
                 print("No word")

            else:
                city_name = comment.body.split(' ', 1)[1]

                try:
                   api_key = "61d8904485f99b27e8604cde0d85a356"
                   base_url = "http://api.openweathermap.org/data/2.5/weather?q="
                   city_name = "bangalore"
                   complete_url = base_url + city_name + "&APPID=" + api_key
                   response = requests.get(complete_url)
                   x = response.json()

                   if x["cod"] == "404":
                       print("Not found")
                       output = "City Not Found"

                   else:
                       # store the value of "main"
                       # key in variable y
                       y = x["main"]

                       # store the value corresponding
                       # to the "temp" key of y
                       current_temperature = y["temp"]

                        # store the value corresponding
                        # to the "pressure" key of y
                       current_pressure = y["pressure"]

                        # store the value corresponding
                        # to the "humidity" key of y
                       current_humidiy = y["humidity"]

                        # store the value of "weather"
                        # key in variable z
                       z = x["weather"]

                        # store the value corresponding
                        # to the "description" key at
                        # the 0th index of z
                       weather_description = z[0]["description"]

                        # print following values
                       output = (" Temperature (in kelvin unit) = " +
                                        str(current_temperature) +
                              "\n atmospheric pressure (in hPa unit) = " +
                                        str(current_pressure) +
                              "\n humidity (in percentage) = " +
                                        str(current_humidiy) +
                              "\n description = " +
                                        str(weather_description))
                       

                        

                   
                except:
                    print("not found")
                    output = "NOt Found"
                
                # Get Username
                username = comment.author
                
                print(output)
                # send Message with answer
                r.redditor(username.name).message("<===>\n  " + city_name,  output)
            
            comments_replied_to.append(comment.id)
            with open("comments_replied_to.txt","a") as f:
                f.write(comment.id + "\n")  
            
            


r = bot_login()
comments_replied_to = get_saved_comments()
while(True):
    run_bot(r)
    print("Going to sleep For 5 sec")
    time.sleep(10)


#Ayden Hayes
#12/12/24
#scrape.py 
# initial test to scrape spanish speaking subreddits for eventual use in a corpus // data analysis // spanish learning project
import praw 
import json
from subs import subreddits
from reddit_config import  REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT
from prawcore.exceptions import RequestException, TooManyRequests 
import time

#----------------------#
#SETINGS:
NUM_POSTS = 100 #posts per sub
OUTPUT_FILE = "./testjson/bigtest3.json"
MAX_RETRIES = 5
#----------------------#



reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)


def scrape_reddit(subreddit_name, limit=NUM_POSTS): #personally lowering this
    attempt = 1
    print(f"Preparing to scrape: r/{subreddit_name}. Attempt: {attempt}")

    subreddit = reddit.subreddit(subreddit_name)
    data = []
    while attempt < MAX_RETRIES:
        try:
            for index, post in enumerate(subreddit.top(limit=limit)): #hot, new, or top
                print(f"Starting post: {index}")
                post_data = {
                    'id': post.id,
                    'title': post.title,
                    'selftext': post.selftext,
                    'comments': []
                }

                post.comments.replace_more(limit=0) # ? 
                comment_index = 0
                for comment_index, comment in enumerate(post.comments.list()):
                    #print(f"Found comment number: {comment_index}")
                    post_data['comments'].append(comment.body)
                print(f"Found: {comment_index} comments")

                data.append(post_data)

                if index +1 >= limit:
                    break
            break

        except TooManyRequests as e:
            time_sleep = attempt * 60
            print(f"Rate limited. sleeping for {time_sleep} seconds")
            time.sleep(time_sleep)
            attempt += 1
            print("Continuing.  . .")
        except RequestException as e:
            print(f"Skipping {subreddit}. Error: {e}") 
    if attempt > MAX_RETRIES:
        print(f"max  retries reached for r/{subredit_name}, Skipping...")

    return data 

if __name__ == "__main__": 
    for sub in subreddits: 
        data = scrape_reddit(sub) 
        try:  
            with open(OUTPUT_FILE, 'r') as output:
                existing_data = json.load(output)
        except FileNotFoundError: #start an empty list if file wasn't found
            existing_data = []
        existing_data.append(data)

        #append all data after creating list
        with open(OUTPUT_FILE, 'w') as output:
            json.dump(data, output, ensure_ascii=False, indent=4)

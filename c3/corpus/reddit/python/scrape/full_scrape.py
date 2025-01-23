#Ayden Hayes
#12/12/24
#full_scrape.py 
# should be able to scrape using larger compilation of subreddits
import praw 
import json
from reddit_config import  REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, REDDIT_USER_AGENT
from prawcore.exceptions import RequestException, TooManyRequests 
from subs import subreddits
import time

#----------------------#
#SETTINGS:
NUM_POSTS = 1000 # posts per sub. Most subs wont reach this rate but it maximizes amount of data per sub
OUTPUT_FILE = "./testjson/fullscrape2.json"
FAILLOG = "./log/fullscrapefail.txt"
BASEDATALOG = "./log/base.txt"
MAX_RETRIES = 5
#----------------------#

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent=REDDIT_USER_AGENT
)

"""
subreddits_to_scrape = []

with open('./subreddits_by_keyword.json', 'r') as data_file:
    data_json = json.load(data_file)

    for keyword in data_json:
        for subreddit in data_json[keyword]:
            subreddits_to_scrape.append(subreddit["name"].lower())
"""

failed_subs = []
subreddit_base_data = {}

def scrape_reddit(subreddit_name, limit=NUM_POSTS):
    attempt = 1
    print(f"Preparing to scrape: r/{subreddit_name}")

    subreddit = reddit.subreddit(subreddit_name)
    data = []
    last_index = 0  # Track the last processed post index

    while attempt <= MAX_RETRIES:
        try:
            for index, post in enumerate(subreddit.top(limit=limit)):
                if index < last_index:  # Skip posts that have already been processed
                    continue

                print(f"Starting post: {index}")
                post_data = {
                    'id': post.id,
                    'title': post.title,
                    'selftext': post.selftext,
                    'comments': []
                }

                post.comments.replace_more(limit=0)
                comment_index = 0
                for comment_index, comment in enumerate(post.comments.list()):
                    post_data['comments'].append(comment.body)

                print(f"Found: {comment_index} comments")
                data.append(post_data)

                # Update the last processed post index
                last_index = index + 1

                # Explicitly check if we hit the post limit
                if last_index >= limit:
                    print(f"Successfully scraped {limit} posts from r/{subreddit_name}")
                    return data

            # Break the retry loop if successful
            break

        except TooManyRequests as e:
            time_sleep = 2 * attempt  # Exponential backoff
            print(f"Rate limited. Sleeping for {time_sleep} seconds")
            time.sleep(time_sleep)
            attempt += 1
            print(f"Retry attempt {attempt}/{MAX_RETRIES} for r/{subreddit_name}...")

        except RequestException as e:
            print(f"Request error for r/{subreddit_name}: {e}")
            break  # Log and move on to the next subreddit

    if attempt > MAX_RETRIES:
        print(f"Max retries reached for r/{subreddit_name}. Skipping...")
    return data


if __name__ == "__main__":
    for sub in subreddits:
        scraped_data = scrape_reddit(sub)
        try:
            with open(OUTPUT_FILE, 'r') as output:
                existing_data = json.load(output)
        except FileNotFoundError:
            existing_data = []
        existing_data.extend(scraped_data)

        # Save scraped data
        with open(OUTPUT_FILE, 'w') as output:
            json.dump(existing_data, output, ensure_ascii=False, indent=4)

    # Save failed subreddits
    with open(FAILLOG, 'a') as log:
        for failed_subreddit in failed_subs:
            log.write(f"{failed_subreddit}\n")

    # Save base data log
    with open(BASEDATALOG, 'a') as log:
        for subreddit, metadata in subreddit_base_data.items():
            log.write(f"{subreddit}: {metadata}\n")

print("Scraping completed!")


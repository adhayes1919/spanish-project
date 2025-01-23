import json
from subs import subreddits

for i, s in enumerate(subreddits):
    subreddits[i] = s.lower()
    
new_subs = []

with open('./subreddits_by_keyword.json', 'r') as data_file:
    data_json = json.load(data_file)

    count = 0
    for keyword in data_json:
        for subreddit in data_json[keyword]:
            count += 1
            name = subreddit["name"]
            new_subs.append(name.lower())

for sub in subreddits:
    if sub not in new_subs:
        new_subs.append(sub)

print(new_subs)
        

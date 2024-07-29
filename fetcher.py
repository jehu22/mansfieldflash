import feedparser
import time
from datetime import datetime, timedelta

city_name = "Mansfield"
city_code = "CAAqIggKIhxDQkFTRHdvSkwyMHZNREV6Yld0aUVnSmxiaWdBUAE"
local_paper = "Mansfield Record"

removal_pubs = ["Lakewood/East Dallas Advocate", "Oak Cliff Advocate"]

def get_news(location):
    # Construct the Google News RSS feed URL for the specified location
    feed_url = f"https://news.google.com/rss/topics/{location}?hl=en-US&gl=US&ceid=US%3Aen"
    
    # Parse the RSS feed
    feed = feedparser.parse(feed_url)
    
    # Extract news entries
    news_entries = feed.entries
    
    return news_entries

# Get entries
news_entries = get_news(city_code)

# Get current time
current_time = time.time()

# Calculate the timestamp for the start of the last day
last_day_timestamp = current_time - 86400  # 86400 seconds in a day

# create a new list of filtered entries
filtered_entries = []

# Separate entries containing "city name"
city_entries = []

# Get all entries in the last day
for entry in news_entries:
    # Convert published time to timestamp
    published_time = time.mktime(entry.published_parsed)

    if published_time >= last_day_timestamp and not any(pub in entry.title for pub in removal_pubs):
        if city_name in entry.title or local_paper in entry.title:
            city_entries.append(entry)
        else:
            filtered_entries.append(entry)


# add city entries into filtered entries
filtered_entries= city_entries + filtered_entries

# Print the titles of the first few news entries
for entry in filtered_entries[:1]:
    print(entry['link'])
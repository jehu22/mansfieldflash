from flask import Flask, render_template
from weather import get_weather_data, generate_weather_summary
import feedparser 
import time
from datetime import datetime
from functools import wraps
import json
from threading import Lock

app = Flask(__name__)

# Cache configuration
NEWS_CACHE_DURATION = 3600  # 1 hour in seconds
WEATHER_CACHE_DURATION = 1800  # 30 minutes in seconds

class Cache:
    def __init__(self):
        self.cache = {}
        self.lock = Lock()
    
    def get(self, key):
        with self.lock:
            if key in self.cache:
                item = self.cache[key]
                if time.time() - item['timestamp'] < item['duration']:
                    return item['data']
                else:
                    del self.cache[key]
            return None
    
    def set(self, key, data, duration):
        with self.lock:
            self.cache[key] = {
                'data': data,
                'timestamp': time.time(),
                'duration': duration
            }

# Initialize cache
cache = Cache()

# Cache decorator
def cached(duration):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Create a cache key from the function name and arguments
            key = f'{f.__name__}:{str(args)}:{str(kwargs)}'
            
            # Try to get from cache
            result = cache.get(key)
            if result is not None:
                return result
            
            # If not in cache, call the function and cache the result
            result = f(*args, **kwargs)
            cache.set(key, result, duration)
            return result
        return decorated_function
    return decorator

city_name = "Mansfield"
city_code = "CAAqIggKIhxDQkFTRHdvSkwyMHZNREV6Yld0aUVnSmxiaWdBUAE"
local_paper = "Mansfield Record"
removal_pubs = ["Lakewood/East Dallas Advocate", "Oak Cliff Advocate"]

@cached(NEWS_CACHE_DURATION)
def get_news(location):
    # Construct the Google News RSS feed URL for the specified location
    feed_url = f"https://news.google.com/rss/topics/{location}?hl=en-US&gl=US&ceid=US%3Aen"
    
    # Parse the RSS feed
    feed = feedparser.parse(feed_url)
    
    # Extract news entries and convert to cacheable format
    news_entries = []
    for entry in feed.entries:
        news_entries.append({
            'title': entry.title,
            'link': entry.link,
            'published_parsed': time.mktime(entry.published_parsed)
        })
    
    return news_entries

@cached(NEWS_CACHE_DURATION)
def filter_news_entries(news_entries_json, city_name, local_paper, removal_pubs):
    # Convert the JSON-serializable news_entries back to a usable format
    news_entries = json.loads(news_entries_json)
    
    # Get current time
    current_time = time.time()
    last_day_timestamp = current_time - 86400

    filtered_entries = []
    city_entries = []

    for entry in news_entries:
        published_time = entry['published_parsed']

        if published_time >= last_day_timestamp and not any(pub in entry['title'] for pub in removal_pubs):
            if city_name in entry['title'] or local_paper in entry['title']:
                city_entries.append(entry)
            else:
                filtered_entries.append(entry)

    filtered_entries = city_entries + filtered_entries
    return filtered_entries[:10]

@cached(WEATHER_CACHE_DURATION)
def get_cached_weather():
    weather_data = get_weather_data()
    return generate_weather_summary(weather_data)

@app.route('/')
def home():
    try:
        # Get news entries with caching
        news_entries = get_news(city_code)
        # Convert to JSON string for caching
        news_entries_json = json.dumps(news_entries)
        filtered_entries = filter_news_entries(news_entries_json, city_name, local_paper, removal_pubs)

        # Get weather with caching
        high_temp, low_temp, temp_unit, wind_speed, wind_direction, short_forecast, detailed_forecast, rain_chance = get_cached_weather()

        return render_template('index.html', 
                             entries=filtered_entries,
                             high_temp=high_temp,
                             low_temp=low_temp,
                             temp_unit=temp_unit,
                             wind_speed=wind_speed,
                             wind_direction=wind_direction,
                             short_forecast=short_forecast,
                             detailed_forecast=detailed_forecast,
                             rain_chance=rain_chance)
    except Exception as e:
        # Log the error (you might want to use a proper logging solution)
        print(f"Error in home route: {str(e)}")
        return render_template('error.html', error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
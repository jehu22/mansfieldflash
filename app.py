from flask import Flask, render_template
from weather import get_weather_data, generate_weather_summary
import feedparser 
import time

app = Flask(__name__)

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

def filter_news_entries(news_entries, city_name, local_paper, removal_pubs):
    # Get current time
    current_time = time.time()

    # Calculate the timestamp for the start of the last day
    last_day_timestamp = current_time - 86400  # 86400 seconds in a day

    # Create a new list of filtered entries
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

    # Add city entries into filtered entries
    filtered_entries = city_entries + filtered_entries

    #limit it to 10
    filtered_entries = filtered_entries[0:10]

    return filtered_entries

@app.route('/')
def home():
    # Get news entries
    news_entries = get_news(city_code)
    filtered_entries = filter_news_entries(news_entries, city_name, local_paper, removal_pubs)

    # Get the weather data and generate the summary
    weather_data = get_weather_data()
    high_temp, low_temp, temp_unit, wind_speed, wind_direction, short_forecast, detailed_forecast, rain_chance = generate_weather_summary(weather_data)

    return render_template('index.html', entries=filtered_entries, high_temp=high_temp, low_temp=low_temp, temp_unit=temp_unit, wind_speed=wind_speed, wind_direction=wind_direction, short_forecast=short_forecast, detailed_forecast=detailed_forecast, rain_chance=rain_chance)

if __name__ == '__main__':
    app.run(debug=True)
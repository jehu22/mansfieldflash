from flask import Flask, render_template
from weather import get_weather_data, generate_weather_summary
from fetcher import fetch_and_filter          # <-- import the rewritten fetcher
import time
from functools import wraps
from threading import Lock

app = Flask(__name__)

# ---------------------------------------------------------------------
# Simple in-memory cache (same pattern you already had)
# ---------------------------------------------------------------------
NEWS_CACHE_DURATION = 3600   # 1 hour
WEATHER_CACHE_DURATION = 1800  # 30 minutes


class Cache:
    def __init__(self):
        self.cache = {}
        self.lock = Lock()

    def get(self, key):
        with self.lock:
            if key in self.cache:
                item = self.cache[key]
                if time.time() - item["timestamp"] < item["duration"]:
                    return item["data"]
                else:
                    del self.cache[key]
            return None

    def set(self, key, data, duration):
        with self.lock:
            self.cache[key] = {
                "data": data,
                "timestamp": time.time(),
                "duration": duration,
            }


cache = Cache()


def cached(duration):
    def decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            key = f"{f.__name__}:{args}:{kwargs}"
            result = cache.get(key)
            if result is not None:
                return result
            result = f(*args, **kwargs)
            cache.set(key, result, duration)
            return result

        return wrapped

    return decorator


# ---------------------------------------------------------------------
# Weather helpers
# ---------------------------------------------------------------------
@cached(WEATHER_CACHE_DURATION)
def get_cached_weather():
    weather_data = get_weather_data()
    return generate_weather_summary(weather_data)


# ---------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------
@app.route("/")
def home():
    try:
        # fetcher.py now does all the RSS + Selenium work and returns filtered entries
        filtered_entries = cache.get("filtered_entries")
        if filtered_entries is None:
            filtered_entries = fetch_and_filter()
            cache.set("filtered_entries", filtered_entries, NEWS_CACHE_DURATION)

        high_temp, low_temp, temp_unit, wind_speed, wind_direction, \
            short_forecast, detailed_forecast, rain_chance = get_cached_weather()

        return render_template(
            "index.html",
            entries=filtered_entries,
            high_temp=high_temp,
            low_temp=low_temp,
            temp_unit=temp_unit,
            wind_speed=wind_speed,
            wind_direction=wind_direction,
            short_forecast=short_forecast,
            detailed_forecast=detailed_forecast,
            rain_chance=rain_chance,
        )
    except Exception as e:
        print(f"Error in home route: {e}")
        return render_template("error.html", error=str(e)), 500


if __name__ == "__main__":
    app.run(debug=True)

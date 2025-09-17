from fetcher import fetch_and_filter
from jinja2 import Environment, FileSystemLoader
from weather import get_weather_data, generate_weather_summary

# --- Step 1: Fetch news once ---
entries = fetch_and_filter()

#--- Step 2: Fetch weather once ---
weather_data = get_weather_data()
(
    high_temp,
    low_temp,
    temp_unit,
    wind_speed,
    wind_direction,
    short_forecast,
    detailed_forecast,
    rain_chance,
) = generate_weather_summary(weather_data)

# --- Step 3: Load your template ---
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("index.html")  # reuse your existing Flask template

# --- Step 4: Render the HTML ---
output = template.render(
    entries=entries,
    high_temp=high_temp,
    low_temp=low_temp,
    temp_unit=temp_unit,
    wind_speed=wind_speed,
    wind_direction=wind_direction,
    short_forecast=short_forecast,
    detailed_forecast=detailed_forecast,
    rain_chance=rain_chance,
)

# --- Step 4: Save to public folder ---
with open("public/index.html", "w", encoding="utf-8") as f:
    f.write(output)

print("✅ Static news page generated with", len(entries), "entries!")

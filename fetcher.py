import feedparser
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def fetch_and_filter():
    """
    Fetch Google News RSS entries for the Mansfield topic,
    filter to the last 24 hours, de-prioritize certain publishers,
    and follow redirects to the real article URLs.
    Returns a list of feedparser-style entry objects
    with updated .link values where possible.
    """

    # --- configuration ---
    city_name = "Mansfield"
    city_code = "CAAqIggKIhxDQkFTRHdvSkwyMHZNREV6Yld0aUVnSmxiaWdBUAE"
    local_paper = "Mansfield Record"
    removal_pubs = ["Lakewood/East Dallas Advocate", "Oak Cliff Advocate"]

    # --- helpers ---
    def setup_driver():
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument(
            "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko)"
        )
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        try:
            return webdriver.Chrome(options=chrome_options)
        except Exception as e:
            print(f"Chrome driver setup failed: {e}")
            return None

    def get_news(location):
        feed_url = (
            f"https://news.google.com/rss/topics/{location}"
            "?hl=en-US&gl=US&ceid=US%3Aen"
        )
        return feedparser.parse(feed_url).entries

    # --- fetch feed ---
    news_entries = get_news(city_code)
    last_day_timestamp = time.time() - 86400  # 24 hours ago

    filtered_entries, city_entries = [], []

    # --- filter by recency and publisher ---
    for entry in news_entries:
        published_time = time.mktime(entry.published_parsed)
        if published_time >= last_day_timestamp and not any(
            pub in entry.title for pub in removal_pubs
        ):
            if city_name in entry.title or local_paper in entry.title:
                city_entries.append(entry)
            else:
                filtered_entries.append(entry)

    # Prioritize city-specific entries, limit to 10
    filtered_entries = (city_entries + filtered_entries)[:10]

    # --- follow redirects to get real article URLs ---
    driver = setup_driver()
    if driver:
        driver.set_page_load_timeout(10)
        for entry in filtered_entries:
            try:
                driver.get(entry.link)
                time.sleep(3)  # allow redirects
                final_url = driver.current_url
                if "google.com" not in final_url and len(final_url) > 30:
                    entry.link = final_url
            except Exception as e:
                print(f"Error processing entry '{entry.title}': {e}")
                continue
        driver.quit()
    else:
        print("❌ Could not initialize Chrome driver - keeping original URLs")

    return filtered_entries


# Optional: allow quick testing from the command line
if __name__ == "__main__":
    for e in fetch_and_filter():
        print(f"{e.title}: {e.link}")

import requests
from bs4 import BeautifulSoup
import datetime

def get_news_headlines(stock, day_offset=0):
    target_date = datetime.datetime.now() - datetime.timedelta(days=day_offset)
    date_str = target_date.strftime("%Y-%m-%d")
    query = f"{stock} stock when:{day_offset}d"
    rss_url = f"https://news.google.com/rss/search?q={query}"

    headlines = []
    try:
        headers = {"User-Agent": "Mozilla/5.0"}

        resp = requests.get(rss_url, headers=headers)
        soup = BeautifulSoup(resp.content, features="xml")
        items = soup.findAll("item")
        for item in items[:5]:
            headlines.append(item.title.text)
    except:
        pass
    return headlines

import requests
from bs4 import BeautifulSoup
import datetime
import streamlit as st


def get_news_headlines(stock, day_offset=0):
    query = f"{stock} stock when:{day_offset}d"
    rss_url = f"https://news.google.com/rss/search?q={query}"
    headlines = []

    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        resp = requests.get(rss_url, headers=headers)

        # Debug output to Streamlit UI
        #st.text(f"Fetching: {rss_url}")
        #st.text(f"Response code: {resp.status_code}")
        #st.text(f"Response size: {len(resp.content)} bytes")

        soup = BeautifulSoup(resp.content, features="xml")
        items = soup.findAll("item")
        for item in items[:5]:
            headlines.append(item.title.text)

    except Exception as e:
        st.error(f"Error fetching news: {e}")

    return headlines

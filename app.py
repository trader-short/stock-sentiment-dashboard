import streamlit as st
from news_scraper import get_news_headlines
from sentiment_model import analyze_sentiment
import pandas as pd
import datetime

from ticker_lookup import load_valid_tickers, is_valid_ticker

valid_tickers = load_valid_tickers()

st.set_page_config(page_title="📈 AI Stock Sentiment", layout="wide")

st.markdown(
    "<h1 style='color:#336699;'>📊 AI Stock Sentiment Dashboard</h1>",
    unsafe_allow_html=True,
)

stock = st.text_input("🔎 Enter Stock Ticker (e.g., AAPL, TSLA)", value="AAPL")

if stock and not is_valid_ticker(stock, valid_tickers):
    st.error("❌ Invalid ticker. Please enter a valid US (NASDAQ) or Indian (NSE) stock symbol.")
    st.stop()
# ========== DAILY TREND ========== #
def get_sentiment_trend(stock, days=7):
    date_list = []
    compound_scores = []

    for day_offset in range(days):
        date = (datetime.datetime.now() - datetime.timedelta(days=day_offset)).strftime("%Y-%m-%d")
        headlines = get_news_headlines(stock, day_offset)
        
        if headlines:
            daily_scores = []
            for headline in headlines:
                result = analyze_sentiment(headline)
                score = result.get("positive", 0) - result.get("negative", 0)  # Fix here
                daily_scores.append(score)
            avg_score = sum(daily_scores) / len(daily_scores)
            date_list.append(date)
            compound_scores.append(avg_score)

    df = pd.DataFrame({
        "Date": date_list[::-1],
        "Sentiment Score": compound_scores[::-1]
    })
    return df

# ========== MAIN LOGIC ========== #
if st.button("📥 Analyze Today's Headlines"):
    with st.spinner("Fetching today's headlines..."):
        headlines = get_news_headlines(stock)
        if not headlines:
            st.warning("No headlines found.")
        else:
            st.subheader("🗞️ Top News & Sentiment")
            for i, headline in enumerate(headlines):
                st.markdown(f"### {i+1}. {headline}")
                sentiment = analyze_sentiment(headline)
                dominant = max(sentiment, key=sentiment.get)
                st.success(f"**{dominant.upper()}** — {sentiment[dominant]*100:.1f}%")
                st.bar_chart(sentiment)
                st.markdown("---")

if st.button("📆 Show 7-Day Sentiment Trend"):
    with st.spinner("Building 7-day sentiment profile..."):
        trend_df = get_sentiment_trend(stock)
        st.subheader("📈 Weekly Sentiment Trend")
        st.line_chart(trend_df.set_index("Date"))


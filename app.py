import requests
import pandas as pd
import streamlit as st

st.set_page_config(page_title="CryptoWatch", layout="wide")
st.title("🚀 CryptoWatch — Real-Time Market Sentiment Tracker")

@st.cache_data(ttl=120)
def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        if not data:
            return None

        df = pd.DataFrame(data)[[
            "name",
            "symbol",
            "current_price",
            "market_cap",
            "price_change_percentage_24h"
        ]]

        df.columns = ["Coin", "Symbol", "Price", "Market Cap", "24h Change (%)"]

        return df

    except Exception as e:
        st.error("⚠ API Error")
        st.write(e)
        return None


def add_sentiment(df):
    def logic(x):
        if x > 5:
            return "🚀 Bullish"
        elif x < -5:
            return "🔻 Bearish"
        else:
            return "😐 Neutral"

    df["Sentiment"] = df["24h Change (%)"].apply(logic)
    return df


df = fetch_crypto_data()

if df is not None:
    df = add_sentiment(df)

    st.subheader("📊 Market Overview")
    st.dataframe(df)

    st.subheader("📈 24h Change Chart")
    st.bar_chart(df.set_index("Coin")["24h Change (%)"])
else:
    st.warning("No data available. API may be temporarily unavailable.")
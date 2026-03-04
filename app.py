import requests
import pandas as pd

def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 20,
        "page": 1
    }

    response = requests.get(url, params=params)
    data = response.json()
    df = pd.DataFrame(data)
    df = df[[
        "name",
        "symbol",
        "current_price",
        "market_cap",
        "price_change_percentage_24h"
    ]]

    df.rename(columns={
        "current_price": "Price",
        "market_cap": "Market Cap",
        "price_change_percentage_24h": "24h Change (%)"
    }, inplace=True)

    return df
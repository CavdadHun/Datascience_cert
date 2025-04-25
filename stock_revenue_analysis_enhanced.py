import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go

# Function to extract revenue data from Macrotrends
def get_revenue_data(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    tables = soup.find_all("table")
    revenue_data = pd.DataFrame(columns=["Date", "Revenue"])

    if len(tables) >= 2:
        revenue_table = tables[1]
        rows = revenue_table.find_all("tr")
        for row in rows[1:]:
            cols = row.find_all("td")
            if len(cols) == 2:
                date = cols[0].text.strip()
                revenue = cols[1].text.strip().replace("$", "").replace(",", "")
                if revenue:
                    revenue_data = pd.concat([
                        revenue_data,
                        pd.DataFrame([{"Date": date, "Revenue": revenue}])
                    ], ignore_index=True)
    return revenue_data

# Function to make stock price and revenue graph
def make_graph(stock_data, revenue_data, title):
    stock_data["Date"] = pd.to_datetime(stock_data["Date"])
    revenue_data["Date"] = pd.to_datetime(revenue_data["Date"])

    fig = go.Figure()

    fig.add_trace(go.Scatter(x=stock_data["Date"], y=stock_data["Close"], name="Stock Price"))
    fig.add_trace(go.Scatter(x=revenue_data["Date"], y=revenue_data["Revenue"].astype(float), name="Revenue"))

    fig.update_layout(title=title, xaxis_title="Date", yaxis_title="USD", template="plotly_dark")
    fig.show()

# Tesla stock data
tesla = yf.Ticker("TSLA")
tesla_data = tesla.history(period="max").reset_index()
print("Tesla Stock Data (Head):")
print(tesla_data.head())

# Tesla revenue data
tesla_revenue = get_revenue_data("https://www.macrotrends.net/stocks/charts/TSLA/tesla/revenue")
print("Tesla Revenue Data (Tail):")
print(tesla_revenue.tail())

# GME stock data
gme = yf.Ticker("GME")
gme_data = gme.history(period="max").reset_index()
print("GME Stock Data (Head):")
print(gme_data.head())

# GME revenue data
gme_revenue = get_revenue_data("https://www.macrotrends.net/stocks/charts/GME/gamestop/revenue")
print("GME Revenue Data (Tail):")
print(gme_revenue.tail())

# Plot Tesla graph
make_graph(tesla_data, tesla_revenue, "Tesla Stock Price vs Revenue")

# Plot GME graph
make_graph(gme_data, gme_revenue, "GameStop Stock Price vs Revenue")

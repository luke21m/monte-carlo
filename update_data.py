# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "pandas",
#     "yfinance",
# ]
# ///
import pandas as pd
import yfinance as yf


def main():
    btc = yf.Ticker("BTC-USD")
    data = btc.history(period="max", interval="1d").reset_index()
    last_date = data["Date"].iloc[-1]
    filename = "btc_price_data.csv"
    data.to_csv(filename)
    print(f"Data updated thru {last_date.date()} and saved as '{filename}'.")


if __name__ == "__main__":
    main()

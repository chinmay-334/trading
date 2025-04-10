import yfinance as yf
import pandas as pd
import os
from datetime import datetime, timedelta



tickers = [
    "^NSEI", "^BSESN", "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "LT.NS", "AXISBANK.NS", "SBIN.NS", "HINDUNILVR.NS", "ITC.NS", "KOTAKBANK.NS", "BHARTIARTL.NS",
    "WIPRO.NS", "ASIANPAINT.NS", "DMART.NS", "SUNPHARMA.NS", "NESTLEIND.NS", "HCLTECH.NS",
    "BAJFINANCE.NS", "ULTRACEMCO.NS", "TITAN.NS", "TECHM.NS", "BAJAJFINSV.NS", "ADANIENT.NS",
    "JSWSTEEL.NS", "NTPC.NS", "POWERGRID.NS", "COALINDIA.NS", "BPCL.NS", "ONGC.NS", "IOC.NS",
    "TATAMOTORS.NS", "MARUTI.NS", "EICHERMOT.NS", "HEROMOTOCO.NS", "BAJAJ-AUTO.NS", "CIPLA.NS",
    "DIVISLAB.NS", "GRASIM.NS", "DRREDDY.NS", "HINDALCO.NS", "TATASTEEL.NS", "INDUSINDBK.NS",
    "BRITANNIA.NS", "M&M.NS", "ADANIPORTS.NS", "SHREECEM.NS", "SBILIFE.NS", "ICICIPRULI.NS",
    "HDFCLIFE.NS"
]

period_map = {
    "1week": "5d"


    
    
}

def fetch_and_save(period_folder: str, period_code: str):
    save_path = f"data/{period_folder}"
    os.makedirs(save_path, exist_ok=True)

    for ticker in tickers:
        try:
            print(f"📥 Downloading {ticker} for {period_folder}")
            df = yf.download(ticker, period=period_code, progress=False)[["Open", "High", "Low", "Close", "Volume"]]
            df = df.reset_index()
            df.insert(0, 'Ticker', ticker)
            df.to_csv(f"{save_path}/{ticker}.csv", index=False)
        except Exception as e:
            print(f"❌ Failed to download {ticker}: {e}")


def fetch_intraday_yesterday():
    save_path = "data/1day"
    os.makedirs(save_path, exist_ok=True)

    today = datetime.today()
    yesterday = today - timedelta(days=1)
    start_date = yesterday.strftime('%Y-%m-%d')
    end_date = today.strftime('%Y-%m-%d')

    for ticker in tickers:
        try:
            print(f"📥 Downloading {ticker} intraday data for {start_date}")
            df = yf.download(ticker, start=start_date, end=end_date,
                             interval='5m', progress=False)[["Open", "High", "Low", "Close", "Volume"]]

            if not df.empty:
                # Localize to UTC first, then convert to IST
                df.index = df.index.tz_localize("UTC").tz_convert("Asia/Kolkata")

                df = df.reset_index()
                df['Time'] = df['Datetime'].dt.strftime('%H:%M')  # Extract time only
                df.insert(0, 'Ticker', ticker)
                df = df[['Ticker', 'Time', 'Open', 'High', 'Low', 'Close', 'Volume']]
                df.to_csv(f"{save_path}/{ticker}.csv", index=False)
            else:
                print(f"⚠️ No data found for {ticker} on {start_date}")
        except Exception as e:
            print(f"❌ Failed to download {ticker}: {e}")

fetch_intraday_yesterday()
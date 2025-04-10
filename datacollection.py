import yfinance as yf
import pandas as pd
import datetime

# NSE tickers (append .NS for yfinance)
tickers = [
    "^NSEI","^BSESN",
    "RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS",
    "LT.NS", "AXISBANK.NS", "SBIN.NS", "HINDUNILVR.NS", "ITC.NS",
    "KOTAKBANK.NS", "BHARTIARTL.NS", "WIPRO.NS", "ASIANPAINT.NS", "DMART.NS",
    "SUNPHARMA.NS", "NESTLEIND.NS", "HCLTECH.NS", "BAJFINANCE.NS", "ULTRACEMCO.NS",
    "TITAN.NS", "TECHM.NS", "BAJAJFINSV.NS", "ADANIENT.NS", "JSWSTEEL.NS",
    "NTPC.NS", "POWERGRID.NS", "COALINDIA.NS", "BPCL.NS", "ONGC.NS",
    "IOC.NS", "TATAMOTORS.NS", "MARUTI.NS", "EICHERMOT.NS", "HEROMOTOCO.NS",
    "BAJAJ-AUTO.NS", "CIPLA.NS", "DIVISLAB.NS", "GRASIM.NS", "DRREDDY.NS",
    "HINDALCO.NS", "TATASTEEL.NS", "INDUSINDBK.NS", "BRITANNIA.NS", "M&M.NS",
    "ADANIPORTS.NS", "SHREECEM.NS", "SBILIFE.NS", "ICICIPRULI.NS", "HDFCLIFE.NS"
]

# Define the target date
target_date = "2025-04-09"
target_dt = datetime.datetime.strptime(target_date, "%Y-%m-%d")
start_dt = target_dt - datetime.timedelta(days=7)
end_dt = target_dt + datetime.timedelta(days=1)

# Prepare to store results
rows = []

for ticker in tickers:
    try:
        data = yf.download(ticker, start=start_dt.strftime("%Y-%m-%d"), end=end_dt.strftime("%Y-%m-%d"))
        data = data.dropna()  # remove incomplete rows (e.g., holidays)

        if target_date not in data.index.strftime('%Y-%m-%d'):
            print(f"⚠️ {ticker} - No data for {target_date}")
            continue

        idx = data.index.get_loc(pd.to_datetime(target_date))
        if idx == 0:
            print(f"⚠️ {ticker} - No previous data available for return calc.")
            continue

        today = data.iloc[idx]
        prev = data.iloc[idx - 1]

        open_price = today["Open"]
        close_price = today["Close"]
        volume = today["Volume"]
        prev_close = prev["Close"]

        daily_return = (close_price - open_price) / open_price
        previous_return = (open_price - prev_close) / prev_close

        rows.append({
            "Ticker": ticker,
            "Open": round(open_price, 2),
            "Close": round(close_price, 2),
            "Volume": int(volume),
            "PrevClose": round(prev_close, 2),
            "DailyReturn": round(daily_return, 6),
            "PrevReturn": round(previous_return, 6)
        })

    except Exception as e:
        print(f"❌ Skipping {ticker} due to error: {e}")

# Final DataFrame
df = pd.DataFrame(rows)
df["Open"] = df["Open"].astype(float)
df["Close"] = df["Close"].astype(float)
df["PrevClose"] = df["PrevClose"].astype(float)
df["Volume"] = df["Volume"].astype(int)
df["DailyReturn"] = df["DailyReturn"].astype(float)
df["PrevReturn"] = df["PrevReturn"].astype(float)
df.to_csv("stock_one_day_snapshot.csv", index=False)
print("✅ Data saved to stock_one_day_snapshot.csv")

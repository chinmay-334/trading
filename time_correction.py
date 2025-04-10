import pandas as pd
from datetime import datetime, timedelta

# Load your CSV
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

for i in range(len(tickers)):
    df = pd.read_csv(f"data/1day/{tickers[i]}.csv")

    # Shift time by 6.5 hours
    df['Time'] = pd.to_datetime(df['Time'], format='%H:%M') + timedelta(hours=5, minutes=30)

    # Optional: format back to HH:MM
    df['Time'] = df['Time'].dt.strftime('%H:%M')

    # Save it back
    df.to_csv(f"data/1day/{tickers[i]}.csv", index=False)



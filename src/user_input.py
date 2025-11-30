import yfinance as yf
import warnings
import sys
import os

def ticker_exists(ticker):
    warnings.filterwarnings("ignore")
    stderr_backup = sys.stderr
    sys.stderr = open(os.devnull, "w")

    try:
        data = yf.download(ticker, period="1d", interval="1d", progress=False)
        return not data.empty
    except:
        return False
    finally:
        sys.stderr.close()
        sys.stderr = stderr_backup


def collect_user_config():
    portfolio = {}
    alerts = {}

    print("=== Portfolio Setup ===")
    while True:
        ticker = input("Enter ticker to buy (Enter to finish): ").strip().upper()
        if ticker == "":
            break

        if not ticker_exists(ticker):
            print("Ticker does not exist. Try again.")
            continue

        try:
            shares = int(input(f"How many shares of {ticker}? "))
        except ValueError:
            print("Invalid number.")
            continue

        portfolio[ticker] = shares

        alert_choice = input(f"Do you want to set an alert for {ticker}? (y/n): ").strip().lower()
        if alert_choice == "y":
            try:
                limit = float(input(f"Alert when {ticker} price exceeds: "))
                alerts[ticker] = limit
            except ValueError:
                print("Invalid price.")

    symbols = list(set(portfolio.keys()) | set(alerts.keys()))
    return portfolio, alerts, symbols

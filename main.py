from src.user_input import collect_user_config
from src.trade_engine import TradeEngine

if __name__ == "__main__":
    portfolio, alerts, symbols = collect_user_config()

    print("\n=== Starting Engine with your configuration ===")
    print("Portfolio:", portfolio)
    print("Alerts:", alerts)
    print("Symbols to watch:", symbols)
    print("----------------------------------------------\n")

    engine = TradeEngine(portfolio, alerts, symbols)
    engine.start()
    engine.run_monitor()

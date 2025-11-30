import threading
import time
import queue
from src.shared_state import SharedState
from src.workers import LoggerThread, PriceProducer, PortfolioConsumer, AlertConsumer

class TradeEngine:
    def __init__(self, portfolio, alerts, symbols):
        self.stop_event = threading.Event()
        self.shared_state = SharedState(portfolio, alerts, symbols)
        self.price_queue = queue.Queue()
        self.log_queue = queue.Queue()

        self.logger_thread = LoggerThread(self.log_queue, self.stop_event)
        self.producer = PriceProducer(
            self.shared_state, self.price_queue, self.log_queue, self.stop_event
        )
        self.portfolio_consumer = PortfolioConsumer(
            self.shared_state, self.price_queue, self.log_queue, self.stop_event
        )
        self.alert_consumer = AlertConsumer(
            self.shared_state, self.log_queue, self.stop_event
        )

    def start(self):
        print("Starting all threads...")
        self.logger_thread.start()
        self.producer.start()
        self.portfolio_consumer.start()
        self.alert_consumer.start()

    def run_monitor(self):
        try:
            while True:
                time.sleep(3)
                with self.shared_state.lock:
                    print("---")
                    print("Prices:", self.shared_state.prices)
                    print("Portfolio value:", self.shared_state.portfolio_value)
                    print("---")
        except KeyboardInterrupt:
            print("You stopped the application")

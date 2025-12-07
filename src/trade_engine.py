import threading
import time
import queue
from src.shared_state import SharedState
from src.workers import PriceProducer, PortfolioConsumer, AlertConsumer

class TradeEngine:
    def __init__(self, portfolio, alerts, symbols):
        self.stop_event = threading.Event()
        self.shared_state = SharedState(portfolio, alerts, symbols)
        self.price_queue = queue.Queue()
        self.log_queue = queue.Queue()

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
        self.log_queue.put("Starting all threads...")
        self.producer.start()
        self.portfolio_consumer.start()
        self.alert_consumer.start()

    def run_monitor(self):
        try:
            while True:
                time.sleep(3)
        except KeyboardInterrupt:
            self.log_queue.put("Application stopped")

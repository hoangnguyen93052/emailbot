import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
import time
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)

class DataHandler:
    def __init__(self, symbol, start_date, end_date):
        self.symbol = symbol
        self.start_date = start_date
        self.end_date = end_date
        self.data = None

    def fetch_data(self):
        logging.info(f"Fetching data for {self.symbol} from {self.start_date} to {self.end_date}")
        self.data = yf.download(self.symbol, start=self.start_date, end=self.end_date)
        self.data = self.data[['Open', 'High', 'Low', 'Close', 'Volume']]
        self.data.dropna(inplace=True)
        logging.info("Data fetched successfully")

    def get_data(self):
        return self.data

class Strategy:
    def __init__(self, data):
        self.data = data

    def moving_average_crossover(self, short_window, long_window):
        logging.info("Starting Moving Average Crossover strategy")
        signals = pd.DataFrame(index=self.data.index)
        signals['price'] = self.data['Close']
        signals['short_mavg'] = self.data['Close'].rolling(window=short_window, min_periods=1).mean()
        signals['long_mavg'] = self.data['Close'].rolling(window=long_window, min_periods=1).mean()
        signals['signal'] = 0.0
        signals['signal'][short_window:] = np.where(signals['short_mavg'][short_window:] > signals['long_mavg'][short_window:], 1.0, 0.0)
        signals['positions'] = signals['signal'].diff()
        logging.info("Signals generated")
        return signals

class Backtester:
    def __init__(self, strategy, initial_capital):
        self.strategy = strategy
        self.initial_capital = initial_capital
        self.positions = pd.Series(index=self.strategy.data.index).fillna(0)
        self.portfolio = pd.DataFrame(index=self.strategy.data.index)

    def backtest(self):
        logging.info("Starting backtest")
        self.portfolio['holdings'] = (self.positions * self.strategy.data['Close'])
        self.portfolio['cash'] = self.initial_capital - (self.positions.diff() * self.strategy.data['Close']).cumsum()
        self.portfolio['total'] = self.portfolio['cash'] + self.portfolio['holdings']
        self.portfolio['returns'] = self.portfolio['total'].pct_change()
        logging.info("Backtest complete")
        return self.portfolio

    def plot_results(self):
        logging.info("Plotting results")
        plt.figure(figsize=(12, 8))
        plt.plot(self.portfolio['total'], label='Total Portfolio Value')
        plt.title('Backtest Portfolio Value')
        plt.legend()
        plt.show()

class TradingBot:
    def __init__(self, symbol, start_date, end_date, short_window, long_window, initial_capital):
        logging.info("Initializing Trading Bot")
        self.data_handler = DataHandler(symbol, start_date, end_date)
        self.data_handler.fetch_data()
        self.data = self.data_handler.get_data()
        self.strategy = Strategy(self.data)
        self.signals = self.strategy.moving_average_crossover(short_window, long_window)
        self.backtester = Backtester(self.signals, initial_capital)
        self.positions = self.signals['positions']

    def run_backtest(self):
        self.backtester.positions = self.positions
        portfolio = self.backtester.backtest()
        self.backtester.plot_results()

if __name__ == "__main__":
    symbol = 'AAPL'
    start_date = '2020-01-01'
    end_date = datetime.now().strftime('%Y-%m-%d')
    short_window = 40
    long_window = 100
    initial_capital = 100000

    trading_bot = TradingBot(symbol, start_date, end_date, short_window, long_window, initial_capital)
    trading_bot.run_backtest()
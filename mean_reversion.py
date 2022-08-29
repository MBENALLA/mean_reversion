import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas_ta as ta
import logging as log
import yfinance as finance
from binance.client import Client


class MeanReversion:

    def __init__(self, ticker, rsi=6, window=Client.KLINE_INTERVAL_30MINUTE):
        self.ticker = ticker
        self.window = window
        self.client_exchange = Client()
        # self.data = finance.download(self.ticker, start='2019-01-01')
        self.data = self.get_ticker_data()
        self.rsi = rsi
        if self.data.empty:
            log.warning('No data fetched ...')
        else:
            self.compute_indicators()
            self.compute_signals()
            self.compute_positions()
            self.profit = self.compute_profit()
            self.cumulative_profit = (self.profit + 1).prod() - 1

    def get_ticker_data(self):
        data = pd.DataFrame(self.client_exchange.get_historical_klines(self.ticker,
                                                                       self.window,
                                                                       start_str='2022-08-28'))
        data = data.iloc[:,0:5]
        data.columns = ['date', 'Open', 'High', 'Low', 'Close']
        data = data.set_index('date')
        data.index = pd.to_datetime(data.index, unit='ms')
        data = data.astype(float)
        return data

    def compute_indicators(self):
        self.data['rsi'] = ta.rsi(self.data.Close, length=self.rsi)
        self.data['ma20'] = self.data.Close.rolling(21).mean()
        self.data['extent'] = self.data.Close.rolling(21).std()
        self.data['lower_bb'] = self.data.ma20 - (2 * self.data.extent)
        self.data['upper_bb'] = self.data.ma20 + (2 * self.data.extent)
        self.data.dropna(inplace=True)

    def compute_signals(self):
        conditions = [(self.data.rsi < 25) & (self.data.Close < self.data.lower_bb),
                      (self.data.rsi > 75) & (self.data.Close > self.data.upper_bb)]
        choices = ['buy', 'sell']
        self.data['signals'] = np.select(conditions, choices)
        self.data.signals = self.data.signals.shift()
        self.data.dropna(inplace=True)

    def compute_positions(self):
        in_position = False
        buys_idx, sells_idx = [], []
        #buy_price = 0
        for idx, row in self.data.iterrows():
            if not in_position and row['signals'] == 'buy':
                buys_idx.append(idx)
                in_position = True
                buy_price = row['Open']
            elif in_position and row['signals'] == 'sell': # or (in_position and row['Close']):
                sells_idx.append(idx)
                in_position = False
        self.buys = self.data.loc[buys_idx].Open
        self.sells = self.data.loc[sells_idx].Open

    def compute_profit(self):
        len_sells = len(self.sells)
        len_buys = len(self.buys)
        if len_buys > len_sells:
            self.buys = self.buys[:len_sells]
        else:
            self.sells = self.sells[:len_buys]
        return (self.sells.values - self.buys.values) / self.buys.values

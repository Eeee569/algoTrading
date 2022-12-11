import yfinance as yf
import pandas as pd

# snp = yf.Ticker("SPY")
# hist = snp.history(period="max",interval='1d')
#
# print(hist.head())

class Stock_data:

    def _get_yf_data(self, ticker):
        self.yf_data = yf.Ticker(ticker)
        self.history = self.yf_data.history(period="max", interval='1d')

    def __init__(self, ticker):
        self._get_yf_data(ticker)

    def data_as_df(self):
        return self.history


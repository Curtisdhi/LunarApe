import os
import json
import requests
import yfinance as yf

class StockApi:

    def __init__(self):
        self._session = requests.Session()
        self._session.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0" 

    def getQuotes(self, quotes: tuple):
        data = []

        for q in quotes:
            q = q.strip().upper()
            ticker = yf.Ticker(q, self._session)
            data.append(Quote(**ticker.info))
        return data


class Quote:
    def __init__(self, **entries):
        self.__dict__.update(entries)
        self.gain = round(self.bid - self.previousClose, 2)
        self.gainPercent = round(1 - (self.previousClose / self.bid), 4)


import os
import json
import requests
import yfinance as yf

class StockApi:

    def __init__(self):
        self._session = requests.Session()
        self._session.headers['User-Agent'] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0" 

    def getQuotes(self, quotes: tuple):
        data = {}

        for q in quotes:
            q = q.strip().upper()
            ticker = yf.Ticker(q, self._session)
            if ticker.info != None and 'symbol' in ticker.info:
                data[q] = Quote(**ticker.info)
            else:
                data[q] = None
        return data


class Quote:
    def __init__(self, **entries):
        self.__dict__.update(entries)
        if not hasattr(self, 'bid') or self.bid is None:
            if hasattr(self, 'regularMarketPrice') and self.regularMarketPrice != None:
                self.bid = self.regularMarketPrice
            else:
                self.bid = 0
        if not hasattr(self, 'name') or self.name is None:
            if hasattr(self, 'longName') and self.longName != None:
                self.name = self.longName
            elif hasattr(self, 'shortName') and self.shortName != None:
                self.name = self.shortName
            else:
                self.name = ""
        if not hasattr(self, 'description') or self.description is None:
            if hasattr(self, 'longBusinessSummary') and self.longBusinessSummary != None:
                self.description = self.longBusinessSummary
            elif hasattr(self, 'shortBusinessSummary') and self.shortBusinessSummary != None:
                self.description = self.shortBusinessSummary
            else:
                self.description = ""
                
        if not hasattr(self, 'previousClose') or self.previousClose is None:
            self.previousClose = 0
        if not hasattr(self, 'regularMarketOpen') or self.regularMarketOpen is None:
            self.regularMarketOpen = 0
        if not hasattr(self, 'dayHigh') or self.dayHigh is None:
            self.dayHigh = 0
        if not hasattr(self, 'dayLow') or self.dayLow is None:
            self.dayLow = 0

        self.gain = self.bid - self.previousClose
        self.gainPercent = 0
        if (self.bid != 0 and self.previousClose != 0):
            self.gainPercent = round((self.bid - self.previousClose) / self.previousClose, 4)


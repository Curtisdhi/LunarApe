import os
import http.client
import json

class StockApi:

    def __init__(self):
        self.token = os.getenv('STOCKAPI_TOKEN')
    

    def getHttpResponse(self, url: str):
        conn = http.client.HTTPSConnection("finnhub.io")

        headers = {
            "Content-type": "application/json",
            "X-Finnhub-Token": self.token
        }
        data = "{}"
        try:
            conn.request("GET", url, headers=headers)
            res = conn.getresponse()
            data = res.read().decode("utf-8")
            
        except http.client.HTTPException as e:
            print("failed to get response from {}. \n error: {}".format(url, e.message))
        finally:
            conn.close()

        return json.loads(data)

    def getQuotes(self, quotes: tuple):
        data = []
        for q in quotes:
            url = "/api/v1/quote?symbol="+ q.strip().upper()
            d = self.getHttpResponse(url)
            data.append(Quote(q, d["c"], d["h"], d["l"], d["pc"], d["o"]))

        return data


class Quote:
    def __init__(self, ticker, current, high, low, previous, open):
        self.ticker = ticker
        self.current = current
        self.high = high
        self.low = low
        self.previous = previous
        self.open = open
        self.gain = round(current - previous, 2)
        self.gainPercent = round(1 - (previous / current), 2)
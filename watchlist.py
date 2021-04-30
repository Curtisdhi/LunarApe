import sqlite3

class WatchList:

    @staticmethod
    def getConnection():
        return sqlite3.connect('stonks.db')

    @staticmethod
    def get(channelId, name):
        con = WatchList.getConnection()
        cur = con.cursor()

        cur.execute("SELECT * FROM watch_list WHERE channel_id = ? AND name = ?", (channelId, name))
        
        data = cur.fetchone()

        con.close()

        if data is None:
            return None

        return WatchList(data[0], data[1], data[2].split(','))

    @staticmethod
    def getAll(channelId = None):
        con = WatchList.getConnection()
        cur = con.cursor()

        if channelId is None:
            cur.execute("SELECT * FROM watch_list")
        else:
            cur.execute("SELECT * FROM watch_list WHERE channel_id = ?", (channelId,))

        data = cur.fetchall()

        con.close()

        watchlists = []
        for d in data:
            watchlists.append(WatchList(d[0], d[1], d[2].split(',')))
        return watchlists

    @staticmethod
    def delete(channelId, name):
        con = WatchList.getConnection()
        cur = con.cursor()

        cur.execute("DELETE FROM watch_list WHERE channel_id = ? AND name = ?", (channelId, name))
        
        con.commit()
        con.close()

    def __init__(self, channelId, name, symbols):
        self.channelId = channelId
        self.name = name
        self.symbols = symbols

    def persist(self, update = False):
        con = WatchList.getConnection()
        cur = con.cursor()

        if update:
            sql = "UPDATE watch_list SET symbols = :symbols WHERE channel_id = :channel_id AND name = :name"
        else:
            sql = "INSERT INTO watch_list (channel_id, name, symbols) VALUES (:channel_id, :name, :symbols)"
        cur.execute(sql, {"channel_id": self.channelId, "name": self.name, "symbols": ','.join(self.symbols)})

        con.commit()
        cur.close()
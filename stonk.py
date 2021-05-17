import os
import textwrap
import discord
from discord.ext import commands
from async_timeout import timeout
from stockapi import StockApi
from watchlist import WatchList
class Stonk(commands.Cog):

    def __init__(self, client):
        self.name = "Stonk"
        self.client = client
        self.api = StockApi()

    @commands.command(aliases=["ticker", "t"])
    async def quote(self, ctx, *stonkSymbols):
        quotes = self.api.getQuotes(stonkSymbols)

        for sym in quotes:
            if (quotes[sym] == None):
                await ctx.send("Unable to find symbol: {}".format(sym))
            else:
                await ctx.send(embed=self.createQuoteEmbed(quotes[sym]))

    @commands.command(aliases=["g"])
    async def gain(self, ctx, *stonkSymbols):
        quotes = self.api.getQuotes(stonkSymbols)

        hasQuote = False
        gains = []
        notFoundSymbols = []
        for sym in quotes:
            if (quotes[sym] == None):
                notFoundSymbols.append(sym)
            else:
                hasQuote = True
                gains.append(self.createGainMessage(quotes[sym]))

        if len(notFoundSymbols) > 0:
            await ctx.send("Unable to find symbol(s): {}".format(', '.join(notFoundSymbols)))    
        if hasQuote:
            await ctx.send("```diff\n{}\n```".format('\n'.join(gains)))
             

    @commands.command(aliases=["w"])
    async def watch(self, ctx, *, args):
        arguments = args.split()
        if (len(arguments) > 0):
            action = arguments[0].strip().lower()
        else:
            await ctx.send("An action or name required!")
            return

        if (len(arguments) > 1):
            name = arguments[1].strip().lower()
        else:
            name = action

        stonkSymbols = []
        if (len(arguments) > 2):
            for i in range(2, len(arguments)):
                stonkSymbols.append(arguments[i])

        #add
        if (action == "add"):
            watchList = WatchList.get(ctx.channel.id, name)
            if watchList != None:
                await ctx.send("Watchlist **{}** already exists.".format(name))
            else:
                quotes = self.api.getQuotes(stonkSymbols)
                safeQuotes = {}
                for sym in quotes:
                    if (quotes[sym] == None):
                        await ctx.send("Unable to find symbol: **{}**".format(sym))
                    else:
                        safeQuotes[sym] = quotes[sym]
                if (len(safeQuotes) > 0):
                    watchList = WatchList(ctx.channel.id, name, list(safeQuotes.keys()))
                    watchList.persist()
                    await ctx.send("Watchlist **{}** has been created.".format(name))
                else:
                    await ctx.send("No symbols to watch!")
        #update
        if (action == "edit"):

            watchList = WatchList.get(ctx.channel.id, name)
            if watchList is None:
                await ctx.send("Watchlist **{}** does not exists.".format(name))
            else:
                quotes = self.api.getQuotes(stonkSymbols)
                safeQuotes = {}
                for sym in quotes:
                    if (quotes[sym] == None):
                        await ctx.send("Unable to find symbol: **{}**".format(sym))
                    else:
                        safeQuotes[sym] = quotes[sym]
                if (len(safeQuotes) > 0):
                    watchList.symbols = list(safeQuotes.keys())
                    watchList.persist(True)
                    await ctx.send("Watchlist **{}** has been updated.".format(name))
                else:
                    await ctx.send("No symbols to watch!")
        
        #delete
        elif (action == "del" or action == "delete"):
            WatchList.delete(name)
            await ctx.send("Deleted {}".format(name))

        #list
        elif (action == "list"):
            watchlists = WatchList.getAll(ctx.channel.id)
            names = []
            if len(watchlists) > 0:
                for watch in watchlists:
                    names.append(watch.name)
                await ctx.send("Available watchlists: **{}**".format(', '.join(names)))
            else:
                await ctx.send("No available watchlists.")
        #help
        elif (action == "help"):
            await ctx.send("Ex: **$watch (action) (name) (symbols)**")
            await ctx.send("Actions: list, add, edit, del, detail")
            await ctx.send("Example: **$watch add meme AMC GME DOGE-USD**")
            await ctx.send("To show a watchlist, simply do **$watch meme**")

        #display full detail
        elif (action == "detail" or action == "d"):
            watchList = WatchList.get(ctx.channel.id, name)
            if watchList is None:
                await ctx.send("Watchlist **{}** does not exist.".format(name))
            else:
                quotes = self.api.getQuotes(watchList.symbols)

                for sym in quotes:
                    await ctx.send(embed=self.createQuoteEmbed(quotes[sym]))
        #short display
        else:
            watchList = WatchList.get(ctx.channel.id, name)
            if watchList is None:
                await ctx.send("Watchlist **{}** does not exist.".format(name))
            else:
                gains = []
                quotes = self.api.getQuotes(watchList.symbols)
                for sym in quotes:
                    gains.append(self.createGainMessage(quotes[sym]))
                await ctx.send("```diff\n{}\n```".format('\n'.join(gains)))

    def createQuoteEmbed(self, quote):
        gain_sym = "+" if quote.gain > 0 else "-"

        embed = discord.Embed(
            title=quote.symbol +" - "+ quote.name,
            description="{}\n{}".format(
                "**Stonking information**" if quote.symbol != "GME" else "**APES HODL TIL PAST THE MOON!!**", 
                textwrap.shorten(quote.description, width=100)
            ),
            color=discord.Color.blurple(),
            url="https://finance.yahoo.com/quote/{}".format(quote.symbol)
        )

        embed.set_thumbnail(url=quote.logo_url)

        width = 2 if (quote.bid > 1) else 6

        embed.add_field(name="Current",  value="```diff\n${0:,.{width}f}\n```".format(quote.bid, width=width),                    inline=False)
        embed.add_field(name="Gain",     value="```diff\n{2}${0:,.{width}f}  {2}{1:,.2f}%\n```".format(abs(quote.gain), abs(quote.gainPercent * 100), gain_sym, width=width), inline=True)
        embed.add_field(name="Previous", value="```diff\n${0:,.{width}f}\n```".format(quote.previousClose, width=width),          inline=True)
        embed.add_field(name="Open",     value="```diff\n${0:,.{width}f}\n```".format(quote.regularMarketOpen, width=width),      inline=True)
        embed.add_field(name="High",     value="```diff\n${0:,.{width}f}\n```".format(quote.dayHigh, width=width),                inline=True)
        embed.add_field(name="Low",      value="```diff\n${0:,.{width}f}\n```".format(quote.dayLow, width=width),                 inline=True)
        if hasattr(quote, 'shortRatio') and quote.shortRatio != None:
            embed.add_field(name="Short Ratio", value="```diff\n{0:,.1f}%\n```".format(quote.shortRatio * 100),      inline=True)

        return embed

    def createGainMessage(self, quote):
        gains = []

        gain_sym = "+" if quote.gain > 0 else "-"
        width = 2 if (quote.bid > 1) else 6
        return "{sym:*^20}\n{gain_sym}${gain:,.{width}f}  {gain_sym}{gain_percent:,.2f}%".format(
            sym = " {} ".format(quote.symbol), gain = abs(quote.gain), gain_percent = abs(quote.gainPercent * 100), gain_sym = gain_sym, width = width
        )
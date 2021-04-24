import os
import discord
from discord.ext import commands
from async_timeout import timeout
from stockapi import StockApi

class Stonk(commands.Cog):

    def __init__(self, client):
        self.name = "Stonk"
        self.client = client
        self.channels = []
        self.api = StockApi()

    @commands.command()
    async def stonk(self, ctx):
        self.channels.append(ctx.channel.id)
        await ctx.send("Now stonking in {}".format(ctx.channel.name))

    @commands.command()
    async def list(self, ctx):
        channelNames = []
        for cId in self.channels:
            channel = await self.client.fetch_channel(cId)
            channelNames.append(channel.name)

        await ctx.send("Currently stonking in: {}".format(", ".join(channelNames)))

    @commands.command(aliases=["ticker"])
    async def quote(self, ctx, *stonkSymbols):
        quotes = self.api.getQuotes(stonkSymbols)

        for quote in quotes:
            await ctx.send(embed=self.createQuoteEmbed(quote))

    def createQuoteEmbed(self, quote):
        gain_sym = "+" if quote.gain > 0 else "-"

        embed = discord.Embed(
            title=quote.ticker,
            description="Stonking information" if quote.ticker != "GME" else "APES HODL TIL PAST THE MOON!!",
            color=discord.Color.blurple(),
            url="https://finance.yahoo.com/quote/{}".format(quote.ticker)
        )

        embed.set_thumbnail(url="https://eodhistoricaldata.com/img/logos/US/{}.png".format(quote.ticker))

        embed.add_field(name="Current",  value="```diff\n${0:,.2f}\n```".format(quote.current),             inline=False)
        embed.add_field(name="Gain",     value="```diff\n{2}${0:,.2f}\n{2}{1:,.2f}%\n```".format(abs(quote.gain), abs(quote.gainPercent), gain_sym), inline=True)
        embed.add_field(name="Previous", value="```diff\n${0:,.2f}\n```".format(quote.previous),            inline=True)
        embed.add_field(name="Open",     value="```diff\n${0:,.2f}\n```".format(quote.open),                inline=True)
        embed.add_field(name="High",     value="```diff\n${0:,.2f}\n```".format(quote.high),                inline=True)
        embed.add_field(name="Low",      value="```diff\n${0:,.2f}\n```".format(quote.low),                 inline=True)

        return embed
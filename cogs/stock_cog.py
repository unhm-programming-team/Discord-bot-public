
from discord.ext import commands
import requests
from our_packages.json_manager import count_command, get_count, easter_egg_animal_lover, get_balance, add_to_balance, get_stocks, add_stock, rem_stock

class StockCog(commands.Cog):
    def __init__(self, client):
        self.client = client

    async def evaluate(self, ctx, stock, period=10, extra_indicators=None):
        indicators = ["SMA", "EMA", "RSI"]
        buy_hold_sell = ""
        message = f"Indicators for {stock}:```"
        if extra_indicators:
            extra_ind = extra_indicators.split(", ")
            for indicator in extra_ind:
                indicators.append(indicator)

        for indicator in indicators:
            ind = ""
            try:
                ind = requests.get(
                    f"https://www.alphavantage.co/query?function={indicator}&symbol={stock}&interval=weekly&time_period={period}&series_type=open&apikey=B7FK59YY2XQ03FES")
                ind = ind.json()[f"Technical Analysis: {indicator}"][
                    list(ind.json()[f"Technical Analysis: {indicator}"].keys())[0]][f"{indicator}"]
                print(f"{stock} {indicator} {ind}")
                if indicator == "RSI":
                    if float(ind) > 70:
                        buy_hold_sell = "Sell"
                    if 70 > float(ind) > 30:
                        buy_hold_sell = "hold"
                    if float(ind) < 30:
                        buy_hold_sell = "sell"
                    message += f"{indicator}: {ind}, based solely off RSI, this indicates a stock you should {buy_hold_sell}\n"
                else:
                    message += f"{indicator}: {ind}\n"
            except KeyError:
                print(ind.json())
                message += f"Unable to grab {indicator} information.\n"
        message += "```"
        return message

    @commands.command(pass_context=True)
    async def technicals(self, ctx, stock, period="10", extra_indicators=None):
        """
        !technicals stock time_period

        returns technical indicator info about a stock
        extra_indicators (optional): list, extra indicators to use besides SMA,EMA, and RSI, see https://www.alphavantage.co/documentation/

        time_period (optional): integer, the time period in days to evaluate indicators over, default 10, must be over 1
        stock: string
        """
        if period.isdigit():
            period = int(period)
            message = await self.evaluate(ctx, stock, period, extra_indicators)
        else:
            extra_indicators = period
            period = 10
            message = await self.evaluate(ctx, stock, period, extra_indicators)

        await ctx.send(message)

    @commands.command(pass_context=True)
    async def evaluateportfolio(self, ctx, period="10", extra_indicators= None):
        """
        !evaluateportfolio period indicators

        period: period to evaluate indicators over, default 10, must be above 1: integer
        indicators: list of indicators to pass
        """
        message = "Here is the evaluation for your portfolio: \n"
        if period.isdigit():
            period = int(period)
            amount_of_stock = await get_stocks(ctx.author)
            for stock in amount_of_stock.keys():
                if amount_of_stock[stock] != 0.0:
                    message += await self.evaluate(ctx, stock, period, extra_indicators)
        else:
            extra_indicators = period
            period = 10
            amount_of_stock = await get_stocks(ctx.author)
            for stock in amount_of_stock.keys():
                if amount_of_stock[stock] != 0.0:
                    message += await self.evaluate(ctx, stock, period, extra_indicators)
        await ctx.send(message)


    @commands.command(pass_context=True)
    async def paperbuy(self, ctx, stock, money):
        """
        !paperbuy <stock> <amt_of_money>
        Used for trading fake money on stocks!
        stock = string, stock to buy
        amt_of_money = integer
        """
        money = float(money)
        if await get_balance(ctx.author) >= money:
            price = requests.get(
                f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval=1min&apikey=B7FK59YY2XQ03FES")
            price = float(
                price.json()["Time Series (1min)"][list(price.json()["Time Series (1min)"].keys())[0]]["4. close"])
            num_of_stocks = money / price
            await ctx.send(
                f"{num_of_stocks} stocks of {stock} purchased for ${money}, at a price of ${price} per share.")

            await add_stock(ctx.author, stock, num_of_stocks)
            await add_to_balance(ctx.author, -1 * money)
        else:
            await ctx.send(f"Your balance is too low! It is currently ${await get_balance(ctx.author)}")

    @commands.command(pass_context=True)
    async def papersell(self, ctx, stock, amt):
        """
        !papersell <stock> <amt_of_stock>

        Sell fake stocks!
        stock = string, stock to sell
        amt_of_stock = integer, amount of stock to sell
        """
        amount_of_stock = await get_stocks(ctx.author)
        amount_of_stock = amount_of_stock[stock]
        if amount_of_stock >= float(amt):
            price = requests.get(
                f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval=1min&apikey=B7FK59YY2XQ03FES")
            price = float(
                price.json()["Time Series (1min)"][list(price.json()["Time Series (1min)"].keys())[0]]["4. close"])
            gain_loss = float(amt) * price
            await ctx.send(
                f"@{ctx.author.name} you sold {amt} shares of {stock}, at a price of ${price} per share, for ${gain_loss}")
            await rem_stock(ctx.author, stock, float(amt))
            await add_to_balance(ctx.author, gain_loss)
        else:
            await ctx.send(
                f"You are not currently holding that much stock! You have {amount_of_stock} stocks in {stock}")

    @commands.command(pass_context=True)
    async def portfolio(self, ctx):
        """
        !portfolio

        Shows you all stocks you currently hold with the paper trading functionality.
        """
        amount_of_stock = await get_stocks(ctx.author)
        message = "You are currently Holding:```"
        for stock in amount_of_stock.keys():
            if amount_of_stock[stock] != 0.0:
                message += f"{amount_of_stock[stock]} shares of {stock}\n"
        message += "```"
        await ctx.send(message)

    @commands.command(pass_context=True)
    async def balance(self, ctx):
        """
        !balance

        Shows current server fake money balance.
        """
        await ctx.send(f"Your balance is currently ${await get_balance(ctx.author)}")

    @commands.command(pass_context=True)
    async def value(self, ctx, stock=None):
        """
        !value stock

        stock (optional): string, if passed returns current price of specific stock

        Shows the value of the stocks you are holding
        """
        if not stock:
            amount_of_stock = await get_stocks(ctx.author)
            message = "You are currently Holding:```"
            for stock in amount_of_stock.keys():
                if amount_of_stock[stock] != 0.0:
                    price = requests.get(
                        f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval=1min&apikey=B7FK59YY2XQ03FES")
                    price = float(
                        price.json()["Time Series (1min)"][list(price.json()["Time Series (1min)"].keys())[0]][
                            "4. close"])
                    message += f"{stock} worth of ${price * amount_of_stock[stock]}\n"
            message += "```"
            await ctx.send(message)
        else:
            price = requests.get(
                f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={stock}&interval=1min&apikey=B7FK59YY2XQ03FES")
            price = float(
                price.json()["Time Series (1min)"][list(price.json()["Time Series (1min)"].keys())[0]]["4. close"])
            await ctx.send(f"The price of {stock} is currently ${price}")

def setup(client):
    client.add_cog(StockCog(client))
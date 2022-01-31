from ctypes import alignment
import discord
import pytz
from discord.commands import Option, slash_command
from discord.ext import commands
from discord.ext.commands.context import Context
from datetime import datetime, timedelta
from tinyman.v1.client import TinymanMainnetClient

guild_id_config = [CHANGEME]

local = pytz.timezone("America/New_York")
check_time = datetime.now() - timedelta(days=1)
utc_dt = check_time.astimezone(pytz.utc)
check_time_start_utc = utc_dt.strftime("%Y-%m-%dT%H:%M:%S") + "+00:00"

client = TinymanMainnetClient()
ALGO = client.fetch_asset(0)
CRSDCOIN = client.fetch_asset(435335235)
pool = client.fetch_pool(CRSDCOIN, ALGO)


class CRSDPrice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=guild_id_config, name="crsdprice", description="Check Tinyman price for CRSD")
    async def crsdprice(self, ctx):
        quote = pool.fetch_fixed_input_swap_quote(CRSDCOIN(1), slippage=0.01)
        coin_value = quote.amount_out.amount/1000000
        await ctx.respond("Tinyman CRSD price:  " + str(coin_value) + " ALGO")

    @crsdprice.error
    async def crsdprice_error(self, ctx: Context, error):
        return await ctx.respond(
            error, ephemeral=True
        )  # ephemeral makes "Only you can see this" message


def setup(bot):
    bot.add_cog(CRSDPrice(bot))
from ctypes import alignment
import discord
import pytz
from discord.commands import Option, slash_command
from discord.ext import commands
from discord.ext.commands.context import Context
from algosdk.v2client import indexer
from datetime import datetime, timedelta

guild_id_config = [CHANGEME]


local = pytz.timezone("America/New_York")
check_time = datetime.now() - timedelta(days=1)
utc_dt = check_time.astimezone(pytz.utc)
check_time_start_utc = utc_dt.strftime("%Y-%m-%dT%H:%M:%S") + "+00:00"

myindexer = indexer.IndexerClient(indexer_token="", indexer_address="https://algoindexer.algoexplorerapi.io", headers={'User-Agent': 'DoYouLoveMe?'})

class CRSDTransactions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(
        guild_ids=guild_id_config, name="crsdtx", description="In/Out transfers in the last 24 hours > 100K CRSD(showing last 9)"
    )
    async def crsdtx(self, ctx):
        """
        ephemeral makes "Only you can see this" message

        `await ctx.respond(f"{round(self.client.latency * 1000)}ms",ephemeral=True)`
        """
        output = check_crsd_tx()
        #return await ctx.respond(f"```\n{output}\n*Time is US Eastern Standard Time\n```")
        return await ctx.respond(embed=output)

    @crsdtx.error
    async def crsdtx_error(self, ctx: Context, error):
        return await ctx.respond(
            error, ephemeral=True
        )  # ephemeral makes "Only you can see this" message


def check_crsd_tx():
    # Get transactions to the designated wallet between the start and end dates
    response = myindexer.search_transactions_by_address(
        address="C3DUWF4E4WHD4NQ52S3QEWB6EOFAEVZ55UBYFJNBJSI2LYFTUSO3IABT34", 
        asset_id=435335235, 
        start_time=check_time_start_utc,  
        min_amount=100000,
        limit=9
        #max_amount=0
    )
    totaltransactions = len(response['transactions'])

    embed = discord.Embed()
    #embed.set_author(name="CRSD Price Bot")
    wallet_str = ""
    crsd_amount_str = ""
    timestamp_str = ""

    for x in range(totaltransactions):
        try: 
            if response['transactions'][x]['asset-transfer-transaction']['receiver'] == 'C3DUWF4E4WHD4NQ52S3QEWB6EOFAEVZ55UBYFJNBJSI2LYFTUSO3IABT34':
                amount_sold = (response['transactions'][x]['asset-transfer-transaction']['amount'])
                amount_sold_format = "{:,}".format(amount_sold)
                crsd_seller_address = response['transactions'][x]['sender']
                tx_sold_time = response['transactions'][x]['round-time']
                tx_sold_time_local = datetime.fromtimestamp(tx_sold_time)
                tx_sold_time_local = tx_sold_time_local.strftime("%y-%m-%d %H:%M:%S")

                wallet_str = wallet_str + "[" + str(crsd_seller_address[0:10]) + "]" + "(https://algoexplorer.io/address/" + str(crsd_seller_address) + ")\n"
                crsd_amount_str = crsd_amount_str + '-' + str(amount_sold_format) + "\n"
                timestamp_str = timestamp_str + str(tx_sold_time_local) + "\n"
        except KeyError:
            pass

        try: 
            if response['transactions'][x]['sender'] == 'C3DUWF4E4WHD4NQ52S3QEWB6EOFAEVZ55UBYFJNBJSI2LYFTUSO3IABT34':
                amount_bought = (response['transactions'][x]['asset-transfer-transaction']['amount'])
                amount_bought_format = "{:,}".format(amount_bought)
                crsd_buyer_address = response['transactions'][x]['asset-transfer-transaction']['receiver']
                tx_bought_time = response['transactions'][x]['round-time']
                tx_bought_time_local = datetime.fromtimestamp(tx_bought_time)
                tx_bought_time_local = tx_bought_time_local.strftime("%y-%m-%d %H:%M:%S")
                
                wallet_str = wallet_str + "[" + str(crsd_buyer_address[0:10]) + "]" + "(https://algoexplorer.io/address/" + str(crsd_buyer_address) + ")\n"
                crsd_amount_str = crsd_amount_str + '+' + str(amount_bought_format) + "\n"
                timestamp_str = timestamp_str + str(tx_bought_time_local) + "\n"
        except KeyError:
            pass
    
    embed.add_field(name="Wallet", value=wallet_str, inline=True)
    embed.add_field(name="CRSD Amount", value=crsd_amount_str, inline=True,)
    embed.add_field(name="TimeStamp", value=timestamp_str, inline=True)

    # print(len(wallet_str))
    # print(len(crsd_amount_str))
    # print(len(timestamp_str))
    #print(output)
    return embed

def setup(bot):
    bot.add_cog(CRSDTransactions(bot))
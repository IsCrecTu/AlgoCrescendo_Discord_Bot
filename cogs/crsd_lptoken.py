import discord
from discord.commands import Option, slash_command
from discord.ext import commands
from discord.ext.commands.context import Context
from algosdk.v2client import indexer

guild_id_config = [CHANGEME]

class CRSDCheckLPToken(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # slash commands with options
    @slash_command(guild_ids=guild_id_config, name="crsdlptoken", description="check CRSD LP token")
    async def register(
        self,
        ctx,
        # <discord.commands.Option>
        lptokens_wanted: Option(int, "Amount of CRSD LP tokens you want", min_value=1, max_value=500, default=1),
    ):
        output = check_lp_token(lptokens_wanted)
        return await ctx.respond(output)

    @register.error
    async def register_error(self, ctx: Context, error):
        return await ctx.respond(
            error, ephemeral=True
        )  # ephemeral makes "Only you can see this" message

def check_lp_token(lptokens_wanted):
    myindexer = indexer.IndexerClient(indexer_token="", indexer_address="https://algoindexer.algoexplorerapi.io", headers={'User-Agent': 'DoYouLoveMe?'})
    response = myindexer.account_info(address="C3DUWF4E4WHD4NQ52S3QEWB6EOFAEVZ55UBYFJNBJSI2LYFTUSO3IABT34")
    totaltransactions = len(response['account']['apps-local-state'][0]['key-value'])

    issued_lp_tokens = 0
    crsd_reserve = 0
    algo_reserve = 0

    for x in range(totaltransactions):
        try: 
            if response['account']['apps-local-state'][0]['key-value'][x]['key'] == 'aWx0':
                issued_lp_tokens = response['account']['apps-local-state'][0]['key-value'][x]['value']['uint']

            if response['account']['apps-local-state'][0]['key-value'][x]['key'] == 'czE=':
                crsd_reserve = response['account']['apps-local-state'][0]['key-value'][x]['value']['uint']
            
            if response['account']['apps-local-state'][0]['key-value'][x]['key'] == 'czI=':
                algo_reserve = response['account']['apps-local-state'][0]['key-value'][x]['value']['uint']
        except KeyError:
            pass
    if issued_lp_tokens > 0:
        asset1_out = (crsd_reserve * (lptokens_wanted / issued_lp_tokens))
        asset2_out = (algo_reserve * (lptokens_wanted / issued_lp_tokens))
        output = f"Need to add {asset1_out*1000000:,.0f} CRSD and {asset2_out:.6f} ALGO to get {lptokens_wanted} CRSD LP Token(s)"
        return output
    return "It broke"

def setup(bot):
    bot.add_cog(CRSDCheckLPToken(bot))

from ctypes import alignment
import discord
from discord.commands import Option, slash_command
from discord.ext import commands
from discord.ext.commands.context import Context

guild_id_config = [CHANGEME]

static_file_locatin = 'CHANGEME'

class CRSDChart1H(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=guild_id_config, name="crsdchart1h", description="Show 1 Hour CRSD Chart on TinyChart (updated every 15 minutes)")
    async def crsdchart1h(self, ctx):
        await ctx.respond(file=discord.File(static_file_location + 'crsd_chart_1H.png'))

    @crsdchart1h.error
    async def crsdchart1h_error(self, ctx: Context, error):
        return await ctx.respond(
            error, ephemeral=True
        )  # ephemeral makes "Only you can see this" message

def setup(bot):
    bot.add_cog(CRSDChart1H(bot))
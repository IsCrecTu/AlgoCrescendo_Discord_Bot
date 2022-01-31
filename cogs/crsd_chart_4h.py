from ctypes import alignment
import discord
from discord.commands import Option, slash_command
from discord.ext import commands
from discord.ext.commands.context import Context

guild_id_config = [CHANGEME]

static_file_locatin = 'CHANGEME'

class CRSDChart4H(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=guild_id_config, name="crsdchart4h", description="Show 4 Hour CRSD Chart on TinyChart (updated every 15 minutes)")
    async def crsdchart4h(self, ctx):
        await ctx.respond(file=discord.File(static_file_location + 'crsd_chart_4H.png'))

    @crsdchart4h.error
    async def crsdchart4h_error(self, ctx: Context, error):
        return await ctx.respond(
            error, ephemeral=True
        )  # ephemeral makes "Only you can see this" message

def setup(bot):
    bot.add_cog(CRSDChart4H(bot))
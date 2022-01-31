from ctypes import alignment
import discord
from discord.commands import Option, slash_command
from discord.ext import commands
from discord.ext.commands.context import Context

guild_id_config = [CHANGEME]

static_file_locatin = 'CHANGEME'

class CRSDChart30M(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=guild_id_config, name="crsdchart30m", description="Show 30 Minute CRSD Chart on TinyChart (updated every 15 minutes)")
    async def crsdchart30m(self, ctx):
        await ctx.respond(file=discord.File(static_file_location + 'crsd_chart_30M.png'))

    @crsdchart30m.error
    async def crsdchart30m_error(self, ctx: Context, error):
        return await ctx.respond(
            error, ephemeral=True
        )  # ephemeral makes "Only you can see this" message

def setup(bot):
    bot.add_cog(CRSDChart30M(bot))
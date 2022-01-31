from ctypes import alignment
import discord
from discord.commands import Option, slash_command
from discord.ext import commands
from discord.ext.commands.context import Context

guild_id_config = [CHANGEME]


static_file_locatin = 'CHANGEME'

class CRSDVoteTally(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=guild_id_config, name="crsdvotetally", description="Show latest vote tally")
    async def crsdvotetally(self, ctx):
        await ctx.respond(file=discord.File(static_file_location + 'crescendo_vote.txt'))

    @crsdvotetally.error
    async def crsdvotetally_error(self, ctx: Context, error):
        return await ctx.respond(
            error, ephemeral=True
        )  # ephemeral makes "Only you can see this" message

def setup(bot):
    bot.add_cog(CRSDVoteTally(bot))
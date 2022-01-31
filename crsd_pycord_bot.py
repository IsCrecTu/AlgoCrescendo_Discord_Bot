import os
import discord
from discord.ext import commands
from discord.ui.view import View

# inherits commands.Bot
class BotClass(discord.Bot):
    def __init__(self):
        super().__init__()
        self.persistent_views_added = False

    # For making the intreaction Button works even after restart.
    async def on_ready(self):
        if not self.persistent_views_added:

            # You can add <discord.ui.View> classes to the <commands.Bot.add_view> to make it work after restart
            # self.add_view(<discord.ui.View>)

            print(f"Connected as {self.user} with ID {self.user.id}")
            print("------")
            self.persistent_views_added = True

bot = BotClass()

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")

bot.run("DISCORD BOT TOKEN GOES HERE")
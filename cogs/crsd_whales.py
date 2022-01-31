import discord
import sqlite3
from discord.commands import Option, slash_command
from discord.ext import commands
from discord.ext.commands.context import Context
from table2ascii import table2ascii, Alignment, PresetStyle

guild_id_config = [CHANGEME]


class CRSDWhales(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(guild_ids=guild_id_config, name="crsdwhales", description="Top 15 CRSD Holders under 20M CRSD(updated every 15 minutes)")
    async def crsdwhales(self, ctx):
        """
        ephemeral makes "Only you can see this" message

        `await ctx.respond(f"{round(self.client.latency * 1000)}ms",ephemeral=True)`
        """
        output = readCRSDTop10holders()
        return await ctx.respond(f"```\nTop 15 CRSD Holders under 20M CRSD(updated every 15 minutes)\n{output}\n```")
        #return await ctx.respond(embed=output)

    @crsdwhales.error
    async def crsdwhales_error(self, ctx: Context, error):
        return await ctx.respond(
            error, ephemeral=True
        )  # ephemeral makes "Only you can see this" message


def readCRSDTop10holders():
    static_file_locatin = 'CHANGEME'
    header=["Rank", "Wallet", "CRSD Amount"]
    body_list =[]
    top10="Top 15 CRSD Holders under 20M CRSD(updated every 15 minutes)"
    try:
        sqliteConnection = sqlite3.connect(static_file_location + 'crsd_holders.db')
        cursor = sqliteConnection.cursor()
        #print("Connected to SQLite")

        sqlite_select_query = """SELECT * FROM holders WHERE crsd_balance < 20000000 ORDER BY crsd_balance DESC LIMIT 15"""
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        i = 1
        for row in records:
            wallet_txt_address = row[0]
            wallet_txt_balance = "{:,}".format(row[1])
            top10 = top10 + '\n' + str(i) + ". " + wallet_txt_address[0:8] + " Balance: " + str(wallet_txt_balance) + " CRSD" 
            body_list.append([str(i), str(wallet_txt_address[0:8]), str(wallet_txt_balance)])
            #print(str(i) + ". " + wallet_txt_address[0:10] + " Balance: " + str(wallet_txt_balance) + " CRSD" )
            i = i + 1

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to read data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            #print("The SQLite connection is closed")
    
    output = table2ascii(
        header=header,
        body=body_list,
        #column_widths=[12,11,11,21],
        style=PresetStyle.thin_compact
    )
    #return top10
    return output

def setup(bot):
    bot.add_cog(CRSDWhales(bot))
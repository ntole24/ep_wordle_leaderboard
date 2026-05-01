import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import numpy as np
import tabulate
import wordle_player

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Specify and enable the needed intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Responding to events
wordle_author_id = "Wordle#2092"
wordle_channel_id = "insert integer here"

# add a dictionary of JM wordle players here!!!

""" players = {
    "Player_ID": ["<@487622829748125696>", "<@1499297517492502609>", "<@&1457353878009020509>"],
    "Player_Name": ["P1", "P2", "P3"],
    "Player_Total": [1, 2, 3]
} """

players = [wordle_player.wordle_player("<@487622829748125696>", "P1"), wordle_player.wordle_player("<@1499297517492502609>", "P2"), wordle_player.wordle_player("<@&1457353878009020509>", "P3")]

for player in players:
    print(player.get_id())
    print(player.get_name())
    print(player.get_total())

# IDEA: adding a new player

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")

@bot.event
async def on_message(message):
    author_id = message.author.id
    channel_id = message.channel.id
    content = message.content

    if message.author == bot.user:
        return

    if author_id == 487622829748125696 and channel_id == 1499450918477762621 and "streak" in content.lower():
        lines = content.splitlines() # splits the diff newlines
        
        for i in range(len(lines)):
            if i == 1:
                guess_number_index = 1
            elif i > 1:
                guess_number_index = 0
            else:
                guess_number_index = -1

            # Get guess number
            if guess_number_index >= 0:
                spaced_line = lines[i].split()
                guess_number = spaced_line[guess_number_index][0]

                print(guess_number)
                for j in range(guess_number_index + 1, len(spaced_line)):
                    # Locate each person, then add it to their total
                    for player in players:
                        if player.get_id() == spaced_line[j]:
                            player.add_total(int(guess_number))

                  
                    # print(spaced_line[j])

    for player in players:
        print(player.get_id())
        print(player.get_name())
        print(player.get_total())

                    
                

    await bot.process_commands(message)

@bot.command()
async def leaderboard(ctx):
    await ctx.reply(tabulate.tabulate(players_arr, headers='keys', tablefmt='grid', showindex=False))

bot.run(token, log_handler=handler, log_level=logging.DEBUG) # any of the debug stuff is gonna be logged into discord.log file
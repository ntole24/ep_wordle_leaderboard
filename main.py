import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

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

    if author_id == 487622829748125696 and channel_id == 1499450918477762621:
        print(content)

    await bot.process_commands(message)

bot.run(token, log_handler=handler, log_level=logging.DEBUG) # any of the debug stuff is gonna be logged into discord.log file
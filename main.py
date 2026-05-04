import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import numpy as np
import tabulate
import datetime as dt
import db
import chat_format

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

# Specify and enable the needed intents
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Responding to events

# add a dictionary of JM wordle players here!!!

leaderboard_db = db.db()
leaderboard_db.tables_init()
leaderboard_db.sample_players()
leaderboard_db.sample_scores()

# IDEA: adding a new player

@bot.event
async def on_ready():
    print(f"We are ready to go in, {bot.user.name}")

@bot.event
async def on_message(message):
    author_id = message.author.id
    content = message.content

    print(author_id)

    now = dt.datetime.now()
    yesterday_date = now.date() - dt.timedelta(days=1)

    if message.author == bot.user:
        return

    if author_id == 1211781489931452447:
        if "streak" in content.lower():
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
                        # spaced line [j] gives you the id of the person in the current guess number
                        # extract the id from the spaced line
                        id_buffer = spaced_line[j][2:-1]

                        leaderboard_db.create_score(id_buffer, guess_number, yesterday_date)
                        print(spaced_line[j])

            await message.channel.send("Added scores to the leaderboards!")

    await bot.process_commands(message)


@bot.event
async def on_reaction_add(reaction, user):
    message = reaction.message
    channel = reaction.message.channel

    if user.bot:
        return
    
    if str(reaction.emoji) == "🤓": # editing leaderboard
        channel = reaction.message.channel
        await channel.send(f"{user.name} reacted!")

        results = leaderboard_db.read_player_stats_averageOrder()

        new_embed = chat_format.format_leaderboard(results, "Average")

        await reaction.message.edit(embed = new_embed)
    elif str(reaction.emoji) == "🦧": # editing leaderboard
        channel = reaction.message.channel
        await channel.send(f"{user.name} reacted!")

        results = leaderboard_db.read_player_stats_totalOrder()

        new_embed = chat_format.format_leaderboard(results, "Total")

        await reaction.message.edit(embed = new_embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("That command doesn't exist!")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to do that!")
    elif isinstance(error, commands.CommandInvokeError):
        # This wraps runtime errors that happen inside a command
        original = error.original
        await ctx.send(f"An error occurred: {original}")
        print(f"Error in command: {original}")  # log it too
    else:
        await ctx.send("An unexpected error occurred.")
        raise error  # re-raise so it still shows in console
        
@bot.command()
async def createPlayer(ctx):
    # Input name as parameter
    buffer = ctx.message.content.split()
    
    if len(buffer) != 2:
        await ctx.channel.send("Format: !createPlayer <insert-name>")

        return
    
    name = buffer[1]
    leaderboard_db.create_player(str(ctx.message.author.id), name)
    await ctx.channel.send("Player has been created.")

@bot.command()
async def leaderboard(ctx):
    results = leaderboard_db.read_player_stats_totalOrder()

    embed = chat_format.format_leaderboard(results, "Total")

    leaderboard_message = await ctx.send(embed=embed)

    await leaderboard_message.add_reaction("🦧")
    await leaderboard_message.add_reaction("🤓")

bot.run(token, log_handler=handler, log_level=logging.DEBUG) # any of the debug stuff is gonna be logged into discord.log file
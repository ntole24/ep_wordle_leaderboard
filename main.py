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
intents.members = True

client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='!', intents=intents)

leaderboard_db = db.db()

class LeaderboardView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(emoji="🤓", style=discord.ButtonStyle.grey)
    async def average_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        results = leaderboard_db.read_player_stats("Average_Guesses")
        new_embed = chat_format.format_leaderboard(results, "Average_Guesses")
        await interaction.response.edit_message(embed=new_embed, view=self)

    @discord.ui.button(emoji="🦧", style=discord.ButtonStyle.grey)
    async def total_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        results = leaderboard_db.read_player_stats("Total_Guesses")
        new_embed = chat_format.format_leaderboard(results, "Total_Guesses")
        await interaction.response.edit_message(embed=new_embed, view=self)

    @discord.ui.button(emoji="💪", style=discord.ButtonStyle.grey)
    async def total_games_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        results = leaderboard_db.read_player_stats("Total_Games")
        new_embed = chat_format.format_leaderboard(results, "Total_Games")
        await interaction.response.edit_message(embed=new_embed, view=self)

@bot.event
async def on_ready():
    # Initialize the tables
    # leaderboard_db.tables_init()

    """ leaderboard_db.sample_players()
    leaderboard_db.sample_scores() """

    """ registered_players = leaderboard_db.read_all_players()
    print(registered_players) """


        
    print(f"We are ready to go in, {bot.user.name}")

# deactivated muna
@bot.event
async def on_message(message):
    author_id = message.author.id
    content = message.content

    now = dt.datetime.now()
    formatted_date = (now - dt.timedelta(days=1)).strftime("%Y-%m-%d")

    if message.author == bot.user:
        return

    if author_id == 487622829748125696: # 1211781489931452447 <- wordle bot's ID
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

                        # create score needs to check if 
                                                # check if this player is even in the leaderboard. If not, add them
                        if (leaderboard_db.read_player_from_id(id_buffer) == -1):
                            # how do I get their name in the discord server?
                            print(id_buffer)
                            leaderboard_db.create_player(id_buffer, server_name_from_discord_id(int(id_buffer)))

                        create_score(id_buffer, guess_number, formatted_date)


            await message.channel.send("Added scores to the leaderboards!")

    await bot.process_commands(message)

@bot.event
async def on_command_error(ctx, error):
    command_content = ctx.message.content

    buffer = command_content.split()

    if isinstance(error, commands.CommandNotFound):
        await ctx.send("That command doesn't exist!")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You don't have permission to do that!")
    elif isinstance(error, commands.CommandInvokeError):
        # This wraps runtime errors that happen inside a command
        original = error.original
        
        if "Duplicate entry" in command_content:

            if buffer[0] == "!createPlayer":
                await ctx.send(f"This user already exists.")
            elif buffer[0] == "!refresh" or "!get_all":
                await ctx.send(f"This score has already been recorded.")
                return
            else:
                await ctx.send(f"An error occurred: {original}")
                print(f"Error in command: {original}")  # log it too

        else:
            await ctx.send(f"An error occurred: {original}")
            print(f"Error in command: {original}")  # log it too
    else:
        await ctx.send("An unexpected error occurred.")
        raise error  # re-raise so it still shows in console

@bot.command()
async def initialize_database(ctx):
    leaderboard_db.database_init()
    await ctx.channel.send("Database has been initialized")
        
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
async def refresh_all(ctx): #kind of like a refresh command
    channel_id = 800376086647144509 # channel of dark

    channel = bot.get_channel(channel_id)
    earliest_wordle_date = "2025-11-27"
    date_format = "%Y-%m-%d"

    # Get the most recent messages
    async for message in channel.history(limit=None):
        sent_at = message.created_at
        formatted_date = (sent_at - dt.timedelta(days=1)).strftime("%Y-%m-%d")
        
        if (dt.datetime.strptime(formatted_date, date_format) < dt.datetime.strptime(earliest_wordle_date, date_format)):
            break

        if message.author.id == 1211781489931452447 and "streak" in message.content.lower():

            lines = message.content.splitlines() # splits the diff newlines
            
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
                    print(spaced_line)
                    print(guess_number)

                    for j in range(guess_number_index + 1, len(spaced_line)):
                        # Locate each person, then add it to their total
                        # spaced line [j] gives you the id of the person in the current guess number
                        # extract the id from the spaced line
                        id_buffer = spaced_line[j][2:-1]
                        print(id_buffer)

                        if (is_integer(id_buffer)):
                            # check if this player is even in the leaderboard. If not, add them
                            server_name = server_name_from_discord_id(int(id_buffer))
                            if server_name != 0:
                                if (leaderboard_db.read_player_from_id(id_buffer) == -1):
                                    # how do I get their name in the discord server?
                                    leaderboard_db.create_player(id_buffer, server_name_from_discord_id(int(id_buffer)))

                                create_score(id_buffer, guess_number, formatted_date)
                                print(spaced_line[j])
                                    

            await ctx.channel.send(("Recorded wordle scores from:", formatted_date))

@bot.command()
async def refresh_last_5(ctx): #kind of like a refresh command
    counter = 0
    channel_id = 800376086647144509
    channel = bot.get_channel(channel_id)

    # Get the most recent messages
    async for message in channel.history(limit=500):
        if message.author.id == 1211781489931452447 and "streak" in message.content.lower():
            sent_at = message.created_at
            formatted_date = (sent_at - dt.timedelta(days=1)).strftime("%Y-%m-%d")

            lines = message.content.splitlines() # splits the diff newlines
            
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
                    print(spaced_line)
                    print(guess_number)

                    for j in range(guess_number_index + 1, len(spaced_line)):
                        # Locate each person, then add it to their total
                        # spaced line [j] gives you the id of the person in the current guess number
                        # extract the id from the spaced line
                        id_buffer = spaced_line[j][2:-1]
                        print(id_buffer)

                        if (is_integer(id_buffer)):
                            # check if this player is even in the leaderboard. If not, add them
                            server_name = server_name_from_discord_id(int(id_buffer))
                            if server_name != 0:
                                if (leaderboard_db.read_player_from_id(id_buffer) == -1):
                                    # how do I get their name in the discord server?
                                    leaderboard_db.create_player(id_buffer, server_name_from_discord_id(int(id_buffer)))

                                create_score(id_buffer, guess_number, formatted_date)
                                print(spaced_line[j])
                                    

            counter = counter + 1

            if (counter == 5):
                break

    await ctx.channel.send("Previous 5 wordle scores have been recorded.")

@bot.command()
async def leaderboard(ctx):
    results = leaderboard_db.read_player_stats("Average_Guesses")

    embed = chat_format.format_leaderboard(results, "Average_Guesses")

    view = LeaderboardView()

    await ctx.send(embed=embed, view=view)

def server_name_from_discord_id(discord_id):
    print(discord_id)
    print(type(discord_id))
    for guild in bot.guilds:
        for member in guild.members:
            print(member.id)
            print(type(member.id))
            if (member.id == discord_id):
                return member.name

        break

    return 0

def create_score(discord_id, guess_number, date):
    print("Checking duplicate...")
    isDuplicate = check_duplicate_score(discord_id, date)

    print("Is it?")
    if (isDuplicate is not True):
        print("Not Duplicate!")
        if (guess_number == 'X'):
            guess_number = 8

        leaderboard_db.create_score(discord_id, guess_number, date)
    else:
        print("Is Duplicate!")

def check_duplicate_score(discord_id, date):
    buffer = leaderboard_db.get_score_from_id_and_date(discord_id, date)

    if buffer == -1:
        return False

    return True

def is_integer(val_str):
    try:
        int(val_str)
        return True
    except ValueError:
        return False

bot.run(token, log_handler=handler, log_level=logging.DEBUG) # any of the debug stuff is gonna be logged into discord.log file
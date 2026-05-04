import discord

def format_leaderboard(results, type):
    embed = discord.Embed(title="🏆 | Leaderboard", color=0xFFD700)

    ranks = ""
    names = ""
    scores = ""
    scores_text = type + " Guesses"

    for rank, row in enumerate(results, start=1):
        ranks += f"{rank}\n"
        names += f"{row['Name']}\n"

        if type == "Total":
            scores += f"{int(row['Total_Guesses'])}\n"
        elif type == "Average":
            scores += f"{float(row['Average_Guesses'])}\n"

    embed.add_field(name="Rank", value=ranks, inline=True)
    embed.add_field(name="Name", value=names, inline=True)
    embed.add_field(name=scores_text, value=scores, inline=True)

    embed.set_footer(text="Click 🦧 to order by total or 🤓 to order by average.")

    return embed
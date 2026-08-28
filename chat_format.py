import discord

def format_leaderboard(results, leaderboard_type):
    embed = discord.Embed(title="🏆 | Leaderboard", color=0xFFD700)

    ranks = ""
    names = ""
    scores = ""
    scores_text = leaderboard_type.replace("_", " ")

    for rank, row in enumerate(results, start=1):
        ranks += f"{rank}\n"
        names += f"{row['Name']}\n"

        if (scores_text != "Average Guesses"):
            scores += f"{int(row[leaderboard_type])}\n"
        else:
            scores += f"{float(row[leaderboard_type])}\n"


    embed.add_field(name="Rank", value=ranks, inline=True)
    embed.add_field(name="Name", value=names, inline=True)
    embed.add_field(name=scores_text, value=scores, inline=True)

    embed.set_footer(text="Click 🤓 to show average guesses, 🦧 to show total guesses, or 💪 to show total games.")

    return embed
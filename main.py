import discord
from discord.ext import commands
import random
import json
import datetime
from pathlib import Path

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="$", intents=intents)

tips = ["🌱 Try to touch some grass and breathe in the real world!"]
motivation = ["💪 Just think... someone out there hasn’t even started yet. You’re already ahead!"]

data_path = Path("E:\Aaaa VS CODE\Application_Projects\Discord_Bot\data\streaks.json")
#Loading data
def load_data():
    try:
        with open(data_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}
#Saving data
def save_data(data):
    with open(data_path, "w") as f:
        json.dump(data, f)

#Updating the streak
def update_streak(user_id):
    data = load_data()
    today = str(datetime.date.today())

    user_id = str(user_id)
    if user_id not in data:
        data[user_id] = {"last_claimed": today, "streak": 1}
    else:
        last_date = datetime.datetime.strptime(data[user_id]["last_claimed"], "%Y-%m-%d").date()
        if last_date == datetime.date.today():
            return data[user_id]["streak"], False  # already claimed today
        elif last_date == datetime.date.today() - datetime.timedelta(days=1):
            data[user_id]["streak"] += 1
        else:
            data[user_id]["streak"] = 1
        data[user_id]["last_claimed"] = today

    save_data(data)
    return data[user_id]["streak"], True

def get_streak(user_id):
    data = load_data()
    return data.get(str(user_id), {}).get("streak", 0)

#Tip command
@bot.command()
async def tip(ctx):
    await ctx.send(f"🧠 **Tip of the day:**\n> {random.choice(tips)}")

#Motivate command
@bot.command()
async def motivate(ctx):
    await ctx.send(f"🔥 **Motivation Boost:**\n> {random.choice(motivation)}")

#Daily command
@bot.command()
async def daily(ctx):
    streak, claimed = update_streak(ctx.author.id)
    if claimed:
        await ctx.send(f"✅ **Daily claimed!**\nYou've kept the fire alive 🔥\n**Current Streak:** `{streak}` days!")
    else:
        await ctx.send("⏳ You've already claimed your daily today!\nCome back tomorrow for more rewards. 🌟")

#Streak command
@bot.command()
async def streak(ctx):
    current_streak = get_streak(ctx.author.id)
    await ctx.send(f"📅 **Your Streak:** `{current_streak}` day(s) in a row!\nKeep it going champ! 🏆")
#Commands command lol
@bot.command()
async def commands(ctx):
    await ctx.send("""📜 **Here’s what I can do:**  
`$tip` – Get a useful tip 👀  
`$motivate` – Feel the hype 💥  
`$daily` – Claim your daily reward 🌞  
`$streak` – Check your streak 🔥  
`$commands` – See all commands 🧾
""")

#Running the bot
bot.run("Your token goes here")
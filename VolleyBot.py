import os
import discord
import requests
import asyncio
from discord.ext import tasks, commands

TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
API_URL = os.getenv("API_URL")

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

async def fetch_matches():
    try:
        res = requests.get(API_URL)
        data = res.json()
        matches = []
        for event in data.get("events", []):
            match = f"📅 {event['dateEvent']} - {event['strTime']} | 🏐 {event['strEvent']}"
            matches.append(match)
        return "\n".join(matches) if matches else "Aucun match trouvé."
    except Exception as e:
        return f"Erreur API: {e}"

@tasks.loop(minutes=60)
async def update_matches():
    channel = bot.get_channel(CHANNEL_ID)
    if channel:
        upcoming = await fetch_matches()
        await channel.send(f"📣 **Matchs de volley à venir :**\n{upcoming}")

@bot.event
async def on_ready():
    update_matches.start()
    print(f"Bot connecté : {bot.user}")

bot.run(TOKEN)

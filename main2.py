import bot2
import discord
import os

intents = discord.Intents.all()
eva_bot = bot2.EvaDiscordBot(command_prefix='!', intents=intents)
eva_bot.run(os.getenv("TOKEN"))


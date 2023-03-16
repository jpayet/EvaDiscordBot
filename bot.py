import EvaDiscordBot
import discord
import os


intents = discord.Intents.all()
eva_bot = EvaDiscordBot.EvaDiscordBot(command_prefix='!', intents=intents)
eva_bot.run(os.getenv("TOKEN"))


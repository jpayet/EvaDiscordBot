import os
import discord
import responses
from discord import app_commands
from discord.ext import commands

from dotenv import load_dotenv
load_dotenv()


def run_discord_bot():
    #définition des droits du bot
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        print(f'{bot.user} est en marche !')
        try:
            synced = await bot.tree.sync()
        except Exception as e:
            print(e)

    @bot.tree.command(name="say")
    @app_commands.describe(thing_to_say="What should I say ? ")
    async def say(interaction: discord.Interaction, thing_to_say: str):
        await interaction.response.send_message(f"{interaction.user.name}! said : '`{thing_to_say}`")

    @bot.event
    async def on_message(message):
        response = responses.handle_response(message.content.lower())

        if message.author == bot.user:
            return

        if response is not None:
            await message.channel.send(response)

        await bot.process_commands(message)

    @bot.event
    async def on_member_join(member):
        bienvenue_channel: discord.TextChannel = bot.get_channel(1085268089257607278)
        await bienvenue_channel.send(content=f"Ravi de te voir parmi nous {member.display_name}")
        role = discord.utils.get(member.guild.roles, name='New')
        await member.add_roles(role)

    @bot.event
    async def on_member_remove(member):
        print(f'bye {member}')
        pass

    @bot.event
    async def on_raw_reaction_add(payload):
        message_id = payload.message_id

        if message_id == 1085189648025927730:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

            if payload.emoji.name == '🎮':
                role = discord.utils.get(guild.roles, name='Gaming')
            elif payload.emoji.name == '🦆':
                role = discord.utils.get(guild.roles, name='🦆Canard')
            else:
                role = None

            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.add_roles(role)

        elif message_id == 1085678888451063849:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

            if payload.emoji.name == '✅':
                role = discord.utils.get(guild.roles, name='Membre')
                role_del = discord.utils.get(guild.roles, name='New')
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.add_roles(role)
                    await member.remove_roles(role_del)

    @bot.event
    async def on_raw_reaction_remove(payload):
        message_id = payload.message_id
        if message_id == 1085189648025927730:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

            if payload.emoji.name == '🎮':
                role = discord.utils.get(guild.roles, name='Gaming')
            elif payload.emoji.name == '🦆':
                role = discord.utils.get(guild.roles, name='🦆Canard')
            else:
                role = None

            if role is not None:
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.remove_roles(role)

        elif message_id == 1085678888451063849:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, bot.guilds)

            if payload.emoji.name == '✅':
                role = discord.utils.get(guild.roles, name='New')
                role_del = discord.utils.get(guild.roles, name='Membre')
                member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
                if member is not None:
                    await member.add_roles(role)
                    await member.remove_roles(role_del)

    @bot.command(name='del')
    async def delete(ctx, nb_of_message):
        try:
            nb = int(nb_of_message)
            messages = ctx.channel.history(limit=nb + 1)
            async for each_message in messages:
                await each_message.delete()
        except ValueError:
            return None

    bot.run(os.getenv("TOKEN"))

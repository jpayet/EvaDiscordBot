import os
import discord
import responses

from dotenv import load_dotenv
load_dotenv()


def run_discord_bot():
    intents = discord.Intents.all()
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f'{client.user} est en marche !')

    @client.event
    async def on_message(message):
        response = responses.handle_response(message.content.lower())

        if message.author == client.user:
            return

        if response is not None:
            await message.channel.send(response)

    @client.event
    async def on_member_join(member):
        bienvenue_channel: discord.TextChannel = client.get_channel(1085268089257607278)
        await bienvenue_channel.send(content=f"Ravi de te voir parmi nous {member.display_name}")
        role = discord.utils.get(member.guild.roles, name='Recrue')
        await member.add_roles(role)

    @client.event
    async def on_raw_reaction_add(payload):
        message_id = payload.message_id
        if message_id == 1085189648025927730:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

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

    @client.event
    async def on_raw_reaction_remove(payload):
        message_id = payload.message_id
        if message_id == 1085189648025927730:
            guild_id = payload.guild_id
            guild = discord.utils.find(lambda g: g.id == guild_id, client.guilds)

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

    client.run(os.getenv("TOKEN"))

from discord.ext import commands
import discord
from discord import app_commands


class MainCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.command()
    async def delete(self, ctx, nb_of_message):
        try:
            nb = int(nb_of_message)
            messages = ctx.channel.history(limit=nb + 1)
            async for each_message in messages:
                await each_message.delete()
        except ValueError:
            return None

    @app_commands.command(name="introduce", description="introduce yourself")
    async def introduce(self, interaction: discord.Interaction, name: str, age: int):
        await interaction.response.send_message(f"My name is: {name} and I'm {age}")


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(MainCog(bot))



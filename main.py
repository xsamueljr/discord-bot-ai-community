import os

from dotenv import load_dotenv
import discord

from components import Category, ApportationView
from constants import SERVER_ID, MAILBOX_CHANNEL

load_dotenv()

bot = discord.Bot()


@bot.event
async def on_ready():
    print("Ready!")


@bot.event
async def on_guild_join(guild: discord.Guild):
    if guild.id != SERVER_ID:
        # Exit the server
        await guild.leave()


@bot.slash_command()
async def hello(ctx, name: str = None):
    name = name or ctx.author.name
    await ctx.respond(f"Hello {name}!", view=ApportationView())


@bot.slash_command(name="aportar")
async def send_apportation(ctx, category: Category, link: str):
    message = discord.Embed(
        title="¡Nueva aportación!"
    )

    message.add_field(name="Autor", value=ctx.author.name)
    message.add_field(name="Categoría", value=category.name)
    message.add_field(name="Link", value=link)

    await discord.channel.Channel(id=MAILBOX_CHANNEL).send(embed=message)


bot.run(os.getenv("BOT_TOKEN"))
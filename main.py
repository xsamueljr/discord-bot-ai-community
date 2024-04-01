import os
import json

from dotenv import load_dotenv
from discord import (
    Bot,
    Guild,
    TextChannel,
    Embed,
    Option
)

from validation import is_valid_url
from components import ApportationView

# Load config
# .env
load_dotenv()

# .json
with open("config/bot.json", "r") as f:
    config: dict = json.load(f)
SERVER_ID = config["SERVER_ID"]
MAILBOX_ID = config["MAILBOX_ID"]
CATEGORY_CHOICES = list(config["categories"].keys())

# Dict to save categories with name and discord.TextChannel
categories: dict[str, TextChannel] = {}
bot: Bot = Bot()


@bot.event
async def on_ready() -> None:
    global mailbox_channel
    mailbox_channel = bot.get_channel(MAILBOX_ID)

    # Load categories from JSON file
    for name, id in config["categories"].items():
        categories[name] = bot.get_channel(id)

    global contributor_role
    contributor_role = bot.get_guild(SERVER_ID).get_role(1222214686695624814)
    global apportation_view
    apportation_view = ApportationView(categories, contributor_role)
    
    print("Ready!")


@bot.event
async def on_guild_join(guild: Guild) -> None:
    """Leave the guild if it's not the server."""
    if guild.id != SERVER_ID:
        await guild.leave()


@bot.slash_command(name="aportar")
async def send_apportation(
    ctx,
    category: Option(description="Categoría para la que va tu aporte", choices=CATEGORY_CHOICES),
    link: Option(description="Pega el enlace del contenido"),
    description: Option(description="Descríbelo", min_length=10, max_length=340)
) -> None:
    """Usa el comando para contribuir a los recursos de la comunidad."""
    if not is_valid_url(link):
        await ctx.send_response("El link no es válido.", ephemeral=True)
        return

    message = Embed(title="¡Nueva aportación!")

    fields = [
        ("Autor", ctx.author.mention),
        ("Categoría", category),
        ("Link", link),
        ("Descripción", description)
    ]
    for name, value in fields:
        message.add_field(name=name, value=value, inline=False)

    await mailbox_channel.send(embed=message, view=apportation_view)
    await ctx.send_response("Aportación enviada con éxito.", ephemeral=True)


bot.run(os.getenv("BOT_TOKEN"))
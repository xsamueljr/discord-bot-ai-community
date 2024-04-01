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
import discord.utils
import discord.ui

from validation import is_valid_url

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


class ApportationView(discord.ui.View):
    @discord.ui.button(label="Aprobar", style=discord.ButtonStyle.green)
    async def approve(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = interaction.message.embeds[0]
        
        # Getting user
        user_id = int(embed.fields[0].value.strip("<@>"))
        author = interaction.guild.get_member(user_id)
        assert author is not None, f"{user_id}, {author}"
        category = embed.fields[1].value
        
        channel = categories[category]

        embed.remove_field(1)
        
        await interaction.message.delete()
        await channel.send(embed=embed)
        await author.add_roles(contributor_role, reason="Aportación aprobada")


    @discord.ui.button(label="Rechazar", style=discord.ButtonStyle.red)
    async def reject(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = interaction.message.embeds[0]
        author = discord.utils.get(interaction.guild.members, mention=embed.fields[0].value)
        assert author is not None, f"{embed.fields[0].value}"

        embed.remove_field(0)
        embed.title = None
        msg = (
            "¡Hola!",
            "Lamentablemente, tu aportación fue rechazada. Contacta con algún administrador si crees que fue un error, o quieres saber el motivo.",
            "Éste mensaje se borrará en 2 minutos. Sácale captura si quieres."
            "Te adjunto la aportación para que puedas revisarla. ¡Un saludo!"
        )
        
        await author.send("\n\n".join(msg), embed=embed, delete_after=120)
        await interaction.message.delete()


@bot.event
async def on_ready() -> None:
    global mailbox_channel
    mailbox_channel = bot.get_channel(MAILBOX_ID)

    # Load categories from JSON file
    for name, id in config["categories"].items():
        categories[name] = bot.get_channel(id)

    global contributor_role
    contributor_role = bot.get_guild(SERVER_ID).get_role(1222214686695624814)
    
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

    await mailbox_channel.send(embed=message, view=ApportationView())
    await ctx.send_response("Aportación enviada con éxito.", ephemeral=True)


bot.run(os.getenv("BOT_TOKEN"))
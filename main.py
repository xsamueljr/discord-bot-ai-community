import os
import json

from dotenv import load_dotenv
from discord import (
    User,
    Member,
    Bot,
    Intents,
    Guild,
    Message,
    Embed
)
import discord.utils

from components import Category
from components import SERVER_ID, MAILBOX_ID
from validation import is_valid_url

load_dotenv()

bot: Bot = Bot()

rejection_messages: list[Message] = []

class ApportationView(discord.ui.View):
    @discord.ui.button(label="Aprobar", style=discord.ButtonStyle.green)
    async def approve(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = interaction.message.embeds[0]
        author = discord.utils.get(interaction.guild.members, mention=embed.fields[0].value)
        assert author is not None, f"{embed.fields[0].value}"
        category = embed.fields[1].value
        channel = category1_channel if category == Category.category1.value else category2_channel

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
            "Éste mensaje se borrará en 20 segundos. Sácale captura si quieres."
            "Te adjunto la aportación para que puedas revisarla. ¡Un saludo!"
        )
        
        message = await author.send("\n\n".join(msg), embed=embed, delete_after=20)
        rejection_messages.append(message)
        await interaction.message.delete()


@bot.event
async def on_ready() -> None:
    global mailbox_channel, category1_channel, category2_channel
    mailbox_channel = bot.get_channel(MAILBOX_ID)
    category1_channel = bot.get_channel(Category.category1.get_channel_id())
    category2_channel = bot.get_channel(Category.category2.get_channel_id())

    global contributor_role
    contributor_role = bot.get_guild(SERVER_ID).get_role(1222214686695624814)
    
    print("Ready!")


@bot.event
async def on_guild_join(guild: Guild) -> None:
    if guild.id != SERVER_ID:
        await guild.leave()


@bot.slash_command()
async def hello(ctx, name: str = None) -> None:
    name = name or ctx.author.name
    await ctx.respond(f"Hello {name}!", view=ApportationView())


@bot.slash_command(name="aportar")
async def send_apportation(ctx, category: Category, link: str, description: str) -> None:
    """Usa el comando para contribuir a los recursos de la comunidad."""

    description = description.strip()
    if len(description) not in range(10, 341):
        await ctx.send_response("La descripción debe tener entre 10 y 340 caracteres.", ephemeral=True)
        return

    link = link.strip()
    if not is_valid_url(link):
        await ctx.send_response("El link no es válido.", ephemeral=True)
        return

    message = Embed(title="¡Nueva aportación!")

    fields = [
        ("Autor", ctx.author.mention),
        ("Categoría", category.name),
        ("Link", link),
        ("Descripción", description)
    ]
    for name, value in fields:
        message.add_field(name=name, value=value, inline=False)

    await mailbox_channel.send(embed=message, view=ApportationView())
    await ctx.send_response("Aportación enviada con éxito.", ephemeral=True)


bot.run(os.getenv("BOT_TOKEN"))
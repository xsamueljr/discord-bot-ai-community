from enum import Enum

import discord


class Category(Enum):
    basics = "basics"
    medium = "medium"
    advanced = "advanced"
    offtopic = "offtopic"


class ApportationView(discord.ui.View):
    @discord.ui.button(label="Aprobar", style=discord.ButtonStyle.green)
    async def approve(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.delete()
        await interaction.channel.send("Aprobado!")
    
    @discord.ui.button(label="Rechazar", style=discord.ButtonStyle.red)
    async def reject(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.message.delete()
        await interaction.channel.send("Rechazado!")
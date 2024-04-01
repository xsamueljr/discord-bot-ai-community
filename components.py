import discord


class ApportationView(discord.ui.View):
    def __init__(self, categories: dict, contributor_role: discord.Role, **kwargs):
        super().__init__(**kwargs)
        self.categories = categories
        self.contributor_role = contributor_role


    @discord.ui.button(label="Aprobar", style=discord.ButtonStyle.green)
    async def approve(self, button: discord.ui.Button, interaction: discord.Interaction):
        embed = interaction.message.embeds[0]
        
        # Getting user
        user_id = int(embed.fields[0].value.strip("<@>"))
        author = interaction.guild.get_member(user_id)
        assert author is not None, f"{user_id}, {author}"
        category = embed.fields[1].value
        
        channel = self.categories[category]

        embed.remove_field(1)
        
        await interaction.message.delete()
        await channel.send(embed=embed)
        await author.add_roles(self.contributor_role, reason="Aportación aprobada")


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

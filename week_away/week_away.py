import discord
from redbot.core import commands, Config, app_commands

class week_away(commands.Cog):
    """Reply to selected words with customized messages."""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=1234567890, force_registration=True)

        # Estrutura: {"palavra": "resposta"}
        default_guild = {"replies": {}}
        self.config.register_guild(**default_guild)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return

        replies = await self.config.guild(message.guild).replies()
        content = message.content.lower()

        for word, reply in replies.items():
            if word.lower() in content:
                try:
                    await message.reply(reply)
                except discord.HTTPException:
                    pass
                break  # responde apenas uma vez por mensagem

    # ===== Comandos de gerenciamento =====
    @commands.group(name="weekaway")
    @commands.guild_only()
    async def weekaway(self, ctx):
        """godo"""
        if ctx.invoked_subcommand is None:
            await ctx.send_help(ctx.command)

    @weekaway.command(name="hello", description="Hello World!")
    async def hello(self, interaction: discord.Interaction):
        await interaction.response.send_message("Hello World!", ephemeral=False)

    @weekaway.command(name="add")
    @commands.is_owner()
    async def add_reply(self, ctx, word: str, *, reply: str):
        """Adiciona uma nova palavra e resposta.
        Exemplo: [p]weekaway add oi 'Olá, tudo bem?'"""
        async with self.config.guild(ctx.guild).replies() as replies:
            replies[word] = reply
        await ctx.send(f"✅ Palavra `{word}` adicionada com resposta: {reply}")

    @weekaway.command(name="remove")
    @commands.is_owner()
    async def remove_reply(self, ctx, word: str):
        """Remove uma palavra configurada."""
        async with self.config.guild(ctx.guild).replies() as replies:
            if word in replies:
                del replies[word]
                await ctx.send(f"❌ Palavra `{word}` removida.")
            else:
                await ctx.send("⚠️ Essa palavra não está configurada.")

    @weekaway.command(name="list")
    async def list_replies(self, ctx):
        """Lista todas as palavras configuradas."""
        replies = await self.config.guild(ctx.guild).replies()
        if not replies:
            await ctx.send("⚠️ Nenhuma palavra configurada ainda.")
            return

        msg = "**Palavras configuradas:**\n"
        for word, reply in replies.items():
            msg += f"- `{word}` → {reply}\n"
        await ctx.send(msg)
    
    async def setup(bot):
        cog = week_away(bot)
        await bot.add_cog(cog)

        # Registra o slash command da cog
        bot.tree.add_command(cog.hello)

        # Sincroniza com o Discord
        await bot.tree.sync()

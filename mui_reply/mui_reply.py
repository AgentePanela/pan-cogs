import discord
from redbot.core import commands

class mui_reply(commands.Cog):
    """Cog that Reply every selected user (mui) message with worst tweet ever meme."""

    def __init__(self, bot):
        self.bot = bot
        self.target_user_id = 1266601981699428403  # hardcoded 😋
        self.image_url = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTbUow0I_f3ZxS8BwnjySNmhrP4vwd1zGTbcw&s" 

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        # if is not a bot
        if message.author.id == self.target_user_id and not message.author.bot:
            try:
                await message.reply(self.image_url)
            except discord.HTTPException as e:
                print(f"Error sending message: {e}")

    @commands.command()
    @commands.is_owner()
    async def mset_image(self, ctx, url: str):
        """Change image reply."""
        self.image_url = url
        await ctx.send(f"Image reply changed: {url}")

    @commands.command()
    @commands.is_owner()
    async def mget_image(self, ctx):
        """See actual image reply."""
        await ctx.send(f"Actuta image is (image)[{self.image_url}]")

    @commands.command()
    @commands.is_owner()
    async def mset_user(self, ctx, userid: str):
        """Change user reply (use id)."""
        self.target_user_id = userid
        await ctx.send(f"User changed to <@{self.target_user_id}>")

async def setup(bot):
    await bot.add_cog(mui_reply(bot))

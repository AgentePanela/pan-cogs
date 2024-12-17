from .mui_reply import mui_reply

async def setup(bot):
    await bot.add_cog(mui_reply(bot))

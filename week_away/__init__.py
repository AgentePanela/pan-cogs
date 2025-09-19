from .weekaway import WeekAway

async def setup(bot):
    await bot.add_cog(WeekAway(bot))

from .week_away import week_away

async def setup(bot):
    await bot.add_cog(week_away(bot))

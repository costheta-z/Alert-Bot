from discord.ext.commands import Cog


class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        #await self.bot.stdout.send("Fun cog ready")
        if not self.bot.ready:
            self.bot.cogs_ready.ready_up("fun")
            
        print("fun cog ready...")

def setup(bot):
    bot.add_cog(Fun(bot))
    #bot.scheduler.add_job()
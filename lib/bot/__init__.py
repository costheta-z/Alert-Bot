from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase

PREFIX = "+"
OWNER_IDS = [745374570424565932]

class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
		self.guild = None
		self.scheduler = AsyncIOScheduler()

		super().__init__(command_prefix = PREFIX, owner_ids=OWNER_IDS)

	def run(self, version):
		self.VERSION = version

		with open("./lib/bot/token", "r", encoding="utf-8") as tf:
			self.TOKEN = tf.read()

		print("running balalala")
		super().run(self.TOKEN, reconnect=True)

	async def on_connect(self):
		print("balalala connected")

	async def on_disconnect(self):
		print("disconnected")

	async def on_ready(self):
		if not self.ready:
			self.ready = True
			self.guild = self.get_guild(738472262298108005)
			print("balalala ready")
		else:
			print("bot reconnected")


	async def on_message(self, message):
		pass


bot = Bot()

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from glob import glob
from discord.ext.commands import Bot as BotBase
from discord import Intents
from discord import Embed, File
from datetime import datetime
from discord.ext.commands import CommandNotFound
from ..db import db
from apscheduler.triggers.cron import CronTrigger
from asyncio.tasks import sleep

PREFIX = "+"
OWNER_IDS = [618104730496925758]
COGS = [path.split("\\")[-1][:-3] for path in glob("./lib/cogs/*.py")]

class Ready(object):
	def __init__(self):
		for cog in COGS:
			setattr(self, cog, False)

	def ready_up(self, cog):
		setattr(self, cog, True)
		print(f"{cog} cog ready")

	def all_ready(self):
		return all([getattr(self, cog) for cog in COGS])

class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
		self.cogs_ready = Ready()
		self.guild = None
		self.scheduler = AsyncIOScheduler()
		db.autosave(self.scheduler)

		#intents=Intents.default()
		#intents.members=True

		super().__init__(
			command_prefix = PREFIX, 
			owner_ids=OWNER_IDS,
			intents=Intents.all()
			)

	def setup(self):
		for cog in COGS:
			self.load_extension(f"lib.cogs.{cog}")
			print(f" {cog} cog loaded")

	def run(self, version):
		self.VERSION = version

		print("running setup...")
		self.setup()

		with open("./lib/bot/token", "r", encoding="utf-8") as tf:
			self.TOKEN = tf.read()

		print("code_workingDisplayMessage")
		super().run(self.TOKEN, reconnect=True)

	async def print_remainder(self):
		#channel=self.get_channel(738472262298108008)

		##########
		#await self.stdout.send("timed_notif")
		##########

		pass
	
	async def on_connect(self):
		print("bot_connected")

	async def on_disconnect(self):
		print("bot_disconnected")

	async def on_error(self, event_method, *args, **kwargs):
		if event_method == "on_command_error":
			await args[0].send("error_message")
		#channel=self.get_channel(738472262298108008)
		await self.stdout.send("RE occured")
		raise

	def on_command_error(self, context, exception):
		if isinstance(exception, CommandNotFound):
			pass
		elif hasattr(exception, "original"):
			raise exception.original
		else:
			raise exception

	async def on_ready(self):
		if not self.ready:
			self.guild = self.get_guild(738472262298108005)
			self.stdout = self.get_channel(738472262298108008)
			self.scheduler.add_job(self.print_remainder, CronTrigger(day_of_week=0, hour=12, minute=0, second=0))
			self.scheduler.start()

			#channel=self.get_channel(738472262298108008)

			##########
			# await self.stdout.send("bot_message") #because asynchronous
			# embed=Embed(title="msg1_title", 
			# 			description="msg1_description", 
			# 			colour=0xFF0000, 
			# 			timestamp=datetime.utcnow())
			# fields=[("msg2_name", "msg2_value", True), 
			# 		("msg3", "true_inline_msg3", True), 
			# 		("msg4", "inline_false_msg4", False)]
			# for name, value, inline in fields:
			# 	embed.add_field(name=name, value=value, inline=inline)
			# embed.set_author(name="message_author", icon_url=self.guild.icon_url)
			# embed.set_footer(text="message_footer")
			# embed.set_thumbnail(url=self.guild.icon_url)
			# embed.set_image(url=self.guild.icon_url)
			
			# await self.stdout.send(embed=embed)
			# await self.stdout.send(file=File(".\data\images\discord_bot_ptoject_image.png"))
			##########

			while not self.cogs_ready.all_ready():
				await sleep(0.5)

			self.ready = True
			print("bot_ready")

		else:
			print("bot_reconnected")


	async def on_message(self, message):
		pass


bot = Bot()

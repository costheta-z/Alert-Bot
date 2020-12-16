from apscheduler.schedulers.asyncio import AsyncIOScheduler
from discord.ext.commands import Bot as BotBase
from discord import Intents
from discord import Embed, File
from datetime import datetime
from discord.ext.commands import CommandNotFound
from ..db import db

PREFIX = "+"
OWNER_IDS = [618104730496925758]

class Bot(BotBase):
	def __init__(self):
		self.PREFIX = PREFIX
		self.ready = False
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

	def run(self, version):
		self.VERSION = version

		with open("maybe/lib/bot/token", "r", encoding="utf-8") as tf:
			self.TOKEN = tf.read()

		print("discord_bot_project_code_workingDisplayMessage")
		super().run(self.TOKEN, reconnect=True)

	async def on_connect(self):
		print("discord_bot_project_bot_connected")

	async def on_disconnect(self):
		print("discord_bot_project_bot_disconnected")

	async def on_error(self, event_method, *args, **kwargs):
		if event_method == "on_command_error":
			await args[0].send("discord_bot_project_error_message")
		channel=self.get_channel(788476024287133731)
		await channel.send("RE occured")
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
			self.ready = True
			self.guild = self.get_guild(788476024287133728)
			self.scheduler.start()

			channel=self.get_channel(788476024287133731)
			await channel.send("discord_bot_project_bot_message") #because asynchronous
			embed=Embed(title="discord_bot_project_msg1_title", 
						description="discord_bot_project_msg1_description", 
						colour=0xFF0000, 
						timestamp=datetime.utcnow())
			fields=[("discord_bot_project_msg2_name", "discord_bot_project_msg2_value", True), 
					("msg3", "true_inline_msg3", True), 
					("msg4", "inline_false_msg4", False)]
			for name, value, inline in fields:
				embed.add_field(name=name, value=value, inline=inline)
			embed.set_author(name="discord_bot_project_message_author_Nandini_Kapoor", icon_url=self.guild.icon_url)
			embed.set_footer(text="discord_bot_project_message_footer")
			embed.set_thumbnail(url=self.guild.icon_url)
			embed.set_image(url=self.guild.icon_url)
			
			await channel.send(embed=embed)
			await channel.send(file=File("maybe\data\images\discord_bot_ptoject_image.png"))

			print("discord_bot_project_bot_ready")

		else:
			print("discord_bot_project_reconnected")


	async def on_message(self, message):
		pass


bot = Bot()

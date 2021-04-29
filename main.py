import asyncio
import os
from datetime import datetime, timedelta
import discord
from dotenv import load_dotenv
import random

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
ABDUCTED_ROLE_ID = os.getenv('ABDUCTED_ROLE')
ABDUCTED_CHANNEL_ID = os.getenv('ABDUCTED_CHANNEL')
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)
version = 1.0


@client.event
async def on_ready():
    global version
    print(f"{client.user.name}-{version} is now running on discord.py version {discord.__version__}")
    now = datetime.now()
    difference = 6 - now.weekday()  # how many days till sunday
    start_time = datetime(now.year, now.month, now.day, 12, 0) + timedelta(days=difference)  # starts next sunday
    interval = timedelta(days=7)
    await begin(start_time, interval)


async def begin(start_time: datetime, interval: timedelta):
    now = datetime.now()
    sleep_time = (start_time - now).total_seconds()
    await asyncio.sleep(sleep_time)
    next_time = start_time
    abducted_channel = client.get_channel(int(ABDUCTED_CHANNEL_ID))
    while True:
        now = datetime.now()
        if now > next_time:
            next_time = next_time + interval

            for guild in client.guilds:
                abducted_role = discord.utils.get(guild.roles, id=int(ABDUCTED_ROLE_ID))
                members = []
                for member in guild.members:
                    if abducted_role not in member.roles and not member.bot:
                        members.append(member)

                if len(members) > 0:
                    abducted = random.choice(members)
                    await abducted.add_roles(abducted_role, reason=f"{abducted.mention} has been deported")
                    await abducted_channel.send(
                        f'{abducted.mention} has been deported. If you wish to stay in this country legally, you may beg to President Solarium, or you can take the Citizenship Test [here](https://docs.google.com/forms/d/e/1FAIpQLScFVm-qm1GyRt2ac9K2gOdMXFhz_wUj-flGiTDzCM7ydFd6LQ/viewform?usp=sf_link)')

        await asyncio.sleep(1)


client.run(TOKEN)

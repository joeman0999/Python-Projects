import disnake
import asyncio

IDS = {
    "general": 428922729329328161
}


MESSAGE = "Nope. Teh only thing that scares me is my wfie when shes hungry"

token = "MTA3Nzc1MzY3MzY5MTcxMzU3Ng.GaOWfg.sg-pY9tu9ybVWuFEE9HRWkZ_3nWgQQFsLTUI4I"
class MyClient(disnake.Client):
    async def on_message(self, message: disnake.Message):
        print(message.content)
        if message.author.bot:
            return
        #if "Hi" in message.content:
        #    await message.reply("I'm already here Mr. Umbrage")
    async def on_ready(self):
        print(f'We have logged in as {client.user}')
        #await client.get_channel(IDS["general"]).send(MESSAGE)
        #asyncio.create_task(self.irritate())
        
    async def irritate(self):
        while True:
            await asyncio.sleep(1)
            await (await client.fetch_user(646914291923943444)).send("fuck you")
        


intents = disnake.Intents.default()
intents.message_content = True

if __name__ == "__main__":
    client = MyClient(intents=intents)
    client.run(token)
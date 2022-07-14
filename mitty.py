#導入 Discord.py
import discord
import ffmpeg
from discord.ext import commands
import asyncio
import json
#client 是我們與 Discord 連結的橋樑
client = commands.Bot(command_prefix = "!!")

with open('token.json','r',encoding = 'utf8') as jfile:
    jdata = json.load(jfile)


#調用 event 函式庫
@client.event
#當機器人完成啟動時
async def on_ready():
    print('目前登入身份：', client.user)
    #這邊設定機器人的狀態
    #discord.Status.<狀態>，可以是online（上線）,offline（下線）,idle（閒置）,dnd（請勿打擾）,invisible（隱身）
    status_w = discord.Status.dnd
    #這邊設定機器當前的狀態文字
    #type可以是playing（遊玩中）、streaming（直撥中）、listening（聆聽中）、watching（觀看中）、custom（自定義）
    activity_w = discord.Activity(type=discord.ActivityType.playing, name="莉可")

    await client.change_presence(status= status_w, activity=activity_w)

@client.event
#當有訊息時
async def on_message(message):
    if "叫一下" in message.content:
        await message.channel.send(f"ニャァァ")
    elif "米蒂" in message.content:
        await message.channel.send(f"ニャァァ?")
    await client.process_commands(message)

'''@client.event
#當有訊息時
async def on_message(message):
    #排除自己的訊息，避免陷入無限循環
    if message.author == client.user:
        return
    #如果包含 ping，機器人回傳 pong
    if message.content == 'ping':
        await message.channel.send('pong')
'''
@client.command(pass_context = True)
async def mitty(contex):
    if(contex.author.voice):
        channel = contex.message.author.voice.channel
        vc = await channel.connect()
        vc.play(discord.FFmpegPCMAudio('mitty.mp3'))
        counter = 0
        duration = 10   # In seconds
        while not counter >= duration:
            await asyncio.sleep(1)
            counter = counter + 1
        await vc.disconnect()
    else:
        await contex.send("Not in a voice channel.")

@client.command(pass_context = True)
async def play_source(voice_client):
    source = discord.FFmpegPCMAudio("mitty.mp3")
    voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else client.loop.create_task(play_source(voice_client)))

@client.command(pass_context = True)
async def mitty_loop(contex):
    if(contex.author.voice):
        channel = contex.message.author.voice.channel
        vc = await channel.connect()
        client.loop.create_task(play_source(vc))
    else:
        await contex.send("Not in a voice channel.")

@client.command(pass_context = True)
async def leave(contex):
    if(contex.voice_client):
        await contex.guild.voice_client.disconnect()
        await contex.send("ニャァァァァァァァー")
    else:
        await contex.send("I'm not in a voice channel.")

client.run(jdata['TOKEN']) #TOKEN 在剛剛 Discord Developer 那邊「BOT」頁面裡面
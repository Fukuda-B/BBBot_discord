import discord
TOKEN=''
CHANNEL_ID=''

# 接続に必要なオブジェクトを生成
client = discord.Client()
channel = client.get_channel(CHANNEL_ID)


async def greet(str):
    channel = client.get_channel(CHANNEL_ID)
    # print(str)
    await channel.send(str)

# 起動時に動作する処理
@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    await greet('BBBotが起動したよ！')

# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # メッセージ送信者がBotだった場合は無視する
    if message.author.bot:
        return
    if message.content == '/B!':
        await message.channel.send('B!')
    if message.content == '/B greet':
        await message.channel.send('こんにちは！ BBBotだよ．\nよろしくね')
    if message.content == '/B hello':
        await message.channel.send('Hello B!')

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)

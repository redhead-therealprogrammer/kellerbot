import disnake
from disnake.ext import commands
import qrcode as qr
import time
import os
import uuid
import datetime
import random

print('Starting...', end='\r')

bot = commands.InteractionBot()

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.slash_command(name='ping')
async def ping(ctx):
    await ctx.send(f'Pong! {round(bot.latency * 1000)}ms')

@bot.slash_command(name='qrcode')
async def qrcode(ctx):
    pass

@qrcode.sub_command(name='text', description='Generate a QR Code')
async def qrcode_text(ctx, text: str):
    img = qr.make(text)
    time_act = str(time.time())
    img.save(f'tmp/qrcodes/qrcode{time_act}.png')
    await ctx.send(file=disnake.File('tmp/qrcodes/qrcode'+time_act+'.png'))
    os.remove('tmp/qrcodes/qrcode'+time_act+'.png')

@qrcode.sub_command(name='vcard', description='Generate a Contact QR Code')
async def qrcode_vcard(ctx, vorname: str, nachname: str, telefon: int, email: str = None, organisation: str = None):
    if email == None:
        email = ''
    if organisation == None:
        organisation = ''
    vcard = f'''BEGIN:VCARD
VERSION:3.0
FN:{vorname} {nachname}
TEL:{telefon}
EMAIL:{email}
ORG:{organisation}
END:VCARD'''
    img = qr.make(vcard)
    time_act = str(time.time())
    img.save(f'tmp/qrcodes/qrcode{time_act}.png')
    await ctx.send(file=disnake.File('tmp/qrcodes/qrcode'+time_act+'.png'))
    os.remove('tmp/qrcodes/qrcode'+time_act+'.png')

@bot.slash_command(name='time', description='Get the current time.')
async def time_(ctx):
    curr_time = datetime.datetime.now()
    string = f'Wir haben den {curr_time.strftime("%d-%m-%Y")}. Es ist {curr_time.strftime("%H:%M:%S")} Uhr.'
    await ctx.send(string)

@bot.slash_command(name='uuid', description='A Universally Unique Identifier (UUID) is a 128-bit number.')
async def uuid_(ctx):
    await ctx.send(uuid.uuid4())

@bot.slash_command(name='kluge_worte', description='Gibt ein random Informatiker Spruch / Weißheit aus')
async def kluge_worter(ctx):
    import sprueche
    embed = disnake.Embed(title=f'{random.choice(sprueche.sprueche)}', color=0x00ff00)
    await ctx.send(embed=embed)

bot.run('TOKEN')

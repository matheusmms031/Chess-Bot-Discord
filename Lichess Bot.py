import discord
import PIL
import numpy as np
import matplotlib
from bs4 import BeautifulSoup
import requests
import json

client = discord.Client()

@client.event
async def on_message(message):
    rating_dict = {}
    partidas_dict = {}
    if message.content.startswith('_playerLichess'):
        playername = message.content.split(' ')[1]
        page = requests.get(f'https://lichess.org/@/{playername}')
        if page.status_code == 200:
            soup = BeautifulSoup(page.text, 'html.parser')
            biografia = soup.find(class_="bio")
            timeago = soup.find(class_="thin").find("time")
            if biografia != None:
                embed=discord.Embed(title=f"{playername}", description=f'{biografia.text}', color=0x0)
            else:
                embed=discord.Embed(title=f"{playername}", description=f'Sem Biografia', color=0x0)
            for span in soup.find_all('span'):
                titulo = span.find('h3')
                if titulo != None:
                    rating = span.find('rating').find('strong').text
                    partidas = span.find('rating').find('span').text
                    embed.add_field(name=f"{titulo.text}", value=f"Rating = {rating} | {partidas}", inline=True)
                    print(f'{titulo} | {rating}')
            await message.channel.send(embed=embed)
        else:
            await message.channel.send('Este jogador não existe...')

client.run("TOKEN")


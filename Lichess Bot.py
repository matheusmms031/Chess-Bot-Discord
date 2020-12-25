import discord
import numpy as np
import matplotlib
from bs4 import BeautifulSoup
import requests
import json
import chess
import chess.svg
from PIL import Image
from io import BytesIO

client = discord.Client() # Chama o client do discord

@client.event # Determina um evento a ocorrer
async def on_message(message): # 'on_message()' é usado para determinar oque fazer quando uma mensagem for mandada no servidor, o objeto 'message' recebe com ele alguns métodos..
    #
    # Está parte do código aqui em baixo eu não usei a API do LICHESS, então ficou muito confuso por isso nem a comentei
    #

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

    #
    # Até aqui eu não tinha conhecimento da existência de uma API para o LICHESS.
    #

    if message.content.startswith('_gamelichess'): # Está linha da inicio a pesquisa de jogos no Lichess
        game_id = message.content.split(' ')[1] # O game_id recebe o código que vem depois da url do Liches
        header = {'content-type': 'application/json'}
        param = {'clocks':'false','evals':'false','litarate':'true'}
        response = requests.get(f'https://lichess.org/game/export/{game_id}', params=param, headers=header) # Requisição na API do Lichess
        if response.status_code == 200:
            board = chess.Board()
            print(response.text) 
            info_lista = response.text.split('\n')
            for info in info_list:
                if '[Opening ' in info:
                    abertura = info.replace('[Opening ','').replace(']','').replace('"','')
                if '[Variant ' in info:
                    variante = info.replace('[Variant ','').replace(']','').replace('"','')
                if '[White ' in info:
                    white = info.replace('[White ','').replace(']','').replace('"','')
                if '[Black ' in info:
                    black = info.replace('[Black ','').replace(']','').replace('"','')
                if '1. ' in info:
                    moves = info
            embed=discord.Embed(title=f"{white} x {black}",description=f'{variante}', color=0x0) # Cria a mensagem que será enviado para o Discord com as informações
            embed.add_field(name=f"Moves", value=f"{moves}", inline=True) # Cria a mensagem que será enviado para o Discord com as informações 
            embed.add_field(name=f"Opening", value=f"{abertura}", inline=True) # Cria a mensagem que será enviado para o Discord com as informações
            await message.channel.send(embed=embed) # Envia a Mensagem

client.run("TOKEN")



import discord
import numpy as np
import matplotlib
from bs4 import BeautifulSoup
import requests
import json
import bancodedados as bd
import time
import datetime
import chess
import chess.svg
from PIL import Image
from io import BytesIO
from svglib.svglib import svg2rlg
import json
import svglib
import reportlab
from reportlab.graphics import renderPDF, renderPM

client = discord.Client() # Chama o client do discord

@client.event
async def on_ready():
    bd.excluir_todas_partidas()
    bd.excluir_todas_propostas()
    
@client.event # Determina um evento a ocorrer
async def on_message(message): # 'on_message()' é usado para determinar oque fazer quando uma mensagem for mandada no servidor, o objeto 'message' recebe com ele alguns métodos..
    if datetime.datetime.now().minute%2 == 0:
        propostas = bd.ver_propostas()
        for proposta in propostas:
            if proposta['tempo'] + 2 < (datetime.datetime.now().minute+datetime.datetime.now().hour*60):
                guild = client.get_guild(proposta['server'])
                channel = guild.get_channel(proposta['canal'])
                bd.excluir_proposta(proposta['_id'])
                await channel.send(f"O tempo para aceitar o convite acabaou <@{proposta['brancas']}>")
    #
    # Está parte do código aqui em baixo eu não usei a API do LICHESS, então ficou muito confuso por isso nem a comentei
    #
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
                    rating = span.find('rating').find('strong')
                    partidas = span.find('rating').find('span')
                    embed.add_field(name=f"{titulo.text}", value=f"Rating = {rating} | {partidas}", inline=True)
                    print(f'{titulo} | {rating}')
            await message.channel.send(embed=embed)
        else:
            await message.channel.send('Este jogador não existe...')

    #
    # Até aqui eu não tinha conhecimento da existência de uma API para o LICHESS.
    #
    if message.content.startswith('_playerChess'):
        nome_usuario = message.content.split(' ')[1]
        st = requests.get(f'https://api.chess.com/pub/player/{nome_usuario}/stats')
        inf = requests.get(f'https://api.chess.com/pub/player/{nome_usuario}')
        if inf.status_code == 200:
            status = json.loads(st.text)
            infos = json.loads(inf.text)
            embed=discord.Embed(title=f"{infos['username']}", color=0x0)
            print(status)
            if 'avatar' in infos:
                embed.set_thumbnail(url=f"{infos['avatar']}")
            for info in status:
                if info == "chess_rapid":
                    embed.add_field(name="Rapid", value=f"Rating = {status['chess_rapid']['last']['rating']}", inline=True)
                if info == "chess_blitz":
                    embed.add_field(name="Blitz", value=f"Rating = {status['chess_blitz']['last']['rating']}", inline=True)
                if info == "chess_bullet":
                    embed.add_field(name="Bullet", value=f"Rating = {status['chess_bullet']['last']['rating']}", inline=True)
            await message.channel.send(embed=embed)
        else:
            await message.channel.send('Este jogador não existe...')

    if message.content.startswith('_gameLichess'): # Está linha da inicio a pesquisa de jogos no Lichess
        try:
            game_id = message.content.split(' ')[1] # O game_id recebe o código que vem depois da url do Liches
            header = {'content-type': 'application/json'}
            param = {'clocks':'false','evals':'false','litarate':'true'}
            response = requests.get(f'https://lichess.org/game/export/{game_id}', params=param, headers=header) # Requisição na API do Lichess
            if response.status_code == 200:
                print(response.text) 
                info_list = response.text.split('\n')
                for info in info_list:
                    if '[Event ' in info:
                        modo = info.replace('[Event ','').replace(']','').replace('"','')
                    if '[UTCDate ' in info:
                        data = info.replace('[UTCDate ','').replace(']','').replace('"','')
                    if '[WhiteElo ' in info:
                        white_elo = info.replace('[WhiteElo ','').replace(']','').replace('"','')
                    if '[BlackElo ' in info:
                        black_elo = info.replace('[BlackElo ','').replace(']','').replace('"','')
                    if '[Result ' in info:
                        ganhador = info.replace('[Result ','').replace(']','').replace('"','')
                    if '[Opening ' in info:
                        abertura = info.replace('[Opening ','').replace(']','').replace('"','')
                    if '[Variant ' in info:
                        variante = info.replace('[Variant ','').replace(']','').replace('"','')
                    if '[White ' in info:
                        white = info.replace('[White ','').replace(']','').replace('"','')
                    if '[Black ' in info:
                        black = info.replace('[Black ','').replace(']','').replace('"','')
                    if '1. ' in info:
                        moves_total = info
                embed=discord.Embed(title=f"{white} x {black}",description=f'{modo}\n```{moves_total}```',color=0x0) # Cria a mensagem que será enviado para o Discord com as informações
                resultado = ganhador.split('-')
                resultado[0] = int(resultado[0])
                resultado[1] = int(resultado[1])
                embed.add_field(name=f"White", value=f"{white} | {white_elo}", inline=True)
                embed.add_field(name=f"Black", value=f"{black} | {black_elo}", inline=True)
                if resultado[0] > resultado[1]:
                    embed.add_field(name=f"Ganhador", value=f"{white}", inline=True)
                if resultado[0] < resultado[1]: 
                    embed.add_field(name=f"Ganhador", value=f"{black}", inline=True)
                print(resultado)
                embed.add_field(name=f"Abertura", value=f"{abertura}", inline=True)
                embed.add_field(name=f"UTC-Date", value=f"{data}", inline=True)
                embed.add_field(name=f"Link", value=f"https://lichess.org/{game_id}", inline=True)
                await message.channel.send(embed=embed)
        except:
            await message.channel.send('Por favor digite o comando da seguinte maneira: ``_gameLichess [id-game]`')
            

    if message.content.startswith('_play') and len(message.mentions) == 1:
        minutos = datetime.datetime.now().minute + datetime.datetime.now().hour*60
        propostas_no_canal = bd.ver_quantidade_propostas_de_canal(message.channel.id)
        if propostas_no_canal == 0:
            partidas = bd.ver_partidas()
            partidas_contador = bd.ver_quantidade_partidas()
            propostas_contador = bd.ver_quantidade_propostas()
            partida_exist = False
            proposta_exist = False
            propostas = bd.ver_propostas()
            if partidas_contador != 0:
                for partida in partidas:
                    if message.mentions[0].id == partida['pretas'] or message.author.id == partida['brancas'] or message.author.id == partida['pretas'] or message.mentions[0].id == partida['brancas']:
                        await message.channel.send('O seu adversário ou você está em uma partida no momento.')
                        partida_exist = True
            if propostas_contador != 0:
                for proposta in propostas:
                    if message.mentions[0].id == proposta['pretas'] or message.author.id == proposta['brancas'] or message.author.id == proposta['pretas'] or message.mentions[0].id == proposta['brancas']:
                        await message.channel.send('O seu adversário ou você já mandaram proposta para alguém.')
                        proposta_exist = True
            if partida_exist == False and proposta_exist == False:
                bd.registrar_proposta(message.author.id,message.mentions[0].id,message.id,message.channel.id,message.guild.id,minutos)
                await message.channel.send(f'<@{message.mentions[0].id}> aceita a proposta de <@{message.author.id}>?')


    if message.content.startswith('_aceitar'):
        propostas_contador = bd.ver_quantidade_propostas()
        propostas = bd.ver_propostas()
        if propostas_contador != 0:
            for proposta in propostas:
                if proposta['pretas'] == message.author.id:
                    bd.registrar_partida(proposta['brancas'],proposta['pretas'],proposta['canal'],proposta['server'],proposta['tempo'])
                    bd.excluir_proposta(proposta['_id'])
                    board_exemplo = chess.Board()
                    fen = board_exemplo.fen().split(" ")[0]
                    await message.channel.send(f'https://chessboardimage.com/{fen}.png')
    
    if message.content.startswith('_mv'):
        board = chess.Board()
        movimento = message.content.split(' ')[1]
        partidas = bd.ver_partidas()
        for partida in partidas:
            if partida['move'] == message.author.id:
                if partida['canal'] == message.channel.id:
                    for move in partida['moves']:
                        board.push_san(move)
                    try:
                        board.push_san(movimento)
                        fen = board.fen()
                        fen = fen.split(' ')[0]
                        await message.channel.send(f'https://chessboardimage.com/{fen}.png')
                        if partida['brancas'] == message.author.id:
                            bd.mover_peca(partida['_id'],partida['pretas'],movimento)
                        if partida['pretas'] == message.author.id:
                            bd.mover_peca(partida['_id'],partida['brancas'],movimento)
                        if board.is_check() and not board.is_checkmate():
                            await message.channel.send('!! CHECK !!')
                        if board.is_checkmate():
                            await message.channel.send('!! CHECK-MATE !!')
                            await message.channel.send(f"VITÓRIA PARA <@{message.author.id}>")
                            bd.excluir_partida(partida['_id'])
                    except:
                        await message.channel.send('Tente um lance válido')
                else:
                    await message.channel.send('Sua partida não foi definida nesse canal-de-texto')
            else:
                await message.channel.send('Não é a sua vez de jogar')

    if message.content.startswith('_desistir'):
        partidas = bd.ver_partidas()
        for partida in partidas:
            if partida['move'] == message.author.id:
                bd.excluir_partida(partida['_id'])
                await message.channel.send('!! DESISTÊNCIA !!')
            else:
                await message.channel.send('Não é a sua vez de jogar')

    if message.content.startswith('_cep'):
        cep = message.content.split(' ')[1]
        response = requests.get(f'https://viacep.com.br/ws/{cep}/json/')
        await message.channel.send(response.text)

    if message.content.startswith('_help'):
        embed = discord.Embed(title=f"Comandos",description='Todos os comandos do nosso bot estará disponivel aqui. Caso precise de mais informações sobre o bot entre em contanto com o nosso desenvolvedor principal o *Matheus Magalhães*', color=0x0)
        embed.add_field(name="Perfis",value='`_playerChess [username]` --> Exibe os ratings da pessoa no **Chess.com**\n`_playerLichess [username]` --> Exibe os ratings da pessoa no **Lichess.com**')
        embed.add_field(name="Jogos",value='`_gameLichess [game-id]` --> Exibe a partida por completo, tal partida tem que ser do **Lichess.com** e o *game-id* tem que ser o código que fica depois do https://lichess.org/\n`_play [@username]` --> Jogar com alguém pelo bot, para o oponente aceitar a proposta, o oponente terá que digitar `_aceitar` no mesmo canal em que foi desafiado e para mover peças é só usar `_mv [jogada]`, as brancas sempre serão quem desafia, para desistir é apenas digitar `_desistir` quando for sua vez, Obs: Não é possível usar um canal-de-texto para dois jogos e se a proposta foi feita no canal **A** a partida só ocorrerá no canal **A**')
        await message.channel.send(embed = embed)

    # if message.content.startswith('_search-gameLichess'):
    #     lista_parmetros = message.content.strip(' ').split('/')
    #     header = {'content-type': 'application/json'}
    #     param = {'clocks':'false','evals':'false','litarate':'true'}
    #     for parametro in lista_parmetros:
    #         if 'username=' in parametro:
    #             username = parametro.replace('username=', '')
    #         if 'max=' in parametro:
    #             param['max'] = parametro.replace('max=', '')
    #         else:
    #             param['max'] = 50
    #         if 'vs=' in parametro:
    #             param['vs'] = parametro.replace('vs=', '')
    #         if 'type=' in parametro:
    #             param['type'] = parametro.replace('type=', '')
    #         if 'rated=' in parametro:
    #             param['rated'] = parametro.replace('rated=', '')
    #     response = requests.get(f'https://lichess.org/api/games/user/{username}', headers=header,params=param)
    #     print(response.text)
    
client.run("TOKEN") # <-- Substitua aqui pela token do seu bot

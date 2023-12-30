import pymongo
from tokens import TOKENS

client = pymongo.MongoClient(TOKENS['mongodb']['ip'],TOKENS['mongodb']['porta'])
db = client.informations
db_membros = client.membros
col_partidas = db.partidas
col_propostas = db.propostas

def registrar_proposta(brancas,pretas,mensagem,canal,server,tempo):
    col_propostas.insert_one({'_id':mensagem,'brancas':brancas,'pretas':pretas,'canal':canal,'server':server,'tempo':tempo})

def registrar_partida(brancas,pretas,canal,server,tempo):
    partidas = col_partidas.count_documents({})
    col_partidas.insert_one({'_id':partidas+1,'brancas':brancas,'pretas':pretas,'canal':canal,'server':server,'tempo':tempo,'move':brancas,'moves':[]})

def excluir_proposta(id):
    col_propostas.delete_one({'_id':id})

def ver_partidas():
    return col_partidas.find()

def ver_quantidade_partidas():
    return col_partidas.count_documents({})

def ver_quantidade_propostas_de_canal(canal):
    return col_propostas.count_documents({'canal':canal})

def ver_quantidade_propostas():
    return col_propostas.count_documents({})

def mover_peca(id,jogador,move):
    partida = col_partidas.find_one({'_id':id})
    data = partida['moves']
    data.append(move)
    newvalues =  {"$set":{'move':jogador,'moves':data}}
    col_partidas.update_one({'_id':id},newvalues)
    
def ver_propostas():
    return col_propostas.find()

def excluir_partida(id):
    col_partidas.delete_one({'_id':id})

def excluir_todas_partidas():
    col_partidas.delete_many({'_id':{'$exists':'True'}})

def excluir_todas_propostas():
    col_propostas.delete_many({'_id':{'$exists':'True'}})
# Chess Bot Discord

**Bot de xadrez para servidores de discord**, nele é possível jogar xadrez usando coordenadas e fazer busca por partidas e jogadores das plataformas mais famosas de xadrez.<br><br><br>
<div align="center" styles='padding:500px'>
    <img src='image.png' height='200'/>
</div>

## Configurando o Bot

Antes de iniciar tudo devemos fazer a instalação dos pacotes e logo em seguida configurar os tokens e informações relevantes.

### Instalando dependências

Para conseguir usar o **Chess Bot Discord** é necessário ter o `Python 3.12.x` e o `MongoDB` instalado, tendo isso em mãos é preciso abaixar o arquivo .zip do repositório e extrair no local desejado, logo depois abra o cmd na pasta do repositorio extraido e execute a seguinte linha de comando:
```bash
pip3 install -r requirementes.txt
```
Esse comando é super importante e não pode ser esquecido, sem ele se torna impossível continuar o processo de execução do bot.
> [!IMPORTANT]
> Caso apareça um erro de instalação e seja necessário instalar o Visual Build C++ instale a versão `1.14`

<hr>

### Criando a aplicação

Para inicializar o Bot é necessário criar uma aplicação na [página de desenvolvedor do discord](https://discord.com/developers/applications), e logo em seguida criar um bot para essa aplicação a habilitar o **MESSAGE CONTENT INTENT**, **SERVER MEMBERS INTENT** e **PRESENCE INTENT**.

### Configurando Tokens

Para configurar é necessário editar o arquivo [tokens.py](./tokens.py) e substituir para os seguintes dados:
```py
TOKENS = {
    'discord': 'O token do bot discord',
    'mongodb': {
        'ip': 'IP do banco de dados',
        'porta': 'Porta do banco de dados'
    }
}
```

## Executando o Bot

Agora para executar basta entrar na pasta do repositório e digitar:

```bash
python setup.py
```

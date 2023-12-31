# Chess Bot Discord

**Chess bot for discord servers**, it is possible to play chess using coordinates and search for matches and players from the most famous chess platforms.<br><br><br>
<div align="center" styles='padding:500px'>
    <img src='image.png' height='200'/>
</div>

## Configuring the Bot

Before starting everything, we must install the packages and then configure the tokens and relevant information.

### Installing dependencies

To be able to use **Chess Bot Discord** you need to have `Python 3.12.x` and `MongoDB` installed, having this in hand you need to download the .zip file from the repository and extract it to the desired location, then open it cmd in the extracted repository folder and execute the following command line:
```bash
pip3 install -r requirementes.txt
```
This command is super important and cannot be forgotten, without it it becomes impossible to continue the bot execution process.
> [!IMPORTANT]
> If an installation error appears and you need to install Visual Build C++, install version `1.14`

<hr>

### Creating the application

To launch the Bot it is necessary to create an application on the [discord developer page](https://discord.com/developers/applications), and then create a bot for this application to enable **MESSAGE CONTENT INTENT**, **SERVER MEMBERS INTENT** and **PRESENCE INTENT**.

### Configuring Tokens

To configure it, you need to edit the file [tokens.py](./tokens.py) and replace it with the following data:
```py
TOKENS = {
    'discord': 'The discord bot token',
    'mongodb': {
        'ip': 'Database IP',
        'port': 'Database port'
    }
}
```

## Running the Bot

Now to run it, just go to the repository folder and type:
```bash
python setup.py
```

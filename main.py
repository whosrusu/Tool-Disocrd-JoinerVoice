# import modules
import os, sys, json, asyncio
import discord

def clear():
    system = os.name
    if system == "nt":
        os.system("cls")
    elif system == "posix":
        os.system("clear")

def database():
    global data
    global folder
    global filename
    global file
    folder = os.path.dirname(os.path.abspath(sys.argv[0]))
    filename = folder + "/" + "data.json"
    
    if os.path.exists(filename):
        pass
    else:
        with open(filename, "w") as fp:
            fp.write("{ \n \"tokens\": {\n} \n }")
            fp.close()
            r2usVoice()
            return

    with open(filename, "r") as _file:
        file = _file
        data = json.load(_file)
        file.close()

def addToken(token):
    with open(filename, "r+") as f:
        load = json.load(f)
        if "tokens" not in load:
            load["tokens"] = {}
        counterToken = len(load["tokens"]) + 1
        load["tokens"][str(counterToken)] = token
        f.seek(0)
        json.dump(load, f, indent=4)
        f.truncate()
        f.close()

def removeToken(counter):
    with open(filename, "r+") as f:
        load = json.load(f)
        try:
          load["tokens"].pop(counter)
        except:
            return print("invalid number")
        f.seek(0)
        json.dump(load, f, indent=4)
        f.truncate()

def listTokens():
    with open(filename, "r") as f:
        file = json.load(f)
        tokens = file["tokens"]
        print(tokens)
        f.close()

async def JoinVoiceSys(token, channel_id):
    client = discord.Client()

    @client.event
    async def on_ready():
        print(f'> - Logged in as {client.user}')
        channel = client.get_channel(id=int(channel_id))
        if channel and channel.type == discord.ChannelType.voice:
            try:
                vc = await channel.connect()
            except discord.errors.ClientException:
                print("> - Already connected to a voice channel.")
        else:
            print("> - Invalid voice channel ID.")

    try:
        await client.start(token, bot=False)
    except discord.LoginFailure:
        print(f"> - Invalid token: {token}")

async def LeaveVoiceSys(token, channel_id):
    client = discord.Client()

    @client.event
    async def on_ready():
        print(f'> - Logged in as {client.user}')
        channel = client.get_channel(id=int(channel_id))
        if channel and channel.type == discord.ChannelType.voice:
            try:
                vc = await channel.connect()
                await vc.disconnect()
            except discord.errors.ClientException:
                print("> - Already connected to a voice channel.")
        else:
            print("> - Invalid voice channel ID.")
        

        await channel.connect()
    try:
        await client.start(token, bot=False)
    except discord.LoginFailure:
        print(f"> - Invalid token: {token}")

def r2usVoice():
    clear()
    print("""

    ██▀███   █    ██   ██████ ██▒   █▓ ▒█████   ██▓ ▄████▄  ▓█████ 
    ▓██ ▒ ██▒ ██  ▓██▒▒██    ▒▓██░   █▒▒██▒  ██▒▓██▒▒██▀ ▀█  ▓█   ▀ 
    ▓██ ░▄█ ▒▓██  ▒██░░ ▓██▄   ▓██  █▒░▒██░  ██▒▒██▒▒▓█    ▄ ▒███   
    ▒██▀▀█▄  ▓▓█  ░██░  ▒   ██▒ ▒██ █░░▒██   ██░░██░▒▓▓▄ ▄██▒▒▓█  ▄ 
    ░██▓ ▒██▒▒▒█████▓ ▒██████▒▒  ▒▀█░  ░ ████▓▒░░██░▒ ▓███▀ ░░▒████▒
    ░ ▒▓ ░▒▓░░▒▓▒ ▒ ▒ ▒ ▒▓▒ ▒ ░  ░ ▐░  ░ ▒░▒░▒░ ░▓  ░ ░▒ ▒  ░░░ ▒░ ░
    ░▒ ░ ▒░░░▒░ ░ ░ ░ ░▒  ░ ░  ░ ░░    ░ ▒ ▒░  ▒ ░  ░  ▒    ░ ░  ░
    ░░   ░  ░░░ ░ ░ ░  ░  ░      ░░  ░ ░ ░ ▒   ▒ ░░           ░   
    ░        ░           ░       ░      ░ ░   ░  ░ ░         ░  ░
                                ░                ░               

    """)
    print(""" 
          > - Please choose an option:
          > - Developer: whosrusu

    1 [+] Add Token.
    2 [+] Remove Token
    3 [+] Connect to VC Token
    4 [+] Disconnect from VC Token
    5 [-] Exit
    """)

    global mode

    mode = input("# Choice: ")

    if mode == "1":
        database()
        _token = input("> - Token: ")
        addToken(_token)
        return r2usVoice()

    elif mode == "2":
        database()
        listTokens()
        counter = input("> - number: ")
        removeToken(counter)
        return  r2usVoice()

    elif mode == "3":
        channel_id = input("> - channel id: ")
        database()
        async def bot():
            print(f"> - Connecting {len(data['tokens'])} tokens to voice channel...")
            tasks = [asyncio.create_task(JoinVoiceSys(data["tokens"][_token], channel_id)) for _token in data["tokens"]]
            await asyncio.gather(*tasks)

        asyncio.run(bot())

    elif mode == "4":
        database()
        channel_id = input("> - channel id: ")
        async def bot():
            tasks = [asyncio.create_task(LeaveVoiceSys(data["tokens"][_token], channel_id)) for _token in data["tokens"]]
            await asyncio.gather(*tasks)

        asyncio.run(bot())

    elif mode == "5":
        clear()
        exit()

    else:
        print("> - Invalid choice. Please type 1 | 2 | 3 | 4 | 5.")

r2usVoice()
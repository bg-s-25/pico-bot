import discord
from bs4 import BeautifulSoup
import requests
import random

COMMANDS_LIST = ['hello', 'help', 'channel', 'add', 'ip', 'flip', 'roll']
client = discord.Client()

# Definitions for client events

@client.event
async def on_message(message):
    # bot should not reply to itself
    if message.author == client.user:
        return

    # not a command
    if message.content.startswith('!') == False:
        return

    msg_content = message.content

    if msg_content.startswith('!hello'): # say hello and mention user
        msg = "Hello {0.author.mention}".format(message)

    elif msg_content.startswith('!help'): # display commands
        msg = "List of commands:"
        for command in COMMANDS_LIST.sort:
            msg += "\n!" + command

    elif msg_content.startswith('!channel'): # create/delete an empty channel in the server
        parameters = str.split(msg_content[9:])
        result = channel(client.get_server('id'), parameters) # fix
        msg = str(result[1])

    elif msg_content.startswith('!add'): # add integers
        result = add(str.split(msg_content[5:]))
        msg = "Result: " + str(result[1]) if result[0] == 0 else str(result[1])

    elif msg_content.startswith('!ip'): # display public IP
        result = ip()
        msg = "Your public IP address: " + str(result[1]) if result[0] == 0 else str(result[1])

    elif msg_content.startswith('!flip'): # flip n coins
        parameters = str.split(msg_content[6:])
        result = flip(parameters[0]) if len(parameters) > 0 else flip(1)
        msg = "You got: " + str(result[1]) if result[0] == 0 else str(result[1])

    elif msg_content.startswith('!roll'): # roll n dice
        parameters = str.split(msg_content[6:])
        result = roll(parameters[0]) if len(parameters) > 0 else roll(1)
        msg = "You got: " + str(result[1]) if result[0] == 0 else str(result[1])

    else:
        msg = "Error: Unknown command"

    await client.send_message(message.channel, msg)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

# Definitions for bot commands
# Each method returns a tuple with a status code and message content; 0 = success, 1 = error

def add(nums):
    if len(nums) == 0:
        return (1, "Error: No numbers specified")
    sum = 0
    for n in nums:
        if safe_cast(n, int) is None:
            return (1, "Error: Unrecognized parameter(s)")
        else:
            sum += int(n)
    return (0, str(sum))

def ip():
    r  = requests.get("https://www.google.com/search?q=my+ip")
    data = r.text
    soup = BeautifulSoup(data, features="html.parser")
    fullstring = str(soup.find_all('div', class_="Sjv6Ff YO8Tje vk_h"))
    ipstring = ''
    append = False
    for s in fullstring:
        if s == '>':
            append = True
        elif s == '<' and append:
            append = False
            break
        elif append:
            ipstring += s
    if fullstring == '' or ipstring == '':
        return (1, "Error: Could not retrieve IP address")
    else:
        return (0, ipstring)

def flip(n):
    if safe_cast(n, int) is None:
        return (1, "Error: Unrecognized parameter(s)")
    result_string = ''
    for i in range(0, int(n)):
        rnd = random.randint(0, 1) 
        if rnd == 0:
            result_string += 'HEADS, '
        else:
            result_string += 'TAILS, '
    return (0, result_string[:-2])

def roll(n):
    if safe_cast(n, int) is None:
        return (1, "Error: Unrecognized parameter(s)")
    result_string = ''
    for i in range(0, int(n)):
        rnd = random.randint(0, 5) + 1
        result_string += str(rnd) + ', '
    return (0, result_string[:-2])

def channel(server, params):
    if params[0] == 'c':
        # create channel
        client.create_channel(server, params[1], False)
    elif params[0] == 'd':
        # delete channel
        if params[1].lower() == 'general':
            return (1, "Error: Cannot delete general channel")
        client.delete_channel(params[1])
    else:
        return (1, "Error: Unrecognized parameter(s)")
    return (0, "Done")

# Misc

def safe_cast(val, to_type, default=None):
    try:
        return to_type(val)
    except (ValueError, TypeError):
        return default

def test():
    print(add([9, 'a']))

# Run bot
client.run('token')

import discord
import socket
from queue import Queue
import threading
import datetime

time = datetime.datetime.now()

open_ports = []
def portscan(host,port):
    try:
        s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.settimeout(2)
        s.connect((host,port))
        return True
    except:
        return False


q = Queue()

def getports():
    for i in range(1,1024):
        q.put(i)

def worker(host):
    while not q.empty():
        port = q.get()
        if portscan(host,port):
            open_ports.append(port)


def run_scanner(threads,host):
    getports()

    threadlist = []

    for t in range(threads):
        thread = threading.Thread(target=worker,args=(host,))
        threadlist.append(thread)

    for thread in threadlist:
        thread.start()

    for thread in threadlist:
        thread.join()

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print("Bot is online and ready!")

@client.event
async def on_message(message):
    if '$scan' in message.content:
        cmd = message.content
        host = cmd.replace('$scan ','')
        await message.channel.send("[+] Port Scan Started! wait a while....")
        run_scanner(100,host)
        with open(f'{time}.txt', 'w') as f:
            f.write(f'[+] Port Scan Started at {time} on Target => {host}.\n')
            for port in open_ports:
                await message.channel.send(f"[+] Port {port} is open!")
                f.write(f"[+] Port {port} is open!\n")
            end_time = datetime.datetime.now()
            f.write(f'[+] Scan Completed at {end_time}!\n')
        await message.channel.send("[+] Log File : ")
        await message.channel.send(file=discord.File(f'{time}.txt'))
        await message.channel.send("[+] Scan Completed!")
        open_ports.clear()
        f.close()


client.run('MTE2MDU4NDYxMTE5NDIwODM2Nw.GgoWQn.kjleoW1Ig_s8DvpBFdJmwTSqw_-LknRY68Tpb8')

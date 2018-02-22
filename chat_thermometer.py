import socket
import random
import sys
import time
import json
import os
import re
from datetime import datetime
from collections import defaultdict

msgsPerMinute = {}
msgsPerMinute = defaultdict(int)

# --------------------------------------------- Start Settings ----------------------------------------------------
HOST = "irc.twitch.tv"                          # Hostname of the IRC-Server in this case twitch's
PORT = 6667                                     # Default IRC-Port
CHAN = "#channel"                               # Channelname = #{Nickname}
NICK = ""                                       # Nickname = Twitch username
PASS = "oauth:..."                              # www.twitchapps.com/tmi/ will help to retrieve the required authkey
# --------------------------------------------- End Settings -------------------------------------------------------

#authorized = {''}

#random.seed()

# --------------------------------------------- Start Functions ----------------------------------------------------
def send_pong(msg):
    con.send(bytes('PONG %s\r\n' % msg, 'UTF-8'))


def send_message(chan, msg):
    con.send(bytes('PRIVMSG %s :%s\r\n' % (chan, msg), 'UTF-8'))


def send_nick(nick):
    con.send(bytes('NICK %s\r\n' % nick, 'UTF-8'))


def send_pass(password):
    con.send(bytes('PASS %s\r\n' % password, 'UTF-8'))


def join_channel(chan):
    con.send(bytes('JOIN %s\r\n' % chan, 'UTF-8'))


def part_channel(chan):
    con.send(bytes('PART %s\r\n' % chan, 'UTF-8'))
# --------------------------------------------- End Functions ------------------------------------------------------


# --------------------------------------------- Start Helper Functions ---------------------------------------------
def get_sender(msg):
    result = ""
    for char in msg:
        if char == "!":
            break
        if char != ":":
            result += char
    return result


def get_message(msg):
    result = ""
    i = 3
    length = len(msg)
    while i < length:
        result += msg[i] + " "
        i += 1
    result = result.lstrip(':')
    return result



t1 = datetime.now()
t2 = None
deltaT = None
data = ''

def parse_message(msg, sender):
	return

def writeToFile(w):
	with open('termometro_chat.json', 'w', encoding='utf8') as myFile:
		json.dump(w, myFile)
	
# --------------------------------------------- End Helper Functions -----------------------------------------------


con = socket.socket()
con.connect((HOST, PORT))

send_pass(PASS)
send_nick(NICK)
join_channel(CHAN)



print("Bot is connected to " + CHAN)
lastMinute = int(datetime.now().strftime('%M'))
key = str('{:%Y-%b-%d %H:%M}'.format(datetime.now()))

# the program counts all messages and returns
# the number of messages per minute, every minute
def main():
	
	while True:
		global data
		try:
			data = data+con.recv(1024).decode('UTF-8')
			data_split = re.split(r"[~\r\n]+", data)
			data = data_split.pop()
		
			for line in data_split:
				line = str.rstrip(line)
				line = str.split(line)
            
				if len(line) >= 1:
				
					# These 2 try-except blocks are important because
					# the request often didn't get a good response...
					# So if for some reason we get a 
					# 'None' (empty object) from the request,
					# our program doesn't crash.
					try:
						if line[0] == 'PING':
							send_pong(line[1])
				
					
						if line != None:
							try:
								if line[1] == 'PRIVMSG':
									# message
									global msgsPerMinute
									global t1
									global t2
									global deltaT
									global lastMinute
									global key
								
									
									msgsPerMinute[str('{:%Y-%b-%d %H:%M}'.format(datetime.now()))] = int(msgsPerMinute[str('{:%Y-%b-%d %H:%M}'.format(datetime.now()))]) + 1
									
									currentMinute = int(datetime.now().strftime('%M'))


									if currentMinute > lastMinute:
										print(key + ': ' + str(msgsPerMinute[key]))
										key = str('{:%Y-%b-%d %H:%M}'.format(datetime.now()))
										lastMinute = currentMinute
										

									t2 = datetime.now()
									deltaT = t2 - t1
									
									# hourly writes all data to file
									if deltaT.total_seconds() > 3600: # you can change this if you want 
										writeToFile(msgsPerMinute)

							except:
								pass
					except:
						pass
						
					
					
		except socket.error:
			print("Socket died")

		except socket.timeout:
			print("Socket timeout")
    
if __name__ == "__main__":
    main()
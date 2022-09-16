import json
import sys
import argparse
import socket
import ssl

# Default settings
HOST = 'proj1.3700.network'
PORT = 27993
BUFFER = 2048
username = "narine.k"
correctWord = ""
global wordList

# Getting the wordlist
f = open('wordlist.txt', 'r')
wl = f.read()
wordList = wl.split()
f.close()


# Setting up the argument parser
# parser = argparse.ArgumentParser()
# parser.add_argument("-p", required=False, type=int)
# parser.add_argument("-s", required=False, type='store_true')
# parser.add_argument("hostname", type=str)
# parser.add_argument("Northeastern-username", type=str)
# args = parser.parse_args()
#
# if args.p:
#     PORT = args.p
# elif args.s:
#     PORT = 27994
#
# HOST = args.hostname
# username = args.Northeastern-username

# Setting up the socket
cliSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# SSL Stuff
# if args.s:
#     cliSocket = ssl.wrap_socket(cliSocket)

ADDRESS = (HOST, PORT)


try:
    cliSocket.connect(ADDRESS)

except:
    print("Connection Error")


# def sendguess(id, word):
#     guess = {"type":"guess", "id":id, "word": word}
#     guessMsg = json.dumps(guess) + "\n"
#     guessMsg = guessMsg.encode(("utf-8"))
#     cliSocket.send(guessMsg)
#
#
# def recvguess(count):
#     returned = cliSocket.recv(BUFFER).decode("utf-8")
#     returned = json.loads(returned)
#     currStatus = returned["type"]
#     returned = returned["guesses"][count]
#     return returned, currStatus

# Starting Message
helloMsg = {"type": "hello", "northeastern_username": username}

startData = json.dumps(helloMsg) + "\n"

cliSocket.sendall(startData.encode())

returnData = cliSocket.recv(BUFFER).decode()
returnData = json.loads(returnData)

gameID = returnData["id"]



while True:
    curWord = wordList.pop()


    guessMsg = json.dumps({"type":"guess", "id":gameID ,"word":curWord}) + "\n"
    cliSocket.sendall(guessMsg.encode())

    guessAns = cliSocket.recv(BUFFER).decode()
    while '\n' not in guessAns:
        guessAns = guessAns + cliSocket.recv(BUFFER).decode()
    guessJson = json.loads(guessAns)

    if guessJson["type"] == "bye":
        print(guessJson["flag"])
        cliSocket.close()
        quit()


    count = 0
    backup = wordList.copy()

    for mark in guessJson["guesses"][-1]["marks"]:

        if mark == 1:
            for w in wordList:
                if curWord[count] not in w:
                    if w in backup:
                        backup.remove(w)

        elif mark == 2:
            for w in wordList:
                if curWord[count] != w[count]:
                    if w in backup:
                        backup.remove(w)

        # Move to next letter
        count += 1

    wordList = backup.copy()


import json
import os
import re
import shlex
import socket
from apis.twitchapi import TwitchApi

import requests
import faster_than_requests as ft_requests

whitelist = [
        "not_a_bot_its_nancy",
        "hannylicious",
        "HyFlicker",
        "pooki3bear",
        "joshwoods2002",
        "JuanCarlosPaco",
        "Amperture",
        ]

blacklist = [
        #"hannylicious",
        ]

def extract_information(twitch_message):
    """
    read the original message from twitch
    """
    username, channel, message = re.search(':(.*)\!.*@.*\.tmi\.twitch\.tv PRIVMSG #(.*) :(.*)', twitch_message).groups()
    return username, channel, message

def get_song_information(command):
    band = command_arguments[0]
    song = command_arguments[1]

    return command_arguments

def commands(user, command, command_arguments=None):
    """
    commands recieved from chat
    """
    if command == "!about":
        return_message = "Hey "+username+" I'm hannylicious!"
        twitch_api.chat(sock, return_message)

    if user in whitelist:
        if command == "!gitcha":
            return_message = "Gotcha! "+username
            twitch_api.chat(sock, return_message)

        if command == '!gr':
            # !gr "blur" "song #2
            song_info = get_song_information(command_arguments)
            # store_song_information(song_info)
            band = command_arguments[0]
            song = command_arguments[1]
            #TODO : verify song/band exist
            request_dictionary = {
                "user": user,
                "song": song,
                "band": band
            }
            #TODO : Turn the base url for the API into an environment variable for ease of switching between dev/prod
            guitar_request = json.dumps(request_dictionary)
            response = requests.post("http://localhost:8000/api/guitarrequests/", json=request_dictionary)
            if response.status_code == 200:
                print("Should be added")
            return_message = f"""
                Hey {username}, thanks for the guitar request for {song} by {band}! I will do my best to learn that quickly for you!
                """
            twitch_api.chat(sock, return_message)
        if command_arguments:
                print(command_arguments)

    if user in blacklist:
        return_message = "Hey "+username+", nice try - but you are not able to do this. Please forgive me. Or blame me, I don't care - I'm Nancy."
        twitch_api.chat(sock, return_message)

while __name__ == "__main__":
    twitch_api = TwitchApi()
    sock = TwitchApi.connect()
    while True:
        twitch_message = sock.recv(2048).decode('utf-8')
        if twitch_message.startswith('PING'):
            print(twitch_message)
            print("PONG")
            sock.send(('PONG :tmi.twitch.tv\r\n').encode('utf-8'))
        username = ""
        channel = ""
        message = ""
        prefix = os.environ.get("PYTWITCHIO_PREFIX")
        if "PRIVMSG" in twitch_message:
            username, channel, message = extract_information(twitch_message)
        print(username + ":" + message)
        if message.startswith(prefix):
            command_string = message.rstrip()
            command_arguments = shlex.split(command_string)
            command = command_arguments.pop(0)
            commands(username, command, command_arguments)

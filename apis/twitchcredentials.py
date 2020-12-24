import os

class TwitchCredentials(object):

    HOST = os.environ['PYTWITCHIO_HOST']
    PORT = os.environ['PYTWITCHIO_PORT']
    NICK = os.environ['PYTWITCHIO_BOT_NICK']
    PASS = os.environ['PYTWITCHIO_OAUTH_KEY']
    CHAN = os.environ['PYTWITCHIO_CHANNEL']

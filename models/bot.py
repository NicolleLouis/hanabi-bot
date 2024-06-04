import sys
import requests
from dotenv import dotenv_values
from models.client import Client


# Authenticate, login to the WebSocket server, and run forever.
class Bot:
    def __init__(self, bot_index=None):
        self.bot_index = bot_index
        self.start()

    def start(self):
        # Load environment variables from the ".env" file.
        config = dotenv_values(".env")

        # Load environment variables from the ".env" file.
        username = config.get(f"HANABI_USERNAME{self.bot_index}")
        password = config.get(f"HANABI_PASSWORD{self.bot_index}")

        # The official site uses HTTPS.
        protocol = "https"
        ws_protocol = "wss"
        host = "hanab.live"

        path = "/login"
        ws_path = "/ws"
        url = protocol + "://" + host + path
        ws_url = ws_protocol + "://" + host + ws_path
        print('Authenticating to "' + url + '" with a username of "' + username + '".')
        response = requests.post(
            url,
            {
                "username": username,
                "password": password,
                "version": "bot",
            },
        )

        # Handle failed authentication and other errors.
        if response.status_code != 200:
            print("Authentication failed:")
            print(response.text)
            sys.exit(1)

        # Scrape the cookie from the response.
        cookie = ""
        for header in response.headers.items():
            if header[0] == "Set-Cookie":
                cookie = header[1]
                break
        if cookie == "":
            print("Failed to parse the cookie from the authentication response headers:")
            print(response.headers)
            sys.exit(1)

        Client(ws_url, cookie).start()

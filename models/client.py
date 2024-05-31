import json
import websocket

from constants.actions import ACTION
from models.game import Game
from services.chat import ChatService
from services.client import ClientService


class Client:
    def __init__(self, url, cookie):
        # Initialize all class variables.
        self.command_handlers = {}
        self.tables = {}
        self.username = ""
        self.ws = None
        self.games = {}
        self.chat_service = ChatService(self)
        self.service = ClientService(self)

        # Initialize the website command handlers (for the lobby).
        self.command_handlers["welcome"] = self.welcome
        self.command_handlers["warning"] = self.warning
        self.command_handlers["error"] = self.error
        self.command_handlers["chat"] = self.chat
        self.command_handlers["table"] = self.table
        self.command_handlers["tableList"] = self.table_list
        self.command_handlers["tableGone"] = self.table_gone
        self.command_handlers["tableStart"] = self.table_start

        # Initialize the website command handlers (for the game).
        self.command_handlers["init"] = self.game_start
        self.command_handlers["gameAction"] = self.game_action
        self.command_handlers["gameActionList"] = self.game_action_list
        self.command_handlers["databaseID"] = self.database_id

        # Start the WebSocket client.
        print('Connecting to "' + url + '".')

        self.ws = websocket.WebSocketApp(
            url,
            on_message=lambda ws, message: self.websocket_message(ws, message),
            on_error=lambda ws, error: self.websocket_error(ws, error),
            on_open=lambda ws: self.websocket_open(ws),
            on_close=lambda ws: self.websocket_close(ws),
            cookie=cookie,
        )
        self.ws.run_forever()

    # ------------------
    # WebSocket Handlers
    # ------------------

    def websocket_message(self, ws, message):
        result = message.split(" ", 1)  # Split it into two things
        if len(result) not in [1, 2]:
            print("error: received an invalid WebSocket message:")
            print(message)
            return

        command = result[0]
        try:
            data = json.loads(result[1])
        except Exception:
            print(
                'error: the JSON data for the command of "' + command + '" was invalid'
            )
            return

        if command in self.command_handlers:
            try:
                self.command_handlers[command](data)
            except Exception as e:
                print('error: command handler for "' + command + '" failed:', e)
                return

    @staticmethod
    def websocket_error(ws, error):
        print("Encountered a WebSocket error:", error)

    @staticmethod
    def websocket_close(ws):
        print("WebSocket connection closed.")

    @staticmethod
    def websocket_open(ws):
        print("Successfully established WebSocket connection.")

    # --------------------------------
    # Website Command Handlers (Lobby)
    # --------------------------------

    def welcome(self, data):
        self.username = data["username"]

    def error(self, data):
        print(data)

    def warning(self, data):
        # We have done something wrong.
        print(data)

    def chat(self, data):
        self.chat_service.receive_message(data)

    def join_table(self, data):
        try:
            table_id = self.service.find_table(data)
        except Exception:
            msg = "Please create a table first before requesting that I join your game"
            self.chat_service.send_message(msg, data["who"])
            return

        self.send(
            "tableJoin",
            {
                "tableID": table_id,
            },
        )

    def table(self, data):
        self.tables[data["id"]] = data

    def table_list(self, data_list):
        for data in data_list:
            self.table(data)

    def table_gone(self, data):
        del self.tables[data["tableID"]]

    def table_start(self, data):
        self.send(
            "getGameInfo1",
            {
                "tableID": data["tableID"],
            },
        )

    # -------------------------------
    # Website Command Handlers (Game)
    # -------------------------------

    def game_start(self, data):
        game = Game()
        game.start(data)
        self.send(
            "getGameInfo2",
            {
                "tableID": data["tableID"],
            },
        )

    def game_action(self, data):
        game = self.games[data["tableID"]]
        game.handle_action(data)

    def game_action_list(self, data):
        for action in data["list"]:
            self.game_action(action)
        self.send(
            "loaded",
            {
                "tableID": data["tableID"],
            },
        )

    def database_id(self, data):
        self.send(
            "tableUnattend",
            {
                "tableID": data["tableID"],
            },
        )
        del self.games[data["tableID"]]

    # ---------------------------------
    # Website Command Handlers (Outputs)
    # ---------------------------------

    def send(self, command, data):
        if not isinstance(data, dict):
            data = {}
        self.ws.send(command + " " + json.dumps(data))

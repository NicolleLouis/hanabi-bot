from typing import Callable


class ChatService:
    def __init__(self, client):
        self.client = client

    def receive_message(self, data):
        try:
            command_arguments = self.is_valid_command(data)
        except Exception:
            return

        sender = self.get_sender(data)

        reaction = self.find_reaction(command_arguments)
        reaction(sender)

    def is_valid_command(self, data):
        if data["recipient"] != self.client.username:
            raise Exception("I am not the recipient")

        if not data["msg"].startswith("/"):
            raise Exception("The message does not start with a slash")

        cleaned_message = data["msg"][1:]  # Remove the slash.

        command_arguments = cleaned_message.split(" ", 1)
        return command_arguments

    def find_reaction(self, command_arguments) -> Callable[[str], None]:
        command = command_arguments[0]
        if command == "join":
            return self.client.join_table
        else:
            return self.send_unrecognized_command_message

    def send_unrecognized_command_message(self, sender):
        self.send_message("That is not a valid command", sender)

    @staticmethod
    def get_sender(data):
        return data["who"]

    def send_message(self, message, recipient):
        self.client.send(
            "chatPM",
            {
                "msg": message,
                "recipient": recipient,
                "room": "lobby",
            },
        )
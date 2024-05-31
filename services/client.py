class ClientService:
    def __init__(self, client):
        self.client = client

    def find_table(self, owner):
        for table in self.client.tables.values():
            # Ignore games that have already started (and shared replays).
            if table["running"]:
                continue

            if owner in table["players"]:
                if len(table["players"]) == 6:
                    msg = "Your game is full. Please make room for me before requesting that I join your game."
                    self.client.chat_service.send_message(msg, owner)
                    return

                return table["id"]

        raise Exception("No table found")

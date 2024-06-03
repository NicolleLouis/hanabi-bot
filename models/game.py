from __future__ import annotations

from constants.actions import ACTION
from models.player import Player

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models.client import Client


class Game:
    def __init__(self, client: Client):
        self.client = client
        self.table_id = None
        self.clue_tokens = 8
        self.players = []
        self.own_index = -1
        self.hands = []
        self.play_stacks = []
        self.discard_pile = []
        self.turn = -1
        self.current_player_index = -1

    def __str__(self):
        return f"Game: table_id={self.table_id}, turn_number={self.turn}"

    def start(self, data):
        self.generate_players(data["playerNames"])
        self.own_index = data["ourPlayerIndex"]
        self.table_id = data["tableID"]

        # Initialize the play stacks.
        # ToDo: Replace by real stacks
        suits_number = 5
        for _ in range(suits_number):
            self.play_stacks.append([])

    def generate_players(self, player_names):
        for i, name in enumerate(player_names):
            self.players.append(Player(name, i))

    def get_players(self, player_index):
        return self.players[player_index]

    def handle_action(self, data):
        # We just received a new action for an ongoing game.
        self.update_state(data)

        if self.current_player_index == self.own_index:
            self.choose_action(data)

    def choose_action(self, data):
        # Decide what to do.
        if self.clue_tokens > 0:
            # There is a clue available, so give a rank clue to the next
            # person's slot 1 card.

            # Target the next player.
            target_index = self.own_index + 1
            if target_index > len(self.players) - 1:
                target_index = 0

            # Cards are added oldest to newest, so "slot 1" is the final
            # element in the list.
            target_hand = self.hands[target_index]
            slot_1_card = target_hand[-1]

            self.send_decision(
                {
                    "type": ACTION.RANK_CLUE,
                    "target": target_index,
                    "value": slot_1_card["rank"],
                }
            )
        else:
            # There are no clues available, so discard our oldest card.
            oldest_card = self.hands[self.own_index][0]
            self.send_decision(
                {
                    "type": ACTION.DISCARD,
                    "target": oldest_card["order"],
                }
            )

    # ToDo refacto in smaller function
    def update_state(self, data):
        # data = data["action"] <- Still needed?

        if data["type"] == "draw":
            player = self.get_players(data["playerIndex"])
            player.add_card_to_hand(
                data["order"],
                data["rank"],
                data["suitIndex"],
            )

        elif data["type"] == "play":
            player = self.get_players(data["which"]["playerIndex"])
            order = data["which"]["order"]
            card = player.remove_card_from_hand(order)
            if card is not None:
                # TODO Add the card to the play stacks.
                pass

        elif data["type"] == "discard":
            player = self.get_players(data["which"]["playerIndex"])
            order = data["which"]["order"]
            card = player.remove_card_from_hand(order)
            if card is not None:
                # TODO Add the card to the discard stacks.
                pass

            # Discarding adds a clue. But misplays are represented as discards,
            # and misplays do not grant a clue.
            if not data["failed"]:
                self.clue_tokens += 1

        elif data["type"] == "clue":
            # Each clue costs one clue token.
            self.clue_tokens -= 1

            # TODO We might also want to update the game of cards that are
            # "touched" by the clue so that we can keep track of the positive
            # and negative information "on" the card.

        elif data["type"] == "turn":
            # A turn is comprised of one or more game actions (e.g. play +
            # draw). The turn action will be the final thing sent on a turn,
            # which also includes the index of the new current player.
            # TODO: This action may be removed from the server in the future
            # since the client is expected to calculate the turn on its own
            # from the actions.
            self.turn = data["num"]
            self.current_player_index = data["currentPlayerIndex"]

    def send_decision(self, decision):
        body = {
            "tableID": self.table_id,
            "type": decision["type"],
            "target": decision["target"],
        }
        if "value" in decision:
            body["value"] = decision["value"]

        self.client.send(
            "action",
            body,
        )

from constants.actions import ACTION


class Game:
    def __init__(self, client):
        self.client = client
        self.table_id = None
        self.clue_tokens = 8
        self.player_names = []
        self.own_index = -1
        self.hands = []  # An array containing card objects (dictionaries).
        self.play_stacks = []
        self.discard_pile = []
        self.turn = -1
        self.current_player_index = -1

    def start(self, data):
        self.player_names = data["playerNames"]
        self.own_index = data["ourPlayerIndex"]
        self.table_id = data["tableId"]

        # Initialize the hands for each player (an array of cards).
        # ToDo: Replace by real cards
        for _ in range(len(self.player_names)):
            self.hands.append([])

        # Initialize the play stacks.
        # ToDo: Replace by real stacks
        suits_number = 5
        for _ in range(suits_number):
            self.play_stacks.append([])

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
            if target_index > len(self.player_names) - 1:
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

    def update_state(self, data):
        data = data["action"]

        if data["type"] == "draw":
            # Add the newly drawn card to the player's hand.
            hand = self.hands[data["playerIndex"]]
            hand.append(
                {
                    "order": data["order"],
                    "suit_index": data["suitIndex"],
                    "rank": data["rank"],
                }
            )

        elif data["type"] == "play":
            player_index = data["which"]["playerIndex"]
            order = data["which"]["order"]
            card = self.remove_card_from_hand(player_index, order)
            if card is not None:
                # TODO Add the card to the play stacks.
                pass

        elif data["type"] == "discard":
            player_index = data["which"]["playerIndex"]
            order = data["which"]["order"]
            card = self.remove_card_from_hand(player_index, order)
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

    def remove_card_from_hand(self, player_index, order):
        hand = self.hands[player_index]
        card_index = -1
        for i in range(len(hand)):
            card = hand[i]
            if card["order"] == order:
                card_index = i
        if card_index == -1:
            print(
                "error: unable to find card with order " + str(order) + " in"
                "the hand of player " + str(player_index)
            )
            return None
        card = hand[card_index]
        del hand[card_index]
        return card

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

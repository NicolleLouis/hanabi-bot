class ActionServiceException(Exception):
    pass


class ActionService:
    @staticmethod
    def translate_action(action: str):
        action = int(action)
        if action == 0:
            return "Play"
        elif action == 1:
            return "Discard"
        elif action == 2:
            return "Color Clue"
        elif action == 3:
            return "Rank Clue"
        else:
            raise ActionServiceException("Invalid action type")

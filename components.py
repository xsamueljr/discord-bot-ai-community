from enum import Enum

import discord


SERVER_ID: int = 1216501295033225227

MAILBOX_ID: int = 1221907546177011762

class Category(Enum):
    category1 = "category1"
    category2 = "category2"
    """
    basics = "basics"
    medium = "medium"
    advanced = "advanced"
    offtopic = "offtopic"
    """

    def get_channel_id(self) -> int:
        return {
            "category1": 1221907587826712738,
            "category2": 1221907603932709006
        }[self.value]

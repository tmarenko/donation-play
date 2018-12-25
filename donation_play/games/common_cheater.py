import autoit
import time


class CommonCheater:
    """Class for working with common cheats."""

    def __init__(self, game_title):
        """Class initialization.

        :param str game_title: game title.
        """
        self.title = game_title

    def send_cheat_code(self, cheat_code):
        if not autoit.win_active(self.title):
            autoit.win_activate(self.title)
            time.sleep(1)
        autoit.send(cheat_code)

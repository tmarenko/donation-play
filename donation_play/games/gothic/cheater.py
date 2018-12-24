import autoit
import time
from .constants import Constants


class GothicCheater(Constants):
    """Class for working with Gothic cheats."""

    def __init__(self, gothic_title, mem_editor=None):
        """Class initialization.

        :param str gothic_title: game title.
        :param memory_editor.MemoryEditor mem_editor: instance of MemCheater.
        """
        self.title = gothic_title
        self.mem_editor = mem_editor

    def call_cheat(self, cheat_code):
        """Call cheat code to game console.

        :param str cheat_code: cheat code.
        """
        if not self.marvin_mode:
            self.marvin_mode = True
        console_code = "{console}{code}{code_end}{console}"
        if not autoit.win_active(self.title):
            autoit.win_activate(self.title)
            time.sleep(0.5)
        time.sleep(1)
        autoit.send(console_code.format(console=self.CONSOLE_KEY, code=cheat_code, code_end=self.ENTER_CHEAT_KEY))
        self.marvin_mode = False

    def call_b_cheat(self, cheat_code):
        """Call B cheat code to game menu.

        :param str cheat_code: cheat code.
        """
        console_code = "{activator}{code}{activator}"
        if not autoit.win_active(self.title):
            autoit.win_activate(self.title)
            time.sleep(0.5)
        time.sleep(1)
        autoit.send(console_code.format(activator=self.B_CHEATS, code=cheat_code))

    def cancel_b_cheats(self):
        """Cancel effect of B cheats."""
        console_code = "{activator}{code}{activator}"
        if not autoit.win_active(self.title):
            autoit.win_activate(self.title)
            time.sleep(0.5)
        time.sleep(1)
        autoit.send(console_code.format(activator=self.B_CHEATS, code=self.CANCEL_B_CHEATS))

    def spawn(self, npc_code):
        """Spawn NPC by code.

        :param npc_code: NPCs code.
        """
        cheat_code = "i{npc_code}".format(npc_code=npc_code)
        self.call_cheat(cheat_code=cheat_code)

    def heal(self):
        """Heal hero."""
        cheat_code = "chf"
        self.call_cheat(cheat_code=cheat_code)

    def teleport(self, waypoint_code):
        """Teleport hero to waypoint.

        :param waypoint_code: waypoint code
        """
        cheat_code = "gw{waypoint_code}".format(waypoint_code=waypoint_code)
        self.call_cheat(cheat_code=cheat_code)

    def set_hour(self, hour):
        """Set in-game hours.

        :param hour: 24-h format of hours.
        """
        cheat_code = "seti{hour}".format(hour=hour)
        self.call_cheat(cheat_code=cheat_code)

    def set_2d_characters(self):
        """Set characters to 2D."""
        cheat_code = "GROMMIT"
        self.call_b_cheat(cheat_code=cheat_code)

    def set_characters_fat(self):
        """Set characters fat."""
        cheat_code = "GARFIELD"
        self.call_b_cheat(cheat_code=cheat_code)

    def set_speed_hack(self):
        """Enable speed hack."""
        cheat_code = "SOUTHPARK"
        self.call_b_cheat(cheat_code=cheat_code)

    @property
    def skill_points(self):
        """Hero's skill points."""
        return self.mem_editor.get_value_from_pointer(*self.SKILL_POINTS_POINTER)

    @skill_points.setter
    def skill_points(self, value):
        self.mem_editor.put_value_into_pointer(value, *self.SKILL_POINTS_POINTER)

    @property
    def strength(self):
        """Hero's strength."""
        return self.mem_editor.get_value_from_pointer(*self.STRENGTH_POINTER)

    @strength.setter
    def strength(self, value):
        self.mem_editor.put_value_into_pointer(value, *self.STRENGTH_POINTER)

    @property
    def agility(self):
        """Hero's agility."""
        return self.mem_editor.get_value_from_pointer(*self.AGILITY_POINTER)

    @agility.setter
    def agility(self, value):
        self.mem_editor.put_value_into_pointer(value, *self.AGILITY_POINTER)

    @property
    def marvin_mode(self):
        """Cheat mode - MARVIN mode."""
        value = self.mem_editor.get_value_from_pointer(*self.MARVIN_POINTER)
        return value == 1

    @marvin_mode.setter
    def marvin_mode(self, value):
        bool_value = value == 1
        self.mem_editor.put_value_into_pointer(bool_value, *self.MARVIN_POINTER)

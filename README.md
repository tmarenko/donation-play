# donation-play

Activate game cheats via donation events.

## Installation

With Python3:

```pip install git+git://github.com/tmarenko/donation-play.git```

## Usage

Sign in to [DonationAlerts](https://www.donationalerts.com/) and copy your token from [settings](https://www.donationalerts.com/dashboard/general) tab.

Write function to handle donation events and wait them.

```python
from donation_play.donation_alerts import DonationAlerts
from donation_play.games.gothic.cheater import GothicCheater
from donation_play.memory_editor import MemoryEditor

# Setup game helpers for cheats and console commands
mem_editor = MemoryEditor(process_name="GothicMod.exe")
gothic_cheater = GothicCheater(gothic_title="GOTHIC 1.08k_mod", mem_editor=mem_editor)

# Setup your callback for donation event
def donation_callback(username, message, amount, is_sub, months):
    if username == "My Favoruite Viewer":
        gothic_cheater.spawn(gothic_cheater.NPC_DEMON)
    if amount > 10:
        gothic_cheater.heal()
    if is_sub:
        gothic_cheater.strength += 5 * months
        gothic_cheater.agility += 5 * months


d_alert = DonationAlerts(host="http://socket.donationalerts.ru", port=3031, token="my_token")
d_alert.add_donation_callback(donation_callback)
d_alert.wait()
```

## Extra

Use games libraries from ```games``` module to help yourself.

Use ```MemoryEditor``` to edit game process memory. Pointers can be scanned via [CheatEngine](https://www.cheatengine.org/)
(read [tutorial](https://wiki.cheatengine.org/index.php?title=Tutorials:Cheat_Engine_Tutorial_Guide_x64)).

```python
from donation_play.memory_editor import MemoryEditor

HEALTH_POINTER = (0x12345678, 0x123)

my_game_memory = MemoryEditor(process_name="MyGame.exe")
health = my_game_memory.get_value_from_pointer(*HEALTH_POINTER)
my_game_memory.put_value_into_pointer(value=9999, *HEALTH_POINTER)
```
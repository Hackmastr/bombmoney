# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from colors import Color
from config.manager import ConfigManager
from core import GAME_NAME
from cvars.flags import ConVarFlags
from cvars.public import PublicConVar
from events import Event
from messages import SayText2
from players.entity import Player
from plugins.info import PluginInfo
from translations.strings import LangStrings


# =============================================================================
# >> PLUGIN INFORMATION
# =============================================================================
info = PluginInfo()
info.author = 'Kill, iPlayer'
info.basename = 'bombmoney'
info.name = 'Bomb Money'
info.description = 'Give money to bomb planter/defuser'
info.version = '1.0'

PublicConVar(info.basename + '_version', info.version)


# ==============================================================================
# >> Constants
# ==============================================================================
CHAT_PREFIX = "\x03[SP]\x01"

if GAME_NAME not in ('csgo',):
    YELLOW_GREEN = Color(154, 205, 50)
else:
    YELLOW_GREEN = "\x05"


# ==============================================================================
# >> Create Config, read it
# ==============================================================================
plugin_config = ConfigManager(info.basename)
plugin_config.header = "Bomb Money configuration file"

bomb_plant_reward = plugin_config.cvar(
    'bomb_plant_reward', 1000,
    'Money to reward the bomb planter.', ConVarFlags.DONTRECORD
)
bomb_defuse_reward = plugin_config.cvar(
    'bomb_defuse_reward', 1000,
    'Money to reward the bomb defuser.', ConVarFlags.DONTRECORD
)

plugin_config.write()
plugin_config.execute()


# ==============================================================================
# >> Translation
# ==============================================================================
lang_bombmoney = LangStrings(info.basename)


@Event('bomb_exploded')
def _event_bomb_planted(ge):
    planter = Player.from_userid(ge['userid'])
    _reward_money = bomb_plant_reward.get_int()
    planter.cash += _reward_money
    SayText2(lang_bombmoney['bomb_planted_reward']).send(
        planter.index,
        cp=CHAT_PREFIX,
        color=YELLOW_GREEN,
        money=_reward_money
    )


@Event('bomb_defused')
def _event_bomb_defused(ge):
    defuser = Player.from_userid(ge['userid'])
    _reward_money = bomb_defuse_reward.get_int()
    defuser.cash += _reward_money
    SayText2(lang_bombmoney['bomb_defused_reward']).send(
        defuser.index,
        cp=CHAT_PREFIX,
        color=YELLOW_GREEN,
        money=_reward_money
    )

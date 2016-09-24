# =============================================================================
# >> IMPORTS
# =============================================================================
# Source.Python
from colors import Color
from config.manager import ConfigManager
from core import GAME_NAME
from cvars.public import PublicConVar
from events import Event
from filters.players import PlayerIter
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
info.version = '1.6'

PublicConVar(info.basename + '_version', info.version)


# ==============================================================================
# >> Constants
# ==============================================================================
CHAT_PREFIX = "\x03[SP]\x01"

if GAME_NAME not in ('csgo',):
    YELLOW_GREEN = Color(154, 205, 50)
else:
    YELLOW_GREEN = "\x05"

bomb_reward = {}


# ==============================================================================
# >> Create Config, read it
# ==============================================================================
with ConfigManager(info.basename) as plugin_config:
    plugin_config.header = "Bomb Money configuration file"

    bomb_reward['bomb_exploded'] = plugin_config.cvar(
        'bomb_plant_reward', 1000,
        'Money to reward the bomb planter.'
    )
    bomb_reward['bomb_defused'] = plugin_config.cvar(
        'bomb_defuse_reward', 1000,
        'Money to reward the bomb defuser.'
    )
    bomb_reward['reward_bot'] = plugin_config.cvar(
        'bomb_reward_bot', 1,
        'Reward bots too? can be 1 (true) or 0 (false).'
    )
    bomb_reward['reward_team'] = plugin_config.cvar(
        'bomb_reward_team', 1,
        'Reward the whole team? can be 1 or 0.'
    )
    bomb_reward['reward_team_money'] = plugin_config.cvar(
        'bomb_reward_team_money', 0,
        'Different money amount? can be 1 or 0.'
    )
    bomb_reward['team_reward_ct'] = plugin_config.cvar(
        'bomb_team_reward_ct', 1000,
        'Money to reward the player\'s team(Counter-Terrorist).'
    )
    bomb_reward['team_reward_t'] = plugin_config.cvar(
        'bomb_team_reward_t', 1000,
        'Money to reward the player\'s team(Terrorist).'
    )


# ==============================================================================
# >> Translation
# ==============================================================================
TRANS = LangStrings(info.basename)


@Event('bomb_exploded', 'bomb_defused')
def _event_bomb_planted(ge):
    team = ''
    cvar = bomb_reward[ge.name]
    try:
        player = Player.from_userid(ge.get_int('userid'))
    except OverflowError:
        return
    if player.is_fake_client() and not bomb_reward['reward_bot'].get_int():
        return
    else:
        if bomb_reward['reward_team'].get_int():
            if player.team is 3:
                team = "ct"
            elif player.team is 2:
                team = "t"
            else:
                return  # we couldn't detect the player's team... stop executing.
            if bomb_reward['reward_team_money'].get_int():
                reward_money = bomb_reward['team_reward_' + team].get_int()
            else:
                reward_money = cvar.get_int()
            for _player in PlayerIter(team):
                _player.cash += reward_money
                if _player.index != player.index:
                    SayText2(TRANS['bomb_msg_team_' + team]).send(
                                                                _player.index,
                                                                cp=CHAT_PREFIX,
                                                                color=YELLOW_GREEN,
                                                                money=reward_money)
            player.cash += reward_money
            SayText2(TRANS['bomb_msg_team_player']).send(
                player.index,
                cp=CHAT_PREFIX,
                color=YELLOW_GREEN,
                money=reward_money
            )
        else:
            reward_money = bomb_reward[ge.name].get_int()
            player.cash += reward_money
            SayText2(TRANS[cvar.name]).send(
                player.index,
                cp=CHAT_PREFIX,
                color=YELLOW_GREEN,
                money=reward_money
            )

"""This file hosts all the different regexes for macro detection, variable detection, objective detection, etc."""
import re

# ================================================================================================================== #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ================================================================================================================== #
# Macros
MACRO_PATTERN = re.compile(r"(?<=\$\()[A-Za-z0-9_]*(?=\))")  # `$(` <- ignore, then macro, then ignore -> `)`
MACRO_MESSAGE = "# This function requires the following macros to be passed in:\n"

# ================================================================================================================== #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ================================================================================================================== #
# Function calls
# FUNCTION_PATTERN = r"([\w-]+:[\w/-]+)"
REGULAR_CALLS = re.compile(r"^\$? *function ([\w-]+:[\w/-]+)")  # function namespace:name/subdir
EXECUTE_RUN = re.compile(r"execute .*? run function ([\w-]+:[\w/-]+)")  # execute as @e run function namespace:name/subdir
SCHEDULE = re.compile(r"schedule function +([\w-]+:[\w/-]+) \d+[st]")  # schedule function namespace:name/subdir 1t/5s
# TODO: Incorporate function tags, e.g.
# $function #pypacks_testing:chunk_scanner_functions {"x": $(x), "y": $(y), "z": $(z)}

FUNCTION_PATTERNS = [
    REGULAR_CALLS, EXECUTE_RUN, SCHEDULE,
]
FUNCTION_MESSAGE = "# This function calls the following functions:\n"
# ================================================================================================================== #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ================================================================================================================== #
# Variables
# ==== Templates: 
# PLAYER_OBJ_PATTERN = r"([A-Za-z0-9_#]*)"
# NAMESPACE_PATTERN = r"(?:[A-Za-z0-9_#]*:[A-Za-z0-9_#]*)"
# PATH_PATTERN = r"(?:[A-Za-z0-9_#]+(?:\.[A-Za-z0-9_#]+)*)?"
# ==== Scores set on the player 
IF_UNLESS_SCORE_PATTERN = re.compile(r"(?:if|unless) score ([A-Za-z0-9_#]*) ([A-Za-z0-9_#]*)")  # Group 1, 2 (player, objective)
EXECUTE_STORE_RESULT = re.compile(r"execute store (?:result|success) score ([A-Za-z0-9_#]*) ([A-Za-z0-9_#]*)")  # Group 1, 2 (player, objective)
TEAM_MODIFY = re.compile(r'team modify [A-Za-z0-9_#]+ (?:prefix|suffix) \[\{"score":\{"name":"([A-Za-z0-9_#]*)", "objective":"([A-Za-z0-9_#]*)"\}\}\]')  # Group 1, 2 (player, objective)
TELLRAW_TITLE_ACTIONBAR = re.compile(r'{"score":\{"name":"([A-Za-z0-9_#]*)", "objective":"([A-Za-z0-9_#]*)"\}}')  # Group 1, 2 (player, objective)
EXECUTE_STORE_STORAGE = re.compile(r"execute store (?:result|success) storage [A-Za-z0-9_:#]+ [A-Za-z0-9_#\.\[\]]+ score ([A-Za-z0-9_#]*) ([A-Za-z0-9_#]*)")  # AI
EXECUTE_STORE_ENTITY = re.compile(r"execute store (?:result|success) entity @[aesprn][A-Za-z_\-#\.]* [A-Za-z0-9_#\.\[\]]+ score ([A-Za-z0-9_#]*) ([A-Za-z0-9_#]*)")  # AI
# Temp disabled because not 2 groups:
# SELECTOR_SCORE_PATTERN = re.compile(r"@[aesprn]\[.*?scores=\{([^}]*)\}.*?\]")  # Group 1 (objective), AI
# SCOREBOARD_OPERATION = re.compile(r"scoreboard players operation ([A-Za-z0-9_#]*) ([A-Za-z0-9_#]*) (?:\+=|-=|\*=|\/=|%=|=|<|>|><) ([A-Za-z0-9_#]*) ([A-Za-z0-9_#]*)")  # Group 1, 2, 3, 4 (target, target_obj, source, source_obj)
# ==== Places which need a scoreboard objective to be initialised 
PLAYER_SCORE_CHANGE = re.compile(r"scoreboard players (?:add|set|remove|reset) ([A-Za-z0-9_#]*) ([A-Za-z0-9_#]*)")  # Group 1, 2 (player, objective)
BOSSBAR_SET = re.compile(r"bossbar set [A-Za-z0-9_#]+ value ([A-Za-z0-9_#]*) ([A-Za-z0-9_#]*)")  # Group 1, 2 (player, objective)
SCOREBOARD_GET = re.compile(r"scoreboard players get ([A-Za-z0-9_#]*) ([A-Za-z0-9_#]*)")  # Group 1, 2 (player, objective)
# ==== NBT 
DATA_MODIFY_STORAGE = re.compile(r"data modify storage (?:[A-Za-z0-9_#]*:[A-Za-z0-9_#]*) (?:[A-Za-z0-9_#]+(?:\.[A-Za-z0-9_#]+)*)? set from score ([A-Za-z0-9_#]*) ([A-Za-z0-9_#]*)")  # Group 1, 2 (player, objective)
DATA_MODIFY_ENTITY = re.compile(r"data modify entity @[aesprn][A-Za-z_\-#\.]* [A-Za-z@_-]* set from score ([A-Za-z0-9_#]*) ([A-Za-z0-9_#]*)")  # Group 1, 2 (player, objective)

VARIABLE_MESSAGE = "# This function interfaces with (requireds or sets) the following scoreboard values:\n"

VARIABLE_PAIR_PATTERNS = [
    IF_UNLESS_SCORE_PATTERN, EXECUTE_STORE_RESULT, TEAM_MODIFY, TELLRAW_TITLE_ACTIONBAR, EXECUTE_STORE_STORAGE,
    EXECUTE_STORE_ENTITY, DATA_MODIFY_STORAGE, DATA_MODIFY_ENTITY,
]
VARIABLE_REQUIRE_OBJECTIVE_PATTERNS = [
    PLAYER_SCORE_CHANGE, BOSSBAR_SET, SCOREBOARD_GET,
]
# REQUIRE_ODD_GROUPS = [
#     SELECTOR_SCORE_PATTERN, SCOREBOARD_OPERATION, 
# ]
# ================================================================================================================== #
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
# ================================================================================================================== #

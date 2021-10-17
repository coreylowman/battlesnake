class Game:
    # https://docs.battlesnake.com/references/api#game
    def __init__(self, data):
        self.id: str = data["id"]
        self.ruleset = Ruleset(data["ruleset"])
        self.timeout: int = data["timeout"]

class Ruleset:
    # https://docs.battlesnake.com/references/api#ruleset
    def __init__(self, data):
        self.name: str = data["name"]
        self.version: str = data["version"]
        self.settings = RulesetSettings(data["settings"])

class RulesetSettings:
    # https://docs.battlesnake.com/references/api#rulesetsettings
    def __init__(self, data):
        self.food_spawn_chance: int = data["foodSpawnChance"]
        self.minimum_food: int = data["minimumFood"]
        self.hazard_damage_per_turn: int = data["hazardDamagePerTurn"]

class RoyaleSettings:
    def __init__(self, data):
        pass

class SquadSettings:
    def __init__(self, data):
        pass

class Battlesnake:
    # https://docs.battlesnake.com/references/api#battlesnake
    def __init__(self):
        pass

class Board:
    # https://docs.battlesnake.com/references/api#board
    def __init__(self):
        pass


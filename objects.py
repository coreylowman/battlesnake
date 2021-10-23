from typing import List
from enum import Enum


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
        self.royale = RoyaleSettings(data["royale"])
        self.squad = SquadSettings(data["squad"])


class RoyaleSettings:
    def __init__(self, data):
        self.shrink_every_n_turns: int = data["shrinkEveryNTurns"]

class SquadSettings:
    def __init__(self, data):
        self.allow_body_collisions: bool = data["allowBodyCollisions"]
        self.shared_elimination: bool = data["sharedElimination"]
        self.shared_health: bool = data["sharedHealth"]
        self.shared_length: bool = data["sharedLength"]


class Position:
    @staticmethod
    def load(data) -> "Position":
        return Position(data["x"], data["y"])

    def __init__(self, x: int, y: int):
        self.x: int = x
        self.y: int = y

    def dist(self, other: "Position") -> int:
        return abs(self.x - other.x) + abs(self.y - other.y)

    def apply(self, move: "Move") -> "Position":
        return self + move.value

    def is_out_of_bounds(self, width: int, height: int) -> bool:
        return not (0 <= self.x < width) or not (0 <= self.y < height)

    def __eq__(self, o: "Position") -> bool:
        return self.x == o.x and self.y == o.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __add__(self, o: "Position") -> "Position":
        return Position(self.x + o.x, self.y + o.y)


class Move(Enum):
    UP = Position(0, 1)
    DOWN = Position(0, -1)
    LEFT = Position(-1, 0)
    RIGHT = Position(1, 0)


class Battlesnake(Position):
    # https://docs.battlesnake.com/references/api#battlesnake
    def __init__(self, data):
        self.id: str = data["id"]
        self.name: str = data["name"]
        self.health: int = data["health"]
        self.body: List[Position] = [Position.load(p) for p in data["body"]]
        self.latency: int = data["latency"]
        self.head: Position = Position.load(data["head"])
        self.length: int = data["length"]
        self.shout: str = data["shout"]
        self.squad: str = data["squad"]
        super().__init__(self.head.x, self.head.y)

    def __eq__(self, o: "Battlesnake") -> bool:
        return self.id == o.id

    def could_move_to(self, p: Position) -> bool:
        return any(p == self.apply(m) for m in [Move.UP, Move.DOWN, Move.LEFT, Move.RIGHT])


class Board:
    # https://docs.battlesnake.com/references/api#board
    def __init__(self, data):
        self.width: int = data["width"]
        self.height: int = data["height"]
        self.foods: List[Position] = [Position.load(p) for p in data["food"]]
        self.hazards: List[Position] = [Position.load(p) for p in data["hazards"]]
        self.snakes: List[Battlesnake] = [Battlesnake(s) for s in data["snakes"]]

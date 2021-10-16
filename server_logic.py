import random
from typing import List, Dict

# NOTE: up is y + 1
# NOTE: right is x + 1


def distance(a, b):
    return (a["x"] - b["x"]) ** 2 + (a["y"] - b["y"]) ** 2


def remove_possible_move(move: str, possible_moves: List[str]):
    if move in possible_moves:
        possible_moves.remove(move)


def avoid_body(head: Dict[str, int], body: List[Dict[str, int]], possible_moves: List[str]):
    x = head["x"]
    y = head["y"]
    for segment in body:
        if x + 1 == segment["x"] and y == segment["y"]:
            remove_possible_move("right", possible_moves)
        elif x - 1 == segment["x"] and y == segment["y"]:
            remove_possible_move("left", possible_moves)
        elif x == segment["x"] and y + 1 == segment["y"]:
            remove_possible_move("up", possible_moves)
        elif x == segment["x"] and y - 1 == segment["y"]:
            remove_possible_move("down", possible_moves)


def avoid_edges(my_head: Dict[str, int], width: int, height: int, possible_moves: List[str]):
    if my_head["x"] + 1 == width:
        remove_possible_move("right", possible_moves)
    if my_head["x"] == 0:
        remove_possible_move("left", possible_moves)
    if my_head["y"] + 1 == height:
        remove_possible_move("up", possible_moves)
    if my_head["y"] == 0:
        remove_possible_move("down", possible_moves)


def apply_move(head, move):
    if move == "left":
        return {"x": head["x"] - 1, "y": head["y"]}
    elif move == "right":
        return {"x": head["x"] + 1, "y": head["y"]}
    elif move == "up":
        return {"x": head["x"], "y": head["y"] + 1}
    elif move == "down":
        return {"x": head["x"], "y": head["y"] - 1}


def choose_move(data: dict) -> str:
    print(
        f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~"
    )
    my_head = data["you"]["head"]
    my_body = data["you"]["body"]
    width = data["board"]["width"]
    height = data["board"]["height"]

    print(f"{width=} {height=}")
    print(f"My battlesnake: {data['you']}")
    print(f"My Battlesnakes head this turn is: {my_head}")
    print(f"My Battlesnakes body this turn is: {my_body}")
    print(f"My Battlesnakes health this turn is: {data['you']['health']}")
    print(len(data['board']['snakes']), "snakes")

    possible_moves = ["up", "down", "left", "right"]
    for snake in data["board"]["snakes"]:
        avoid_body(my_head, snake["body"], possible_moves)
    avoid_edges(my_head, width, height, possible_moves)

    # TODO: remove collisions, unless that's our only possible move
    closest_food = min(data["board"]["food"], key=lambda food: distance(food, my_head))

    # Choose a random direction from the remaining possible_moves to move in, and then return that move
    # move = random.choice(possible_moves)
    move = min(possible_moves, key=lambda move: distance(apply_move(my_head, move), closest_food))

    # TODO: Explore new strategies for picking a move that are better than random

    print(
        f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves}"
    )

    return move

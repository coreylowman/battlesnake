import random
from typing import List, Dict
import datetime

# NOTE: up is y + 1
# NOTE: right is x + 1


def distance(a, b):
    return abs(a["x"] - b["x"]) + abs(a["y"] - b["y"])


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

def avoid_head(myhead: Dict[str, int], mylength , snakehead: Dict[str, int], snakelength, possible_moves: List[str]):
    if mylength > snakelength:
        return
    myx = myhead["x"]
    myy = myhead["y"]
    snakex = myhead["x"]
    snakey = myhead["y"]
    if myx + 2 == snakex and myy == snakey:
        remove_possible_move("right", possible_moves)
    elif myx - 2 == snakex and myy == snakey:
        remove_possible_move("left", possible_moves)
    elif myx == snakex and myy + 2 == snakey:
        remove_possible_move("up", possible_moves)
    elif myx == snakex and myy - 2 == snakey:
        remove_possible_move("down", possible_moves)


def could_die(move, me, other) -> bool:
    # returns whether or not this move could collide with the `other` snake
    # if `me` is longer than `other`, this returns False
    if distance(me["head"], other["head"]) > 2 or me["length"] > other["length"]:
        return False
    next_pos = apply_move(me["head"], move)
    for other_move in ["up", "down", "left", "right"]:
        if next_pos == apply_move(other["head"], other_move):
            return True
    return False


def risk(move, me, snakes) -> int:
    # risk is the number of other snakes that this move could collide with
    return sum(could_die(move, me, s) for s in snakes if s["id"] != me["id"])


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


def food_is_mine(snakes, food_coords, me):
    return me == min(snakes, key=lambda s: distance(s["head"], food_coords))


def choose_move(data: dict) -> str:
    start = datetime.datetime.now()
    #print(
    #    f"~~~ Turn: {data['turn']}  Game Mode: {data['game']['ruleset']['name']} ~~~"
    #)
    me = data["you"]
    my_head = data["you"]["head"]
    # my_length = data["you"]["length"]
    my_head = data["you"]["head"]
    # my_body = data["you"]["body"]
    width = data["board"]["width"]
    height = data["board"]["height"]
    snakes = data["board"]["snakes"]
    foods = data["board"]["food"]
    # print(f"{width=} {height=}")
    # print(f"My battlesnake: {data['you']}")
    # print(f"My Battlesnakes head this turn is: {my_head}")
    # print(f"My Battlesnakes body this turn is: {my_body}")
    #print(f"My Battlesnakes health this turn is: {data['you']['health']}")
    # print(len(data['board']['snakes']), "snakes")

    possible_moves = ["up", "down", "left", "right"]

    # stay on the board!
    avoid_edges(my_head, width, height, possible_moves)

    for snake in snakes:
        # avoid collisions with any snake's body
        avoid_body(my_head, snake["body"], possible_moves)

        # avoid possible collisions with any snake's head
        # avoid_head(my_head, my_length, snake["head"], snake["length"], possible_moves)

    # get a list of foods that belong to us (i.e. that we are the closest snake to)
    my_foods = list(filter(lambda f: food_is_mine(snakes, f, data["you"]), foods))

    if len(my_foods) > 0:
        # choose the food that is closest to us & that belongs to us
        closest_food = min(my_foods, key=lambda food: distance(food, my_head))

        # choose the move that brings us closest to the `closest_food`
        move = min(possible_moves, key=lambda move: (risk(move, me, snakes), distance(apply_move(my_head, move), closest_food)))
    else:
        move = min(possible_moves, key=lambda move: risk(move, me, snakes))

    # TODO: remove collisions, unless that's our only possible move

    dur = (datetime.datetime.now() - start).total_seconds() * 1000

    print(
        f"{data['game']['id']} MOVE {data['turn']}: {move} picked from all valid options in {possible_moves} in {dur:.3}ms"
    )

    return move

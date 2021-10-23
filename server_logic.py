from typing import List, Dict
import datetime
import random
from objects import Battlesnake, Board, Move, Position


class Strategy:
    def __init__(self, data: Dict):
        # load in data
        self.me = Battlesnake(data["you"])
        self.board = Board(data["board"])

        self.possible_moves: List[Move] = [Move.UP, Move.DOWN, Move.LEFT, Move.RIGHT]
        random.shuffle(self.possible_moves)
        self.other_snakes: List[Battlesnake] = [s for s in self.board.snakes if s != self.me]

        # syntactic sugar for stuff used a lot
        self.width = self.board.width
        self.height = self.board.height
        self.x = self.me.head.x
        self.y = self.me.head.y
        self.head = self.me.head
        self.length = self.me.length

    def _floodfill(self, move: Move) -> int:
        queue = [self.head.apply(move)]
        done = set()
        while len(queue) > 0:
            position = queue.pop()
            done.add(position)
            for move in [Move.RIGHT, Move.LEFT, Move.DOWN, Move.UP]:
                neighbor = position.apply(move)
                blocked = any(neighbor in s.body for s in self.board.snakes)
                on_grid = 0 <= neighbor.x < self.width and 0 <= neighbor.y < self.height
                if neighbor not in done and neighbor not in queue and not blocked and on_grid:
                    queue.append(neighbor)
        return len(done)


    def _discard(self, move: Move):
        if move in self.possible_moves:
            self.possible_moves.remove(move)

    def _avoid_edges(self):
        for move in [Move.RIGHT, Move.LEFT, Move.DOWN, Move.UP]:
            if self.me.apply(move).is_out_of_bounds(self.width, self.height):
                self._discard(move)

    def _avoid_positions(self, positions: List[Position]):
        for move in [Move.RIGHT, Move.LEFT, Move.DOWN, Move.UP]:
            # if moving this way would intersect with any of the `positions`, don't move this way
            if self.me.apply(move) in positions:
                self._discard(move)

    def _risk(self, move: Move) -> int:
        # calculate where we'll be after this move
        next_pos = self.me.apply(move)

        # a dangerous snake is one that is longer than us and within 1 square of `next_pos`
        dangerous_snakes = filter(lambda s: s.dist(next_pos) <= 1 and self.length <= s.length, self.other_snakes)

        # risk is the number of other snakes that could be at the next position after following `move`
        return sum(snake.could_move_to(next_pos) for snake in dangerous_snakes)

    def _hazardous(self, move: Move) -> bool:
        next_pos = self.me.apply(move)
        return not self._safe(next_pos)

    def _safe(self, p: Position) -> bool:
        return p not in self.board.hazards

    def _own(self, p: Position) -> bool:
        return min(self.board.snakes, key=p.dist) == self.me

    def _pop_tails(self):
        for snake in self.board.snakes:
            if snake.body[-1] != snake.body[-2]:
                snake.body.pop()

    def choose(self) -> Move:
        # remove tails from snakes so we don't have to avoid them
        self._pop_tails()

        # avoid moving off the board
        self._avoid_edges()

        # avoid collisions with any snake's body (including our own!)
        for snake in self.board.snakes:
            self._avoid_positions(snake.body)

        # get a list of foods that belong to us (i.e. that we are the closest snake to)
        # and that is safe
        food_we_own = list(filter(self._own, filter(self._safe, self.board.foods)))

        if len(food_we_own) > 0:
            # choose the food that is closest to us & that belongs to us
            closest_food = min(food_we_own, key=self.me.dist)

            """
            choose move by ordered preference:
            1. minimize risk
            2. minimize distance to closest_food after apply the move
            i.e. first minimize #1, if there are any ties for lowest, use minimum for #2
            """
            move = min(self.possible_moves, key=lambda move: (
                self._risk(move),
                self._hazardous(move),
                self.head.apply(move).dist(closest_food),
                -self._floodfill(move),
            ))
        else:
            # choose move by lowest risk
            move = min(self.possible_moves, key=lambda move: (
                self._risk(move),
                self._hazardous(move),
                -self._floodfill(move),
            ))
        return move


def choose_move(data: dict) -> str:
    start = datetime.datetime.now()

    move = Strategy(data).choose()
    
    duration_ms = (datetime.datetime.now() - start).total_seconds() * 1000
    # print(f"Turn {data['turn']}: {move} in {duration_ms:.3}ms | GID={data['game']['id']}")
    return move.name.lower()

from typing import List, Dict
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

    def _options(self, move: Move, max_dist=4) -> float:
        # a mini floodfill that counts open nearby squares
        queue = [self.head.apply(move)]
        done = set()
        score = 0.0
        while len(queue) > 0:
            position = queue.pop()
            done.add(position)
            if position in self.board.hazards:
                score += 0.5
            else:
                score += 1.0
            for move in [Move.RIGHT, Move.LEFT, Move.DOWN, Move.UP]:
                neighbor = position.apply(move)
                nearby = self.me.dist(neighbor) <= max_dist
                blocked = any(neighbor in s.body for s in self.board.snakes)
                on_grid = 0 <= neighbor.x < self.width and 0 <= neighbor.y < self.height
                if nearby and neighbor not in done and neighbor not in queue and not blocked and on_grid:
                    queue.append(neighbor)
        return score

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
        return min(len(done), self.length + 1)

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

    def _chance_of_killing(self, move: Move) -> int:
        # calculate where we'll be after this move
        next_pos = self.me.apply(move)

        # a weak snake is one that is shorter than us and within 1 square of `next_pos`
        weak_snakes = filter(lambda s: s.dist(next_pos) <= 1 and self.length > s.length, self.other_snakes)

        # risk is the number of other snakes that could be at the next position after following `move`
        return sum(snake.could_move_to(next_pos) for snake in weak_snakes)

    def _risk_of_dying(self, move: Move) -> int:
        # TODO be aggressive if move takes us onto food
        # calculate where we'll be after this move
        next_pos = self.me.apply(move)

        # a dangerous snake is one that is longer than us and within 1 square of `next_pos`
        dangerous_snakes = filter(lambda s: s.dist(next_pos) <= 1 and self.length <= s.length, self.other_snakes)

        # risk is the number of other snakes that could be at the next position after following `move`
        return sum(snake.could_move_to(next_pos) for snake in dangerous_snakes)

    def _is_into_hazard(self, move: Move) -> bool:
        # TODO this will also not let us get food thats in hazard, while we are in hazard, IF there's a move that takes us out of the hazard
        next_pos = self.me.apply(move)
        return next_pos in self.board.hazards and (next_pos not in self.board.foods or 100 - self._dist_to_exit_hazard(move) * 16 <= self.me.health)

    def _safe_or_close(self, p: Position) -> bool:
        return p not in self.board.hazards or self.me.dist(p) * 16 < self.me.health

    def _can_reach(self, p: Position) -> bool:
        # TODO update this to check if we can get back out of hazard
        return self.me.dist(p) * 16 < self.me.health

    def _own(self, p: Position) -> bool:
        my_dist = p.dist(self.me)
        closest_snake = min(self.other_snakes, key=p.dist)
        closest_dist = p.dist(closest_snake)
        return my_dist < closest_dist or (my_dist == closest_dist and self.length >= closest_snake.length)

    def _dist_to_exit_hazard(self, move: Move) -> int:
        next_pos = self.me.apply(move)
        empty_non_hazards = [
            p for p in self.board.non_hazards
            if not any(p in s.body for s in self.board.snakes)
        ]
        return min((next_pos.dist(p) for p in empty_non_hazards), default=0)

    def _dist_to_larger_snake(self, move: Move) -> int:
        next_pos = self.me.apply(move)
        return min((next_pos.dist(s) for s in self.other_snakes if s.length >= self.length), default=0)

    def _dist_to_smaller_snake(self, move: Move) -> int:
        next_pos = self.me.apply(move)
        return min((next_pos.dist(s) for s in self.other_snakes if s.length < self.length), default=0)

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

        if self.head in self.board.hazards:
            # TODO rework this to exit asap. if we can't exit, then look for food to live until we can
            food_we_can_reach = list(filter(self._own, filter(self._can_reach, self.board.foods)))

            if len(food_we_can_reach) > 0:
                closest_food = min(food_we_can_reach, key=self.me.dist)
                move = min(self.possible_moves, key=lambda move: (
                    -self._floodfill(move),
                    self._risk_of_dying(move),
                    self.head.apply(move).dist(closest_food),
                    -self._chance_of_killing(move),
                    -self._options(move),
                    #-self._dist_to_larger_snake(move),
                    # self._dist_to_smaller_snake(move),
                ))
            else:
                move = min(self.possible_moves, key=lambda move: (
                    -self._floodfill(move),
                    self._risk_of_dying(move),
                    self._dist_to_exit_hazard(move),
                    -self._chance_of_killing(move),
                    -self._options(move),
                    #-self._dist_to_larger_snake(move),
                    # self._dist_to_smaller_snake(move),
                ))
        else:
            # TODO rework to only look for food if we are not the longest, or if our health is < 50
            # get a list of foods that belong to us (i.e. that we are the closest snake to)
            # and that is safe
            food_we_own = list(filter(self._own, filter(self._safe_or_close, self.board.foods)))

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
                    -self._floodfill(move),
                    self._risk_of_dying(move),
                    self._is_into_hazard(move),
                    self.head.apply(move).dist(closest_food),
                    -self._chance_of_killing(move),
                    -self._options(move),
                    -self._dist_to_larger_snake(move),
                    self._dist_to_smaller_snake(move),
                ))
            else:
                # choose move by lowest risk
                move = min(self.possible_moves, key=lambda move: (
                    -self._floodfill(move),
                    self._risk_of_dying(move),
                    self._is_into_hazard(move),
                    -self._chance_of_killing(move),
                    -self._options(move),
                    -self._dist_to_larger_snake(move),
                    self._dist_to_smaller_snake(move),
                ))
        return move


def choose_move(data: dict) -> str:
    #start = datetime.datetime.now()

    move = Strategy(data).choose()
    
    #duration_ms = (datetime.datetime.now() - start).total_seconds() * 1000
    # print(f"Turn {data['turn']}: {move} in {duration_ms:.3}ms | GID={data['game']['id']}")
    return move.name.lower()

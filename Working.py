# ORIGINAL

#def avoid_body(head: Dict[str, int], body: List[Dict[str, int]], possible_moves: List[str]):
#    x = head["x"]
#    y = head["y"]
#    for segment in body:
#        if x + 1 == segment["x"] and y == segment["y"]:
#            remove_possible_move("right", possible_moves)
#        elif x - 1 == segment["x"] and y == segment["y"]:
#            remove_possible_move("left", possible_moves)
#        elif x == segment["x"] and y + 1 == segment["y"]:
#            remove_possible_move("up", possible_moves)
#        elif x == segment["x"] and y - 1 == segment["y"]:
#            remove_possible_move("down", possible_moves)


#PROPOSED CHANGE 

#def avoid_body(head: Dict[str, int], body: List[Dict[str, int]], possible_moves: List[str]):
#    x = head["x"]
#    y = head["y"]

#    if body[:-1] != body[:-2]:
#	       body.pop

#    for segment in body:
#        if x + 1 == segment["x"] and y == segment["y"]:
#            remove_possible_move("right", possible_moves)
#        elif x - 1 == segment["x"] and y == segment["y"]:
#            remove_possible_move("left", possible_moves)
#        elif x == segment["x"] and y + 1 == segment["y"]:
#            remove_possible_move("up", possible_moves)
#        elif x == segment["x"] and y - 1 == segment["y"]:
#            remove_possible_move("down", possible_moves)


            #-floodfill(my_head, move, snakes),


#def floodfill(head, move, snakes) -> int:
#    x = head["x"]
#    y = head["y"]
#    queue = [apply_move(head, move)]
#    done = set()
#    while len(queue) > 0:
#        square = queue.pop()
#        done.add(square)
#        for move in ["left", "right", "up", "down"]:
#            neighbor = apply_move(square, move)
#            blocked = any(neighbor in s["body"] for s in snakes)
#            off_grid = 0 <= x < 11 and 0 <= y < 11
#            if neighbor not in done and neighbor not in queue and not blocked and not off_grid:
#                queue.append(neighbor)
#    return len(done)
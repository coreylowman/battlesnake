    # in_h = in_hazard(my_head, hazards)
    # print(in_h)
    # avoid hazards!
    # if len(hazards) > 0 and not in_h:
    #   avoid_hazards(my_head, hazards, possible_moves)

        # avoid possible collisions with any snake's head
        # avoid_head(my_head, my_length, snake["head"], snake["length"], possible_moves)


#def in_hazard(myHead, hazards: List[Dict[str, int]]) -> bool:
#    # returns whether or not this head is in a hazard location
#    x = myHead["x"]
#    y = myHead["y"]
#    if len(hazards) == 0: 
#        return False
#
#    for hazard in hazards:
#        if x == hazard["x"] and y == hazard["y"]:
#            return True
#        return False
    

#def avoid_hazards(head: Dict[str, int], hazards: List[Dict[str, int]], possible_moves: List[str]):
#    x = head["x"]
#    y = head["y"]
#    for segment in hazards:
#        if x + 1 == segment["x"] and y == segment["y"]:
#            remove_possible_move("right", possible_moves)
#        elif x - 1 == segment["x"] and y == segment["y"]:
#            remove_possible_move("left", possible_moves)
#        elif x == segment["x"] and y + 1 == segment["y"]:
#            remove_possible_move("up", possible_moves)
#        elif x == segment["x"] and y - 1 == segment["y"]:
#            remove_possible_move("down", possible_moves)


#def avoid_head(myhead: Dict[str, int], mylength , snakehead: Dict[str, int], snakelength, possible_moves: List[str]):
#    if mylength > snakelength:
#        return
#    myx = myhead["x"]
#    myy = myhead["y"]
#    snakex = myhead["x"]
#    snakey = myhead["y"]
#    if myx + 2 == snakex and myy == snakey:
#        remove_possible_move("right", possible_moves)
#    elif myx - 2 == snakex and myy == snakey:
#        remove_possible_move("left", possible_moves)
#    elif myx == snakex and myy + 2 == snakey:
#        remove_possible_move("up", possible_moves)
#    elif myx == snakex and myy - 2 == snakey:
#        remove_possible_move("down", possible_moves)



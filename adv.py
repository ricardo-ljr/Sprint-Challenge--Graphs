from room import Room
from player import Player
from world import World

import random
from ast import literal_eval
from maybe_useful import Queue

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

visited = {}  # loop dict until visited each node

go_backwards = []  # simply to keep track of players

# which way to go after each value
backwards_traversal_path = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}

curr_room = player.current_room.id  # where is player

visited[curr_room] = player.current_room.get_exits()  # get room index

# 1004 moves - MVP ok, time to try for a better approach

while len(visited) < len(room_graph):
    if player.current_room.id not in visited:
        visited[player.current_room.id] = player.current_room.get_exits()

        last_path = go_backwards[-1]
        visited[player.current_room.id].remove(last_path)

    if len(visited[player.current_room.id]) == 0:

        last_path = go_backwards[-1]
        go_backwards.pop()
        traversal_path.append(last_path)
        # move player to unvisited node
        player.travel(last_path)

    if len(visited[player.current_room.id]) > 0:

        # sequence aaaaand go...
        visits = visited[player.current_room.id][-1]
        # take out of visited
        visited[player.current_room.id].pop()
        # add to traversal
        traversal_path.append(visits)
        # add backwards
        go_backwards.append(backwards_traversal_path[visits])
        # move player to new room
        player.travel(visits)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")

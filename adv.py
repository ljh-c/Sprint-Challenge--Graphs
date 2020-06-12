from room import Room
from player import Player
from world import World
from util import Stack, opp_dir, bfs

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []
"""
Understand
----------
Traverse entire graph (undirected and unweighted with cycles; not disjoint)
Construct traversal graph for traversal_path, a list of moves
{
    0: {'n': 4, 's': '?', 'e': '?'}
}
This representation is an adjacency dict - { room: { direction: neighbor } }
Complete traversal is 500 entries and no '?'

Traverse entire subgraph, then backtrack (unless 500 entries)
Helper function to convert path to n/s/e/w directions

Tricolor algorithm
- White nodes are undiscovered (not in dict)
- Gray nodes are discovered but not explored (in dict, has '?')
- Black nodes are explored (in dict, no '?')
- White --> gray --> black
- There should be no edges from white nodes to black nodes

Color root node gray
While gray node x exists
    Color white successors of x gray
    If x has no successors left, paint it black

If a gray loop is visited, there is a cycle

When you add an adjacency, the mutual one can be added

Ideas:
DFT to traverse subgraph of a single node
BFS to find nearest unexplored node
To minimize backtracking, maximize distance from root (heuristic)
"Manhattan distance" is |cell_x - exit_x| + |cell_y - exit_y|
Store current root node being explored

Plan
----------
Visit root node and push onto stack
While stack is not empty or traversal_graph < 500 entries:
    Pop unexplored root node from stack
    DFT explore using heuristic, adding unexplored nodes to stack
    Backtrack to nearest gray node if dead end
"""
print('\n=================================================================\n')
player.current_room = world.starting_room # reset

s = Stack() # stores unexplored nodes as (origin, move)
traversal_graph = dict()
explored = set()

# seed stack
traversal_graph[player.current_room.id] = dict()

for direction in player.current_room.get_exits():
    traversal_graph[player.current_room.id][direction] = '?'
    s.push((player.current_room.id, direction))

curr_unexplored = None

while s.size() > 0:
    origin, move = s.pop()

    if player.current_room.id != origin:
        # need to backtrack
        print(f'{player.current_room.id} is not {origin}. Time to backtrack!')
        path = bfs(player.current_room.id, origin, traversal_graph)

        # turn path into directional moves
        for room in path[1:]:
            # swap directions and rooms
            swapped = {value: key for key, value in 
                traversal_graph[player.current_room.id].items()}

            player.travel(swapped[room], True)
            traversal_path.append(swapped[room])
    
    player.travel(move, False)
    traversal_path.append(move)

    if player.current_room.id not in traversal_graph:
        traversal_graph[player.current_room.id] = {
            direction: '?' for direction in player.current_room.get_exits()}

    if player.current_room.id not in explored:
        traversal_graph[origin][move] = player.current_room.id
        traversal_graph[player.current_room.id][opp_dir(move)] = origin

        # check if origin or current are now explored
        if '?' not in traversal_graph[origin].values():
            explored.add(origin)
        
        if '?' not in traversal_graph[player.current_room.id].values():
            explored.add(player.current_room.id)
        else:
            for direction, room in traversal_graph[player.current_room.id].items():
                if room == '?':
                    s.push((player.current_room.id, direction))

# print(f'final path: {traversal_path}')
# print(f'final dict: {traversal_graph}')
# print(f'stopped at: {player.current_room.id}')
print('\n=================================================================\n')

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")

from collections import deque

class Stack():
    def __init__(self):
        self.stack = []

    def push(self, value):
        self.stack.append(value)

    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None

    def size(self):
        return len(self.stack)

def opp_dir(direction):
    if direction == 'n':
        return 's'
    elif direction == 's':
        return 'n'
    elif direction == 'w':
        return 'e'
    elif direction == 'e':
        return 'w'
    else:
        print('===== An unexpected error has occurred with opp_dir(). =====')

def bfs(starting_vertex, destination_vertex, traversal_graph):
    """
    Return a list containing the shortest path from
    starting_vertex to destination_vertex in
    breath-first order.
    """
    # Create a queue and enqueue a PATH
    q = deque()
    q.append([starting_vertex])
    # Create a set to store visited vertices
    visited = set()
    # While the queue is not empty:
    while len(q) > 0:
        # Dequeue the first PATH
        curr = q.popleft()
        # Grab the last vertex from the PATH
        vertex = curr[-1]
        # If that vertex has not been visited:
        if vertex not in visited:
            # Check if it's the target
            if vertex == destination_vertex:
                # Return PATH
                return curr
            # Mark as visited
            visited.add(vertex)
            # Add a PATH to its neighbors to the back of the queue
            for _, neighbor in traversal_graph[vertex].items():
                if neighbor != '?':
                    # Copy path because different paths are added
                    path = curr.copy()
                    # Append neighbor - append returns None
                    path.append(neighbor)
                    q.append(path)
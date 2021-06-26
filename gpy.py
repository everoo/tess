def get_value(m, (x, y)):
    if 0 <= y < len(m) and 0 <= x < len(m[-1]):
        return m[y][x]

class Tree:
    def __init__(self, path, ticket):
        self.path = path
        self.ticket = ticket
        self.children = []

    def move(self, dir):
        return self.path[-1][0]+dir[0], self.path[-1][1]+dir[1]

    def addChild(self, nextPoint, hasTicket):
        # all_points.append(nextPoint)
        self.children.append(Tree(self.path+[nextPoint], hasTicket))

    def find_children(self, maze):
        for direction in (0, 1), (1, 0), (0, -1), (-1, 0):
            nextPoint = self.move(direction)
            if nextPoint == (len(maze[-1])-1, len(maze)-1):
                return self.path+[nextPoint]
            elif nextPoint not in self.path:
                value = get_value(maze, nextPoint)
                if value == 0:
                    self.addChild(nextPoint, self.ticket)
                elif value == 1 and self.ticket:
                    self.addChild(nextPoint, False)

def solution(m):
    queue = [Tree([(0, 0)], True)]
    while len(queue) > 0:
        if len(queue) > 400:
            new_queue = {}
            for t in queue:
                key = t.path[-1], t.ticket
                if key not in new_queue:
                    new_queue[key] = t
                elif len(t.path) < len(new_queue[key].path):
                    new_queue[key] = t
            queue = new_queue.values()
        path = queue[0].find_children(m)
        if path == None:
            queue += queue[0].children
            del queue[0]
        else:
            return path

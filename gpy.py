all_points = [(0, 0)]

class Tree:
    def __init__(self, path, ticket):
        self.path = path
        self.ticket = ticket
        self.children = []

    def move(self, dir):
        return self.path[-1][0]+dir[0], self.path[-1][1]+dir[1]

    def addChild(self, nextPoint, hasTicket):
        all_points.append(nextPoint)
        self.children.append(Tree(self.path+[nextPoint], hasTicket))

    def find_children(self, maze):
        wh = len(maze[-1])-1, len(maze)-1
        for direction in (0, 1), (1, 0), (0, -1), (-1, 0):
            nextPoint = self.move(direction)
            if nextPoint == wh:
                return self.path+[nextPoint]
            elif nextPoint not in self.path and nextPoint not in all_points:
                value = get_value(maze, nextPoint)
                if value == 0:
                    self.addChild(nextPoint, self.ticket)
                elif value == 1 and self.ticket:
                    self.addChild(nextPoint, False)

def get_value(m, (x, y)):
    if 0 <= y < len(m) and 0 <= x < len(m[0]):
        return m[y][x]

def solution(m):
    queue = [Tree([(0, 0)], True)]
    while len(queue) > 0:
        path = queue[0].find_children(m)
        if path == None:
            queue += queue[0].children
            del queue[0]
        else:
            return path

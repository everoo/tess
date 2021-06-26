class Tree:
    def __init__(self, maze, point, ticket):
        self.maze = maze
        self.ticket = ticket
        self.point = point
        self.children = []
        self.path = []

    def createChild(self, newPoint, hasTicket):
        child = Tree(self.maze, newPoint, hasTicket)
        child.path = self.path+[self.point]
        self.children.append(child)

    def move_self(self, dir):
        return self.point[0]+dir[0], self.point[1]+dir[1]

    def find_children(self):
        for direction in (0, 1), (1, 0), (0, -1), (-1, 0):
            nextPoint = self.move_self(direction)
            if nextPoint == (len(self.maze[-1])-1, len(self.maze)-1):
                return self.path+[self.point, nextPoint]
            elif nextPoint not in self.path:
                value = get_value(self.maze, nextPoint)
                if value == 0:
                    self.createChild(nextPoint, self.ticket)
                elif value == 1 and self.ticket:
                    self.createChild(nextPoint, False)

def get_value(m, (x, y)):
    if y < 0 or x < 0 or y >= len(m) or x >= len(m[0]):
        return '-'
    return m[y][x]

def solution(m):
    queue = [Tree(m, (0, 0), True)]
    path = None
    while len(queue) > 0 and path == None:
        path = queue[0].find_children()
        if path == None:
            queue += queue[0].children
            del queue[0]
    return path

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
            if nextPoint == (len(self.maze[0])-1, len(self.maze)-1):
                return self.path+[self.point, nextPoint]
            elif nextPoint not in self.path:
                value = get_value(self.maze, nextPoint)
                if value == 0:
                    self.createChild(nextPoint, self.ticket)
                elif value == 1 and self.ticket:
                    self.createChild(nextPoint, False)
        for child in self.children:
            n = child.find_children()
            if n != None: return n


def get_value(m, (x, y)):
    if y < 0 or x < 0 or y >= len(m) or x >= len(m[0]):
        return '-'
    return m[y][x]

def solve(m):
    for x in m:
        print(x)
    t = Tree(m, (0, 0), True)
    return t.find_children()


seven = [
    [0,1,1,0],
    [0,0,0,1],
    [1,1,0,0],
    [1,1,1,0]]

eleven = [
    [0,0,0,0,0,0],
    [1,1,1,1,1,0],
    [0,0,0,0,0,0],
    [0,1,1,1,1,1],
    [0,1,1,1,1,1],
    [0,0,0,0,0,0]]

deadends = [
    [0,0,0,0,0,1],
    [1,1,1,1,1,0],
    [1,0,1,0,0,0],
    [0,1,0,0,1,1],
    [0,1,0,1,1,1],
    [0,0,0,0,0,0]]

for m in [seven, eleven, deadends]:
    print(solve(m))

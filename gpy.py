def get_value(m, (x, y)):
    if 0 <= y < len(m) and 0 <= x < len(m[-1]):
        return m[y][x]

class Tree:
    def __init__(self, path, ticket):
        self.path = path
        self.ticket = ticket
        self.children = []

    def addChild(self, nextPoint, hasTicket):
        self.children.append(Tree(self.path+[nextPoint], hasTicket))

    def find_children(self, maze):
        #harder to read but faster than *||*
        #just hard checks to see if it's next to the end because it's always passable
        if (self.path[-1][0] == len(maze[-1])-2 and self.path[-1][1] == len(maze)-1) or (self.path[-1][1] == len(maze)-2 and self.path[-1][0] == len(maze[-1])-1):
            return self.path+[(len(maze[-1])-1, len(maze)-1)]
        for direction in (0, 1), (1, 0), (0, -1), (-1, 0):
            nextPoint = self.path[-1][0]+direction[0], self.path[-1][1]+direction[1]
            # *||*
            # if nextPoint == (len(maze[-1])-1, len(maze)-1):
            #     return self.path+[nextPoint]
            # elif ...
            if nextPoint not in self.path:
                value = get_value(maze, nextPoint)
                if value == 0:
                    self.addChild(nextPoint, self.ticket)
                elif value == 1 and self.ticket:
                    self.addChild(nextPoint, False)

def solution(m):
    queue = [Tree([(0, 0)], True)]
    area = len(m)*len(m[0])*2
    ## Reducing area significantly increases speed 
    ## this is currently the max to guarantee the correct answer 
    ## but my tests showed it working up until 100
    while len(queue) > 0:
        if len(queue) > area:
            ## reduces the queue down to the shortest path for each point
            ## keeps track of if it has broken a wall already
            new_queue = {}
            for t in queue:
                key = t.path[-1], t.ticket
                if key not in new_queue:
                    new_queue[key] = t
                elif len(t.path) <= len(new_queue[key].path):
                    new_queue[key] = t
            queue = new_queue.values()
        path = queue[0].find_children(m)
        if path == None:
            queue += queue[0].children
            del queue[0]
        else:
            return len(path)
    return 0

## For fuel injection perfection
def solution(n):
    n, count = int(n), 0
    while n != 1:
        count += 1
        b = bin(n)
        n = (n + (1, -1)[b[-2]=='0' or n == 3], n >> 1)[b[-1] == '0']
    return count

for n in range(1, 100)+[int('9'*309)]:
    print solution(n), bin(n)

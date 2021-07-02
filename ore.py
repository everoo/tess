from fractions import Fraction

def find_lcm(x, y):
    lcm = x*y
    while(y):
        x, y = y, x % y
    return lcm // x

def matrixMinor(m,i,j):
    return [row[:j] + row[j+1:] for row in (m[:i]+m[i+1:])]

def matrixDet(m):
    l = len(m)
    if l == 2:
        return m[0][0]*m[1][1]-m[0][1]*m[1][0]
    return sum([((-1)**c)*m[0][c]*matrixDet(matrixMinor(m,0,c)) for c in range(l)])

def solution(m):
    sums = [sum(s) for s in m]
    if sums.count(0)==1:
        return [1, 1]
    m = [[Fraction(n, sums[i]) if sums[i] else 0 for n in s] for i, s in enumerate(m)]
    q, r = [], []
    for k, state in enumerate(m):
        if sums[k]:
            for t in q, r: t.append([])
            for i, s in enumerate(state):
                (q[-1] if sums[i] else r[-1]).append(s)
    l = range(len(q))
    inverse = [[1-q[x][y] if x==y else -q[x][y] for y in l] for x in l]
    determinant = matrixDet(inverse)
    if l == [0, 1]:
        inverse = [inverse[1][1]/determinant, inverse[0][1]/-determinant]
    else:
        inverse = [((-1)**t) * matrixDet(matrixMinor(inverse,t,0))/determinant for t in l]
    finals = [sum(a*b for a, b in zip(inverse, y_col)) for y_col in zip(*r)]
    lcm = find_lcm(finals[0].denominator, finals[1].denominator)
    for i in range(2, len(finals)):
        lcm = find_lcm(lcm, finals[i].denominator)
    return [f.numerator*(lcm//f.denominator) for f in finals] + [lcm]

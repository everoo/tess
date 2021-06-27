from fractions import Fraction

def round_tracker(t):
    return [round(v, 5) for v in t]

def fractionize(t, denom):
    return [Fraction(f).limit_denominator(max_denominator=denom) for f in t]

def find_next(ore, tracker):
    oldTracker = tracker[:]
    for i, v in enumerate(tracker):
        s = sum(ore[i])
        if v > 0 and s > 0:
            tracker[i] = 0.0
            for k, vv in enumerate(ore[i]):
                tracker[k] += float(vv)/s*v
    if round_tracker(tracker) == round_tracker(oldTracker):
        return tracker
    else:
        return find_next(ore, tracker)

def multiply(m):
    d = 1
    for n in m:
        mm = sum(n)
        if mm > 0: d*=mm
    return d

def increase_fraction(m, fra):
    return fra[0]*m, fra[1]*m

def solution(m):
    t = find_next(m, [float(n)/sum(m[0]) for n in m[0]])
    fra = fractionize(t, multiply(m))
    ret = {i:(f.numerator,f.denominator) for i, f in enumerate(fra) if sum(m[i]) == 0}
    max_denom = max([n[1] for n in ret.values()])
    for k, v in ret.items():
        ret[k] = increase_fraction(max_denom/v[1], v)
    return [n[0] for n in ret.values()]+[ret.values()[0][1]]

import math

tenPi = math.pi * 10.
upper = int(round(100. * tenPi))
rr = [0.01 * r for r in range(upper)]
hh = range(len(rr))
assert len(rr) == len(hh)
for i in range(len(rr)):
    r = rr[i]
    h = 0.001 * hh[i]
    h += 1.
    pt = func.polar2square([r,h])
    print(pt)

    

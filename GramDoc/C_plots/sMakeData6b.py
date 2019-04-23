read("data6.py")
import math

# You probably don't have this module ...
from RStats import RStats
r = RStats()
m = r.polyModel(xx1, yy1, 3)
print(m)

maxX = max(xx1)
minX = min(xx1)
diffX = maxX - minX
incrX = diffX / 100.

xx2 = []
yy2 = []

for i in range(100):
    theX = minX + (i * incrX)
    theY = (m[0] * math.pow(theX,3)) + (m[1] * math.pow(theX,2)) + (m[2] * theX) + m[3]
    xx2.append(theX)
    yy2.append(theY)

theX = maxX
theY = (m[0] * math.pow(theX,3)) + (m[1] * math.pow(theX,2)) + (m[2] * theX) + m[3]
xx2.append(theX)
yy2.append(theY)

f=file('data6b.py', 'w')
f.write('xx2 = %s\n' % xx2)
f.write('yy2 = %s\n' % yy2)
f.close()



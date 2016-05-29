import random,math
from RStats import RStats

xx1 = []
for i in range(1,20):
    x = (i - 3) * 10.
    #x = math.sqrt(x)
    r = random.random() - 0.5
    r *= 10.
    x += r
    xx1.append(x)

yy1 = []
for i in range(1,20):
    y = 3 * i 
    r = random.random() - 0.5
    r *= 15.
    y += r
    yy1.append(y)

xx2 = []
for i in range(1,20):
    x = (i - 7) * 10.
    #x = math.sqrt(x)
    r = random.random() - 0.5
    r *= 30.
    x += r
    xx2.append(x)

yy2 = []
for i in range(1,20):
    y = i + 10
    r = random.random() - 0.5
    r *= 5.
    y += r
    yy2.append(y)

myR = RStats()
s1,m1 = myR.linearModel(xx1, yy1)
s2,m2 = myR.linearModel(xx2, yy2)


f = file('data3.py', 'w')
f.write("xx1 = %s\n" % xx1)
f.write('yy1 = %s\n' % yy1)
f.write('s1 = %f\n' % s1)
f.write('m1 = %f\n' % m1)
f.write("xx2 = %s\n" % xx2)
f.write('yy2 = %s\n' % yy2)
f.write('s2 = %f\n' % s2)
f.write('m2 = %f\n' % m2)
f.close()


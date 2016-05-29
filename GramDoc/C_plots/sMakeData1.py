import random,math
xx1 = []
for i in range(1,20):
    x = i * 10.
    x = math.sqrt(x)
    r = random.random() - 0.5
    r /= x
    x += r
    x -= 2.
    xx1.append(x)

yy1 = []
for i in range(1,20):
    y = i + 10
    r = random.random() - 0.5
    r *= 5
    y += r
    yy1.append(y)

f = file('data1.py', 'w')
f.write("xx1 = %s\n" % xx1)
f.write('yy1 = %s\n' % yy1)
f.close()


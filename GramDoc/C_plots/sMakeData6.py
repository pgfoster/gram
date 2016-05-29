a = 3.
b = -30.
c = 30.
d = 38.

if 1:
    xx1 = []
    yy1 = []
    for i in range(-20,111):
        x = i / 13.
        r1 = ((random.random() - 0.5) * 0.2)
        x += x * r1
        y = (a * x * x * x) + (b * x * x) + (c * x) + d
        r1 = ((random.random() - 0.5) * 0.5)
        y += y * r1
        print "%6.3f %6.3f" % (x, y)
        xx1.append(x)
        yy1.append(y)

    #print yy1

if 1:

    f = file('data6.py', 'w')
    f.write('xx1 = %s\n' % xx1)
    f.write('yy1 = %s\n' % yy1)
    f.close()


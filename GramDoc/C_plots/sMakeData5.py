
a = 5
b = 1./a

if 1:
    xx1 = []
    yy1 = []
    for i in range(31):
        x = i / 10.
        g = pf.gsl_ran_gamma_pdf(x, a, b)
        print("%6.3f %6.3f" % (x, g))
        xx1.append(x)
        yy1.append(g)

    #print yy1

if 1:
    rr = []
    for i in range(10000):
        r = func.gsl_ran_gamma(a, b)
        rr.append(r)

    n = Numbers(rr)
    n.binSize = 0.5
    n.histo()
    print(n.bins)

    binNames = []
    binVals = []
    for b in n.bins:
        bn = '%.1f' % b[0]
        binNames.append(bn)
        binVals.append(b[1])

f = file('data5.py', 'w')
f.write('xx1 = %s\n' % xx1)
f.write('yy1 = %s\n' % yy1)
f.write('binNames = %s\n' % binNames)
f.write('binVals = %s\n' % binVals)
f.close()


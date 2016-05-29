import random,math

nPts = 2000
mu = 1
sigma = 1
nv1 = []
for i in range(nPts):
    nv1.append(random.normalvariate(mu, sigma))

if 0:
    n1 = Numbers(nv1)
    n1.binSize = 1
    n1.histo(padMin=-3, padMax=15.)

mu = 8
sigma = 2
nv2 = []
for i in range(nPts):
    nv2.append(random.normalvariate(mu, sigma))

if 0:
    n2 = Numbers(nv2)
    n2.binSize = 1
    n2.histo(padMin=-3, padMax=15.)




if 1:
    f = file('data4.py', 'w')
    f.write("nv1 = %s\n" % nv1)
    f.write('nv2 = %s\n' % nv2)
    f.close()


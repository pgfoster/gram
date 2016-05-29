aa = range(1000)
for i in range(len(aa)):
    aa[i] /= 10.

xx = []
yy = []
for i in range(len(aa)):
    a = aa[i]
    ret = func.polar2square([a, 1.])
    xx.append(ret[0] + (i * 0.02))
    yy.append(ret[1] + (i * 0.01) * (i * i * 0.001))

from gram import Plot
gp = Plot()
gp.baseName = 'circle'
gp.line(xx, yy)

gp.xAxis.title = None
gp.yAxis.title = None
gp.maxYToShow = 10000

gp.png()
gp.svg()


import math

upper = int(round(25. * math.pi * 2.))
rr = [0.04 * r for r in range(upper)]
xxx = []
yyy = []
j = 0
for rev in range(8):
    xx = []
    yy = []
    for i in range(len(rr)):
        r = rr[i]
        h = 0.0005 * j
        h += 0.5
        j += 1
        pt = func.polar2square([r,h])
        xx.append(pt[0])
        yy.append(pt[1])
    xxx.append(xx)
    yyy.append(yy)
    
from gram import Plot
gp = Plot()
gp.baseName = 'spiral'
for rev in range(8):
    xx = xxx[rev]
    yy = yyy[rev]
    g = gp.line(xx,yy,smooth=True)
    g.lineStyle = gp.goodLineStyles[rev]
    print(g.lineStyle)
gp.contentSizeX = 4.5
gp.contentSizeY = gp.contentSizeX
gp.xAxis.title = None
gp.yAxis.title = None
gp.yAxis.styles.remove('ticks') 
gp.xAxis.styles.remove('ticks') 
gp.frameT = None
gp.frameB = None
gp.frameL = None
gp.frameR = None
gp.png()
gp.svg()


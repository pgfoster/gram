import math
from gram import Plot
gp = Plot()
gp.baseName = 'xyText'
# make an invisible plot
xx = range(17)
yy = [math.sin(x) for x in xx]
c = gp.line(xx, yy)
c.colour = 'green'
# make some text at x,y
for i in range(len(xx)):
    c = gp.xYText(xx[i],yy[i],'%i' % i)
    c.shape = 'circle'
    c.fill = 'red!10'
    c.rotate = i * 15
gp.contentSizeX = 5.
# remove the axes and frame
gp.yAxis.title = None 
gp.xAxis.title = None 
gp.yAxis.styles.remove('ticks') 
gp.xAxis.styles.remove('ticks')
gp.frameT = None 
gp.frameB = None 
gp.frameL = None 
gp.frameR = None 
gp.png() 
# gp.svg()  # yuk!

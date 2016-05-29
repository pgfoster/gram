import math
xx1 = [x/100. for x in range(-400, 401)]
yy1a = [math.sqrt(1. + (x * x)) for x in xx1]
yy1b = [-y for y in yy1a]

from gram import Plot
gp = Plot()
g = gp.line(xx1, yy1a)
g.colour = 'green'
g = gp.line(xx1, yy1b)
g.colour = 'green'

g = gp.line(yy1a, xx1)
g.colour = 'blue'
g = gp.line(yy1b, xx1)
g.color = 'blue'

g = gp.line([-4, 4], [-4, 4])
g.color = 'red'
g = gp.line([-4, 4], [4, -4])
g.colour = 'red'

myTextSize = 'tiny'
l1 = r'$y^2 + x^2 = 1$'
g = gp.xYText(-2, 2.5, l1)
g.anchor = 'west'
g.textSize = myTextSize

l1 = r'$x^2 - y^2 = 1$'
g = gp.xYText(1.5, 1., l1)
g.anchor = 'west'
g.textSize = myTextSize

howBig = 3.5
gp.contentSizeX = howBig
gp.contentSizeY = howBig
gp.xAxis.title = None
gp.yAxis.title = None
gp.yAxis.sig = '%.1f'
gp.baseName = 'hyperbolas'
gp.png()
#gp.svg()

gp.xAxis.sig = '%s'
gp.xAxis.ticks[0].text.rawText = '-4'
gp.xAxis.ticks[1].text.rawText = '-2.0'
gp.xAxis.ticks[2].text.rawText = '0.00'
gp.xAxis.ticks[3].text.rawText = '2.000'
gp.xAxis.ticks[4].text.rawText = '4.0000'
gp.yAxis.sig = '%s'
gp.yAxis.ticks[0].text.rawText = r'$\alpha$'
gp.yAxis.ticks[1].text.rawText = 'xyz'
gp.yAxis.ticks[1].text.textSize = 'LARGE'
gp.yAxis.ticks[1].text.color = 'gray'
gp.yAxis.ticks[2].text.rawText = ''
gp.yAxis.ticks[3].text.draw = True
gp.yAxis.ticks[4].text.anchor = 'west'
gp.yAxis.ticks[4].text.rotate = 180

gp.baseName = 'hyperbolas2'
gp.png()
#gp.svg()

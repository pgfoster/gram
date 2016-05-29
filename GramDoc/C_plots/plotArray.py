import random
from gram import Plot
plotmarks = ['o', 'square',
             'triangle', 'diamond']
gg = []
for i in [0,1]:
    for j in [0,1]:
        xx1 = []
        yy1 = []
        for k in range(23):
            xx1.append(random.random())
            yy1.append(random.random())

        gp = Plot()
        gp.contentSizeX = 2.5
        gp.contentSizeY = 2.
        thePlotMark = plotmarks[(2 * i) +j]
        c = gp.scatter(xx1, yy1,
                       plotMark=thePlotMark)
        gp.minXToShow = 0.0
        gp.minYToShow = 0.0
        gp.maxXToShow = 1.0
        gp.maxYToShow = 1.0
        theText = '[%i.%i]' % (i, j)
        c = gp.xYText(0.5, 0.5, theText)
        c.colour = 'blue'

        if i == 0:
            gp.xAxis.title = None
            gp.xAxis.styles.remove('ticks') 
        else:
            gp.xAxis.title = 'xx1'
        if j == 0:
            gp.yAxis.title = 'yy1'
        else:
            gp.yAxis.title = None
            gp.yAxis.styles.remove('ticks')
        gp.gX = j * 3.2
        gp.gY = i * -2.7
        gg.append(gp)

gr = gg[0]
gr.baseName = 'plotArray'
gr.grams += gg[1:]
#gr.png()
gr.svg()


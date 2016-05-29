from gram import Plot
xx1 = [2,4,7,3,9]
yy1 = [4,5,1,7,4]
gp = Plot()
gp.baseName = 'linesInPlot'
gp.scatter(xx1, yy1, plotMark='diamond')
gp.minXToShow = 0.0
g = gp.lineFromSlopeAndIntercept(1, 2)
g.lineThickness = 'thick'
gp.verticalLine(x=3, y=4)
c = gp.verticalLine(8)
c.colour = 'gray'
c.lineThickness = 'very thick'
gp.xAxis.title = None
gp.yAxis.title = None
gp.png()
gp.svg()

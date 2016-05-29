from gram import Plot
read("data6.py")
read("data6b.py")
gp = Plot()
gp.baseName = 'regression'
gp.scatter(xx1, yy1, plotMark='square')
g = gp.line(xx2, yy2, smooth=True)
g.lineThickness = 'thick'
gp.maxYToShow=100
gp.minXToShow=-2
gp.xAxis.title = None
gp.yAxis.title = None
gp.png()
gp.svg()


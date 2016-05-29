from gram import Plot
read("data3.py")
gp = Plot()
gp.baseName = 'scatterB'
g = gp.scatter(xx1, yy1)
g.color = 'blue'
gp.lineFromSlopeAndIntercept(s1, m1)
g = gp.scatter(xx2, yy2, plotMark='*')
g.color = "orange"
g.fill = 'blue!30'
g = gp.lineFromSlopeAndIntercept(s2, m2)
g.lineStyle = 'densely dotted'
g.lineThickness = 'very thick'
gp.xAxis.title = None
gp.yAxis.title = None
gp.minYToShow = 0.0
gp.maxYToShow = 60.
gp.png()
gp.svg()

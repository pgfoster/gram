from gram import Plot

xx1 = [2.3, 3.5, 7.]
yy1 = [3.3, 1.2, 5.6]

xx2 = [-19.3, -14.3, -10.5]
yy2 = [-2.6, -15.9, -9.3]

gp = Plot()
gp.baseName = 'plotArrayB'
gp.line(xx1, yy1, smooth=True)
gp.scatter(xx1, yy1)
gp.yAxis.title = 'widgets'
gp.xAxis.title = 'time (hours)'
gp.minXToShow = 0.0

gp2 = Plot()
gp2.line(xx2, yy2, smooth=False)
gp2.scatter(xx2, yy2)
gp2.yAxis.title = 'spin'
gp2.yAxis.position = 'r'
gp2.xAxis.title = 'impetus'
gp2.gX = 4.3
gp2.gY = 0.

gp.grams.append(gp2)
gp.png()
gp.svg()  # smooth line plots do not work in svg

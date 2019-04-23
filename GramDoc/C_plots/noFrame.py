from gram import Plot
read("data1.py")
gp = Plot()
gp.baseName = 'noFrame'
gp.line(xx1, yy1)
gp.yAxis.title = None
gp.xAxis.title = None
gp.yAxis.styles.remove('ticks')
gp.xAxis.styles.remove('ticks')
gp.frameT = None
gp.frameB = None
gp.frameL = None
gp.frameR = None
gp.font = 'helvetica'
gp.png()
gp.svg()

from gram import Plot
read("data1.py")
gp = Plot()
gp.svgPxForCm = 100
gp.baseName = 'scatter'
gp.scatter(xx1, yy1)
gp.yAxis.title = 'scratches'
gp.xAxis.title = 'itches'
gp.minXToShow = 0
gp.maxXToShow = 12
gp.minYToShow = 0.
gp.maxYToShow = 34
gp.png()
gp.svg()
   

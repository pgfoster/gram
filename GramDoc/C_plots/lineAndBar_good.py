from gram import Plot
read('data5.py')
gp = Plot()
gp.baseName = 'lineAndBar_good'
c = gp.bars(binNames,binVals)
gp.minBarValToShow = 0.0
gp.barNameAxis.title = None
gp.barValAxis.title = 'frequency'
c.barSets[0].fillColor = 'black!10'
gp.barNameAxis.barLabelsEvery = 2
#gp.barNameAxis.textRotate = 90
gp.line(xx1, yy1, smooth=True)
gp.xAxis.position = 't'
gp.yAxis.position = 'r'
gp.xAxis.title = None
gp.yAxis.title = 'density'
gp.maxXToShow = 4.0
gp.xAxis.tickLabelsEvery = 1
gp.maxBarValToShow = 5000
gp.maxYToShow = 1.0
gp.png()
gp.svg()

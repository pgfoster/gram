from gram import Plot
read("data2.py")
gp = Plot()
gp.baseName = 'barB'
gp.font = 'helvetica'
c = gp.bars(xx1, yy1)
# c.barSets[0].fillColor = 'violet!20'
gp.barValAxis.title = 'gnat infestations'
gp.barNameAxis.title = None
#gp.barValAxis.position = 'r'
#gp.barNameAxis.position = 't'
gp.minBarValToShow = 0.
gp.maxBarValToShow = 80.
gp.barNameAxis.textRotate = 44
# gp.png()
gp.png()
gp.svg()

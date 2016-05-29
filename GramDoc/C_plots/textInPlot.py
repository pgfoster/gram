from gram import Plot
xx1 = [2,4,7,3,9]
yy1 = [4,5,1,7,4]
gp = Plot()
gp.contentSizeX = 2
gp.contentSizeY = 1.5
gp.baseName = 'textInPlot'
gp.scatter(xx1, yy1, plotMark='asterisk')
c = gp.xYText(7, 1.2, r'$\Downarrow$')
c.anchor = 'south'
c = gp.xYText(3.3, 7,
      r'$\leftarrow$\ Ignore this point')
c.textSize = 'tiny'
c.anchor = 'west'
gp.xAxis.title = None
gp.yAxis.title = None
gp.png()
# gp.svg()  # looks bad, the latex text is not rendered

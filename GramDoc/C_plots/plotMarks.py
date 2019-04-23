from gram import Plot

markerShapes = ['+', 'x', '*', '-', '|', 'o', 'asterisk',
                'square', 'square*', 'triangle',
                'triangle*', 'diamond', 'diamond*']

gp = Plot()
gp.baseName = 'plotMarks'
for mShNum in range(len(markerShapes)):
    xx = [5]
    yy = [len(markerShapes) - mShNum]
    myMarker = markerShapes[mShNum]
    gp.scatter(xx, yy, plotMark=myMarker)
    g = gp.xYText(0, yy[0], myMarker)
    g.textFamily = 'ttfamily'
    g.anchor = 'west'

    xx = [6]
    g = gp.scatter(xx, yy, plotMark=myMarker)
    g.color = 'red'

    xx = [7]
    g = gp.scatter(xx, yy, plotMark=myMarker)
    g.fill = 'red'

    xx = [8]
    g = gp.scatter(xx, yy, plotMark=myMarker)
    g.color = 'blue'
    g.fill = 'yellow'

gp.line([4.5,8.5], [14, 14])

colorY = 16
gp.xYText(3, colorY, "color")
gp.xYText(5, colorY, "-")
gp.xYText(6, colorY, "+")
gp.xYText(7, colorY, "-")
gp.xYText(8, colorY, "+")

fillY = 15
gp.xYText(3, fillY, "fill")
gp.xYText(5, fillY, "-")
gp.xYText(6, fillY, "-")
gp.xYText(7, fillY, "+")
gp.xYText(8, fillY, "+")



gp.yAxis.title = None
gp.xAxis.title = None
gp.yAxis.styles.remove('ticks')
gp.xAxis.styles.remove('ticks')
gp.frameT = None
gp.frameB = None
gp.frameL = None
gp.frameR = None
gp.contentSizeX = 4.0
gp.contentSizeY = 7.0
gp.minXToShow = 0
gp.maxYToShow = 16

gp.pdf()
gp.font = 'helvetica'
gp.svg()

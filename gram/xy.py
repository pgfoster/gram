from gram.gram import *
from gram.plot import Plot
from gram.axis import XYAxis


class XYPoint(object):

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.xPosn = None
        self.yPosn = None

    def getString(self):
        try:
            return "(%.3f,%.3f)" % (self.xPosn, self.yPosn)
        except:
            gm = ['XYPoint.getString()']
            gm.append('Bad point?  x %s, y %s, xPosn %s, yPosn %s' %
                      (self.x, self.y, self.xPosn, self.yPosn))
            raise GramError(gm)


class PlotXYContent(GramGraphic):
    # Use this list, as it is slighly rearranged from self.goodDotStyles.
    #_dots = ['*', '+', 'o', 'x', 'asterisk', 'diamond*', 'diamond',
    #                  'oplus', 'otimes',
    #                  'square*', 'square', 'triangle*', 'triangle', 'pentagon*', 'pentagon', '|']
    #_dotIndex = 0
    #_plotMarks = ['+', 'x', '*']
    #_plotMarkIndex = 0

    def __init__(self, plot, xx, yy):
        GramGraphic.__init__(self)
        gm = ['PlotXYContent.__init__()']

        self.plot = plot

        if not xx or not yy:
            gm.append("No numbers?")
            raise GramError(gm)
        if not isinstance(xx, list):
            gm.append("arg xx should be a list")
            raise GramError(gm)
        if not isinstance(yy, list):
            gm.append("arg yy should be a list")
            raise GramError(gm)
        if len(xx) != len(yy):
            gm.append("The lengths of xx and yy should be the same.")
            raise GramError(gm)

        # Find the min and max in the input data
        if plot.minXInData is None:
            # This is the first content, and so it has never been set before
            plot._minXInData = min(xx)
            plot._maxXInData = max(xx)
            plot._minYInData = min(yy)
            plot._maxYInData = max(yy)
        else:
            m = min(xx)
            if m < plot.minXInData:
                plot._minXInData = m
            m = max(xx)
            if m > plot.maxXInData:
                plot._maxXInData = m

            m = min(yy)
            if m < plot.minYInData:
                plot._minYInData = m
            m = max(yy)
            if m > plot.maxYInData:
                plot._maxYInData = m

        # print "PlotXYContent.  minXInData=%s, maxXInData=%s, minYInData=%s maxYInData=%s" % (
        #    plot.minXInData, plot.maxXInData, plot.minYInData, plot.maxYInData)
        # sys.exit()

        plot.minXToShow = plot.minXInData
        plot.maxXToShow = plot.maxXInData
        plot.minYToShow = plot.minYInData
        plot.maxYToShow = plot.maxYInData

        # Make the x-y points
        self.xYPoints = []
        for i in range(len(xx)):
            self.xYPoints.append(XYPoint(xx[i], yy[i]))

        if not plot.xAxis:
            plot.xAxis = XYAxis('b', plot)
            plot.xAxis.styles.append('ticks')
            plot.xAxis.styles.append('labels')
            plot.xAxis.title = 'gp.xAxis.title'

            plot.yAxis = XYAxis('l', plot)
            plot.yAxis.styles.append('ticks')
            plot.yAxis.styles.append('labels')
            plot.yAxis.title = 'gp.yAxis.title'

        #self.xPosn = self.contentPosnX
        #self.yPosn = self.contentPosnY

    def setPositions(self):
        xOrig = self.plot.minXToShow
        yOrig = self.plot.minYToShow
        assert xOrig is not None
        assert yOrig is not None

        assert self.plot.xYScaleX
        assert self.plot.xYScaleY
        for xyp in self.xYPoints:
            xyp.xPosn = self.plot.contentPosnX + \
                ((xyp.x - xOrig) * self.plot.xYScaleX)
            xyp.yPosn = self.plot.contentPosnY + \
                ((xyp.y - yOrig) * self.plot.xYScaleY)


class PlotLine(PlotXYContent):

    def __init__(self, plot, xx, yy, smooth=False):
        PlotXYContent.__init__(self, plot, xx, yy)
        self.smooth = smooth
        gm = ['PlotLine.__init__()']

        if 0:
            # Make sure that x-values increase
            if len(xx) > 1:
                i = 1
                while i < len(xx):
                    if xx[i - 1] >= xx[i]:
                        gm.append("x data is not always increasing")
                        gm.append("eg pos %i %s, pos %i %s" %
                                  ((i - 1), xx[i - 1], i, xx[i]))
                        raise GramError(gm)
                    i += 1

    def getTikz(self):
        #ss = [PlotXYContent.getTricks(self)]
        ss = []

        ss.append("\n% line plot")
        pList = [r'\draw ']

        if self.smooth:
            stuff = ['smooth']
        else:
            stuff = []
        options = self.getTikzOptions()
        if options:
            stuff += options
        if stuff:
            pList.append('[%s] ' % ','.join(stuff))

        pList.append("plot coordinates {")

        pList.append(' '.join([xyp.getString() for xyp in self.xYPoints]))
        pList.append('};')
        pLine = ''.join(pList)
        ss.append(pLine)
        return '\n'.join(ss)

    def getSvg(self):
        ss = []
        ss.append("\n<!-- line plot -->")
        ss.append('\n<polyline points="')
        ss.append(' '.join(["%.2f,%.2f" % (xyp.xPosn * self.svgPxForCm, 
                -xyp.yPosn * self.svgPxForCm) for xyp in self.xYPoints]))
        ss.append('"')
        options = self.getSvgOptions()
        #if options:
        #    print options
        #    sys.exit()
        #else:
        #ss.append('stroke="black" fill="none"')
        ss += options
        ss.append('/>')
        return ' '.join(ss)



class PlotLineFromSlopeAndIntercept(GramLine):

    def __init__(self, plot, slope, intercept):
        cA = GramCoord()
        cB = GramCoord()
        GramLine.__init__(self, cA, cB)
        self.plot = plot
        self.slope = slope
        self.intercept = intercept

    def setPositions(self):
        gm = ["PlotLineFromSlopeAndIntercept.setPositions()"]
        assert self.plot.minXToShow is not None
        assert self.plot.maxXToShow is not None
        assert self.plot.minYToShow is not None
        assert self.plot.maxYToShow is not None
        yAtXMin = (self.slope * self.plot.minXToShow) + self.intercept
        yAtXMax = (self.slope * self.plot.maxXToShow) + self.intercept
        if self.slope == 0.0:
            xAtYMax = self.intercept
            xAtYMin = self.intercept
        else:
            xAtYMax = (self.plot.maxYToShow - self.intercept) / self.slope
            xAtYMin = (self.plot.minYToShow - self.intercept) / self.slope

        if self.slope == 0.0:
            if yAtXMin >= self.plot.minYToShow and yAtXMin <= self.plot.maxYToShow:
                xA = self.plot.minXToShow
                yA = yAtXMin
            else:
                gm.append("Line off range. I.")
                gm.append(
                    "The line (slope=%f) is not between minYToShow and maxYToShow" % self.slope)
                raise GramError(gm)
            if yAtXMax >= self.plot.minYToShow and yAtXMin <= self.plot.maxYToShow:
                xB = self.plot.maxXToShow
                yB = yAtXMax
            else:
                gm.append("Line off range. II.")
                gm.append(
                    "The line (slope=%f) is not between minYToShow and maxYToShow" % self.slope)
                gm.append(
                    "How did this happen?!? -- programming error, fix me.")
                raise GramError(gm)
        elif self.slope > 0.0:
            # Does the line intercept the y-axis?
            if yAtXMin >= self.plot.minYToShow and yAtXMin <= self.plot.maxYToShow:
                xA = self.plot.minXToShow
                yA = yAtXMin
            # ...or does it intercept below?
            elif yAtXMin < self.plot.minYToShow:
                # Does the line intercept the x-axis?
                if xAtYMin >= self.plot.minXToShow and xAtYMin <= self.plot.maxXToShow:
                    xA = xAtYMin
                    yA = self.plot.minYToShow
                else:
                    gm.append("Line off range. 3.")
                    raise GramError(gm)
            else:
                gm.append("Line off range. 4.   Too high")
                raise GramError(gm)

            # Does the line intercept the right frame?
            if yAtXMax >= self.plot.minYToShow and yAtXMax <= self.plot.maxYToShow:
                xB = self.plot.maxXToShow
                yB = yAtXMax
            # ...or does it intercept the top frame?
            elif yAtXMax > self.plot.maxYToShow:
                if xAtYMax >= self.plot.minXToShow and xAtYMax <= self.plot.maxXToShow:
                    xB = xAtYMax
                    yB = self.plot.maxYToShow
                else:
                    gm.append("a This should not happen")
                    raise GramError(gm)
            else:
                gm.append("b This should not happen")
                raise GramError(gm)

        elif self.slope < 0.0:
            # Does the line intercept the y-axis?
            if yAtXMin >= self.plot.minYToShow and yAtXMin <= self.plot.maxYToShow:
                xA = self.plot.minXToShow
                yA = yAtXMin
            # ...or does it intercept above?
            elif yAtXMin > self.plot.maxYToShow:
                # Does the line intercept the top frame?
                if xAtYMax >= self.plot.minXToShow and xAtYMax <= self.plot.maxXToShow:
                    xA = xAtYMax
                    yA = self.plot.maxYToShow
                else:
                    gm.append("Line off range. 5.")
                    raise GramError(gm)
            else:
                gm.append("Line off range. 6.   Too low")
                raise GramError(gm)

            # Does the line intercept the right frame?
            if yAtXMax >= self.plot.minYToShow and yAtXMax <= self.plot.maxYToShow:
                xB = self.plot.maxXToShow
                yB = yAtXMax
            # ...or does it intercept the x-axis?
            elif yAtXMax < self.plot.minYToShow:
                if xAtYMin >= self.plot.minXToShow and xAtYMin <= self.plot.maxXToShow:
                    xB = xAtYMin
                    yB = self.plot.minYToShow
                else:
                    gm.append("a This should not happen")
                    raise GramError(gm)
            else:
                gm.append("b This should not happen")
                raise GramError(gm)

        # print "self.xYScaleX =%s, self.xYScaleY=%s" % (self.xYScaleX, self.xYScaleY)
        # sys.exit()

        self.cA.xPosn = self.plot.contentPosnX + \
            ((xA - self.plot.minXToShow) * self.plot.xYScaleX)
        self.cA.yPosn = self.plot.contentPosnY + \
            ((yA - self.plot.minYToShow) * self.plot.xYScaleY)
        self.cB.xPosn = self.plot.contentPosnX + \
            ((xB - self.plot.minXToShow) * self.plot.xYScaleX)
        self.cB.yPosn = self.plot.contentPosnY + \
            ((yB - self.plot.minYToShow) * self.plot.xYScaleY)

    def getTikz(self):
        ss = []
        ss.append("\n% line from slope and intercept in plot")
        ss.append(GramLine.getTikz(self))
        return '\n'.join(ss)


class PlotVerticalLine(GramLine):

    def __init__(self, plot, x, y=None):
        cA = GramCoord()
        cB = GramCoord()
        GramLine.__init__(self, cA, cB)
        self.plot = plot
        self.x = x
        self.y = y

    def setPositions(self):
        gm = ["PlotVerticalLine.setPositions()"]
        assert self.plot.minXToShow is not None
        assert self.plot.maxXToShow is not None
        assert self.plot.minYToShow is not None
        assert self.plot.maxYToShow is not None

        self.cA.xPosn = self.plot.contentPosnX + \
            ((self.x - self.plot.minXToShow) * self.plot.xYScaleX)
        self.cA.yPosn = self.plot.contentPosnY
        self.cB.xPosn = self.cA.xPosn
        if self.y is not None:
            self.cB.yPosn = self.plot.contentPosnY + \
                ((self.y - self.plot.minYToShow) * self.plot.xYScaleY)
        else:
            self.cB.yPosn = self.plot.contentPosnY + \
                ((self.plot.maxYToShow - self.plot.minYToShow)
                 * self.plot.xYScaleY)

    def getTikz(self):
        ss = []
        ss.append("\n% vertical line in plot")
        ss.append(GramLine.getTikz(self))
        return '\n'.join(ss)

class PlotHorizontalBracket(GramLine):

    def __init__(self, plot, xA, xB, y, theText):
        cA = GramCoord()
        cB = GramCoord()

        GramLine.__init__(self, cA, cB)
        self.plot = plot
        assert xB > xA
        self.xA = xA
        self.xB = xB
        self.y = y
        self.text = GramText(theText)
        self.text.cA = GramCoord()


    def setPositions(self):
        gm = ["PlotHorizontalBracket.setPositions()"]
        assert self.plot.minXToShow is not None
        assert self.plot.maxXToShow is not None
        assert self.plot.minYToShow is not None
        assert self.plot.maxYToShow is not None

        self.cA.xPosn = self.plot.contentPosnX + \
            ((self.xA - self.plot.minXToShow) * self.plot.xYScaleX)
        self.cA.yPosn = self.plot.contentPosnY + \
            ((self.y - self.plot.minYToShow) * self.plot.xYScaleY)
        self.cB.xPosn = self.plot.contentPosnX + \
            ((self.xB - self.plot.minXToShow) * self.plot.xYScaleX)
        self.cB.yPosn = self.cA.yPosn

        self.text.cA.xPosn = self.cA.xPosn + ((self.cB.xPosn - self.cA.xPosn) / 2.)
        self.text.cA.yPosn = self.cA.yPosn
        self.text.style = 'tickLabel'
        self.text.anchor = 'south'
        


    def getTikz(self):
        ss = []
        ss.append("\n% horizontal bracket in plot")
        ss.append(GramLine.getTikz(self))
        ss.append(GramText.getTikz(self.text))
        return '\n'.join(ss)


class PlotScatter(PlotXYContent):
    _plotMarksA = ['+', 'x', '*']
    _plotMarksB = ['-', '|', 'o', 'asterisk', # 'star', 'oplus', 'oplus*',
                   #'otimes', 'otimes*', 
                   'square', 'square*', 'triangle',
                   'triangle*', 'diamond', 'diamond*'] #, 'pentagon', 'pentagon*']
    _plotMarkIndex = 0

    def __init__(self, plot, xx, yy, plotMark='next'):
        PlotXYContent.__init__(self, plot, xx, yy)
        gm = ['PlotScatter.__init__()']

        # Choose a plotMark
        self.plotMark = None
        if plotMark == 'next':
            self.plotMark = self.plotMarksA[self.plotMarkIndex]
        elif plotMark in self.plotMarksA:
            self.plotMark = plotMark
        elif plotMark in self.plotMarksB:
            self.plotMark = plotMark
            # need to \usetikzlibrary{plotmarks}
            self.useTikzPlotMarkLib = True
        else:
            gm.append("arg plotMark specified as '%s'" % plotMark)
            gm.append("Should be one of %s" % self.plotMarksA)
            gm.append(
                "or 'next' (to choose the next plotMark from those three)")
            gm.append("or, for special occasions, one of %s" % self.plotMarksB)
            #gm.append("or None")
            raise GramError(gm)
        assert self.plotMark
        
        # GramMarker
        self.marker = GramSvgMarker(self.plotMark)

    def _getPlotMarksA(self):
        return PlotScatter._plotMarksA
    plotMarksA = property(_getPlotMarksA)

    def _getPlotMarksB(self):
        return PlotScatter._plotMarksB
    plotMarksB = property(_getPlotMarksB)

    def _getPlotMarkIndex(self):
        thePlotMarkIndex = PlotScatter._plotMarkIndex
        PlotScatter._plotMarkIndex += 1
        if PlotScatter._plotMarkIndex >= len(PlotScatter._plotMarksA):
            PlotScatter._plotMarkIndex = 0
        return thePlotMarkIndex

    plotMarkIndex = property(_getPlotMarkIndex)

    def setPositions(self):
        PlotXYContent.setPositions(self)
        if self.engine == 'svg':
            #print "xyxyxyxyxy self.getColor returns %s" % self.getColor()
            #print "xyxyxyxyxy self.getFill returns %s" % self.getFill()
            self.marker._color = self.getColor()
            self.marker._fill = self.getFill()
            #self.marker.resetMarkerId()

    def getTikz(self):
        #ss = [PlotXYContent.getTricks(self)]
        ss = []

        ss.append("\n% PlotScatter.getTikz()")
        pList = [r'\draw ']

        stuff = ['only marks', 'mark=%s' % self.plotMark]
        options = self.getTikzOptions()
        if not options and self.marker:
            options = self.marker.getTikzOptions()
        if options:
            stuff += options
        if self.plotMark == '*':
            stuff.append('mark size=2')
        pList.append('[%s] ' % ','.join(stuff))

        pList.append("plot coordinates {")

        pList.append(' '.join([xyp.getString() for xyp in self.xYPoints]))
        pList.append('};')
        pLine = ''.join(pList)
        ss.append(pLine)
        return '\n'.join(ss)

    def getSvg(self):
        ss = []
        ss.append("\n<!-- PlotScatter.getSvg() -->")
        ss.append('\n<polyline points="')
        ss.append(' '.join(["%.2f,%.2f" % (xyp.xPosn * self.svgPxForCm, 
                -xyp.yPosn * self.svgPxForCm) for xyp in self.xYPoints]))
        ss.append('"')
        ss.append('stroke="none" fill="none"')
        ss.append('marker-start="url(#%s)"' % self.marker.markerId)
        ss.append('marker-mid="url(#%s)"' % self.marker.markerId)
        ss.append('marker-end="url(#%s)"' % self.marker.markerId)
        ss.append('/>')
        return ' '.join(ss)


class PlotXYText(GramText):

    def __init__(self, plot, x, y, theText):
        GramText.__init__(self, theText)
        self.cA = GramCoord()
        self.plot = plot
        self.x = x
        self.y = y

    def setPositions(self):
        xOrig = self.plot.minXToShow
        yOrig = self.plot.minYToShow
        assert xOrig is not None
        assert yOrig is not None
        # if xOrig is None:
        #    xOrig = 0.0
        # if yOrig is None:
        #    yOrig = 0.0

        #assert self.xYScaleX
        #assert self.xYScaleY
        theXYScaleX = self.plot.xYScaleX
        theXYScaleY = self.plot.xYScaleY
        # if theXYScaleX is None:
        #    theXYScaleX = 1.
        # if theXYScaleY is None:
        #    theXYScaleY = 1.
        assert theXYScaleX
        assert theXYScaleY

        self.cA.xPosn = self.plot.contentPosnX + \
            ((self.x - xOrig) * theXYScaleX)
        self.cA.yPosn = self.plot.contentPosnY + \
            ((self.y - yOrig) * theXYScaleY)

    def getTikz(self):
        ss = []
        ss.append("\n% xy text in plot")
        ss.append(GramText.getTikz(self))
        return '\n'.join(ss)

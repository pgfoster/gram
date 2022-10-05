from gram.plot import Plot
from gram.gram import GramGraphic, GramText, GramCoord, GramRect, GramError, GramColor, GramLine
from gram.axis import XYAxis, BarsAxis
import math
import sys


class PlotBarSets(GramGraphic):
    _fillColorIndex = 0

    def __init__(self, plot, barNames, barVals):

        GramGraphic.__init__(self)
        gm = ['PlotBarSets.__init__()']
        gm.append("The first arg should be a list of bar names (as strings).")
        gm.append("Then you need to provide a list, ")
        gm.append("arg 'barVals', which should be a list of floats,")
        gm.append("or a list of lists of floats, all the same length.")
        gm.append("It should be the same length as the barNames list.")

        if not barNames:
            gm.append("****  No barNames?")
            raise GramError(gm)
        lType = type([])
        if type(barNames) != lType:
            raise GramError(gm)
        else:
            firstOne = barNames[0]
            if not isinstance(firstOne, str):
                gm.append(
                    "***** First barName (%s) is not a string." % firstOne)
                raise GramError(gm)

        if not barVals:
            gm.append("****  No barVals?")
            raise GramError(gm)
        lType = type([])
        if type(barVals) != lType:
            raise GramError(gm)
        else:
            firstOne = barVals[0]
            try:
                fOne = float(firstOne)
                barVals = [barVals]
            except:
                if type(firstOne) != lType:
                    raise GramError(gm)

        # So now barVals is a list of lists.  Confirm
        for innerList in barVals:
            if type(innerList) != lType:
                raise GramError(gm)
            for n in innerList:
                try:
                    fl = float(n)
                except:
                    gm.append("**** Bad float '%s'" % n)
                    raise GramError(gm)
        lenOfFirstInnerList = len(barVals[0])
        if not lenOfFirstInnerList:
            raise GramError(gm)
        for innerList in barVals:
            if len(innerList) != lenOfFirstInnerList:
                raise GramError(gm)
        if not barNames:
            raise GramError(gm)
        if len(barNames) != lenOfFirstInnerList:
            gm.append("len of barNames is %i" % len(barNames))
            gm.append("len of first inner list is %i" % lenOfFirstInnerList)
            raise GramError(gm)

        gm = ['PlotBarSets.__init__()']

        self.barVals = barVals
        self.barSets = []
        self.plot = plot

        self.plot.nBars = len(barNames)
        # for bNum in range(self.nBars):
        #    lab = GramText(barNames[bNum])
        #    self.barNames.append(lab)
        self.barNames = barNames

        theMin = min(self.barVals[0])
        theMax = max(self.barVals[0])
        for nL in self.barVals:
            m = min(nL)
            if m < theMin:
                theMin = m
            m = max(nL)
            if m > theMax:
                theMax = m

        if self.plot.minBarValInData is None:
            self.plot._minBarValInData = theMin
        elif theMin < self.plot.minBarValInData:
            self.plot._minBarValInData = theMin
        if self.plot.maxBarValInData is None:
            self.plot._maxBarValInData = theMax
        elif theMax > self.plot.maxBarValInData:
            self.plot._maxBarValInData = theMax

        self.plot.minBarValToShow = self.plot.minBarValInData
        self.plot.maxBarValToShow = self.plot.maxBarValInData

        for i in range(len(self.barVals)):
            nL = self.barVals[i]
            b = PlotBarSet(nL, self, self.plot, i, self.plot.goodBarFills[self.fillColorIndex])
            self.barSets.append(b)

        self.plot.barNameAxis = BarsAxis('b', self.plot)
        self.plot.barNameAxis.styles.append('ticks')
        self.plot.barNameAxis.styles.append('labels')
        self.plot.barNameAxis.title = 'gp.barNameAxis.title'

        self.plot.barValAxis = XYAxis('l', self.plot, useBarVals=True)
        self.plot.barValAxis.styles.append('ticks')
        self.plot.barValAxis.styles.append('labels')
        self.plot.barValAxis.title = 'gp.barValAxis.title'

        self.tickWidth = None
        self.oneBarWidth = None

    def _getFillColorIndex(self):
        theFillColorIndex = PlotBarSets._fillColorIndex
        PlotBarSets._fillColorIndex += 1
        if PlotBarSets._fillColorIndex >= len(self.plot.goodBarFills):
            PlotBarSets._fillColorIndex = 0
        return theFillColorIndex

    fillColorIndex = property(_getFillColorIndex)

    def setPositions(self):

        self.tickWidth = float(self.plot.contentSizeX) / self.plot.nBars
        availableWidth = self.tickWidth - \
            (2 * self.plot.halfSpaceBetweenBarGroups * self.tickWidth)
        self.oneBarWidth = float(availableWidth) / len(self.barSets)

        for bs in self.barSets:
            bs.setPositions()

    def getTikz(self):
        ss = []
        for bs in self.barSets:
            ss.append(bs.getTikz())
        return '\n'.join(ss)

    def getSvg(self):
        ss = []
        for bs in self.barSets:
            ss.append(bs.getSvg())
        return '\n'.join(ss)


class PlotBarSet(GramGraphic):

    def __init__(self, barVals, barSetsObject, plot, barSetNum, fillColor):
        GramGraphic.__init__(self)
        gm = ['PlotBarSet.__init__()']
        # self.barVals = barVals # a list of floats.
        self.plot = plot
        self.barSetNum = barSetNum
        self.barSetsObject = barSetsObject
        assert isinstance(fillColor, str)
        self.fillColor = fillColor
        self.drawColor = 'black'
        self.bars = []

        for binNum in range(self.plot.nBars):
            b = PlotBar(self.plot, barVals[binNum], binNum, self.barSetNum, self)
            self.bars.append(b)
            # self.graphics.append(b)

    def setPositions(self):
        for b in self.bars:
            b.setPositions()
            if self.fillColor:
                b.rect.fill = self.fillColor
            b.rect.draw = self.drawColor

    def getTikz(self):
        ss = ["\n%% BarSet %i, fillColor %s" %
              (self.barSetNum, self.fillColor)]
        for b in self.bars:
            ss.append(b.getTikz())
        return '\n'.join(ss)

    def getSvg(self):
        ss = ["\n<!-- BarSet %i, fillColor %s -->" %
              (self.barSetNum, self.fillColor)]
        for b in self.bars:
            ss.append(b.getSvg())
        return '\n'.join(ss)


class PlotBar(GramGraphic):
    def __init__(self, plot, val, barNum, barSetNum, barSetObject):
        GramGraphic.__init__(self)
        self.plot = plot
        self.val = val
        self.barNum = barNum
        self.barSetNum = barSetNum
        self.barSetObject = barSetObject
        self.barSetsObject = self.barSetObject.barSetsObject
        self.cA = GramCoord()
        self.cB = GramCoord()
        self.rect = GramRect(self.cA, self.cB)
        self.rect.draw = 'black'
        # We have xPosn, yPosn, length, height, _frame, _color, graphics, and
        # bb, inherited.

    def setPositions(self):
        thisVal = (self.val - self.plot.minBarValToShow) * \
            self.plot.barValScale
        # print "val=%s, minBarValToShow=%s, thisVal=%s, barValScale=%s" % (
        # self.val, self.plot.minBarValToShow, thisVal, self.plot.barValScale)
        self.cA.xPosn = (self.plot.contentPosnX +
                         ((float(self.barNum) / float(self.plot.nBars)) * self.plot.contentSizeX) +
                         (self.plot.halfSpaceBetweenBarGroups * self.barSetsObject.tickWidth) +
                         (self.barSetNum * self.barSetsObject.oneBarWidth))
        self.cA.yPosn = self.plot.contentPosnY
        self.cB.xPosn = self.cA.xPosn + self.barSetsObject.oneBarWidth
        self.cB.yPosn = self.cA.yPosn + thisVal
        #print(f"PlotBar.setPositions() val={self.val}, cA.xPosn {self.cA.xPosn:.2f}, cA.yPosn {self.cA.yPosn:.2f}, ", end='')
        #print(f"cB.xPosn {self.cB.xPosn:.2f}, cB.yPosn {self.cB.yPosn:.2f}")
        # print(f"PlotBar.setPositions() barSetNum={self.barSetNum}")

    def getTikz(self):
        thisBarName = self.barSetsObject.barNames[self.barNum]
        yDiff = self.cB.yPosn - self.cA.yPosn
        if yDiff == 0.0:   # maybe should be math.fabs() < epsilon?
            return "%% val=%s" % self.val
        return self.rect.getTikz() + " %% bar %s, val=%s" % (thisBarName, self.val)

    def getSvg(self):
        if self.rect.fill:
            assert isinstance(self.rect.fill, GramColor)
        yDiff = self.cB.yPosn - self.cA.yPosn
        if yDiff == 0.0:   # maybe should be math.fabs() < epsilon?
            return "<!-- val=%s -->" % self.val
        return self.rect.getSvg() + " <!-- val=%s -->" % self.val

class PlotBarsText(GramText):

    def __init__(self, plot, binNum, val, theText):
        # GramGraphic.__init__(self)
        GramText.__init__(self, theText)
        self.cA = GramCoord()
        self.plot = plot
        self.binNum = binNum
        self.val = val

    def setPositions(self):
        self.cA.xPosn = (self.plot.contentPosnX +
                         ((float(self.binNum + 0.5) / float(self.plot.nBars)) * self.plot.contentSizeX))
        self.cA.yPosn = self.plot.contentPosnY + \
            ((self.val - self.plot.minBarValToShow) * self.plot.barValScale)

    def getTikz(self):
        ss = []
        ss.append("\n% bars text in plot")
        ss.append(GramText.getTikz(self))
        return '\n'.join(ss)

    def getSvg(self):
        ss = []
        ss.append("\n<!-- bars text in plot -->")
        ss.append(GramText.getSvg(self))
        return '\n'.join(ss)


class PlotHorizontalBracketBars(GramLine):

    def __init__(self, plot, binNumA, binNumB, val, theText):
        cA = GramCoord()
        cB = GramCoord()

        GramLine.__init__(self, cA, cB)
        self.plot = plot
        assert binNumB > binNumA
        self.binNumA = binNumA
        self.binNumB = binNumB
        self.val = val
        self.text = GramText(theText)
        self.text.cA = GramCoord()


    def setPositions(self):
        gm = ["PlotHorizontalBracketBars.setPositions()"]

        self.cA.xPosn = self.plot.contentPosnX + ((float(self.binNumA + 0.1) / float(self.plot.nBars)) * self.plot.contentSizeX)
        self.cA.yPosn = self.plot.contentPosnY + ((self.val - self.plot.minBarValToShow) * self.plot.barValScale)
        self.cB.xPosn = self.plot.contentPosnX + ((float(self.binNumB + 0.9) / float(self.plot.nBars)) * self.plot.contentSizeX)
        self.cB.yPosn = self.cA.yPosn

        self.text.cA.xPosn = self.cA.xPosn + ((self.cB.xPosn - self.cA.xPosn) / 2.)
        self.text.cA.yPosn = self.cA.yPosn
        self.text.style = 'tickLabel'
        self.text.anchor = 'south'
        


    def getTikz(self):
        ss = []
        ss.append("\n% horizontal bracket in bar plot")
        ss.append(GramLine.getTikz(self))
        ss.append(GramText.getTikz(self.text))
        return '\n'.join(ss)

    def getSvg(self):
        ss = []
        ss.append("\n<!-- horizontal bracket in bar plot -->")
        ss.append(GramLine.getSvg(self))
        ss.append(GramText.getSvg(self.text))
        return '\n'.join(ss)

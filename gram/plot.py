from __future__ import print_function
from gram import *
import os
import math
import string
import sys

# We do these at the bottom of this file...
#from XY import *
#from Axis import *
#from Bars import *


class Plot(Gram):

    def __init__(self):
        Gram.__init__(self)
        self.dirName = 'Gram'
        self.baseName = 'gp'
        #self.lineWidth = 0.4
        self.plotDefaultLineThickness = 'thin'

        self.frameB = PlotFrame('b', self)
        self.frameT = PlotFrame('t', self)
        self.frameL = PlotFrame('l', self)
        self.frameR = PlotFrame('r', self)

        self.lines = []
        self.scatters = []
        self.barsList = []

        self.framePosnX = 2
        self.framePosnY = 2
        self.contentSizeX = 3.5
        self.contentSizeY = 2.65

        self.frameToContent_llx = 0.175
        self.frameToContent_lly = 0.175
        self.frameToContent_urx = 0.175
        self.frameToContent_ury = 0.175

        # properties, implemented below
        #contentPosnX = _framePosnX + frameToContent_llx
        #contentPosnY = _framePosnY + frameToContent_lly
        #frameSizeX = _contentSizeX + frameToContent_llx + frameToContent_urx
        #frameSizeY = _contentSizeY + frameToContent_lly + frameToContent_ury

        self._minXInData = None
        self._maxXInData = None
        self._minXToShow = None
        self._maxXToShow = None

        self._minYInData = None
        self._maxYInData = None
        self._minYToShow = None
        self._maxYToShow = None

        self.xYScaleX = None
        self.xYScaleY = None

        self.xAxis = None
        self.yAxis = None

        self.barNameAxis = None
        self.barValAxis = None

        self._nBars = None
        self.barNames = []
        self._barValScale = None
        self._minBarValInData = None
        self._maxBarValInData = None
        self._minBarValToShow = None
        self._maxBarValToShow = None

        self._halfSpaceBetweenBarGroups = 0.12

        #_frameB = None
        #_frameT = None
        #_frameL = None
        #_frameR = None

        self.titleExtraSpaceFromAxisB = None
        self.titleExtraSpaceFromAxisT = None
        self.titleExtraSpaceFromAxisL = None
        self.titleExtraSpaceFromAxisR = None

        self.titleDefaultAddSpaceFromAxisB = 0.1
        self.titleDefaultAddSpaceFromAxisT = 0.1
        self.titleDefaultAddSpaceFromAxisL = 0.1
        self.titleDefaultAddSpaceFromAxisR = 0.1

        self._tickLabelSize = 'tiny'
        self._axisLabelSize = 'footnotesize'

        self._goodBarFills = ['white', 
                              'black', 
                              'darkgray', 
                              'lightgray']

    # ========================================================================

    def _getContentPosnX(self):
        return self.framePosnX + self.frameToContent_llx

    def _setContentPosnX(self, newVal):
        raise GramError("Don't set this value.")
    contentPosnX = property(_getContentPosnX, _setContentPosnX)

    def _getContentPosnY(self):
        return self.framePosnY + self.frameToContent_lly

    def _setContentPosnY(self, newVal):
        raise GramError("Don't set this value.")
    contentPosnY = property(_getContentPosnY, _setContentPosnY)

    def _getFrameSizeX(self):
        return self.contentSizeX + self.frameToContent_llx + self.frameToContent_urx

    def _setFrameSizeX(self, newVal):
        raise GramError("Don't set this value.")
    frameSizeX = property(_getFrameSizeX, _setFrameSizeX)

    def _getFrameSizeY(self):
        return self.contentSizeY + self.frameToContent_lly + self.frameToContent_ury

    def _setFrameSizeY(self, newVal):
        raise GramError("Don't set this value.")
    frameSizeY = property(_getFrameSizeY, _setFrameSizeY)

    # ========================================================================

    def _getMinXInData(self):
        return self._minXInData

    def _setMinXInData(self, newVal):
        gm = ['self._setMinXInData()']
        gm.append("This is not user-settable.")
        raise GramError(gm)
    minXInData = property(_getMinXInData, _setMinXInData)

    def _getMaxXInData(self):
        return self._maxXInData

    def _setMaxXInData(self, newVal):
        gm = ['Plot._setMaxXInData()']
        gm.append("This is not user-settable.")
        raise GramError(gm)
    maxXInData = property(_getMaxXInData, _setMaxXInData)

    def _getMinYInData(self):
        return self._minYInData

    def _setMinYInData(self, newVal):
        gm = ['Plot._setMinYInData()']
        gm.append("This is not user-settable.")
        raise GramError(gm)
    minYInData = property(_getMinYInData, _setMinYInData)

    def _getMaxYInData(self):
        return self._maxYInData

    def _setMaxYInData(self, newVal):
        gm = ['Plot._setMaxYInData()']
        gm.append("This is not user-settable.")
        raise GramError(gm)
    maxYInData = property(_getMaxYInData, _setMaxYInData)

    # ==============================================================================================

    def _getMinXToShow(self):
        return self._minXToShow

    def _setMinXToShow(self, newVal):
        try:
            newVal = float(newVal)
        except:
            if newVal is None:
                self._minXToShow = None
                return
            else:
                gm = ['Plot._setMinXToShow()']
                gm.append(
                    "Should set it to a float, or None.  Got %s" % newVal)
                raise GramError(gm)
        assert self.minXInData is not None, "No minXInData. This needs some xy-content before setting minXToShow."
        if newVal > self.minXInData:
            gm = ['Plot._setMinXToShow()']
            gm.append(
                "Can't set it to more than minXInData=%s.  Got %s" % (self.minXInData, newVal))
            raise GramError(gm)
        self._minXToShow = newVal

    def _delMinXToShow(self):
        self._minXToShow = None
    minXToShow = property(_getMinXToShow, _setMinXToShow, _delMinXToShow)

    def _getMaxXToShow(self):
        return self._maxXToShow

    def _setMaxXToShow(self, newVal):
        try:
            newVal = float(newVal)
        except:
            if newVal is None:
                self._maxXToShow = None
                None
            else:
                gm = ['Plot._setMaxXToShow()']
                gm.append(
                    "Should set it to a float, or None.  Got %s" % newVal)
                raise GramError(gm)
        assert self.maxXInData is not None, "No maxXInData. This needs some xy-content before setting maxXToShow."
        if newVal < self.maxXInData:
            gm = ['Plot._setMaxXToShow()']
            gm.append(
                "Can't set it to less than maxXInData=%s.  Got %s" % (self.maxXInData, newVal))
            raise GramError(gm)
        self._maxXToShow = newVal

    def _delMaxXToShow(self):
        self._maxXToShow = None
    maxXToShow = property(_getMaxXToShow, _setMaxXToShow, _delMaxXToShow)

    def _getMinYToShow(self):
        return self._minYToShow

    def _setMinYToShow(self, newVal):
        try:
            newVal = float(newVal)
        except:
            if newVal is None:
                self._minYToShow = None
                return
            else:
                gm = ['Plot._setMinYToShow()']
                gm.append(
                    "Should set it to a float, or None.  Got %s" % newVal)
                raise GramError(gm)

        assert self.minYInData is not None, "No minYInData. This needs some xy-content before setting minYToShow."
        if newVal > self.minYInData:
            gm = ['Plot._setMinYToShow()']
            gm.append(
                "Can't set it to more than minYInData=%s.  Got %s" % (self.minYInData, newVal))
            raise GramError(gm)
        self._minYToShow = newVal

    def _delMinYToShow(self):
        self._minYToShow = None
    minYToShow = property(_getMinYToShow, _setMinYToShow, _delMinYToShow)

    def _getMaxYToShow(self):
        return self._maxYToShow

    def _setMaxYToShow(self, newVal):
        try:
            newVal = float(newVal)
        except:
            if newVal is None:
                self._maxYToShow = None
                return
            else:
                gm = ['Plot._setMaxYToShow()']
                gm.append(
                    "Should set it to a float, or None.  Got %s" % newVal)
                raise GramError(gm)
        assert self.maxYInData is not None, "No maxYInData. This needs some xy-content before setting maxYToShow."
        if newVal < self.maxYInData:
            gm = ['Plot._setMaxYToShow()']
            gm.append(
                "Can't set it to less than maxYInData=%s.  Got %s" % (self.maxYInData, newVal))
            raise GramError(gm)
        self._maxYToShow = newVal

    def _delMaxYToShow(self):
        self._maxYToShow = None
    maxYToShow = property(_getMaxYToShow, _setMaxYToShow, _delMaxYToShow)

    # =============================================================================================

    def _getNBars(self):
        return self._nBars

    def _setNBars(self, theNBars):
        if not isinstance(theNBars, int):
            gm = ['Plot._setNBars()']
            gm.append("Should set it to an int.  Got %s" % theNBars)
            raise GramError(gm)
        self._nBars = theNBars
    nBars = property(_getNBars, _setNBars)

# def _getBarNames(self):
# return self._barNames
# def _setBarNames(self, newVal):
##        self._barNames = newVal
##    barNames = property(_getBarNames, _setBarNames)

    def _getBarValScale(self):
        return self._barValScale

    def _setBarValScale(self, newVal):
        try:
            newVal = float(newVal)
            self._barValScale = newVal
        except:
            if newVal is None:
                self._barValScale = newVal
            else:
                gm = ['Plot._setBarValScale()']
                gm.append(
                    "Should set it to a float, or None.  Got %s" % newVal)
                raise GramError(gm)

    def _delBarValScale(self):
        self._barValScale = None
    barValScale = property(_getBarValScale, _setBarValScale, _delBarValScale)

    # =========================================================================================

    def _getMinBarValInData(self):
        return self._minBarValInData

    def _setMinBarValInData(self, newVal):
        gm = ['Plot._setMinBarValInData()']
        gm.append("Not user-settable")
        raise GramError(gm)
    minBarValInData = property(_getMinBarValInData, _setMinBarValInData)

    def _getMaxBarValInData(self):
        return self._maxBarValInData

    def _setMaxBarValInData(self, newVal):
        gm = ['Plot._setMaxBarValInData()']
        gm.append("Not user-settable.")
        raise GramError(gm)
    maxBarValInData = property(_getMaxBarValInData, _setMaxBarValInData)

    def _getMinBarValToShow(self):
        return self._minBarValToShow

    def _setMinBarValToShow(self, newVal):
        try:
            newVal = float(newVal)
            self._minBarValToShow = newVal
        except:
            if newVal is None:
                self._minBarValToShow = newVal
            else:
                gm = ['Plot._setMinBarValToShow()']
                gm.append(
                    "Should set it to a float, or None.  Got %s" % newVal)
                raise GramError(gm)

    def _delMinBarValToShow(self):
        self._minBarValToShow = None
    minBarValToShow = property(
        _getMinBarValToShow, _setMinBarValToShow, _delMinBarValToShow)

    def _getMaxBarValToShow(self):
        return self._maxBarValToShow

    def _setMaxBarValToShow(self, newVal):
        try:
            newVal = float(newVal)
            self._maxBarValToShow = newVal
        except:
            if newVal is None:
                self._maxBarValToShow = newVal
            else:
                gm = ['Plot._setMaxBarValToShow()']
                gm.append(
                    "Should set it to a float, or None.  Got %s" % newVal)
                raise GramError(gm)

    def _delMaxBarValToShow(self):
        self._maxBarValToShow = None
    maxBarValToShow = property(
        _getMaxBarValToShow, _setMaxBarValToShow, _delMaxBarValToShow)

    def _getHalfSpaceBetweenBarGroups(self):
        return self._halfSpaceBetweenBarGroups

    def _setHalfSpaceBetweenBarGroups(self, newVal):
        nVal = float(newVal)
        if nVal >= 0.0 and nVal < 0.9:
            self._halfSpaceBetweenBarGroups = nVal
        else:
            raise GramError(
                "_setHalfSpaceBetweenBarGroups new value should be >= zero, and less than 0.9.")

    halfSpaceBetweenBarGroups = property(
        _getHalfSpaceBetweenBarGroups, _setHalfSpaceBetweenBarGroups)

    def _getGoodBarFills(self):
        return self._goodBarFills
    goodBarFills = property(_getGoodBarFills)

    def _setRl(self, theRl):
        if theRl is not False:  # not in [True, False]:
            gm = ['Plot._setRl()']
            gm.append("rl cannot be set to True for Plot")
            raise GramError(gm)
        Gram._rl = theRl

    def _getTickLabelSize(self):
        return self._tickLabelSize

    def _setTickLabelSize(self, newVal):
        if newVal in self.goodTextSizes:
            self._tickLabelSize = newVal
        else:
            gm = ['Plot._setTickLabelSize()']
            gm.append("The size must be one of %s" % self.goodTextSizes)
            gm.append("Got %s." % newVal)
            raise GramError(gm)
    tickLabelSize = property(_getTickLabelSize, _setTickLabelSize)

    def _getAxisLabelSize(self):
        return self._axisLabelSize

    def _setAxisLabelSize(self, newVal):
        if newVal in self.goodTextSizes:
            self._axisLabelSize = newVal
        else:
            gm = ['Plot._setAxisLabelSize()']
            gm.append("The size must be one of %s" % self.goodTextSizes)
            gm.append("Got %s." % newVal)
            raise GramError(gm)
    axisLabelSize = property(_getAxisLabelSize, _setAxisLabelSize)

#==================================================================
#==================================================================
#==================================================================
#==================================================================
#==================================================================
#==================================================================
#==================================================================
#==================================================================

    def setBuiltInTikzStyles(self):

        g = GramText('Xxy')
        g.cA = GramCoord(0, 0)
        g.name = 'tickLabel'
        g.textSize = self.tickLabelSize
        if self.engine == 'tikz':
            g.setBB()
        Gram._styleDict[g.name] = g

        g = GramText('Xxy')
        g.cA = GramCoord(0, 0)
        g.name = 'axisLabel'
        g.textSize = self.axisLabelSize
        if self.engine == 'tikz':
            g.setBB()
        Gram._styleDict[g.name] = g

    def render(self):
        self.tikzPictureDefaults.lineThickness = self.plotDefaultLineThickness
        self.tikzPictureDefaults.innerSep = self.defaultInnerSep

        if self.minXToShow is not None and self.maxXToShow is not None:
            self.xYScaleX = self.contentSizeX / \
                (self.maxXToShow - self.minXToShow)
        if self.minYToShow is not None and self.maxYToShow is not None:
            self.xYScaleY = self.contentSizeY / \
                (self.maxYToShow - self.minYToShow)

        if self.nBars:
            self.barValScale = self.contentSizeY / \
                (self.maxBarValToShow - self.minBarValToShow)

        Gram.render(self)

        if 1:
            spacer1 = ' ' * 10
            spacer2 = '    --    '
            print("%s %20s  %s" % (spacer1, 'minXInData', self.minXInData))
            print("%s %20s  %s" % (spacer1, 'minXToShow', self.minXToShow))
            print("%s %20s  %s" % (spacer1, 'maxXInData', self.maxXInData))
            print("%s %20s  %s" % (spacer1, 'maxXToShow', self.maxXToShow))
            print("%s %20s  %s" % (spacer2, 'xYScaleX', self.xYScaleX))
            print("%s %20s  %s" % (spacer1, 'minYInData', self.minYInData))
            print("%s %20s  %s" % (spacer1, 'minYToShow', self.minYToShow))
            print("%s %20s  %s" % (spacer1, 'maxYInData', self.maxYInData))
            print("%s %20s  %s" % (spacer1, 'maxYToShow', self.maxYToShow))
            print("%s %20s  %s" % (spacer2, 'xYScaleY', self.xYScaleY))
            print()
            print("%s %20s  %s" % (spacer1, 'nBars', self.nBars))
            print("%s %20s  %s" % (spacer1, 'minBarValInData', self.minBarValInData))
            print("%s %20s  %s" % (spacer1, 'minBarValToShow', self.minBarValToShow))
            print("%s %20s  %s" % (spacer1, 'maxBarValInData', self.maxBarValInData))
            print("%s %20s  %s" % (spacer1, 'maxBarValToShow', self.maxBarValToShow))
            print("%s %20s  %s" % (spacer2, 'barValScale', self.barValScale))

        if self.xAxis:
            self.xAxis.setPositions()
        if self.yAxis:
            self.yAxis.setPositions()
        if self.barNameAxis:
            self.barNameAxis.setPositions()
        if self.barValAxis:
            self.barValAxis.setPositions()
        if self.frameB:
            self.frameB.setPositions()
        if self.frameT:
            self.frameT.setPositions()
        if self.frameL:
            self.frameL.setPositions()
        if self.frameR:
            self.frameR.setPositions()

        if self.lines:
            for g in self.lines:
                g.setPositions()

        if self.scatters:
            for g in self.scatters:
                g.setPositions()

        if self.barsList:
            for g in self.barsList:
                g.setPositions()

        if self.graphics:
            for g in self.graphics:
                g.setPositions()

    def line(self, xx, yy, smooth=False):
        c = PlotLine(self, xx, yy, smooth)
        self.lines.append(c)
        return c

    def scatter(self, xx, yy, plotMark='next'):
        c = PlotScatter(self, xx, yy, plotMark)
        self.scatters.append(c)
        return c

    def bars(self, barNames, counts):
        self.barNames = barNames
        c = PlotBarSets(self, barNames, counts)
        self.barsList.append(c)
        return c

    def xYText(self, x, y, theText):
        assert isinstance(theText, str), "The arg theText should be a string."
        c = PlotXYText(self, x, y, theText)
        self.graphics.append(c)
        return c

    def barsText(self, barNum, val, theText):
        assert isinstance(theText, str)
        c = PlotBarsText(self, barNum, val, theText)
        self.graphics.append(c)
        return c

    def lineFromSlopeAndIntercept(self, slope, intercept):
        c = PlotLineFromSlopeAndIntercept(self, slope, intercept)
        self.graphics.append(c)
        return c

    def verticalLine(self, x, y=None):
        c = PlotVerticalLine(self, x, y)
        self.graphics.append(c)
        return c

    def getTikz(self):
        ss = []

        #ss.append(r"\draw[gray,very thin] (0,0) grid (7,7);")

        if self.xAxis:
            ss.append('')
            ss.append("%% xAxis")
            ss.append(self.xAxis.getTikz())

        if self.yAxis:
            ss.append('')
            ss.append("%% yAxis")
            ss.append(self.yAxis.getTikz())

        if self.barNameAxis:
            ss.append('')
            ss.append("%% barNameAxis")
            ss.append(self.barNameAxis.getTikz())

        if self.barValAxis:
            ss.append('')
            ss.append("%% barValAxis")
            ss.append(self.barValAxis.getTikz())

        if self.frameB or self.frameT or self.frameL or self.frameR:
            ss.append('')
            ss.append("%% frame lines")

            if self.frameB:
                ss.append(self.frameB.getTikz())

            if self.frameT:
                ss.append(self.frameT.getTikz())

            if self.frameL:
                ss.append(self.frameL.getTikz())

            if self.frameR:
                ss.append(self.frameR.getTikz())

        if self.barsList:
            for bar in self.barsList:
                ss.append(bar.getTikz())

        if self.lines:
            for line in self.lines:
                ss.append(line.getTikz())

        if self.scatters:
            for scatter in self.scatters:
                ss.append(scatter.getTikz())

        for gr in self.graphics:
            ss.append(gr.getTikz())

        ss.append('')
        return '\n'.join(ss)

    def getSvg(self):
        ss = []

        if self.xAxis:
            ss.append('')
            ss.append("<!--  xAxis -->")
            ss.append(self.xAxis.getSvg())

        if self.yAxis:
            ss.append('')
            ss.append("<!--   yAxis -->")
            ss.append(self.yAxis.getSvg())

        if self.barNameAxis:
            ss.append('')
            ss.append("<!--   barNameAxis -->")
            ss.append(self.barNameAxis.getSvg())

        if self.barValAxis:
            ss.append('')
            ss.append("<!--  barValAxis -->")
            ss.append(self.barValAxis.getSvg())

        if self.frameB or self.frameT or self.frameL or self.frameR:
            ss.append('')
            ss.append("<!--  frame lines -->")

            if self.frameB:
                ss.append(self.frameB.getSvg())

            if self.frameT:
                ss.append(self.frameT.getSvg())

            if self.frameL:
                ss.append(self.frameL.getSvg())

            if self.frameR:
                ss.append(self.frameR.getSvg())

        if self.barsList:
            for bar in self.barsList:
                ss.append(bar.getSvg())

        if self.lines:
            for line in self.lines:
                ss.append(line.getSvg())

        if self.scatters:
            for scatter in self.scatters:
                ss.append(scatter.getSvg())

        for gr in self.graphics:
            ss.append(gr.getSvg())

        ss.append('')
        return '\n'.join(ss)

    def calcBigBoundingBox(self):
        if self.engine == 'tikz':
            print("TreeGram.tikzCalcBigBoundingBox() is turned off.")
            #self.tikzCalcBigBoundingBox()
        else:
            assert self.engine == 'svg'
            self.svgCalcBigBoundingBox()


#--------------------------------------------------------
#--------------------------------------------------------
#--------------------------------------------------------
#--------------------------------------------------------
#--------------------------------------------------------


# class PlotGraphic(GramGraphic):
#     def __init__(self):
#         #Plot.__init__(self)
#         GramGraphic.__init__(self)

#         #print "===== PlotGraphic.setPositions == GramGraphic.setPositions %s" % (
#         #    PlotGraphic.setPositions == GramGraphic.setPositions)
#         #print "===== PlotGraphic.setPositions == Plot.setPositions %s" % (
#         #    PlotGraphic.setPositions == Plot.setPositions)
#         #print "===== PlotGraphic.setBB == GramGraphic.setBB %s" % (
#         #    PlotGraphic.setBB == GramGraphic.setBB)
#         #print "===== PlotGraphic.setBB == Plot.setBB %s" % (
#         #    PlotGraphic.setBB == Plot.setBB)


from gram.xy import *
from gram.axis import *
from gram.bars import *

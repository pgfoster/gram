from gram import *
import sys


class PlotFrame(GramGraphic):

    def __init__(self, position, plot):
        GramGraphic.__init__(self)
        if position not in ['b', 't', 'l', 'r']:
            raise GramError("Axis. position must be b, t, l, or r")
        self.position = position
        self.plot = plot
        self.orientation = None
        if self.position in ['b', 't']:
            self.orientation = 'h'
        else:
            self.orientation = 'v'
        self.cA = GramCoord()
        self.cB = GramCoord()
        self.line = GramLine(self.cA, self.cB)
        if self.orientation == 'v':
            self.line.cap = 'rect'

        #self.whiteDot = None

        if 0 and self.position == 't':
            self.whiteDot = GramText('.')
            self.whiteDot.cA = GramCoord(0, 0)
            self.whiteDot.color = 'red'
            self.whiteDot.textSize = 'tiny'
            self.whiteDot.anchor = 'center'
            self.whiteDot.draw = 'red'
            self.whiteDot.innerSep = 0.0
            self.whiteDot.textHeight = 0.0
            self.whiteDot.textDepth = 0.0

    def setPositions(self):

        endX = self.plot.framePosnX + self.plot.frameSizeX
        endY = self.plot.framePosnY + self.plot.frameSizeY

        if self.position == 'b':
            self.cA.xPosn = self.plot.framePosnX
            self.cA.yPosn = self.plot.framePosnY
        elif self.position == 't':
            self.cA.xPosn = self.plot.framePosnX
            self.cA.yPosn = endY
        elif self.position == 'l':
            self.cA.xPosn = self.plot.framePosnX
            self.cA.yPosn = self.plot.framePosnY
        elif self.position == 'r':
            self.cA.xPosn = endX
            self.cA.yPosn = self.plot.framePosnY

        if self.orientation == 'h':
            self.cB.xPosn = endX
            self.cB.yPosn = self.cA.yPosn
        elif self.orientation == 'v':
            self.cB.xPosn = self.cA.xPosn
            self.cB.yPosn = endY

    def getTikz(self):
        return self.line.getTikz()

    def getSvg(self):
        return self.line.getSvg()


class Tick(GramGraphic):

    def __init__(self, val):
        GramGraphic.__init__(self)
        self.val = val
        self.textRotate = 0.0
        self.sig = "%.0f"
        self.line = None
        self.text = None
        self.textOn = True

    def getTikz(self):
        ss = []
        aLine = self.line.getTikz()
        if self.text:
            aLine += "  %% tick at %s" % self.text.rawText
        ss.append(aLine)
        if self.text:
            ss.append(self.text.getTikz())
        return '\n'.join(ss)

    def getSvg(self):
        ss = []
        aLine = self.line.getSvg()
        if self.text:
            aLine += "  <!-- tick at %s -->" % self.text.rawText
        ss.append(aLine)
        if self.text:
            ss.append(self.text.getSvg())
        return '\n'.join(ss)


class AxisStyles(list):

    def __init__(self):
        list.__init__(self)
        self.goodStyles = ['ticks', 'labels']

    def append(self, item):
        if item in self.goodStyles:
            if item not in self:
                list.append(self, item)
            else:
                print("AxisStyles.append()")
                print("    Got attempt to append '%s' -- but its already there!" % item)
                print("    styles is currently %s" % self)

        else:
            gm = ["AxisStyles.append()"]
            gm.append("Can't append '%s'" % item)
            gm.append("Can only append %s" % self.goodStyles)
            gm.append("styles is currently %s" % self)
            raise GramError(gm)

    def remove(self, item):
        if item in self.goodStyles:
            if item in self:
                list.remove(self, item)
            else:
                print("AxisStyles.append()")
                print("    Got attempt to remove '%s' -- but it is not one of the current styles!" % item)
                print("    styles is currently %s" % self)

        else:
            gm = ["AxisStyles.remove()"]
            gm.append("Can't remove '%s'" % item)
            gm.append(
                "Can only remove %s (and of course only if they are in styles)" % self.goodStyles)
            gm.append("styles is currently %s" % self)
            raise GramError(gm)


class Axis(GramGraphic):
    _tickLen = 0.1

    def __init__(self, position, plot):
        GramGraphic.__init__(self)
        if position not in ['b', 't', 'l', 'r']:
            raise GramError("Axis. position must be b, t, l, or r")
        self.position = position
        self.plot = plot
        self.orientation = None
        if self.position in ['b', 't']:
            self.orientation = 'h'
        else:
            self.orientation = 'v'
        self.styles = AxisStyles()
        self.ticks = []
        self.tickInterval = None
        self.tickLabelsSkipFirst = 0
        self.tickLabelsSkipLast = 0
        self.tickLabelsEvery = 1
        self.labelTextSize = 'footnotesize'
        self.textRotate = 0.0
        self.sig = None
        #self.title = None
        self.titleText = None
        self.bb = [0.0] * 4
        self.barLabelsSkipFirst = 0
        self.barLabelsSkipLast = 0
        self.barLabelsEvery = 1

    def _getTickLen(self):
        return Axis._tickLen

    def _setTickLen(self, theTickLen):
        Axis._tickLen = theTickLen
    tickLen = property(_getTickLen, _setTickLen)

    def _getTitle(self):
        return self.titleText

    def _setTitle(self, theTitle):
        if theTitle is None:
            self.titleText = None
        else:
            self.titleText = GramText(theTitle)
            self.titleText.style = 'axisLabel'
            self.titleText.cA = GramCoord()
            if self.orientation == 'v':
                self.titleText.rotate = 90
            #self.titleText.draw = True

    def _delTitle(self):
        self.titleText = None
    title = property(_getTitle, _setTitle, _delTitle)

    def setTitlePosition(self):

        # The user can set titleExtraSpaceFromAxisB etc, which will be used
        # if they exist.  Otherwise a good distance will be
        # calculated.
        if self.orientation == 'h':
            self.titleText.cA.xPosn = self.plot.framePosnX + \
                (self.plot.frameSizeX / 2.)

            if self.position == 'b':
                self.titleText.anchor = 'north'
                tPos = self.plot.framePosnY
                # print "wwx hb tickLen=%s, tPos = %s, self.styles=%s" %
                # (self.tickLen, tPos, self.styles)
                if 'labels' in self.styles:
                    for tick in self.ticks:
                        if tick.text:
                            # print "tick %s, bb=%s" % (tick.text.rawText,
                            # tick.text.bb)
                            if tick.text.bb[1] < tPos:
                                tPos = tick.text.bb[1]
                            if tick.text.bb[3] < tPos:
                                tPos = tick.text.bb[3]
                elif 'ticks' in self.styles:
                    tPos -= self.tickLen
                # print "www hb tickLen=%s, tPos = %s" % (self.tickLen, tPos)
                self.titleText.cA.yPosn = tPos  # - (3. * self.labelSep)
                self.titleText.cA.yPosn -= self.plot.titleDefaultAddSpaceFromAxisB

                if self.plot.titleExtraSpaceFromAxisB:
                    self.titleText.cA.yPosn -= self.plot.titleExtraSpaceFromAxisB
            elif self.position == 't':
                self.titleText.anchor = 'south'
                tPos = self.plot.framePosnY + self.plot.frameSizeY
                if 'labels' in self.styles:
                    for tick in self.ticks:
                        if tick.text:
                            if tick.text.bb[1] > tPos:
                                tPos = tick.text.bb[1]
                            if tick.text.bb[3] > tPos:
                                tPos = tick.text.bb[3]
                elif 'ticks' in self.styles:
                    tPos += self.tickLen
                self.titleText.cA.yPosn = tPos
                self.titleText.cA.yPosn += self.plot.titleDefaultAddSpaceFromAxisT

                if self.plot.titleExtraSpaceFromAxisT:
                    self.titleText.cA.yPosn += self.plot.titleExtraSpaceFromAxisT
        elif self.orientation == 'v':
            if self.position == 'l':
                self.titleText.anchor = 'south'
                tPos = self.plot.framePosnX
                if 'labels' in self.styles:
                    for tick in self.ticks:
                        if tick.text:
                            if tick.text.bb[0] < tPos:
                                tPos = tick.text.bb[0]
                elif 'ticks' in self.styles:
                    tPos -= self.tickLen

                self.titleText.cA.xPosn = tPos
                self.titleText.cA.xPosn -= self.plot.titleDefaultAddSpaceFromAxisL
                if self.plot.titleExtraSpaceFromAxisL:
                    self.titleText.cA.xPosn -= self.plot.titleExtraSpaceFromAxisL

            elif self.position == 'r':
                self.titleText.anchor = 'north'
                tPos = self.plot.framePosnX + self.plot.frameSizeX
                if 'labels' in self.styles:
                    for tick in self.ticks:
                        if tick.text:
                            if tick.text.bb[2] > tPos:
                                tPos = tick.text.bb[2]
                elif 'ticks' in self.styles:
                    tPos += self.tickLen

                self.titleText.cA.xPosn = tPos
                self.titleText.cA.xPosn += self.plot.titleDefaultAddSpaceFromAxisR
                if self.plot.titleExtraSpaceFromAxisR:
                    self.titleText.cA.xPosn += self.plot.titleExtraSpaceFromAxisR

            self.titleText.cA.yPosn = self.plot.framePosnY + \
                (self.plot.frameSizeY / 2.)

    def getTikz(self):
        ss = []
        ss.append("%% Axis.getTikz()  %s ticks" % len(self.ticks))
        if self.titleText and self.titleText.rawText:
            ss.append(self.titleText.getTikz())
        if self.ticks:
            for tick in self.ticks:
                ss.append(tick.getTikz())
        return '\n'.join(ss)

    def getSvg(self):
        ss = []
        ss.append("<!-- Axis.getSvg()  %s ticks -->" % len(self.ticks))
        if self.titleText and self.titleText.rawText:
            ss.append(self.titleText.getSvg())
        if self.ticks:
            for tick in self.ticks:
                ss.append(tick.getSvg())
        return '\n'.join(ss)


class XYAxis(Axis):

    def __init__(self, position, plot, useBarVals=False):
        Axis.__init__(self, position, plot)
        #self.plot = plot
        self.useBarVals = useBarVals
        if self.useBarVals:
            assert self.orientation == 'v', 'You can only useBarVals for vertical axis'

    def setTicks(self, minPos, maxPos):
        rng = maxPos - minPos
        orderOfMag = int(math.floor(math.log(rng, 10)))
        rng *= math.pow(10, -orderOfMag)
        # print "minPos=%f, maxPos=%f, rng=%f, orderOfMag = %i" % (minPos,
        # maxPos, rng, orderOfMag)

        if not self.tickInterval:

            # if rng < 1.7:
            #    step = 0.2
            # elif rng < 2.1:
            #    step = 0.25
            # elif rng < 4.1:
            #    step = 0.5
            # elif rng < 8.9:
            #    step = 1.0
            # else:
            #    step = 2.0

            if rng < 1.21:
                step = 0.2
            elif rng < 1.55:
                step = 0.25
            elif rng < 3.1:
                step = 0.5
            elif rng < 6.9:
                step = 1.0
            else:
                step = 2.0

            self.tickInterval = step * math.pow(10, orderOfMag)
        else:
            step = self.tickInterval

        # print "self.sig = ", self.sig
        if not self.sig:
            # print "==== choosing a sig.  orderOfMag is %i, step is %.2f, tickInterval is %f" % (
            #    orderOfMag, step, self.tickInterval)
            if orderOfMag > 1:
                self.sig = "%.0f"
            elif orderOfMag == 1:
                if step == 0.25:
                    self.sig = "%.1f"
                else:
                    self.sig = "%.0f"
            elif orderOfMag == 0:
                if step < 1.0:
                    if step == 0.25:
                        self.sig = "%.2f"
                    else:
                        self.sig = "%.1f"
                else:
                    self.sig = "%.0f"
            elif orderOfMag < 0:
                if step == 1.0 or step == 2.0:
                    self.sig = "%%.%if" % (-orderOfMag)
                elif step == 0.25:
                    self.sig = "%%.%if" % (-orderOfMag + 2)
                else:
                    self.sig = "%%.%if" % (-orderOfMag + 1)

        # print "self.sig = ", self.sig

        assert self.tickInterval

        fl = minPos / self.tickInterval
        niceMin = math.ceil(fl)
        niceMin *= self.tickInterval

        fl = maxPos / self.tickInterval
        niceMax = math.floor(fl)
        niceMax *= self.tickInterval

        epsilon = 0.01 * self.tickInterval
        self.ticks = []
        val = niceMin
        while val <= niceMax:
            # We do not want -0, ie minus zero, which can happen sometimes.
            if math.fabs(val - 0.0) < epsilon:
                val = 0.0
            t = Tick(val)
            t.textRotate = self.textRotate
            t.sig = self.sig
            # self.graphics.append(t)
            self.ticks.append(t)
            val += self.tickInterval

        # Turn off text based on self.tickLabelsEvery
        for tick in self.ticks:
            tick.textOn = False
        maxTickNum = len(self.ticks) - self.tickLabelsSkipLast
        tNum = self.tickLabelsSkipFirst
        while tNum < maxTickNum:
            self.ticks[tNum].textOn = True
            tNum += self.tickLabelsEvery

        if 0:
            print("self.sig = ", self.sig)
            print("self.tickInterval is %f" % self.tickInterval)
            print("niceMin = %f" % niceMin)
            print("niceMax = %f" % niceMax)

            for tick in self.ticks:
                print("tick: val=%s, textRotate=%s, sig=%s" % (
                    tick.val, tick.textRotate, tick.sig), tick.sig % tick.val)
            sys.exit()

    def setPositions(self):

        if self.useBarVals:
            assert self.orientation == 'v', "orientation must be 'v' if useBarVals is turned on."
            theMinYToShow = self.plot.minBarValToShow
            theMaxYToShow = self.plot.maxBarValToShow
            theXYScaleY = self.plot.barValScale
        else:
            theMinYToShow = self.plot.minYToShow
            theMaxYToShow = self.plot.maxYToShow
            theXYScaleY = self.plot.xYScaleY

        if 0:
            print("XYAxis.setPositions()")
            print("    position = %s, orientation = %s" % (self.position, self.orientation))
            if self.orientation == 'h':
                print("    minXInData = %s, maxXInData = %s" % (self.plot.minXInData, self.plot.maxXInData))
                print("    minXToShow = %s, maxXToShow = %s" % (self.plot.minXToShow, self.plot.maxXToShow))
            elif self.orientation == 'v':
                print("    useBarVals = %s" % self.useBarVals)
                print("    minYInData = %s, maxYInData = %s" % (self.plot.minYInData, self.plot.maxYInData))
                print("    minYToShow = %s, maxYToShow = %s" % (theMinYToShow, theMaxYToShow))
            print("    framePosnX = %.1f, framePosnY = %.1f" % (self.plot.framePosnX, self.plot.framePosnY))
            print("    self.styles = %s" % self.styles)
            # sys.exit()

        if 'ticks' in self.styles:

            if not self.ticks:
                # If the ticks do not exist yet, make them.  Using
                # setTicks() gives a nice number and spacing.
                if self.orientation == 'h':
                    if self.plot.minXToShow is not None and self.plot.maxXToShow is not None:
                        self.setTicks(
                            self.plot.minXToShow, self.plot.maxXToShow)
                elif self.orientation == 'v':
                    if theMinYToShow is not None and theMaxYToShow is not None:
                        self.setTicks(theMinYToShow, theMaxYToShow)

            # Set the coords of the tick, cA is where it touches the frame.
            for tick in self.ticks:
                tick.cA = GramCoord()
                tick.cB = GramCoord()
                if self.orientation == 'h':
                    tick.cA.xPosn = self.plot.contentPosnX + \
                        ((tick.val - self.plot.minXToShow)
                         * self.plot.xYScaleX)
                    tick.cB.xPosn = tick.cA.xPosn
                    if self.position == 'b':
                        tick.cA.yPosn = self.plot.framePosnY
                        tick.cB.yPosn = tick.cA.yPosn - self.tickLen
                    elif self.position == 't':
                        tick.cA.yPosn = self.plot.framePosnY + \
                            self.plot.frameSizeY
                        tick.cB.yPosn = tick.cA.yPosn + self.tickLen
                elif self.orientation == 'v':
                    if self.position == 'l':
                        tick.cA.xPosn = self.plot.framePosnX
                        tick.cB.xPosn = tick.cA.xPosn - self.tickLen
                    elif self.position == 'r':
                        tick.cA.xPosn = self.plot.framePosnX + \
                            self.plot.frameSizeX
                        tick.cB.xPosn = tick.cA.xPosn + self.tickLen
                    tick.cA.yPosn = self.plot.contentPosnY + \
                        ((tick.val - theMinYToShow) * theXYScaleY)
                    tick.cB.yPosn = tick.cA.yPosn

            # Make the tick line.
            for tick in self.ticks:
                if not tick.line:
                    tick.line = GramLine(tick.cA, tick.cB)

            if 'labels' in self.styles:

                # If the text label does not exist yet, make it.
                for tick in self.ticks:
                    if tick.textOn and not tick.text:
                        # print "the tick.sig is %s, the tick.val is %s" %
                        # (tick.sig, tick.val)
                        theText = tick.sig % tick.val
                        tick.text = GramText(theText)
                        #tick.text.draw = True
                        tick.text.cA = tick.cB
                        # tick.graphics.append(tick.text)
                        tick.text.style = 'tickLabel'
                        #tick.text.textSize = self.labelTextSize
                        # tick.text.setCookedText()
                        # tick.text.setTextLengthHeightAndMetrics()
                        if self.orientation == 'h':
                            if self.position == 'b':
                                tick.text.anchor = 'north'
                            elif self.position == 't':
                                tick.text.anchor = 'south'

                            # the coord is the end of the tick.  Shift the text up or down
                            # if self.position == 'b':
                            #    tick.text.yShift = - (tick.text.bigX + tick.text.defaultInnerSep)
                            # elif self.position == 't':
                            #    tick.text.yShift = tick.text.yuh + tick.text.defaultInnerSep

                            if tick.textRotate:
                                tick.text.rotate = tick.textRotate
                                if tick.textRotate >= 45:
                                    if self.position == 'b':
                                        tick.text.anchor = 'east'
                                    elif self.position == 't':
                                        tick.text.anchor = 'west'
                                elif tick.textRotate <= -45:
                                    if self.position == 'b':
                                        tick.text.anchor = 'west'
                                    elif self.position == 't':
                                        tick.text.anchor = 'east'
                        elif self.orientation == 'v':
                            if self.position == 'l':
                                tick.text.anchor = 'east'
                            elif self.position == 'r':
                                tick.text.anchor = 'west'

                if 0 and self.orientation == 'h':
                    exemplar = None
                    for tick in self.ticks:
                        if tick.text:
                            exemplar = tick
                            break
                    assert exemplar

                    tickTextYOffset = self.tickLen  # + self.labelSep
                    if self.position == 'b':
                        tickTextYOffset = -tickTextYOffset
                        tickTextYOffset -= exemplar.text.bigX
                    elif self.position == 't':
                        tickTextYOffset += 0.5 * exemplar.text.ex

                    for tick in self.ticks:
                        if tick.textOn:
                            pass
                            #tick.text.xPosn = tick.xPosn
                            # if tick.textRotate >= 45:
                            #    tick.text.xPosn += 0.5 * tick.text.ex
                            # elif tick.textRotate <= -45:
                            #    pass
                            #tick.text.yPosn = tick.yPosn + tickTextYOffset
                            # tick.text.setPositions()

                # elif self.orientation == 'v':
                #    tickTextXOffset = self.tickLen #+ self.labelSep
                    #assert self.ticks
                    #tickTextYOffset = 0.5 * self.ticks[0].text.ex

                #    for tick in self.ticks:
                #        if tick.textOn:
                #            pass
                            # if self.position == 'l':
                            #    tick.text.xPosn = tick.xPosn - tickTextXOffset
                            # elif self.position == 'r':
                            #    tick.text.xPosn = tick.xPosn + tickTextXOffset
                            # if tick.textRotate >= 45:
                            #    tick.text.xPosn += 0.5 * tick.text.ex
                            # elif tick.textRotate <= -45:
                            #    pass
                            #tick.text.yPosn = tick.yPosn
                            # tick.text.setPositions()
            for tick in self.ticks:
                tick.setPositions()
                if tick.text and self.engine == 'tikz':
                    tick.text.setBB()  # needed to place the title

        if self.titleText:
            self.setTitlePosition()
            self.titleText.setPositions()

        # self.setBB()


class BarsAxis(Axis):

    def __init__(self, position, plot):
        Axis.__init__(self, position, plot)
        self.barLabels = []

    def _getPosition(self):
        return 'b'

    def _setPosition(self, newVal):
        if newVal == 'b':
            pass
        else:
            raise GramError(
                "BarsAxis must be position 'b', got attempt to set it to '%s'" % newVal)
    position = property(_getPosition, _setPosition)

    def setPositions(self):
        if 1:
            print("BarsAxis.setPositions()")
            print("    position = %s, orientation = %s" % (self.position, self.orientation))
            if self.orientation == 'h':
                print("    nBars %s" % self.plot.nBars)
                print("    barNames = %s" % self.plot.barNames)
            elif self.orientation == 'v':
                raise GramError("vertical position is not implemented")
            print("    framePosnX = %.1f, framePosnY = %.1f" % (self.plot.framePosnX, self.plot.framePosnY))
            print("    self.styles = %s" % self.styles)

        if 'ticks' in self.styles:

            # If we do not have ticks yet, make them.
            if not self.ticks:
                self.ticks = []
                # One tick for each bin ...
                for bNum in range(self.plot.nBars):
                    tick = Tick(bNum)
                    tick.cA = GramCoord()
                    tick.cB = GramCoord()
                    if self.textRotate:
                        tick.textRotate = self.textRotate
                    self.ticks.append(tick)
                # ... and one last one ...
                tick = Tick(self.plot.nBars)
                tick.cA = GramCoord()
                tick.cB = GramCoord()
                self.ticks.append(tick)
                # for tick in self.ticks:
                #    self.graphics.append(tick)

            # Set the coords of the tick, cA is where it touches the frame.
            for tick in self.ticks:
                if self.orientation == 'h':
                    tick.cA.xPosn = self.plot.contentPosnX + \
                        ((float(tick.val) / float(self.plot.nBars))
                         * self.plot.contentSizeX)
                    tick.cB.xPosn = tick.cA.xPosn
                    tick.cA.yPosn = self.plot.framePosnY
                    tick.cB.yPosn = tick.cA.yPosn - self.tickLen
                elif self.orientation == 'v':
                    raise GramError("Fix me!")

            # If they don't exist yet, make the lines
            for tick in self.ticks:
                if not tick.line:
                    tick.line = GramLine(tick.cA, tick.cB)

            if 'labels' in self.styles:
                assert len(self.ticks) == self.plot.nBars + 1
                assert self.barLabelsSkipFirst < self.plot.nBars
                assert self.barLabelsSkipLast < self.plot.nBars
                assert self.plot.barNames
                maxLabelPos = self.plot.nBars - self.barLabelsSkipLast
                mainBody = maxLabelPos - self.barLabelsSkipFirst
                assert mainBody > 0
                tNum = 0
                while tNum < self.barLabelsSkipFirst:
                    # print "skipping tNum %i" % tNum
                    tNum += 1
                while tNum < maxLabelPos:
                    # print "doing tNum %i" % tNum
                    tick = self.ticks[tNum]
                    if not tick.text:
                        # self.barNames[] are strings
                        tick.text = GramText(self.plot.barNames[tNum])
                        tick.text.cA = GramCoord()
                        tick.text.style = 'tickLabel'
                        #tick.text.textSize = self.labelTextSize
                        tick.text.anchor = 'north'
                        # tick.text.setCookedText()
                        # tick.text.setTextLengthHeightAndMetrics()
                        if tick.textRotate:
                            if tick.textRotate > 0.0:
                                tick.text.anchor = 'north east'
                                if tick.textRotate >= 45:
                                    tick.text.anchor = 'east'
                            else:
                                tick.text.anchor = 'north west'
                                if tick.textRotate <= -45:
                                    tick.text.anchor = 'west'
                            tick.text.rotate = tick.textRotate
                        self.barLabels.append(tick.text)
                    tNum += self.barLabelsEvery

                if self.barLabels:
                    #tickTextYOffset = (self.tickLen + self.labelSep + self.barNames[0].ex)
                    #tickTextYOffset = (self.tickLen + self.barLabels[0].ex)
                    #tickTextYOffset = (self.tickLen + self.labelSep)

                    tickTextXOffset = 0.5 * \
                        (self.ticks[1].cA.xPosn - self.ticks[0].cA.xPosn)

                    for tick in self.ticks:
                        if tick.text:
                            tick.text.cA.xPosn = tick.cB.xPosn
                            tick.text.cA.yPosn = tick.cB.yPosn
                            if 0:
                                if tick.textRotate >= 45:
                                    tick.text.cA.xPosn += 0.5 * tick.text.ex
                                elif tick.textRotate <= -45:
                                    pass
                            tick.text.cA.xPosn += tickTextXOffset
                            #tick.text.cA.yPosn -= tickTextYOffset
                            # tick.text.setPositions()
        for tick in self.ticks:
            tick.setPositions()
            if tick.text:
                tick.text.setBB()

        if self.titleText:
            self.setTitlePosition()
            self.titleText.setPositions()

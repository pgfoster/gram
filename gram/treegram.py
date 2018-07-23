from __future__ import print_function
from gram import *
from p4 import Tree


class TreeGram(Gram):

    def __init__(self, theTree=None, scale=None, yScale=0.7, showNodeNums=False, widthToHeight=0.67, doVLines=True):
        gm = ['TreeGram()']

        self.tree = None
        #self._title = None
        self._scaleBar = None
        self.bracketsLineUp = True
        self._doSmartLabels = True
        self._rootLabelLeft = True
        self.wrapLeafLabelsAt = None
        #self.fixOverlaps = True
        #self.haveFixedOverlaps = False
        self.doVLines = doVLines
        #_doDiagonalLines = False     off

        # _leafLabelSize = 'small'
        # _internalNodeLabelSize = 'tiny'
        # _branchLabelSize = 'tiny'
        self._leafLabelSize = 'normalsize'
        self._internalNodeLabelSize = 'scriptsize'
        self._branchLabelSize = 'tiny'
        self.doLiningNumeralsHack = True

        if theTree:
            # print "theTree is %s" % theTree
            if isinstance(theTree, Tree):
                pass
            # assume to be a p4 Tree
            elif hasattr(theTree, 'root') and hasattr(theTree, 'recipWeight'):
                pass
            else:
                gm.append("Expecting a Tree instance.")
                gm.append("Got %s" % theTree)
                raise GramError(gm)

            self.tree = theTree
            # if showNodeNums:
            #    for n in theTree.iterNodes():
            #        if n.name:
            #            n.name += '_%i' % n.nodeNum
            #        else:
            #            n.name = '%i' % n.nodeNum
        self.scale = scale
        self.yScale = yScale
        self.showNodeNums = showNodeNums
        self.widthToHeight = float(widthToHeight)
        # if self.widthToHeight < 0.05:
        #    raise GramError("TreeGram()  widthToHeight is %s.  Too small?!" % self.widthToHeight)
        self.brackets = []
        self.thickBranches = []
        self.cBoxes = []
        self.brokenBranches = []

        Gram.__init__(self)
        self.dirName = 'Gram'
        self.baseName = 'tg'
        self.tgDefaultLineThickness = 'semithick'

        if self._config and self._config.sections() and self._config.has_section('Gram'):
            settables = "leafLabelSize internalNodeLabelSize branchLabelSize tgDefaultLineThickness".split()
            for myAttr in settables:
                try:
                    ret = self._config.get('Gram', myAttr)
                    if ret:
                        if myAttr in "tsone".split():
                            try:
                                ret = int(ret)
                            except ValueError:
                                raise GramError("Bad value '%s' for '%s' in conf file." %\
                                                (ret, myAttr))
                    writeInColor("conf file: Setting TreeGram %s to %s\n" % (myAttr, ret))
                    setattr(self, myAttr, ret)
                except configparser.NoOptionError:
                    pass
            # Get rid of the colour ...
            sys.stdout.flush()


        if self.tree:
            if not self.tree.preAndPostOrderAreValid:
                self.tree.setPreAndPostOrder()
            # set xPosn
            self.tree.root.xPosn0 = 0.0
            for n in self.tree.iterPreOrder():
                if n != self.tree.root:
                    n.xPosn0 = n.parent.xPosn0 + n.br.len

            # set yPosn0
            counter = self.tree.nTax - 1
            if self.tree.root.isLeaf:
                counter -= 1

            for n in self.tree.iterPostOrder():
                if n.isLeaf:
                    if n == self.tree.root:
                        pass
                    else:
                        n.yPosn0 = float(counter)
                        counter -= 1
                else:
                    n.yPosn0 = (
                        n.leftChild.yPosn0 + n.rightmostChild().yPosn0) / 2.0

            # terminal root
            if self.tree.root.isLeaf:
                self.tree.root.yPosn0 = self.tree.root.leftChild.yPosn0

            if 0:
                print("index   isLeaf        xPosn0        yPosn0")
                for n in self.tree.iterNodes():
                    print("%4i" % n.nodeNum, end=' ')
                    print("%8i" % n.isLeaf, end=' ')
                    print("%12s" % n.xPosn0, end=' ')
                    print("%12s" % n.yPosn0)
                # print self.leaves
                # sys.exit()

            # Set the scale so that the width of the lines is widthToHeight of
            # the height.
            if not self.scale:  # then guess
                longestTipToRoot = 0.0
                for n in self.tree.root.iterLeaves():
                    # print "node %i" % n.nodeNum
                    p = n
                    thisLen = 0.0
                    while p != self.tree.root:
                        thisLen += p.br.len
                        p = p.parent
                    if thisLen > longestTipToRoot:
                        longestTipToRoot = thisLen
                # print "got longestTipToRoot = %f" % longestTipToRoot
                theHeight = self.tree.nTax * self.yScale
                self.scale = (self.widthToHeight * theHeight) / \
                    longestTipToRoot
                print("widthToHeight %.2f, scale set to %f" % (self.widthToHeight, self.scale))
            else:
                print("given scale %.2f" % self.scale)

            # Make coordinates for the nodes.
            for n in self.tree.iterNodes():
                n.cA = GramCoord(
                    (n.xPosn0 * self.scale), (n.yPosn0 * self.yScale), 'n%i' % n.nodeNum)
                if n.parent:
                    n.cB = GramCoord(
                        (n.parent.xPosn0 * self.scale), (n.yPosn0 * self.yScale), 'n%ip' % n.nodeNum)
                else:
                    n.cB = None

            # Node names make node labels
            for n in self.tree.iterNodes():
                if n.name:
                    n.label = GramText(n.name)
                    n.label.cA = n.cA    # switcheroo of cA in TreeGramRadial
                    #n.label.draw = True
                    if n == self.tree.root:
                        if self.rootLabelLeft:
                            n.label.style = 'root'
                        else:
                            n.label.style = 'node right'
                    else:
                        if n.isLeaf:
                            n.label.style = 'leaf'
                        else:
                            n.label.style = 'node right'

                else:
                    n.label = None

            if self.doVLines:
                for n in self.tree.iterNodes():
                    if not n.isLeaf:
                        n.vLine = GramLine(
                            n.leftChild.cB, n.rightmostChild().cB)
                        #n.vLine.lineThickness = self.tgDefaultLineThickness
                        n.vLine.cap = 'rect'
                    else:
                        n.vLine = None
            else:
                for n in self.tree.iterNodes():
                    n.vLine = None

            # Make horizontal lines.
            # If there are branch labels or uLabels, place them on the line.
            for n in self.tree.iterNodesNoRoot():
                n.line = GramLine(n.cB, n.cA)
                if hasattr(n.br, 'name') and n.br.name:
                    n.br.label = GramText(n.br.name)
                    n.br.label.cA = GramCoord()
                    n.br.label.cA.xPosn = n.cB.xPosn + \
                        (n.cA.xPosn - n.cB.xPosn) / 2.
                    n.br.label.cA.yPosn = n.cB.yPosn + \
                        (n.cA.yPosn - n.cB.yPosn) / 2.
                    n.br.label.style = 'branch'
                    n.br.label.anchor = 'south'
                else:
                    n.br.label = None
                if hasattr(n.br, 'uName') and n.br.uName:
                    n.br.uLabel = GramText(n.br.uName)
                    n.br.uLabel.cA = GramCoord()
                    n.br.uLabel.cA.xPosn = n.cB.xPosn + \
                        (n.cA.xPosn - n.cB.xPosn) / 2.
                    n.br.uLabel.cA.yPosn = n.cB.yPosn + \
                        (n.cA.yPosn - n.cB.yPosn) / 2.
                    n.br.uLabel.style = 'branch'
                    n.br.uLabel.anchor = 'north'
                else:
                    n.br.uLabel = None
            self.tree.root.line = None

            # # branch names make branch labels
            # for n in self.tree.iterNodesNoRoot():
            #     if hasattr(n.br, 'name') and n.br.name:
            #         #self.setBranchLabel(n, n.br.name)
            #         #n.br.label.anchor = 'base'
            #         n.br.label = self.text(n.br.name, 0, 0)
            #         #n.br.label.draw = True
            #     else:
            #         n.br.label = None
            #     if hasattr(n.br, 'uName') and n.br.uName:
            #         #self.setBranchULabel(n, n.br.uName)
            #         #n.br.uLabel.anchor = 'base'
            #         n.br.uLabel = GramText(n.br.uName)
            #     else:
            #         n.br.uLabel = None

            # Add node numbers centered on nodes.
            if self.showNodeNums:
                for n in self.tree.iterNodes():
                    n.nodeNumLabel = GramText('%i' % n.nodeNum)
                    n.nodeNumLabel.cA = n.cA
                    n.nodeNumLabel.textSize = 'tiny'
                    n.nodeNumLabel.color = 'red'
                    n.nodeNumLabel.fill = 'white'
                    n.nodeNumLabel.innerSep = 0.02


    # def _getTitle(self):
    #     return self._title

    # def _setTitle(self, theTitle):
    #     gm = ["TreeGram._setTitle()"]
    #     gm.append("The title should be set via the setTitle() method.")
    #     gm.append(
    #         "That way you can set the content, and adjust the position as well.")
    #     raise GramError(gm)

    # def _delTitle(self):
    #     self._title = None
    # title = property(_getTitle, _setTitle, _delTitle)

    def _getScaleBar(self):
        return self._scaleBar

    def _setScaleBar(self, theScaleBar):
        gm = ["TreeGram._setScaleBar()"]
        gm.append("The scaleBar should be set via the setScaleBar() method.")
        raise GramError(gm)
    scaleBar = property(_getScaleBar, _setScaleBar)

    def _getBranchLabelSize(self):
        return self._branchLabelSize

    def _setBranchLabelSize(self, newVal):
        if newVal in self.goodTextSizes:
            TreeGram._branchLabelSize = newVal
        else:
            gm = ['TreeGram._setBranchLabelSize()']
            gm.append("The size must be one of %s" % self.goodTextSizes)
            gm.append("Got %s." % newVal)
            raise GramError(gm)
    branchLabelSize = property(_getBranchLabelSize, _setBranchLabelSize)

    def _getLeafLabelSize(self):
        return self._leafLabelSize

    def _setLeafLabelSize(self, newVal):
        if newVal in self.goodTextSizes:
            self._leafLabelSize = newVal
        else:
            gm = ['TreeGram._setLeafLabelSize()']
            gm.append("The size must be one of %s" % self.goodTextSizes)
            gm.append("Got %s." % newVal)
            raise GramError(gm)
    leafLabelSize = property(_getLeafLabelSize, _setLeafLabelSize)

    def _getInternalNodeLabelSize(self):
        return self._internalNodeLabelSize

    def _setInternalNodeLabelSize(self, newVal):
        if newVal in self.goodTextSizes:
            self._internalNodeLabelSize = newVal
        else:
            gm = ['TreeGram._setInternalNodeLabelSize()']
            gm.append("The size must be one of %s" % self.goodTextSizes)
            gm.append("Got %s." % newVal)
            raise GramError(gm)
    internalNodeLabelSize = property(
        _getInternalNodeLabelSize, _setInternalNodeLabelSize)

    def _getDoSmartLabels(self):
        return self._doSmartLabels

    def _setDoSmartLabels(self, newVal):
        if isinstance(newVal, str):
            nV = newVal.lower()
        else:
            nV = newVal
        assert nV in [True, False, 'semi']
        self._doSmartLabels = nV
    doSmartLabels = property(_getDoSmartLabels, _setDoSmartLabels)

    def _getRootLabelLeft(self):
        return self._rootLabelLeft

    def _setRootLabelLeft(self, newVal):
        assert newVal in [True, False]
        self._rootLabelLeft = newVal
    rootLabelLeft = property(_getRootLabelLeft, _setRootLabelLeft)

    def _getWrapLeafLabelsAt(self):
        return self._wrapLeafLabelsAt

    def _setWrapLeafLabelsAt(self, newVal):
        if newVal is None:
            self._wrapLeafLabelsAt = newVal
        elif newVal == 'commas':
            self._wrapLeafLabelsAt = newVal
        elif newVal == 'comma':
            self._wrapLeafLabelsAt = 'commas'
        else:
            try:
                nV = float(newVal)
                self._wrapLeafLabelsAt = nV
            except ValueError:
                raise GramError(
                    "_setWrapLeafLabelAt(), should be None, 'commas', or a number.  Got %s" % newVal)
    wrapLeafLabelsAt = property(_getWrapLeafLabelsAt, _setWrapLeafLabelsAt)

    def setBranchLabel(self, theNode, theText):
        n = theNode
        assert self.tree
        assert n in self.tree.nodes
        assert n.parent
        assert n.cA
        #assert n.cB

        n.br.label = GramText(theText)
        n.br.label.cA = GramCoord()
        n.br.label.cA.xPosn = n.cB.xPosn + (n.cA.xPosn - n.cB.xPosn) / 2.
        n.br.label.cA.yPosn = n.cB.yPosn + (n.cA.yPosn - n.cB.yPosn) / 2.
        n.br.label.style = 'branch'
        n.br.label.anchor = 'south'

    def setBranchULabel(self, theNode, theText):
        n = theNode
        assert self.tree
        assert n in self.tree.nodes
        assert n.parent
        assert n.cA
        #assert n.cB

        n.br.uLabel = GramText(theText)
        n.br.uLabel.cA = GramCoord()
        n.br.uLabel.cA.xPosn = n.cB.xPosn + (n.cA.xPosn - n.cB.xPosn) / 2.
        n.br.uLabel.cA.yPosn = n.cB.yPosn + (n.cA.yPosn - n.cB.yPosn) / 2.
        n.br.uLabel.style = 'branch'
        n.br.uLabel.anchor = 'north'

    # def setTitle(self, theTitle, xOffset=0., yOffset=0.):
    #     self._title = GramText(theTitle)
    #     self.title.cA = GramCoord(0, 0, 'title')
    #     self.title.textSize = 'Large'
    #     self.title.anchor = 'south west'

    #     self.title.xOffset = xOffset
    #     self.title.yOffset = yOffset

    def setScaleBar(self, length=None, xOffset=0, yOffset=0):

        # If length is None, make a guess
        if length is None:
            rootToTip = 0.0
            for n in self.tree.root.iterLeaves():
                thisRootToTip = 0.0
                n2 = n
                while n2 != self.tree.root:
                    thisRootToTip += n2.br.len
                    n2 = n2.parent
                if thisRootToTip > rootToTip:
                    rootToTip = thisRootToTip
            # print "rootToTip =", rootToTip

            # We want the scale bar to be about 20% of the rootToTip
            x = 0.2 * rootToTip
            order = 0
            while x < 1.0:
                x *= 10.0
                order -= 1
            while x > 10.0:
                x /= 10.0
                order += 1
            # print "x =', x, 'order =", order

            if x > 7.5:
                x = 1.0
                order += 1
            elif x > 3.0:
                x = 5.0
            elif x > 1.5:
                x = 2.0
            else:
                x = 1.0
            # print "x =', x, 'order =", order

            while order < 0:
                x /= 10.0
                order += 1
            while order > 0:
                x *= 10.0
                order -= 1
            # print "x =', x, 'order =", order
            length = x

        self._scaleBar = TreeGramScaleBar(self, length, xOffset, yOffset)

    def setBrokenBranch(self, nodeSpecifier):
        theNode = self.tree.node(nodeSpecifier)
        self.brokenBranches.append(TreeGramBrokenBranch(self, theNode))

    def extraYSpaceAtNode(self, nodeSpecifier, extra):
        theNode = self.tree.node(nodeSpecifier)
        extr = float(extra) / self.yScale

        # adjust yPosn0
        for n in self.tree.iterLeavesNoRoot():
            n.yPosn0 += extr
            if n == theNode:
                n.yPosn0 -= (0.5 * extr)
                break

        for n in self.tree.iterPostOrder():
            if not n.isLeaf:
                n.yPosn0 = (
                    n.leftChild.yPosn0 + n.rightmostChild().yPosn0) / 2.0

        # terminal root
        if self.tree.root.isLeaf:
            self.tree.root.yPosn0 = self.tree.root.leftChild.yPosn0

        if 0:
            print("index   isLeaf        xPosn0        yPosn0")
            for n in self.tree.iterNodes():
                print("%4i" % n.nodeNum, end=' ')
                print("%8i" % n.isLeaf, end=' ')
                print("%12s" % n.xPosn0, end=' ')
                print("%12s" % n.yPosn0)
            # print self.leaves
            # sys.exit()

        # Adjust coordinates for the nodes.
        for n in self.tree.iterNodes():
            n.cA.yPosn = n.yPosn0 * self.yScale
            if n.parent:
                n.cB.yPosn = n.yPosn0 * self.yScale

    def setBracket(self, upperNodeSpecifier, lowerNodeSpecifier, text=None, leftNode=None, rotated=False):
        uN = self.tree.node(upperNodeSpecifier)
        assert uN.isLeaf, "setBracket(). The bottomNode must be a leaf."
        lN = self.tree.node(lowerNodeSpecifier)
        assert lN.isLeaf, "The topNode must be a leaf."
        assert uN.yPosn0 >= lN.yPosn0, "setBracket(). The upperNode must be higher than the lowerNode."
        if leftNode is not None:
            lftN = self.tree.node(leftNode)
            assert not lftN.isLeaf, "setBracket(). The leftNode should be an internal node."
        else:
            lftN = None
        uN.bracket = TreeGramBracket(self, uN, lN, text, lftN, rotated)
        self.brackets.append(uN.bracket)
        return uN.bracket

    def setThickBranch(self, nodeSpecifier, thickness, colour):
        theNode = self.tree.node(nodeSpecifier)
        theNode.thickBranch = TreeGramThickBranch(self, theNode, thickness, colour)
        self.thickBranches.append(theNode.thickBranch)

    def setNodeConfidenceBox(self, theNode):
        # print "%3i  %.1f  %.1f %.1f" % (theNode.nodeNum, theNode.height,
        # theNode.height_95_HPD[0], theNode.height_95_HPD[1])
        up = theNode.height - theNode.height_95_HPD[0]
        down = theNode.height_95_HPD[1] - theNode.height
        theNode.cBox = TreeGramNodeConfidenceBox(self, theNode, down, up)
        self.cBoxes.append(theNode.cBox)

    def setBuiltInTikzStyles(self):

        g = GramText('Xxy')
        g.cA = GramCoord(0, 0)
        g.name = 'leaf'
        g.anchor = 'west'
        g.textSize = self.leafLabelSize
        g.innerSep = 0.13
        if self.engine in ['tikz']:
            g.setBB()
        Gram._styleDict[g.name] = g

        g = GramText('Xxy')
        g.cA = GramCoord(0, 0)
        g.name = 'root'
        g.anchor = 'east'
        g.textSize = self.leafLabelSize
        if self.engine in ['tikz']:
            g.setBB()
        Gram._styleDict[g.name] = g

        g = GramText('Xxy')
        g.cA = GramCoord(0, 0)
        g.name = 'node right'
        g.anchor = 'west'
        g.textSize = self.internalNodeLabelSize
        g.innerSep = 0.03
        if self.engine in ['tikz']:
            g.setBB()
        Gram._styleDict[g.name] = g

        g = GramText('Xxy')
        g.cA = GramCoord(0, 0)
        g.name = 'node upper right'
        g.anchor = 'south west'
        g.textSize = self.internalNodeLabelSize
        g.innerSep = 0.03
        if self.engine in ['tikz']:
            g.setBB()
        Gram._styleDict[g.name] = g

        g = GramText('Xxy')
        g.cA = GramCoord(0, 0)
        g.name = 'node lower right'
        g.anchor = 'north west'
        g.textSize = self.internalNodeLabelSize
        g.innerSep = 0.03
        if self.engine in ['tikz']:
            g.setBB()
        Gram._styleDict[g.name] = g

        g = GramText('Xxy')
        g.cA = GramCoord(0, 0)
        g.name = 'node upper left'
        g.anchor = 'south east'
        g.textSize = self.internalNodeLabelSize
        g.innerSep = 0.03
        if self.engine in ['tikz']:
            g.setBB()
        if self.doLiningNumeralsHack:
            if self.engine in ['svg']:
                # svg text does not know at this point what yuh is.
                # So we have to figure it out now.
                myTextSizeStr = g.getTextSize()
                if myTextSizeStr is None or myTextSizeStr == 'normalsize':
                    myTextSizeCm = g.svgTextNormalsize
                else:
                    myTextSizeCm = g.fontSizeMultiplierDict[
                        myTextSizeStr] * g.svgTextNormalsize
                if self.font == 'helvetica':
                    xYuh = 0.20
                elif self.font == 'palatino':
                    xYuh = 0.27
                elif self.font == 'times':
                    xYuh = 0.22
                elif self.font == 'cm':
                    raise GramError("TreeGram.setBuiltInTikzStyles() svg does not work with cm")
                g.yuh = xYuh * myTextSizeCm
            # Now both tikz and svg have yuh set, and we can do the hack
            print("TreeGram.setBuiltInTikzStyles doLiningNumeralsHack; yuh is %f" % g.yuh)
            g.yShift = -0.4 * g.yuh
        Gram._styleDict[g.name] = g

        g = GramText('Xxy')
        g.cA = GramCoord(0, 0)
        g.name = 'node lower left'
        g.anchor = 'north east'
        g.textSize = self.internalNodeLabelSize
        g.innerSep = 0.03
        if self.engine in ['tikz']:
            g.setBB()
        if self.doLiningNumeralsHack:
            if self.engine in ['svg']:
                # svg text does not know at this point what yuh is.
                # So we have to figure it out now.
                myTextSizeStr = g.getTextSize()
                if myTextSizeStr is None or myTextSizeStr == 'normalsize':
                    myTextSizeCm = g.svgTextNormalsize
                else:
                    myTextSizeCm = g.fontSizeMultiplierDict[
                        myTextSizeStr] * g.svgTextNormalsize
                if self.font == 'helvetica':
                    xYuh = 0.20
                elif self.font == 'palatino':
                    xYuh = 0.27
                elif self.font == 'times':
                    xYuh = 0.22
                g.yuh = xYuh * myTextSizeCm
            # Now both tikz and svg have yuh set, and we can do the hack
            print("TreeGram.setBuiltInTikzStyles doLiningNumeralsHack; yuh is %f" % g.yuh)
            g.yShift = -0.4 * g.yuh
        Gram._styleDict[g.name] = g

        g = GramText('Xxy')
        g.cA = GramCoord(0, 0)
        g.name = 'branch'
        g.textSize = self.branchLabelSize
        g.innerSep = 0.025
        #g.anchor = 'south'
        if self.engine in ['tikz']:
            g.setBB()
        Gram._styleDict[g.name] = g

        g = GramText('Xxy')
        g.cA = GramCoord(0, 0)
        g.name = 'bracket label'
        g.anchor = 'west'
        g.textSize = self.leafLabelSize
        g.innerSep = 0.2
        if self.engine in ['tikz']:
            g.setBB()
        #g.rotate = 90
        Gram._styleDict[g.name] = g

        # Don't use this, as it does not work with tweaking.  Rotate must be after xShift or yShift.
        #g = GramText('Xxy')
        #g.cA = GramCoord(0,0)
        #g.name = 'bracket label rotated'
        #g.anchor = 'north'
        #g.textSize = self.leafLabelSize
        #g.innerSep = 0.1
        #g.rotate = 90
        # g.setBB()
        #Gram._styleDict[g.name] = g

        #g = GramLine(GramCoord(0,0), GramCoord(1,1))
        #g.name = 'vline'
        #g.lineThickness = self.tgDefaultLineThickness
        #g.cap = 'rect'
        #Gram._styleDict[g.name] = g

        del(g)
        ######################################################################
        ######################################################################
        ######################################################################

    def setPositions(self):

        Gram.setPositions(self)
        self.tikzPictureDefaults.lineThickness = self.tgDefaultLineThickness
        #self.tikzPictureDefaults.innerSep = self.defaultInnerSep

        # In case the scale has been re-set by the user ...
        for n in self.tree.iterNodes():
            n.cA.xPosn = n.xPosn0 * self.scale
            n.cA.yPosn = n.yPosn0 * self.yScale
            if n.parent:
                n.cB.xPosn = n.parent.xPosn0 * self.scale
                n.cB.yPosn = n.yPosn0 * self.yScale

        if self.wrapLeafLabelsAt:
            if self.wrapLeafLabelsAt == 'commas':
                #raise GramError("no workee! fix me!")
                for n in self.tree.iterLeavesNoRoot():
                    if self.engine in ['tikz']:
                        n.label.setBB()
                    #print "%s  textDepth %s" % (n.label.rawText, n.label.textDepth)
                    if ',' in n.label.rawText:
                        print("wrap", n.label.rawText)
                        oldHeight = n.label.bb[3] - n.label.bb[1]
                        #n.label.rawText = n.label.rawText.replace(", ", ",\n")
                        n.label.rawText = ",\n".join([aLine.strip() for aLine in n.label.rawText.split(',')])
                        n.label.textWidth = n.label.getBiggestWidth()
                        n.label.rawText = n.label.rawText.replace(
                            ",\n", r",\\")
                        n.label.style = None
                        #n.label.draw = True
                        n.label.textJustification = 'badly ragged'
                        n.label.textSize = self.leafLabelSize
                        n.label.anchor = 'west'
                        n.label.setCookedText()
                        n.label.setTextLengthHeightAndMetrics()
                        if self.engine in ['tikz']:
                            n.label.setBB()
                        newHeight = n.label.bb[3] - n.label.bb[1]
                        # print "bb is %s, newHeight is %f" % (n.label.bb, newHeight)
                        # sys.exit()
                        theExtra = newHeight - oldHeight
                        self.extraYSpaceAtNode(n, extra=theExtra)
                    #print "%s  textDepth %s" % (n.label.rawText, n.label.textDepth)

            else:
                for n in self.tree.iterLeavesNoRoot():
                    if self.engine in ['tikz']:
                        n.label.setBB()
                    theLen = n.label.bb[2] - n.label.bb[0]
                    if theLen > self.wrapLeafLabelsAt:
                        oldHeight = n.label.bb[3] - n.label.bb[1]

                        # Bad hack!  Color etc is ignored!  Bah!
                        #savedSize = self.leafLabelSize
                        # if n.label.style:
                        #    savedSize = n.label.style.textSize

                        n.label.style = None
                        n.label.textWidth = self.wrapLeafLabelsAt
                        n.label.textJustification = 'badly ragged'
                        n.label.textSize = self.leafLabelSize
                        #n.label.textSize = savedSize
                        n.label.anchor = 'west'
                        n.label.setCookedText()
                        n.label.setTextLengthHeightAndMetrics()
                        if self.engine in ['tikz']:
                            n.label.setBB()
                        newHeight = n.label.bb[3] - n.label.bb[1]
                        # print "bb is %s, newHeight is %f" % (n.label.bb, newHeight)
                        # sys.exit()
                        theExtra = newHeight - oldHeight
                        self.extraYSpaceAtNode(n, extra=theExtra)

        # Node.br.label and Node.br.uLabel
        for n in self.tree.iterNodes():
            if n.br and n.br.label:
                n.br.label.cA.xPosn = n.cB.xPosn + \
                    (n.cA.xPosn - n.cB.xPosn) / 2.
                n.br.label.cA.yPosn = n.cB.yPosn + \
                    (n.cA.yPosn - n.cB.yPosn) / 2.
            if n.br and n.br.uLabel:
                n.br.uLabel.cA.xPosn = n.cB.xPosn + \
                    (n.cA.xPosn - n.cB.xPosn) / 2.
                n.br.uLabel.cA.yPosn = n.cB.yPosn + \
                    (n.cA.yPosn - n.cB.yPosn) / 2.

        if self.doSmartLabels:  # Either True or 'semi'
            print("TreeGram.setPositions().  doSmartLabels is %s" % self.doSmartLabels)
            for n in self.tree.iterInternalsNoRoot():
                if n.label:

                    # Rearrange internal node labels for better legibility

                    # (Of course if there are br.name's or br.uName's, they might
                    # get in the way.)

                    # The rules are:

                    # The label goes on top of the branch, just behind the node,
                    # unless the label is too long.

                    # If the label is too long, then where it goes depends on the
                    # node.  If the node is the left child of its parent, then the
                    # (too long) label stays on top of the branch anyway.  If the
                    # node is a rightmost child then the (too long) label gets put
                    # under the line, just behind the node.  For other nodes, that
                    # are not rightmost children, the (too long) label gets put on
                    # the right of the node.  In that case, if there are an odd
                    # number of children then it is nudged up a little to avoid
                    # being put directly on top of a line.

                    # New -- 'semi'-smart.  If the label is
                    # too long for the branch, then it goes on
                    # the right.

                    # print("n %2i %s        %s" % (n.nodeNum,n.label.style, n.label.myStyle))
                    if self.doSmartLabels is True:
                        if n.parent.leftChild == n:
                            n.label.style = 'node upper left'
                        else:
                            if self.engine in ['tikz']:
                                n.label.setBB()
                            theLabelLen = n.label.bb[2] - n.label.bb[0]
                            if self.engine == 'svg':
                                theLabelLen += 0.1  # a mm
                            theBrLen = n.cA.xPosn - n.parent.cA.xPosn
                            # print("theLabelLen %.3f     theBrLen  %.3f" %(theLabelLen, theBrLen))
                            if theLabelLen <= theBrLen:
                                # print "The label is short enough, so it goes
                                # on upper left (anchor='')."
                                n.label.style = 'node upper left'
                            else:
                                # print "The label is too long.  ",
                                if n.parent.rightmostChild() == n:
                                    n.label.style = 'node lower left'
                                else:
                                    # print "Put it on the right of the node
                                    # (anchor='' or '')."
                                    n.label.style = 'node right'
                                    nChildren = n.getNChildren()
                                    if (nChildren % 2) == 1:
                                        n.label.style = 'node upper right'
                    elif self.doSmartLabels == 'semi':
                        if self.engine in ['tikz']:
                            n.label.setBB()
                        theLabelLen = n.label.bb[2] - n.label.bb[0]
                        if self.engine == 'svg':
                            theLabelLen += 0.1  # a mm
                        theBrLen = n.cA.xPosn - n.parent.cA.xPosn
                        if theLabelLen <= theBrLen:
                            # print "The label is short enough, so it goes on
                            # upper left (anchor='')."
                            n.label.style = 'node upper left'
                        else:
                            n.label.style = 'node right'
                            nChildren = n.getNChildren()
                            if (nChildren % 2) == 1:
                                n.label.style = 'node upper right'

        # if self.fixOverlaps and not self.haveFixedOverlaps:
        #    self.doFixOverlaps()
        #    self.haveFixedOverlaps = True

        if self.brackets:
            for b in self.brackets:
                b.setRight()
            biggestRight = self.brackets[0].right
            for b in self.brackets:
                if b.right > biggestRight:
                    biggestRight = b.right
            for b in self.brackets:
                b.alignedRight = biggestRight
            for b in self.brackets:
                b.setPositions()

        # thickBranches
        if self.thickBranches:
            print("There are %i thickBranches!" % len(self.thickBranches))
            for b in self.thickBranches:
                b.setPositions()

        # node confidence boxes
        if self.cBoxes:
            for b in self.cBoxes:
                b.setPositions()

        if self.brokenBranches:
            for bb in self.brokenBranches:
                bb.setPositions()

        # if self.title:
        #     self.setTitlePosition()

        if self.scaleBar:
            # This next line is here for TreeGramRadial, where it actually does
            # something.
            self.setScaleBarPosition()
            #self.scaleBar.cA.xPosn = self.scaleBar.xOffset
            #self.scaleBar.cA.yPosn = (0.5 * self.yScale) + self.scaleBar.yOffset
            self.scaleBar.setPositions()            
                
        print("Finished TreeGram.setPositions()")

    def getAllGramTexts(self):
        # to feed into fixTextOverlaps()

        tbb = []
        for n in self.tree.iterNodes():
            if n.label:
                tbb.append(n.label)
            if n.br and n.br.label:
                tbb.append(n.br.label)
            if n.br and n.br.uLabel:
                tbb.append(n.br.uLabel)

        return tbb

    # def setTitlePosition(self):
    #     self.title.cA.xPosn = 0.0 + self.title.xOffset
    #     if self.tree.root.isLeaf:
    #         nRightLeaves = self.tree.nTax - 1
    #     else:
    #         nRightLeaves = self.tree.nTax
    #     self.title.cA.yPosn = (
    #         (nRightLeaves - 1) * self.yScale) + (1. * self.yScale) + self.title.yOffset

    def setScaleBarPosition(self):
        pass

    def getTikz(self):

        l = self.tree.textDrawList(showInternalNodeNames=1, addToBrLen=0.2, width=None,
                                   autoIncreaseWidth=True, showNodeNums=1, partNum=0, model=False)
        ss = ["%% %s" % x for x in l]
        #s = '\n'.join(["%% %s" % x for x in l])
        ss.append('')
        ss.append("%% The scale is %f, and the yScale is %f" %
                  (self.scale, self.yScale))

        if self.graphics:
            ss.append('')
            ss.append("%% GramGraphics in the graphics list")
            for gr in self.graphics:
                ss.append(gr.getTikz())

        ss.append('')
        ss.append("%% Coordinates of nodes.")
        hasInternalNodeNames = False
        hasBranchNames = False

        for n in self.tree.iterNodes():
            ss.append(n.cA.getTikz())
            
            # A trick to accommodate TreeGramRadial trees, where n.label.cA is
            # not the same as n.cA.
            if n.label and n.label.cA != n.cA:
                ss.append(n.label.cA.getTikz())
                
            if n.cB:
                ss.append(n.cB.getTikz())
            if not n.isLeaf and n.name:
                hasInternalNodeNames = True
            if n.br and (n.br.label or n.br.uLabel):
                hasBranchNames = True

        if self.brackets:
            ss.append('')
            ss.append("%% brackets, behind everything, so first")
            for b in self.brackets:
                ss.append(b.getTikz())

        if self.cBoxes:
            ss.append('')
            ss.append("%% node confidence boxes")
            for b in self.cBoxes:
                ss.append(b.getTikz())

        if self.doVLines:
            ss.append('')
            ss.append("%% horizontal lines")
            for n in self.tree.iterNodes():
                if n.line:
                    ss.append(n.line.getTikz())

            ss.append('')
            ss.append("%% vertical lines")
            for n in self.tree.iterNodes():
                if n.vLine:
                    ss.append(n.vLine.getTikz())
        else:
            ss.append('')
            ss.append("%% branchlines")
            for n in self.tree.iterNodes():
                if n.line:
                    ss.append(n.line.getTikz())

        if self.brokenBranches:
            ss.append('')
            ss.append("%% broken branches")
            for bb in self.brokenBranches:
                ss.append(bb.getTikz())

        if self.thickBranches:
            ss.append('')
            ss.append("%% thickBranches, in front, so after")
            for b in self.thickBranches:
                ss.append(b.getTikz())



        ss.append('')
        ss.append("%% leaf labels")
        for n in self.tree.iterLeavesNoRoot():
            if n.label:
                ss.append(n.label.getTikz())
        n = self.tree.root
        if n.label:
            ss.append('')
            ss.append("%% root label")
            ss.append(n.label.getTikz())

        if hasInternalNodeNames:
            ss.append('')
            ss.append("%% internal node labels (doSmartLabels is %s)" %
                      self.doSmartLabels)
            for n in self.tree.iterInternalsNoRoot():
                if n.label:
                    ss.append(n.label.getTikz())

        if hasBranchNames:
            ss.append('')
            ss.append("%% branch labels")
            for n in self.tree.iterNodesNoRoot():
                if n.br:
                    if n.br.label:
                        ss.append(n.br.label.getTikz())
                    if n.br.uLabel:
                        ss.append(n.br.uLabel.getTikz())

        if self.scaleBar:
            ss.append('')
            ss.append("%% scale bar")
            ss.append(self.scaleBar.getTikz())

        # if self.title:
        #     ss.append('')
        #     ss.append("%% title")
        #     ss.append(self.title.cA.getTikz())
        #     ss.append(self.title.getTikz())

        if self.showNodeNums:
            ss.append('')
            ss.append("%% node numbers")
            for n in self.tree.iterNodes():
                ss.append(n.nodeNumLabel.getTikz())

        ss.append('')
        return '\n'.join(ss)

    def getSvg(self):

        # l = self.tree.textDrawList(showInternalNodeNames=1, addToBrLen=0.2, width=None,
        #                    autoIncreaseWidth=True, showNodeNums=1, partNum=0, model=False)
        # ss = ["%% %s" % x for x in l]
        # #s = '\n'.join(["%% %s" % x for x in l])
        # ss.append('')
        # ss.append("%% The scale is %f, and the yScale is %f" % (self.scale, self.yScale))
        # ss.append('')
        # ss.append("%% Coordinates of nodes.")
        ss = []
        hasInternalNodeNames = False
        hasBranchNames = False

        #print "TreeGram.getSvg() here"

        for gr in self.graphics:
            ss.append(gr.getSvg())

        for n in self.tree.iterNodes():
            # ss.append(n.cA.getSvg())
            # if n.cB:
            #     ss.append(n.cB.getSvg())
            if not n.isLeaf and n.name:
                hasInternalNodeNames = True
            if n.br and (n.br.label or n.br.uLabel):
                hasBranchNames = True

        if self.brackets:
            ss.append('')
            ss.append("<!--  brackets, behind everything, so first. -->")
            for b in self.brackets:
                ss.append(b.getSvg())

        if self.cBoxes:
            ss.append('')
            ss.append("<!--  node confidence boxes.  -->")
            for b in self.cBoxes:
                ss.append(b.getSvg())

        if self.doVLines:
            ss.append('')
            ss.append("<!--  horizontal lines  -->")
            for n in self.tree.iterNodes():
                if n.line:
                    ss.append(n.line.getSvg())

            ss.append('')
            ss.append("<!--  vertical lines -->")
            for n in self.tree.iterNodes():
                if n.vLine:
                    ss.append(n.vLine.getSvg())
        else:
            ss.append('')
            ss.append("<!--  branchlines -->")
            for n in self.tree.iterNodes():
                if n.line:
                    ss.append(n.line.getSvg())

        if self.brokenBranches:
            ss.append('')
            ss.append("<!--  broken branches -->")
            for bb in self.brokenBranches:
                ss.append(bb.getSvg())

        ss.append('')
        ss.append("<!--  leaf labels -->")
        for n in self.tree.iterLeavesNoRoot():
            if n.label:
                ss.append(n.label.getSvg())
        n = self.tree.root
        if n.label:
            ss.append('')
            ss.append("<!--   root label -->")
            ss.append(n.label.getSvg())

        if hasInternalNodeNames:
            ss.append('')
            ss.append(
                "<!--   internal node labels (doSmartLabels is %s) -->" % self.doSmartLabels)
            for n in self.tree.iterInternalsNoRoot():
                if n.label:
                    ss.append(n.label.getSvg())

        if hasBranchNames:
            ss.append('')
            ss.append("<!--  branch labels -->")
            for n in self.tree.iterNodesNoRoot():
                if n.br.label:
                    ss.append(n.br.label.getSvg())
                if n.br.uLabel:
                    ss.append(n.br.uLabel.getSvg())

        if self.scaleBar:
            ss.append('')
            ss.append("<!--   scale bar -->")
            ss.append(self.scaleBar.getSvg())

        # if self.title:
        #     ss.append('')
        #     ss.append("<!--  title -->")
        #     ss.append(self.title.cA.getSvg())
        #     ss.append(self.title.getSvg())

        if self.showNodeNums:
            ss.append('')
            ss.append("<!-- node numbers -->")
            for n in self.tree.iterNodes():
                ss.append(n.nodeNumLabel.getSvg())

        ss.append('')
        return '\n'.join(ss)


    def calcBigBoundingBox(self):
        if self.engine == 'tikz':
            print("TreeGram.tikzCalcBigBoundingBox() is turned off.")
            #self.tikzCalcBigBoundingBox()
        else:
            assert self.engine == 'svg'
            self.svgCalcBigBoundingBox()

    def tikzCalcBigBoundingBox(self):
        # print "TreeGram.calcBigBoundingBox().  self is %s" % self
        n = self.tree.root
        self.bbb[0] = n.cA.xPosn - 0.1
        self.bbb[1] = n.cA.yPosn - 0.1
        self.bbb[2] = n.cA.xPosn + 0.1
        self.bbb[3] = n.cA.yPosn + 0.1

        for n in self.tree.iterNodes():
            if n.name:
                g = n.label
                g.setBB()
                self.adjustBBBFromGraphicBB(g)

            if n.br and hasattr(n.br, 'textBox') and n.br.textBox:
                g = n.br.textBox
                g.setBB()
                self.adjustBBBFromGraphicBB(g)

        if self.brackets:
            for b in self.brackets:
                g = b.label
                g.setBB()
                self.adjustBBBFromGraphicBB(g)

        if self.cBoxes:
            for g in self.cBoxes:
                g.setBB()
                self.adjustBBBFromGraphicBB(g)

        if self.scaleBar:
            g = self.scaleBar
            g.setBB()
            self.adjustBBBFromGraphicBB(g)

        if self.showNodeNums:
            for n in self.tree.iterNodes():
                g = n.nodeNumLabel
                self.adjustBBBFromGraphicBB(g)

        for g in self.graphics:
            if isinstance(g, GramCoord):
                pass
            elif isinstance(g, GramCode):
                pass
            else:
                g.setBB()
                self.adjustBBBFromGraphicBB(g)

        for g in self.grams:
            # print  g
            g.calcBigBoundingBox()
            if (g.bbb[0] + g.gX) < self.bbb[0]:
                self.bbb[0] = (g.bbb[0] + g.gX)
            if (g.bbb[1] + g.gY) < self.bbb[1]:
                self.bbb[1] = (g.bbb[1] + g.gY)
            if (g.bbb[2] + g.gX) > self.bbb[2]:
                self.bbb[2] = (g.bbb[2] + g.gX)
            if (g.bbb[3] + g.gY) > self.bbb[3]:
                self.bbb[3] = (g.bbb[3] + g.gY)

        # print "=========== (TreeGram) end of calcBigBoundingBox()  final bbb
        # is %s" % self.bbb



class TreeGramGraphic(TreeGram, GramGraphic):

    def __init__(self):
        # TreeGram.__init__(self)
        GramGraphic.__init__(self)

        # print "===== TreeGramGraphic.setPositions == GramGraphic.setPositions %s" % (     True
        #    TreeGramGraphic.setPositions == GramGraphic.setPositions)
        # print "===== TreeGramGraphic.setPositions == TreeGram.setPositions %s" % (      False
        #    TreeGramGraphic.setPositions == TreeGram.setPositions)
        # print "===== TreeGramGraphic.setBB == GramGraphic.setBB %s" % (                    True
        #    TreeGramGraphic.setBB == GramGraphic.setBB)
        # print "===== TreeGramGraphic.setBB == TreeGram.setBB %s" % (                      False
        #    TreeGramGraphic.setBB == TreeGram.setBB)


class TreeGramScaleBar(GramText, TreeGramGraphic):

    def __init__(self, treeGram, barLength, xOffset, yOffset):
        GramText.__init__(self, '%s' % barLength)
        TreeGramGraphic.__init__(self)
        self.tg = treeGram
        self.barLength = barLength
        self.xOrig = 0.0
        self.yOrig = 0.0
        self.xOffset = xOffset
        self.yOffset = yOffset
        self.cB = GramCoord(xOffset, yOffset, 'sb_B')
        self.cC = GramCoord(
            xOffset + (barLength * self.tg.scale), yOffset, 'sb_C')
        self.line = GramLine(self.cB, self.cC)
        self.cA = GramCoord(
            self.cB.xPosn + ((self.cC.xPosn - self.cB.xPosn) / 2.), yOffset, 'sb_A')
        self.anchor = 'south'
        self.textSize = 'small'

    def setPositions(self):
        # print "TreeGramScaleBar.setPositions() here."
        if not self.xShift:
            theXShift = 0.0
        else:
            theXShift = self.xShift
        if not self.yShift:
            theYShift = 0.0
        else:
            theYShift = self.yShift

        self.cB.xPosn = self.xOrig + self.xOffset + theXShift
        self.cB.yPosn = self.yOrig + self.yOffset + theYShift

        self.cC.xPosn = self.cB.xPosn + (self.barLength * self.tg.scale)
        # print "TreeGramScaleBar.scale is %.3f, barLength is %.3f, cC.xPosn is %.3f" % (
        #    self.scale, self.barLength, self.cC.xPosn)
        self.cC.yPosn = self.cB.yPosn

        self.cA.xPosn = self.cB.xPosn - theXShift + \
            ((self.cC.xPosn - self.cB.xPosn) / 2.)
        self.cA.yPosn = self.cB.yPosn - theYShift

    def getTikz(self):
        ss = []
        ss.append(self.cA.getTikz())
        ss.append(self.cB.getTikz())
        ss.append(self.cC.getTikz())
        ss.append(self.line.getTikz())
        ss.append(GramText.getTikz(self))
        return '\n'.join(ss)

    def getSvg(self):
        ss = []
        ss.append(self.line.getSvg())
        # print "TreeGramScaleBar.getSvg() self.line is %s" % self.line
        # print "TreeGramScaleBar.getSvg() self.line.getSvg is %s" % ss[0]
        ss.append(GramText.getSvg(self))
        # print ss
        return '\n'.join(ss)

    def setBB(self):
        self.line.setBB()
        # print "self.line.bb is %s" % self.line.bb

        GramText.setBB(self)
        g = self.line
        if g.bb[0] < self.bb[0]:
            self.bb[0] = g.bb[0]
        if g.bb[1] < self.bb[1]:
            self.bb[1] = g.bb[1]
        if g.bb[2] > self.bb[2]:
            self.bb[2] = g.bb[2]
        if g.bb[3] > self.bb[3]:
            self.bb[3] = g.bb[3]

class TreeGramBracket(TreeGramGraphic):

    def __init__(self, treeGram, upperNode, lowerNode, text, leftNode, rotated):
        TreeGramGraphic.__init__(self)
        self.tg = treeGram
        self.label = GramText(text)
        self.label.cA = GramCoord(upperNode.cA.xPosn, upperNode.cA.yPosn, 'bx')
        #self.rotated = rotated
        if rotated:
            self.label.style = 'bracket label'
            self.label.anchor = 'north'
            self.label.rotate = 90.      # need to rotate AFTER xShift or yShift
        else:
            self.label.style = 'bracket label'
        self.upperNode = upperNode
        self.lowerNode = lowerNode
        self.leftNode = leftNode
        self.fill = 'Black!5'
        #self.svgFill = 'Black'
        #self.svgFillOpacity = 0.05
        self.bottom = None
        self.top = None
        self.left = None
        self.right = None
        self.alignedRight = None

        self.topOverRide = None  # for top of bracket
        self.bottomOverRide = None  # for bottom of bracket
        self.rightOverRide = None  # for self.right
        self.rightExtra = None

    def setRight(self):
        if self.rightOverRide:
            self.right = self.rightOverRide
        else:
            # Need the bb of the nodel.labels, which of course are not
            # made yet.  So we need to setBB() of each node label
            nodesInGroup = []
            for n in self.tg.tree.iterLeavesNoRoot():
                if n.cA.yPosn <= self.upperNode.cA.yPosn and n.cA.yPosn >= self.lowerNode.cA.yPosn:
                    nodesInGroup.append(n)
                    if self.engine in ['tikz']:
                        n.label.setBB()

            # Now we have the bb of each node label.
            self.right = nodesInGroup[0].label.bb[2]
            for n in nodesInGroup:
                if n.label.bb[2] > self.right:
                    self.right = n.label.bb[2]
            #self.right += 6
            # print "got self.right = %f" % self.right

    def setPositions(self):

        theInnerSep = self.upperNode.label.getInnerSep()
        #if self.engine == 'svg':
        #    theInnerSep = 0.0
        # 0.1 for tikz
        print("TreeGramBracket.setPositions().  got theInnerSep %f" % theInnerSep)
        if self.topOverRide:
            self.top = self.topOverRide
        else:
            self.top = self.upperNode.label.bb[3] - theInnerSep

        if self.bottomOverRide:
            self.bottom = self.bottomOverRide
        else:
            self.bottom = self.lowerNode.label.bb[1] + theInnerSep

        if self.leftNode:
            self.left = self.leftNode.cA.xPosn

        # Find the position of the label
        if self.tg.bracketsLineUp:
            theRight = self.alignedRight
        else:
            theRight = self.right

        # Hack alert.  Compensate 0.1 for svg tight bounding box.
        # Add 0.1 to make it a bit less tight agains the text
        if self.engine == 'svg':
            theRight += 0.2
        if self.engine == 'tikz':
            theRight += 0.1
        if self.rightExtra:
            theRight += self.rightExtra

        self.label.cA.xPosn = theRight
        self.label.cA.yPosn = self.bottom + (0.5 * (self.top - self.bottom))
        if self.engine in ['tikz']:
            self.label.setBB()

        if 0:
            print("bracket a.  self.upperNode is node %i, at (%.3f,%.3f)." % (
                self.upperNode.nodeNum, self.upperNode.label.cA.xPosn, self.upperNode.label.cA.yPosn))
            print("bracket b.  self.lowerNode is node %i, at (%.3f,%.3f)." % (
                self.lowerNode.nodeNum, self.lowerNode.label.cA.xPosn, self.lowerNode.label.cA.yPosn))
            print("bracket c.  self.top is %.3f, self.bottom is %.3f" % (self.top, self.bottom))

    def getTikz(self):
        ss = []
        if self.tg.bracketsLineUp:
            theRight = self.alignedRight
        else:
            theRight = self.right
        if self.rightExtra:
            theRight += self.rightExtra

        # Add 0.1 to make it a bit less tight agains the text
        theRight += 0.1

        if self.leftNode:
            theFill = self.getFill()
            if theFill:
                cA = GramCoord(xPosn=self.left, yPosn=self.bottom)
                cB = GramCoord(xPosn=theRight, yPosn=self.top)
                aRect = GramRect(cA, cB)
                aRect.draw = None
                aRect.fill = theFill
                ssB = aRect.getTikz()
                ss.append(ssB)
        ss.append(r"\draw [thin,line cap=round] (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f) -- (%.3f,%.3f);" % (
            theRight - 0.1, self.top, theRight, self.top, theRight, self.bottom, theRight - 0.1, self.bottom))
        if self.label:
            ss.append(self.label.cA.getTikz())
            ss.append(self.label.getTikz())
        return '\n'.join(ss)

    def getSvg(self):
        ss = []
        if self.tg.bracketsLineUp:
            theRight = self.alignedRight
        else:
            theRight = self.right
        # Hack alert.  Compensate for svg tight bounding box.
        # Add 0.1 to make it a bit less tight agains the text
        theRight += 0.2

        if self.leftNode:
            theFill = self.getFill()
            if theFill:
                cA = GramCoord(xPosn=self.left, yPosn=self.bottom)
                cB = GramCoord(xPosn=theRight, yPosn=self.top)
                aRect = GramRect(cA, cB)
                aRect.draw = None
                aRect.fill = theFill
                ssB = aRect.getSvg()
                ss.append(ssB)
        ss.append('<path d="M%.2f,%.2f L%.2f,%.2f L%.2f,%.2f L%.2f,%.2f" stroke-width="1" fill="none" stroke="black"/>' % (
            (theRight - 0.1) * self.svgPxForCm, -self.top * self.svgPxForCm,
            theRight * self.svgPxForCm, -self.top * self.svgPxForCm,
            theRight * self.svgPxForCm, -self.bottom * self.svgPxForCm,
            (theRight - 0.1) * self.svgPxForCm, -self.bottom * self.svgPxForCm))
        if self.label:
            ss.append(self.label.getSvg())
        return '\n'.join(ss)




class TreeGramThickBranch(TreeGramGraphic):

    def __init__(self, treeGram, theNode, thickness, colour):
        TreeGramGraphic.__init__(self)
        assert theNode.parent
        # self.tg = treeGram
        self.node = theNode
        #self.thickness = thickness
        self.cA = GramCoord(0, 0)
        self.cB = GramCoord(1, 1)

        self.gl = GramLine(self.cA, self.cB)
        self.gl.color = colour
        self.gl.lineThickness = thickness
            

    def setPositions(self):
        self.cA.xPosn = self.node.cA.xPosn
        self.cA.yPosn = self.node.cA.yPosn
        self.cB.xPosn = self.node.parent.cA.xPosn
        self.cB.yPosn = self.node.cA.yPosn
        

    def getTikz(self):
        return self.gl.getTikz()

    def getSvg(self):
        pass

    def setBB(self):
        pass


class TreeGramNodeConfidenceBox(TreeGramGraphic):

    def __init__(self, treeGram, theNode, down, up):
        TreeGramGraphic.__init__(self)
        self.tg = treeGram
        self.node = theNode
        self.down = down
        self.up = up
        self.cA = GramCoord(0, 0)
        self.cB = GramCoord(1, 1)
        self.cBox = GramRect(self.cA, self.cB)
        if self.engine == 'tikz':
            self.cBox.fill = 'black!10'
            self.cBox.draw = 'black!50'
            self.cBox.fill.transparent = True
        elif self.engine == 'svg':
            self.cBox.draw = 'black!50'
            self.cBox.fill = 'black!10'
            self.cBox.fill.transparent = True
            

    def setPositions(self):
        self.cA.xPosn = self.node.cA.xPosn - (self.down * self.tg.scale)
        self.cA.yPosn = self.node.cA.yPosn - 0.1
        self.cB.xPosn = self.node.cA.xPosn + (self.up * self.tg.scale)
        self.cB.yPosn = self.node.cA.yPosn + 0.1

    def getTikz(self):
        return self.cBox.getTikz()

    def getSvg(self):
        return self.cBox.getSvg()

    def setBB(self):
        #theLineThickness = cmForLineThickness(self.getLineThickness())
        #halfLineThick = theLineThickness/2.
        self.bb[0] = self.cA.xPosn  # - halfLineThick
        self.bb[1] = self.cA.yPosn  # - halfLineThick
        self.bb[2] = self.cB.xPosn  # + halfLineThick
        self.bb[3] = self.cB.xPosn  # + halfLineThick
        # print("TreeGramNodeConfidenceBox ")

class TreeGramBrokenBranch(TreeGramGraphic):

    def __init__(self, treeGram, theNode):
        TreeGramGraphic.__init__(self)
        self.tg = treeGram
        self.node = theNode
        self.cA = GramCoord(0, 0)
        self.cB = GramCoord(1, 1)
        self.cAa = GramCoord(0, 0)
        self.cAb = GramCoord(0, 0)
        self.cBa = GramCoord(0, 0)
        self.cBb = GramCoord(0, 0)

        self.glCover = GramLine(self.cA, self.cB)
        self.glCover.colour = 'white'
        self.glCover.lineThickness = 'very thick'
        self.glA = GramLine(self.cAa, self.cAb)
        self.glB = GramLine(self.cBa, self.cBb)

    def setPositions(self):
        # The node branch goes from self.node.cA to self.node.cB
        if isinstance(self, TreeGram):
            # The centre of the node branch line will be
            centre = self.node.cA.xPosn - \
                ((self.node.cA.xPosn - self.node.cB.xPosn) / 2.)
            self.cA.xPosn = centre + 0.04
            self.cA.yPosn = self.node.cA.yPosn
            self.cB.xPosn = centre - 0.04
            self.cB.yPosn = self.node.cB.yPosn
            # print "TreeGramBrokenBranch.setPositions() ... exiting!"
            # sys.exit()

            #self.glA.colour = 'red'
            #self.glB.colour = 'red'

            self.cAa.xPosn = self.cA.xPosn - 0.02
            self.cAa.yPosn = self.cA.yPosn - 0.1
            self.cAb.xPosn = self.cA.xPosn + 0.02
            self.cAb.yPosn = self.cA.yPosn + 0.1

            self.cBa.xPosn = self.cB.xPosn - 0.02
            self.cBa.yPosn = self.cB.yPosn - 0.1
            self.cBb.xPosn = self.cB.xPosn + 0.02
            self.cBb.yPosn = self.cB.yPosn + 0.1

        elif isinstance(self, TreeGramRadial):
            raise GramError("TreeGramRadial is not implemented yet.")

    def getTikz(self):
        ss = []
        ss.append(self.glCover.getTikz())
        ss.append(self.glA.getTikz())
        ss.append(self.glB.getTikz())
        return '\n'.join(ss)

    def getSvg(self):
        ss = []
        ss.append(self.glCover.getSvg())
        ss.append(self.glA.getSvg())
        ss.append(self.glB.getSvg())
        return '\n'.join(ss)

    def setBB(self):
        #theLineThickness = cmForLineThickness(self.getLineThickness())
        #halfLineThick = theLineThickness/2.
        self.bb[0] = self.cB.xPosn  # - halfLineThick
        self.bb[1] = self.cB.yPosn  # - halfLineThick
        self.bb[2] = self.cA.xPosn  # + halfLineThick
        self.bb[3] = self.cA.xPosn  # + halfLineThick
        # print("TreeGramBrokenBranch ")


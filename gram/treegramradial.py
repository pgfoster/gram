from gram.treegram import *
from p4 import func

# drawtree_commands = """
# intree
# p
# l
# v
# n
# y
#"""

if 1:
    x1piOver8 = math.pi / 8.
    x3piOver8 = 3 * x1piOver8
    x5piOver8 = 5 * x1piOver8
    x7piOver8 = 7 * x1piOver8
    x1piOver4 = math.pi / 4.
    xpiOver2 = math.pi / 2.
    x3piOver4 = 3 * x1piOver4


class TreeGramRadial(TreeGram):

    """Make a radial-style tree

    By default this makes a simple radial tree where the 
    leaf branch angles increase monotonically.

    By turning on the arg equalDaylight, it will alternatively 
    use the phylip drawtree program to make an equal daylight 
    tree.  Equal daylight trees often look better for small trees, 
    but might give poor results for bigger trees. 

    maxLinesDim is the size that you want to end up with, in cm,
                of the biggest x or y dimension of the lines
                part of the drawing, excluding the taxNames and
                such.

    """

    # Tree init is
    # def __init__(self, theTree, scale=None, yScale=0.45, showNodeNums=False,
    # widthToHeight=0.67):

    def __init__(self, theTree, scale=None, maxLinesDim=5, rotate=0, slopedBrLabels=True, showNodeNums=False, equalDaylight=False):

        gm = ['TreeGramRadial.__init__()']

        if scale and maxLinesDim:
            # print "Scale is defined, so ignoring maxLinesDim"
            maxLinesDim = None

        savedScale = scale  # TreeGram.__init__() messes with the scale.
        TreeGram.__init__(
            self, theTree, scale=scale, showNodeNums=showNodeNums, doVLines=False)
        # TreeGram.__init__() sets node.xPosn0, which is in hits/site (ie
        # unscaled brLens), node.yPosn0, node.vLine.

        # Also sets self.scale, node.cA (from the node.xPosn0) and
        # node.cB (from the node.parent.xPosn0), node.label (for
        # names), node.br.label and node.br.uLabel, node.line (from cB
        # to cA), node.textBox, and node.nodeNumLabel

        rotate = int(rotate)
        assert rotate >= -360 and rotate <= 360
        #self.leafLabelSize = 'small'
        #self.internalNodeLabelSize = 'tiny'
        #self.internalNodeLabelSize = self.leafLabelSize
        #self.branchLabelSize = 'tiny'
        self.doSmartLabels = False

        self.smallestXPosn0 = 1000000.0
        self.smallestYPosn0 = 1000000.0
        self.biggestXPosn0 = -1000000.0
        self.biggestYPosn0 = -1000000.0

        if maxLinesDim:
            try:
                self.maxLinesDim = float(maxLinesDim)
            except ValueError:
                gm.append("maxLinesDim should be a float.")
                raise GramError(gm)
        else:
            self.maxLinesDim = None

        if not (self.maxLinesDim or savedScale):
            gm.append("Need to set either maxLinesDim or scale.")
            raise GramError(gm)
        if self.maxLinesDim and savedScale:
            gm.append("Need to set either maxLinesDim or scale, but not both.")
            raise GramError(gm)

        if equalDaylight:
            # We need to write some files, but we do not want to over-write.
            if os.path.exists("intree"):
                gm.append("get rid of the 'intree' file")
                raise GramError(gm)
            if os.path.exists("plotfile"):
                gm.append("get rid of the 'plotfile' file")
                raise GramError(gm)
            if os.path.exists("drawTreeCommands"):
                gm.append("get rid of the 'drawTreeCommands' file")
                raise GramError(gm)

        # Make a dupe tree to write to a phylip file, with no internal node
        # names
        if self.tree:
            if equalDaylight:
                dupeTree = self.tree.dupe()
                for n in dupeTree.iterInternalsNoRoot():
                    if n.name:
                        n.name = None
                dupeTree.root.name = None
                # Check for long names before writing phylip tree.
                needsRenaming = False
                for n in dupeTree.iterLeavesNoRoot():
                    if len(n.name) > 10:
                        needsRenaming = True
                        break
                if needsRenaming:
                    dupeTree.renameForPhylip()
                    os.remove('p4_renameForPhylip_dict.py')

                # Do the phylip drawtree command
                dupeTree.writePhylip("intree")
                # sys.exit()
                f = open("drawtree_commands", 'w')
                drawtree_commands2 = "\nintree\np\nl\nv\nn\nr\n%i\ny\n" % rotate
                f.write(drawtree_commands2)
                f.close()
                myCmd = 'drawtree < drawtree_commands > /dev/null'
                os.system(myCmd)
                print("finished doing '%s'" % myCmd)
                assert os.path.exists(
                    "plotfile"), "Something didn't work.  Probably with the drawtree_commands.  Fix me!"
                os.remove("intree")
                os.remove("drawtree_commands")
                f = open("plotfile")
                ll = f.readlines()
                f.close()
                #os.system('open plotfile')
                # sys.exit()
                os.remove("plotfile")
                strokes = []
                ll_indx = 0

                # Now try to get the line info from the plotfile
                while 1:
                    try:
                        l = ll[ll_indx]
                        ll_indx += 1
                    except IndexError:
                        gm.append("could not digest plotfile (I).")
                        raise GramError(gm)
                    l2 = l.strip()
                    if l2.endswith("setlinejoin"):
                        break
                try:
                    l = ll[ll_indx]
                    ll_indx += 1
                except IndexError:
                    gm.append("could not digest plotfile (II).")
                    raise GramError(gm)
                l2 = l.strip()
                if not l2.endswith("newpath"):
                    gm.append("could not digest plotfile (III).")
                    raise GramError(gm)

                i = 0

                # Each node.br (except the root of course) gets a
                # stroke, a list of 4 numbers that are the 2 endpoints
                # of the line
                for n in self.tree.iterPreOrder():
                    if n == self.tree.root:
                        pass
                    else:
                        try:
                            l = ll[ll_indx + i]
                            i += 1
                        except IndexError:
                            gm.append("could not digest plotfile (IV).")
                            raise GramError(gm)
                        l2 = l.strip()
                        if not l2.endswith("l"):
                            gm.append("could not digest plotfile (V).")
                            raise GramError(gm)
                        # print l2
                        splitL2 = l2.split()
                        n.br.stroke = []
                        for j in range(4):
                            if splitL2[j] == 'nan':
                                gm.append(
                                    "could not digest plotfile (VI). -- got nan")
                                raise GramError(gm)
                            try:
                                fl = float(splitL2[j])
                                n.br.stroke.append(fl)
                            except:
                                gm.append("could not digest plotfile (VII).")
                                raise GramError(gm)

            else:  # not equalDaylight
                # self.tree.draw()
                angle_increment = - (2. * math.pi) / self.tree.nTax
                # print "angle_increment = %f" % angle_increment
                if rotate:
                    myAngle = rotate * math.pi / 180.
                else:
                    myAngle = 0.0
                for n in self.tree.iterLeavesNoRoot():
                    n.br.angle = myAngle
                    myAngle += angle_increment
                for n in self.tree.iterInternalsNoRootPostOrder():
                    # print n.nodeNum
                    leftAngle = n.leftChild.br.angle
                    rightAngle = n.rightmostChild().br.angle
                    n.br.angle = ((leftAngle - rightAngle) / 2.) + rightAngle
                for n in self.tree.iterPreOrder():
                    if n == self.tree.root:
                        pass
                    else:
                        n.br.stroke = []
                        # print n.nodeNum, n.br.angle, n.br.len,
                        if n.parent == self.tree.root:
                            n.br.stroke.append(0.)
                            n.br.stroke.append(0.)
                            xyList = func.polar2square([n.br.angle, n.br.len])
                            n.br.stroke += xyList
                        else:
                            n.br.stroke.append(n.parent.br.stroke[2])
                            n.br.stroke.append(n.parent.br.stroke[3])
                            xyList = func.polar2square([n.br.angle, n.br.len])
                            n.br.stroke.append(n.br.stroke[0] + xyList[0])
                            n.br.stroke.append(n.br.stroke[1] + xyList[1])
                        # print n.br.stroke

            llx = 1000000.
            lly = 1000000.
            urx = -1000000.
            ury = -1000000.

            for n in self.tree.iterNodesNoRoot():
                if n.br.stroke[2] < llx:
                    llx = n.br.stroke[2]
                if n.br.stroke[3] < lly:
                    lly = n.br.stroke[3]
                if n.br.stroke[2] > urx:
                    urx = n.br.stroke[2]
                if n.br.stroke[3] > ury:
                    ury = n.br.stroke[3]
            # print "a current bb is %.3f %.3f %.3f %.3f " % (llx, lly, urx,
            # ury)

            twoDims = [urx - llx, ury - lly]
            theMaxDim = max(twoDims)
            # print "The two dims are %.3f %.3f, max %.3f " % (twoDims[0],
            # twoDims[1], theMaxDim)

            # 1 PostScript point = 0.35277138 mm
            # cmPerPoint = 0.035277138
            if self.maxLinesDim:
                theFactor = self.maxLinesDim / theMaxDim

                # print "maxLinesDim set to %.1f, so multiplying all the node locations by %.3f" % (
                #    self.maxLinesDim, theFactor)
                for n in self.tree.iterNodesNoRoot():
                    for i in range(4):
                        n.br.stroke[i] *= theFactor

                if 1:  # Check
                    llx = 1000000.
                    lly = 1000000.
                    urx = -1000000.
                    ury = -1000000.

                    for n in self.tree.iterNodesNoRoot():
                        if n.br.stroke[2] < llx:
                            llx = n.br.stroke[2]
                        if n.br.stroke[3] < lly:
                            lly = n.br.stroke[3]
                        if n.br.stroke[2] > urx:
                            urx = n.br.stroke[2]
                        if n.br.stroke[3] > ury:
                            ury = n.br.stroke[3]
                    # print "b current bb is %.3f %.3f %.3f %.3f " % (llx, lly,
                    # urx, ury)
                    twoDims = [urx - llx, ury - lly]
                    theMaxDim = max(twoDims)
                    # print "The two dims are %.3f %.3f, max %.3f " %
                    # (twoDims[0], twoDims[1], theMaxDim)

                treeLengthOnTree = self.tree.getLen()
                treeLengthFromStrokes = 0.0
                for n in self.tree.iterNodesNoRoot():
                    aStroke = math.sqrt(((n.br.stroke[0] - n.br.stroke[2]) * (n.br.stroke[0] - n.br.stroke[2])) +
                                        ((n.br.stroke[1] - n.br.stroke[3]) * (n.br.stroke[1] - n.br.stroke[3])))
                    # print "node %i   %s" % (n.nodeNum, aStroke)
                    treeLengthFromStrokes += aStroke
                # print "the treeLengthOnTree is %f, the treeLengthFromStrokes is %.2f" % (
                #    treeLengthOnTree, treeLengthFromStrokes)

                self.scale = treeLengthFromStrokes / treeLengthOnTree
                self.yScale = self.scale
                print("maxLinesDim=%.1f, scale set to %.2f" % (self.maxLinesDim, self.scale))

            elif savedScale:
                treeLengthOnTree = self.tree.getLen()

                treeLengthFromStrokes = 0.0
                for n in self.tree.iterNodesNoRoot():
                    aStroke = math.sqrt(((n.br.stroke[0] - n.br.stroke[2]) * (n.br.stroke[0] - n.br.stroke[2])) +
                                        ((n.br.stroke[1] - n.br.stroke[3]) * (n.br.stroke[1] - n.br.stroke[3])))
                    # print "node %i   %s" % (n.nodeNum, aStroke)
                    treeLengthFromStrokes += aStroke
                # print "the treeLengthOnTree is %f, the treeLengthFromStrokes is %.2f" % (
                #    treeLengthOnTree, treeLengthFromStrokes)

                theFactor = savedScale / \
                    (treeLengthFromStrokes / treeLengthOnTree)
                # print "multiplying all the node locations by factor %.3f" %
                # theFactor
                for n in self.tree.iterNodesNoRoot():
                    for i in range(4):
                        n.br.stroke[i] *= theFactor

                # check
                treeLengthFromStrokes = 0.0
                for n in self.tree.iterNodesNoRoot():
                    aStroke = math.sqrt(((n.br.stroke[0] - n.br.stroke[2]) * (n.br.stroke[0] - n.br.stroke[2])) +
                                        ((n.br.stroke[1] - n.br.stroke[3]) * (n.br.stroke[1] - n.br.stroke[3])))
                    # print "node %i   %s" % (n.nodeNum, aStroke)
                    treeLengthFromStrokes += aStroke
                # print "the treeLengthOnTree is %f, the treeLengthFromStrokes is %.2f" % (
                #    treeLengthOnTree, treeLengthFromStrokes)

                self.scale = treeLengthFromStrokes / treeLengthOnTree
                assert math.fabs(
                    savedScale - self.scale) < 0.01, "Bad scale calc.  Fix me!"
                self.yScale = self.scale

                # print "given scale %.2f" % self.scale  # No need for this --
                # TreeGram.__init__() speaks it.

            # check
            for n in self.tree.iterNodesNoRoot():
                theStrokeLen = math.sqrt(((n.br.stroke[0] - n.br.stroke[2]) * (n.br.stroke[0] - n.br.stroke[2])) +
                                         ((n.br.stroke[1] - n.br.stroke[3]) * (n.br.stroke[1] - n.br.stroke[3])))
                theBrLen = n.br.len * self.scale
                # print "a %3i   %.3f" % (n.nodeNum, math.fabs(theStrokeLen -
                # theBrLen))
                if math.fabs(theStrokeLen - theBrLen) > 0.01:
                    gm.append("bad branch length %f %f" %
                              (theStrokeLen, theBrLen))
                    gm.append("node %i" % n.nodeNum)
                    raise GramError(gm)

            # Set coordinates of the nodes.
            for n in self.tree.iterNodesNoRoot():
                # print "node %2i %s" % (n.nodeNum, n.br.stroke)
                #n.cA = GramCoord((n.br.stroke[2] / self.scale), (n.br.stroke[3] / self.scale), 'n%i' % n.nodeNum)
                n.xPosn0 = n.br.stroke[2] / self.scale
                n.cA.xPosn = n.br.stroke[2]
                n.yPosn0 = n.br.stroke[3] / self.scale
                n.cA.yPosn = n.br.stroke[3]

                n.cB.xPosn = n.br.stroke[0]
                n.cB.yPosn = n.br.stroke[1]
                #n.cB = GramCoord((n.br.stroke[0] / self.scale), (n.br.stroke[1] / self.scale), 'n%ip' % n.nodeNum)
                #n.cB = None
                #n.cRef = GramCoord(n.cA.xPosn, n.cA.yPosn)
                if n.xPosn0 < self.smallestXPosn0:
                    self.smallestXPosn0 = n.xPosn0
                if n.yPosn0 < self.smallestYPosn0:
                    self.smallestYPosn0 = n.yPosn0
                if n.xPosn0 > self.biggestXPosn0:
                    self.biggestXPosn0 = n.xPosn0
                if n.yPosn0 > self.biggestYPosn0:
                    self.biggestYPosn0 = n.yPosn0

            n = self.tree.root
            n.xPosn0 = n.leftChild.br.stroke[0] / self.scale
            n.yPosn0 = n.leftChild.br.stroke[1] / self.scale
            n.cA.xPosn = n.leftChild.br.stroke[0]
            n.cA.yPosn = n.leftChild.br.stroke[1]
            # self.tree.root.cA = GramCoord((self.tree.root.leftChild.br.stroke[0] / self.scale),
            #                              (self.tree.root.leftChild.br.stroke[1] / self.scale),
            #                              'n%i' % self.tree.root.nodeNum)
            self.tree.root.cB = None
            #self.tree.root.cRef = GramCoord(self.tree.root.cA.xPosn, self.tree.root.cA.yPosn)

            # Check
            for n in self.tree.iterNodesNoRoot():
                theStrokeLen = math.sqrt(((n.parent.cA.xPosn - n.cA.xPosn) * (n.parent.cA.xPosn - n.cA.xPosn)) +
                                         ((n.parent.cA.yPosn - n.cA.yPosn) * (n.parent.cA.yPosn - n.cA.yPosn)))
                theBrLen = n.br.len * self.scale
                # print "%3i   %.3f" % (n.nodeNum, math.fabs(theStrokeLen -
                # theBrLen))
                if math.fabs(theStrokeLen - theBrLen) > 0.01:
                    gm.append("bad branch length %f %f" %
                              (theStrokeLen, theBrLen))
                    gm.append("node %i" % n.nodeNum)
                    raise GramError(gm)

            # for n in self.tree.iterNodesNoRoot():
            #    print "%2i %.1f %.1f" % (n.nodeNum, n.cA.xPosn, n.cA.yPosn)

            # angle
            for n in self.tree.iterNodesNoRoot():
                ret = func.square2polar(
                    [n.br.stroke[2] - n.br.stroke[0], n.br.stroke[3] - n.br.stroke[1]])
                n.angle = ret[0]
            self.tree.root.angle = 0.0

            # Adjust the graphics -- GramTexts and lines
            for n in self.tree.iterNodes():
                if n.name:
                    assert n.label  # from TreeGram.__init__()
                    # At this point, from TreeGram init, n.label.cA == n.cA
                    # That is good for TreeGram, but not for TreeGramRadial
                    # Now I want the cA's to be independent,
                    # so make a new one, with a new name, cL%i
                    n.label.cA = GramCoord(xPosn=n.cA.xPosn, 
                                           yPosn=n.cA.yPosn, 
                                           name="cL%i" % n.nodeNum)
                    if n == self.tree.root:
                        n.label.style = 'tgr root'
                    else:
                        if n.isLeaf:
                            n.label.style = 'tgr leaf'
                        else:
                            n.label.style = 'tgr internal'
                if n.br:
                    if n.br.label:
                        n.br.label.style = 'tgr branch'
                    if n.br.uLabel:
                        n.br.uLabel.style = 'tgr branch'

            self.slopedBrLabels = slopedBrLabels

            for n in self.tree.iterNodesNoRoot():
                n.line.cap = 'round'  # Extended round?

            for n in self.tree.iterNodes():
                if n.label:
                    #n.label.xPosn = n.xPosn
                    #n.label.yPosn = n.yPosn

                    if hasattr(n, 'angle'):
                        # print n.name, n.nodeNum, n.angle
                        #n.label.anchor = 'center'
                        #theBrLen = n.br.len * self.scale
                        #sqCoords = func.polar2square([n.angle, 0.2])
                        # print n.nodeNum, n.name, sqCoords
                        #n.label.cA.xPosn += sqCoords[0]
                        #n.label.cA.yPosn += sqCoords[1]

                        if 0:
                            if n.angle > 1.5707963 or n.angle < -1.5707963:
                                n.label.anchor = 'south east'
                            else:
                                n.label.anchor = 'south west'
                        if 0:
                            #angleLenList = [n.angle, self.labelSep]
                            #deltaXY = func.polar2square(angleLenList)
                            #n.label.xPosn += deltaXY[0]
                            #n.label.yPosn += deltaXY[1]

                            if n.angle > x3piOver4 or n.angle < -x3piOver4:
                                # 9 o'clock
                                n.label.anchor = 'east'
                            elif n.angle <= x3piOver4 and n.angle >= x5piOver8:
                                # 11 o'clock
                                n.label.anchor = 'south east'
                            elif n.angle < x5piOver8 and n.angle >= x3piOver8:
                                # 12 o'clock
                                n.label.anchor = 'south'
                            elif n.angle < x3piOver8 and n.angle >= x1piOver4:
                                # 1 o'clock
                                n.label.anchor = 'south west'

                            elif n.angle >= -x3piOver4 and n.angle <= -x5piOver8:
                                # 7 o'clock
                                n.label.anchor = 'north east'
                            elif n.angle > -x5piOver8 and n.angle <= -x3piOver8:
                                # 6 o'clock
                                n.label.anchor = 'north'
                            elif n.angle > -x3piOver8 and n.angle <= -x1piOver4:
                                # 5 o'clock
                                n.label.anchor = 'north west'
                            else:
                                # 3 o'clock
                                n.label.anchor = 'west'

                if n.br and n.br.label:
                    tb = n.br.label
                    if self.slopedBrLabels:
                        piOver2 = math.pi / 2.
                        tb.anchor = 'south'
                        if n.angle > -piOver2 and n.angle < piOver2:
                            tb.rotate = n.angle * (180. / math.pi)
                        elif n.angle >= piOver2:
                            tb.rotate = -(math.pi - n.angle) * (180. / math.pi)
                        else:  # n.angle <= -piOver2
                            tb.rotate = (math.pi + n.angle) * (180. / math.pi)
                    else:
                        # print "node %2i, angle %.2f" % (n.nodeNum, n.angle)
                        # print "node %2i " % n.nodeNum,
                        if n.angle >= 170./180. * math.pi:
                            tb.anchor = 'south'
                        elif n.angle >= x3piOver4:
                            # print "angle a"
                            tb.anchor = 'south west'
                        elif n.angle >= xpiOver2:
                            # print "angle b"
                            tb.anchor = 'south west'
                        elif n.angle >= x1piOver4:
                            # print "angle c"
                            tb.anchor = 'south east'
                        elif n.angle >= 10./180. * math.pi:
                            tb.anchor = 'south east'
                        elif n.angle >= 0:
                            # print "angle d"
                            tb.anchor = 'south'
                        elif n.angle <= -170./180. * math.pi:
                            tb.anchor = 'south'
                        elif n.angle <= -x3piOver4:
                            # print "angle e"
                            tb.anchor = 'south east'
                        elif n.angle <= -xpiOver2:
                            # print "angle f"
                            tb.anchor = 'south east'
                        elif n.angle <= -x1piOver4:
                            # print "angle g"
                            tb.anchor = 'south west'
                        elif n.angle <= -10./180. * math.pi:
                            tb.anchor = 'south west'
                        elif n.angle < 0:
                            # print "angle h"
                            tb.anchor = 'south'
                if n.br and n.br.uLabel:
                    tb = n.br.uLabel
                    if self.slopedBrLabels:
                        piOver2 = math.pi / 2.
                        tb.anchor = 'north'
                        if n.angle > -piOver2 and n.angle < piOver2:
                            tb.rotate = n.angle * (180. / math.pi)
                        elif n.angle >= piOver2:
                            tb.rotate = -(math.pi - n.angle) * (180. / math.pi)
                        else:  # n.angle <= -piOver2
                            tb.rotate = (math.pi + n.angle) * (180. / math.pi)
                    else:
                        # print "node %2i " % n.nodeNum,
                        if n.angle >= 170./180. * math.pi:
                            tb.anchor = 'north'                       
                        elif n.angle >= x3piOver4:
                            # print "angle a"
                            tb.anchor = 'north east'
                        elif n.angle >= xpiOver2:
                            # print "angle b"
                            tb.anchor = 'north east'
                        elif n.angle >= x1piOver4:
                            # print "angle c"
                            tb.anchor = 'north west'
                        elif n.angle >= 10./180. * math.pi:
                            tb.anchor = 'north west'
                        elif n.angle >= 0:
                            # print "angle d"
                            tb.anchor = 'north'
                        elif n.angle <= -170./180. * math.pi:
                            tb.anchor = 'north'
                        elif n.angle <= -x3piOver4:
                            # print "angle e"
                            tb.anchor = 'north west'
                        elif n.angle <= -xpiOver2:
                            # print "angle f"
                            tb.anchor = 'north west'
                        elif n.angle <= -x1piOver4:
                            # print "angle g"
                            tb.anchor = 'north east'
                        elif n.angle <= -10./180. * math.pi:
                            tb.anchor = 'north east'
                        elif n.angle < 0:
                            # print "angle h"
                            tb.anchor = 'north'

            # print "-" * 25
            # for n in self.tree.iterLeavesNoRoot():
            # print n.nodeNum, n.label.cA.xPosn, n.label.cA.yPosn
            #    print n.nodeNum, n.cA.xPosn, n.cA.yPosn
            # print "-" * 25
            # sys.exit()

    def setBuiltInStyles(self):


        g = GramText('Xxy')
        g.cA = GramCoord(0, 0)
        g.name = 'tgr leaf'
        g.anchor = 'center'
        g.innerSep = 0.0
        g.textSize = self.leafLabelSize
        if g.defaultTextFamily:
            g.textFamily = g.defaultTextFamily
        #g.textShape = 'itshape'
        if self.engine == 'tikz':
            g.setBB()
        else:
            g.getSvg()
        Gram._styleDict[g.name] = g

        g = GramText('Xxy')
        g.cA = GramCoord(0, 0)
        g.name = 'tgr internal'
        #g.anchor = 'west'
        g.innerSep = 0.07
        g.fill = 'white'
        g.textSize = self.internalNodeLabelSize
        if g.defaultTextFamily:
            g.textFamily = g.defaultTextFamily
        if self.engine == 'tikz':
            g.setBB()
        else:
            g.getSvg()
        Gram._styleDict[g.name] = g

        g = GramText('Xxy')
        g.cA = GramCoord(0, 0)
        g.name = 'tgr root'
        #g.anchor = 'west'
        g.innerSep = 0.07
        g.fill = 'white'
        g.textSize = self.internalNodeLabelSize
        if g.defaultTextFamily:
            g.textFamily = g.defaultTextFamily
        if self.engine == 'tikz':
            g.setBB()
        else:
            g.getSvg()
        Gram._styleDict[g.name] = g

        g = GramText('Xxy')
        g.cA = GramCoord(0, 0)
        g.name = 'tgr branch'
        g.textSize = self.branchLabelSize
        if g.defaultTextFamily:
            g.textFamily = g.defaultTextFamily
        g.innerSep = 0.05
        if self.engine == 'tikz':
            g.setBB()
        else:
            g.getSvg()
        Gram._styleDict[g.name] = g

    def setPositions(self):
        # return
        Gram.setPositions(self)
        self.tikzPictureDefaults.lineThickness = self.tgDefaultLineThickness

        if self.engine == 'svg':
            self.getSvg()

        piOver2 = math.pi / 2.
        slop = 0.1

        for n in self.tree.iterNodes():
            n.cA.xPosn = n.xPosn0 * self.scale
            n.cA.yPosn = n.yPosn0 * self.scale
            if n.parent:
                n.cB.xPosn = n.parent.xPosn0 * self.scale
                n.cB.yPosn = n.parent.yPosn0 * self.scale

            if n.label:
                if self.engine == 'tikz':
                    n.label.setBB()
                    
                if 0:
                    
                    print("TreeGramRadial.setPositions()  angle=%s, anchor=%s  rawText=%s, fullHeight=%s exWid=%s" % (
                        n.angle, n.label.getAnch(), n.label.rawText, n.label.fullHeight, n.label.exWid))
                n.label.cA.xPosn = n.cA.xPosn
                n.label.cA.yPosn = n.cA.yPosn

                if n.isLeaf:

                    if 1:
                        # Move the label coordinate label.cA a small amount outwards, 
                        # along the line of the leaf branch

                        sqCoords = func.polar2square([n.angle, (n.label.fullHeight)])
                        n.label.cA.xPosn += sqCoords[0]
                        n.label.cA.yPosn += sqCoords[1]

                    if 1:
                        # We do not want the n.label to be at the same yPosn as the n.cA.yPosn; 
                        # if it does the label could over-write the line 
                        diff = n.label.cA.yPosn - n.cA.yPosn
                        halfHeight = n.label.fullHeight / 2.
                        if diff > 0.0:
                            # label.cA is above n.cA
                            if diff < halfHeight:
                                diff2 = halfHeight - diff
                                n.label.cA.yPosn 

                    if 1:

                        # If the branch points to the left, move the label left
                        if n.angle > (piOver2 + slop) or n.angle < -(piOver2 + slop):
                            # if the label is short, don't do anything
                            if n.label.length < 0.4:
                                pass
                            else:
                                # We do not want the n.label to be at the same yPosn as the n.cA.yPosn; 
                                # if it does the label could over-write the line.
                                diff = math.fabs(n.label.cA.yPosn - n.cA.yPosn)
                                halfHeight = n.label.fullHeight / 2.
                                if diff < halfHeight:  # potential collision
                                    n.label.cA.xPosn -= (n.label.length * 0.5) 
                                else:
                                    n.label.cA.xPosn -= n.label.length * 0.4

                        # If the branch points to the right
                        elif n.angle < (piOver2 - slop) and n.angle > -(piOver2 - slop):
                            if n.label.length < 0.4:
                                pass
                            else:
                                diff = math.fabs(n.label.cA.yPosn - n.cA.yPosn)
                                halfHeight = n.label.fullHeight / 2.
                                if diff < halfHeight:    # potential collision
                                    n.label.cA.xPosn += (n.label.length * 0.5) 
                                else:
                                    n.label.cA.xPosn += n.label.length * 0.4

                    if 0:
                        # Lower the Labels on downward-pointing branches
                        if n.angle < -(0.25 * math.pi) and n.angle > -(0.75 * math.pi):
                            n.label.cA.yPosn -= n.label.fullHeight * 0.15

                    # # theXShift = n.label.getXShift()
                    # # if theXShift is not None:
                    # #     n.label.cA.xPosn += theXShift
                    # # theYShift = n.label.getYShift()
                    # # if theYShift is not None:
                    # #     n.label.cA.yPosn += theYShift

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


    def setScaleBarPosition(self):
        self.scaleBar.xOrig = (self.smallestXPosn0 * self.scale) - 0.5
        self.scaleBar.yOrig = (self.smallestYPosn0 * self.scale) - 0.8

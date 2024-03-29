from p4 import func
import pyx
import os
import math
import string
import sys
import io
from subprocess import Popen, PIPE
import textwrap
import copy
import configparser

# I got these definitions of points from the web somewhere.
# The didot system originated in France but was used in most of Europe.
# 1 didot point = 0.376065 mm
# = 1.07007 pica point
# = 0.0148057 inch
# 1 cicero equals 12 didot points.

# Pica points
# This system was developed in England and is used in Great-Britain and the US.
# 1 pica point = 0.35146 mm
# = 0.93457 didot point
# = 0.013837 inch
# 1 pica equals 12 pica points.

# PostScript points
# When Adobe created PostScript, they added their own system of points. There are exactly 72 PostScript points in 1 inch.
# 1 PostScript point = 0.35277138 mm
# = 1.00375001 pica point
# = 0.01388888 inch

# US Letter paper is 21.59 by 27.94 cm = 612.011 by 792.014 postscript points
# A4 paper is 20.99 by 29.70 cm        = 595.003 by 842.905 postscript
# points (I get 841.905)

# Dvips gives %%BoundingBox: 0 0 596 842 for a4

# I found the following on the web somewhere.  I don't think they are correct, tho.  But I use them anyway.
# Command	Nominal Point Size	Exact Point Size
# \tiny	                 5                    5
# \scriptsize            7                    7
# \footnotesize          8                    8
# \small                 9                    9
# \normalsize           10                   10
# \large                12                   12
# \Large                14                   14.40
# \LARGE                18                   17.28
# \huge	                20                   20.74
# \Huge	                24                   24.88

# SVG UNITS
# See here https://pythonhosted.org/svgwrite/overview.html#units
# | unit | identifier description                                                   |
# |------+--------------------------------------------------------------------------|
# | px   | one px unit is defined to be equal to one user unit                      |
# | em   | font-size (actual font height)                                           |
# | ex   | x-height (height of letter x of actual font)                           |
# | pt   | point 1pt equals 1.25px (and therefore 1.25 user units)              |
# | pc   | pica 1pc equals 15px (and therefore 15 user units)                   |
# | mm   | millimeter 1mm would be 3.543307px (3.543307 user units)             |
# | cm   | centimeter 1cm equals 35.43307px (and therefore 35.43307 user units) |
# | in   | inch 1in equals 90px (and therefore 90 user units)                   |

# svg colors, from the svgnames option of the LaTeX xcolor package.
validSvgColorNames = ['AliceBlue', 'AntiqueWhite', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque', 'Black', 'BlanchedAlmond', 'Blue', 'BlueViolet', 'Brown', 'BurlyWood', 'CadetBlue', 'Chartreuse', 'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan', 'DarkBlue', 'DarkCyan', 'DarkGoldenrod', 'DarkGray', 'DarkGreen', 'DarkGrey', 'DarkKhaki', 'DarkMagenta', 'DarkOliveGreen', 'DarkOrange', 'DarkOrchid', 'DarkRed', 'DarkSalmon', 'DarkSeaGreen', 'DarkSlateBlue', 'DarkSlateGray', 'DarkSlateGrey', 'DarkTurquoise', 'DarkViolet', 'DeepPink', 'DeepSkyBlue', 'DimGray', 'DimGrey', 'DodgerBlue', 'FireBrick', 'FloralWhite', 'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'Goldenrod', 'Gray', 'Green', 'GreenYellow', 'Grey', 'Honeydew', 'HotPink', 'IndianRed', 'Indigo', 'Ivory', 'Khaki', 'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue', 'LightCoral', 'LightCyan', 'LightGoldenrod', 'LightGoldenrodYellow', 'LightGray', 'LightGreen', 'LightGrey', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue', 'LightSlateBlue', 'LightSlateGray', 'LightSlateGrey', 'LightSteelBlue', 'LightYellow', 'Lime', 'LimeGreen', 'Linen', 'Magenta', 'Maroon', 'MediumAquamarine', 'MediumBlue', 'MediumOrchid', 'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen', 'MediumTurquoise', 'MediumVioletRed', 'MidnightBlue', 'MintCream', 'MistyRose', 'Moccasin', 'NavajoWhite', 'Navy', 'NavyBlue', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed', 'Orchid', 'PaleGoldenrod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed', 'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple', 'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Salmon', 'SandyBrown', 'SeaGreen', 'Seashell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue', 'SlateGray', 'SlateGrey', 'Snow', 'SpringGreen', 'SteelBlue', 'Tan', 'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'VioletRed', 'Wheat', 'White', 'WhiteSmoke', 'Yellow', 'YellowGreen']

baseColors = ['black',
 'darkgray',
 'blue',
 'gray',
 'brown',
 'green',
 'cyan',
 'lightgray',
 'lime',
 'magenta',
 'olive',
 'orange',
 'pink',
 'purple',
 'red',
 'teal',
 'violet',
 'white',
 'yellow']


def cmForLineThickness(lt):
    pts = ptsForLineThickness(lt)
    cmPerPt = 0.035277138
    cm = pts * cmPerPt
    return cm


def ptsForLineThickness(lt):
    if lt is None:  # assume 'thin'
        pts = 0.4
    elif isinstance(lt, str):
        if lt == 'ultra thin':
            pts = 0.1
        elif lt == 'very thin':
            pts = 0.2
        elif lt == 'thin':
            pts = 0.4
        elif lt == 'semithick':
            pts = 0.6
        elif lt == 'thick':
            pts = 0.8
        elif lt == 'very thick':
            pts = 1.2
        elif lt == 'ultra thick':
            pts = 1.6
        else:
            raise GramError(
                "cmForLineThickness(), unknown string thickness %s" % lt)
    else:
        try:
            pts = float(lt)
        except ValueError:
            raise GramError(
                "cmForLineThickness(), unknown non-string thickness %s" % lt)
    assert pts
    return pts


def bbOverlap(bb1, bb2):
    # print "      bb1  %.1f %.1f %.1f %.1f" % tuple(bb1)
    # print "      bb2  %.1f %.1f %.1f %.1f" % tuple(bb2)

    bl1 = (bb1[0], bb1[1])
    tl1 = (bb1[0], bb1[3])
    br1 = (bb1[2], bb1[1])
    tr1 = (bb1[2], bb1[3])
    bl2 = (bb2[0], bb2[1])
    tl2 = (bb2[0], bb2[3])
    br2 = (bb2[2], bb2[1])
    tr2 = (bb2[2], bb2[3])
    for corner in [bl1, tl1, br1, tr1]:
        if isInside(corner, bb2):
            return True
    for corner in [bl2, tl2, br2, tr2]:
        if isInside(corner, bb1):
            return True


def isInside(point, bb):
    if point[0] > bb[0] and point[0] < bb[2] and point[1] > bb[1] and point[1] < bb[3]:
        return True

def svgDasharrayForLinestyle(theLS):
    if theLS in [None, 'solid']:
        return None
    elif theLS == 'dotted':
        return "2 4"
    elif theLS == 'densely dotted':
        return "2 2"
    elif theLS == 'loosely dotted':
        return "2 8"
    elif theLS == 'dashed':
        return "10 8"
    elif theLS == "densely dashed":
        return "10 4"
    elif theLS == "loosely dashed":
        return "10 16"

def writeInColour(theString, colour='blue'):
    goodColours = [
        'red', 'RED', 'blue', 'BLUE', 'cyan', 'CYAN', 'violet', 'VIOLET']
    if colour not in goodColours:
        raise P4Error(
            "func.printColour().  The colour should be one of %s" % goodColours)
    codeDict = {
        'red': '\033[0;31m',
        'RED': '\033[1;31m',
        'blue': '\033[0;34m',
        'BLUE': '\033[1;34m',
        'cyan': '\033[0;36m',
        'CYAN': '\033[1;36m',
        'violet': '\033[0;35m',
        'VIOLET': '\033[1;35m',
    }
    backToBlackCode = '\033[m'
    sys.stdout.write("%s%s%s" % (codeDict[colour], theString, backToBlackCode))


def setTerminalColour(theColour):
    goodTerminalColours = [
        'red', 'RED', 'blue', 'BLUE', 'cyan', 'CYAN', 'violet', 'VIOLET']
    terminalColourCodeDict = {
        'red': '\033[0;31m',
        'RED': '\033[1;31m',
        'blue': '\033[0;34m',
        'BLUE': '\033[1;34m',
        'cyan': '\033[0;36m',
        'CYAN': '\033[1;36m',
        'violet': '\033[0;35m',
        'VIOLET': '\033[1;35m',
    }
    #self.terminalBackToBlackCode = '\033[m'

    assert theColour in goodTerminalColours, "The colour must be one of %s" % goodTerminalColours
    sys.stdout.write(terminalColourCodeDict[theColour])


def unsetTerminalColour():
    sys.stdout.write('\033[m')

# Color and colour.
writeInColor = writeInColour
setTerminalColor = setTerminalColour
unsetTerminalColor = unsetTerminalColour



###################################################################

class Gram(object):

    _font = 'helvetica'
    _defaultTextFamily = "sffamily"  # 'sffamily'  rmfamily ttfamily
    _engine = 'tikz'  # or 'svg'
    _documentFontSize = 10   # 10, 11, or 12
    _pdfViewer = 'ls'
    _pngViewer = 'ls'
    _svgViewer = 'ls'
    _pngResolution = 140

    _config = None
    _configAttrs = """font documentFontSize pdfViewer pngViewer svgViewer
                              defaultTextFamily
                              pngResolution svgPxForCm svgTextNormalWeight""".split()

    _goodLineThicknesses = [
        'ultra thin', 'very thin', 'thin', 'semithick', 'thick', 'very thick', 'ultra thick']
    _goodTextFamilies = ['rmfamily', 'sffamily', 'ttfamily']
    _goodTextSeries = ['bfseries']
    _goodTextShapes = ['itshape', 'scshape']
    _goodTextSizes = ['tiny', 'scriptsize', 'footnotesize', 'small', 'normalsize', 'large',
                      'Large', 'LARGE', 'huge', 'Huge']

    _goodAnchors = ['west', 'north west', 'north', 'north east', 'east',
                    'base', 'base west', 'base east',
                    'mid', 'mid west', 'mid east',
                    'south west', 'south', 'south east',
                    'center']  # center is the default
   
    #_goodShapes = ['rounded rectangle']
    _goodLineStyles = [None, 'solid', 'dotted', 'densely dotted', 'loosely dotted',
                       'dashed', 'densely dashed', 'loosely dashed']

    _goodTextAligns = [None, 'left', 'flush left', 'right', 'flush right', 
                       'center', 'flush center', 'justify', 'none']
    _styleDict = {}
    _tikzPictureDefaults = None
    _htmlColorDict = {}
    _haveStartedPyX = False
    
    
    _useTikzPlotMarkLib = False
    _xRecenter = 1.
    _yRecenter = 1.
    _recenterExtra = 0.1

    _showTextBB = False
    _showTextAnchor = False
    _pdflatexOutputGoesToDevNull = True

    _svgPxForCm = 55.  # 70.86614  # 35.43307
    #_svgTextNormalsize = 0.34
    _svgTextNormalsize = 0.36      # estimate
    _defaultInnerSep = None
    _svgIdCounter = 1
    _svgGForIdDict = {}
    _svgHackDoRotate = False
    _svgHack_x_Only = False
    _svgNormalsize_x = None
    _svgTextNormalWeight = 400    # Slightly bold     

    # _labelIdCounter = 1
    # _labelGForIdDict = {}
    
    def __init__(self):
        self._dirName = 'Gram'
        self._baseName = 'gram'
        self.latexUsePackages = []
        self.latexOtherPreambleCommands = []
        self.haveSetBuiltInStyles = False
        self.bbb = [0.0] * 4  # big bounding box, ie of the whole gram
        self.useSfMathIfSffamily = True      # sometimes roman math is wanted

        self.graphics = []
        self.grams = []
        self.gX = 0.0  # the xShift of an included gram
        self.gY = 0.0  # the yShift 

        self.theGpdf = None

        if not Gram._config:
            config = configparser.SafeConfigParser()
            Gram._config = config
            config.optionxform = str
            filesRead = config.read([os.path.expanduser('~/.gram.conf'), 'gram.conf'])
            if filesRead:
                writeInColor("... read conf files %s\n" % filesRead)
                theSections = config.sections()
                if theSections:
                    assert len(theSections) == 1
                    assert theSections[0] == 'Gram'

                    # theOpts = config.options('Gram')
                    # for anOpt in theOpts:
                    #     ret = config.get('Gram', anOpt)
                    #     print anOpt, ret, type(ret)
                    
                    for myAttr in self.configAttrs:
                        try:
                            ret = config.get('Gram', myAttr)
                            if ret:
                                if myAttr in "documentFontSize pngResolution svgTextNormalWeight".split():
                                    try:
                                        ret = int(ret)
                                    except ValueError:
                                        raise GramError("Bad value '%s' for '%s' in conf file." %\
                                                        (ret, myAttr))
                                writeInColor("conf file: Setting Gram %s to %s" % (myAttr, ret)) # no \n
                                sys.stdout.flush()   # Get rid of the colour
                                print()                # line ending, finally
                                setattr(self, myAttr, ret)
                        except configparser.NoOptionError:
                            pass

    
            
    def _getDirName(self):
        return self._dirName

    def _setDirName(self, theDirName):
        gm = ['Gram._setDirName()']
        assert isinstance(theDirName, str)
        if ' ' in theDirName:
            gm.append("The dirName should not have any spaces.")
            raise GramError(gm)
        self._dirName = theDirName

    def _delDirName(self):
        gm = ['Gram._delDirName()']
        gm.append(
            "Caught an attempt to delete self.dirName-- Set it to something else, but don't delete it, ok?")
        raise GramError(gm)

    dirName = property(_getDirName, _setDirName, _delDirName)

    def _getBaseName(self):
        return self._baseName

    def _setBaseName(self, theBaseName):
        gm = ['Gram._setBaseName()']
        assert isinstance(theBaseName, str)
        if ' ' in theBaseName:
            gm.append("The baseName should not have any spaces.")
            raise GramError(gm)
        self._baseName = theBaseName

    def _delBaseName(self):
        gm = ['Gram._delBaseName()']
        gm.append(
            "Caught an attempt to delete self.baseName-- Set it to something else, but don't delete it, ok?")
        raise GramError(gm)

    baseName = property(_getBaseName, _setBaseName, _delBaseName)

    def _getFont(self):
        return Gram._font
    def _setFont(self, theFont):
        gm = ['Gram._setFont()']
        assert isinstance(theFont, str)
        lowFont = theFont.lower()
        goodFonts = ['cm', 'helvetica', 'palatino', 'times']
        if lowFont not in goodFonts:
            gm.append("You can only set property 'font' to one of")
            gm.append("%s" % goodFonts)
            gm.append("Got attempt to set to '%s'" % theFont)
            raise GramError(gm)
        Gram._font = lowFont
    def _delFont(self):
        gm = ['Gram._delFont()']
        gm.append("Caught an attempt to delete self.font-- don't do that.")
        raise GramError(gm)
    font = property(_getFont, _setFont, _delFont)

    def _getDefaultTextFamily(self):
        return Gram._defaultTextFamily
    def _setDefaultTextFamily(self, theDefaultTextFamily):
        gm = ['Gram._setDefaultTextFamily()']
        if theDefaultTextFamily == None:   # this week, not allowed
            self._defaultTextFamily = None
        else:
            assert isinstance(theDefaultTextFamily, str)
            lowDefaultTextFamily = theDefaultTextFamily.lower()
            goodDefaultTextFamilies = self._goodTextFamilies
            if lowDefaultTextFamily not in goodDefaultTextFamilies:
                gm.append("You can only set property 'defaultTextFamily' to one of")
                gm.append("%s" % goodDefaultTextFamilies)
                gm.append("or None. Got attempt to set to '%s'" % theDefaultTextFamily)
                raise GramError(gm)
            if self.font == 'helvetica':
                if lowDefaultTextFamily == "sffamily":
                    pass
                else:
                    gm.append(f"Attempt to set defaultTextFamily to {theDefaultTextFamily}")
                    gm.append("but helvetica is a sans font")
                    raise GramError(gm)
            elif self.font in ['palatino', 'times']:
                if lowDefaultTextFamily == "rmfamily":
                    pass
                else:
                    gm.append(f"Attempt to set defaultTextFamily to {theDefaultTextFamily}")
                    gm.append(f"but {self.font} is a roman family font")
                    raise GramError(gm)


            Gram._defaultTextFamily = lowDefaultTextFamily
    defaultTextFamily = property(_getDefaultTextFamily, _setDefaultTextFamily)

    def _getEngine(self):
        return Gram._engine
    def _setEngine(self, theEngine):
        engines = ['tikz', 'svg']
        if theEngine not in engines:
            gm = ['Gram._setEngine()']
            gm.append("engine should be one of %s" % engines)
            raise GramError(gm)
        Gram._engine = theEngine
    def _delEngine(self):
        gm = ['Gram._delEngine()']
        gm.append("Caught an attempt to delete self.engine -- don't do that.")
        raise GramError(gm)
    engine = property(_getEngine, _setEngine, _delEngine)

    def _getDocumentFontSize(self):
        return Gram._documentFontSize
    def _setDocumentFontSize(self, theDocumentFontSize):
        gm = ['Gram._setDocumentFontSize()']
        gm.append('The documentFontSize should be an integer, 10-12')
        if not isinstance(theDocumentFontSize, int):
            raise GramError(gm)
        if theDocumentFontSize < 10 or theDocumentFontSize > 12:
            raise GramError(gm)
        Gram._documentFontSize = theDocumentFontSize
    documentFontSize = property(_getDocumentFontSize, _setDocumentFontSize)

    def _getPdfViewer(self):
        return Gram._pdfViewer
    def _setPdfViewer(self, thePdfViewer):
        Gram._pdfViewer = thePdfViewer
    pdfViewer = property(_getPdfViewer, _setPdfViewer)

    def _getPngViewer(self):
        return Gram._pngViewer
    def _setPngViewer(self, thePngViewer):
        Gram._pngViewer = thePngViewer
    pngViewer = property(_getPngViewer, _setPngViewer)

    def _getSvgViewer(self):
        return Gram._svgViewer
    def _setSvgViewer(self, theSvgViewer):
        Gram._svgViewer = theSvgViewer
    svgViewer = property(_getSvgViewer, _setSvgViewer)

    def _getPngResolution(self):
        return Gram._pngResolution
    def _setPngResolution(self, thePngResolution):
        Gram._pngResolution = int(thePngResolution)
    pngResolution = property(_getPngResolution, _setPngResolution)

    def _getConfigAttrs(self):
        return Gram._configAttrs
    configAttrs = property(_getConfigAttrs)

    def _getGoodTextFamilies(self):
        return Gram._goodTextFamilies
    goodTextFamilies = property(_getGoodTextFamilies)

    def _getGoodTextSeries(self):
        return Gram._goodTextSeries
    goodTextSeries = property(_getGoodTextSeries)

    def _getGoodTextShapes(self):
        return Gram._goodTextShapes
    goodTextShapes = property(_getGoodTextShapes)

    def _getGoodTextSizes(self):
        return Gram._goodTextSizes
    goodTextSizes = property(_getGoodTextSizes)

    def _getGoodAnchors(self):
        return Gram._goodAnchors
    goodAnchors = property(_getGoodAnchors)

    def _getGoodLineStyles(self):
        return Gram._goodLineStyles
    goodLineStyles = property(_getGoodLineStyles)

    def _getStyleDict(self):
        return Gram._styleDict

    def _setStyleDict(self, newVal):
        raise GramError("Don't set styleDict, just modify it.")
    styleDict = property(_getStyleDict, _setStyleDict)

    def _getTikzPictureDefaults(self):
        if not Gram._tikzPictureDefaults:
            Gram._tikzPictureDefaults = GramTikzStyle()
            Gram._tikzPictureDefaults.name = 'tikzPictureDefaults'
        return Gram._tikzPictureDefaults

    def _setTikzPictureDefaults(self, newVal):
        Gram._tikzPictureDefaults = newVal
    tikzPictureDefaults = property(
        _getTikzPictureDefaults, _setTikzPictureDefaults)

    def _getHtmlColorDict(self):
        return Gram._htmlColorDict

    def _setHtmlColorDict(self, newVal):
        raise GramError("Don't set htmlColorDict, just modify it.")
    htmlColorDict = property(_getHtmlColorDict, _setHtmlColorDict)

    def _getHaveStartedPyX(self):
        return Gram._haveStartedPyX

    def _setHaveStartedPyX(self, newVal):
        if newVal in [True, False]:
            Gram._haveStartedPyX = newVal
        else:
            raise GramError(
                "Set haveStartedPyX to True or False, only (got %s)" % newVal)
    haveStartedPyX = property(_getHaveStartedPyX, _setHaveStartedPyX)

    def _getDefaultInnerSep(self):
        if Gram._defaultInnerSep:
            return Gram._defaultInnerSep
        else:
            if Gram._engine == "tikz":
                cmPerPt = 0.035277138
                myDocumentFontSize = self.documentFontSize  # pts
                myDocumentFontSize *= cmPerPt
                return myDocumentFontSize * 0.3333
            else:
                myNormalSize = self.svgTextNormalsize  # cm
                return myNormalSize * 0.3333

    def _setDefaultInnerSep(self, newVal):
        try:
            nV = float(newVal)
            Gram._defaultInnerSep = nV
        except ValueError:
            raise GramError(
                "_setDefaultInnerSep().  newVal should be a float.")
    defaultInnerSep = property(_getDefaultInnerSep, _setDefaultInnerSep)

    def _getUseTikzPlotMarkLib(self):
        return Gram._useTikzPlotMarkLib

    def _setUseTikzPlotMarkLib(self, newVal):
        if newVal in [True, False]:
            Gram._useTikzPlotMarkLib = newVal
        else:
            raise GramError(
                "Set useTikzPlotMarkLib to True or False, only (got %s)" % newVal)
    useTikzPlotMarkLib = property(
        _getUseTikzPlotMarkLib, _setUseTikzPlotMarkLib)


    def _get_xRecenter(self):
        return Gram._xRecenter

    def _set_xRecenter(self, newVal):
        try:
            nV = float(newVal)
        except ValueError:
            raise GramError("_set_xRecenter().  newVal should be a float.")
        Gram._xRecenter = nV
    xRecenter = property(_get_xRecenter, _set_xRecenter)

    def _get_yRecenter(self):
        return Gram._yRecenter

    def _set_yRecenter(self, newVal):
        try:
            nV = float(newVal)
        except ValueError:
            raise GramError("_set_yRecenter().  newVal should be a float.")
        # print "Gram setting class var yRecenter to %.2f" % nV
        Gram._yRecenter = nV
    yRecenter = property(_get_yRecenter, _set_yRecenter)

    def _get_recenterExtra(self):
        return Gram._recenterExtra

    def _set_recenterExtra(self, newVal):
        try:
            nV = float(newVal)
        except ValueError:
            raise GramError("_set_recenterExtra().  newVal should be a float.")
        Gram._recenterExtra = nV
    recenterExtra = property(_get_recenterExtra, _set_recenterExtra)
    
    def _get_showTextBB(self):
        return Gram._showTextBB

    def _set_showTextBB(self, newVal):
        Gram._showTextBB = newVal
    showTextBB = property(_get_showTextBB, _set_showTextBB)

    def _get_showTextAnchor(self):
        return Gram._showTextAnchor

    def _set_showTextAnchor(self, newVal):
        Gram._showTextAnchor = newVal
    showTextAnchor = property(_get_showTextAnchor, _set_showTextAnchor)

    def _get_pdflatexOutputGoesToDevNull(self):
        return Gram._pdflatexOutputGoesToDevNull

    def _set_pdflatexOutputGoesToDevNull(self, newVal):
        Gram._pdflatexOutputGoesToDevNull = newVal
    pdflatexOutputGoesToDevNull = property(
        _get_pdflatexOutputGoesToDevNull, _set_pdflatexOutputGoesToDevNull)

    def _get_svgPxForCm(self):
        return Gram._svgPxForCm

    def _set_svgPxForCm(self, newVal):
        Gram._svgPxForCm = float(newVal)
    svgPxForCm = property(_get_svgPxForCm, _set_svgPxForCm)

    def _get_svgTextNormalsize(self):
        return Gram._svgTextNormalsize

    def _set_svgTextNormalsize(self, newVal):
        Gram._svgTextNormalsize = float(newVal)
    svgTextNormalsize = property(
        _get_svgTextNormalsize, _set_svgTextNormalsize)

    def _get_svgIdCounter(self):
        return Gram._svgIdCounter

    def _set_svgIdCounter(self, newVal):
        Gram._svgIdCounter = float(newVal)
    svgIdCounter = property(_get_svgIdCounter, _set_svgIdCounter)

    def _get_svgGForIdDict(self):
        return Gram._svgGForIdDict

    def _set_svgGForIdDict(self, newVal):
        raise GramError("Don't set svgGForIdDict, just read it.")
    svgGForIdDict = property(_get_svgGForIdDict, _set_svgGForIdDict)

    def _get_svgTextNormalWeight(self):
        return Gram._svgTextNormalWeight

    def _set_svgTextNormalWeight(self, newVal):
        Gram._svgTextNormalWeight = int(newVal)
    svgTextNormalWeight = property(_get_svgTextNormalWeight, _set_svgTextNormalWeight)

    # def _get_labelIdCounter(self):
    #     return Gram._labelIdCounter

    # def _set_labelIdCounter(self, newVal):
    #     Gram._labelIdCounter = int(newVal)
    # labelIdCounter = property(_get_labelIdCounter, _set_labelIdCounter)

    # def _get_labelGForIdDict(self):
    #     return Gram._labelGForIdDict

    # def _set_labelGForIdDict(self, newVal):
    #     raise GramError("Don't set labelGForIdDict, just read it.")
    # labelGForIdDict = property(_get_labelGForIdDict, _set_labelGForIdDict)

    ##################################

    def setPositions(self):
        # print(self, "setPositions()")
        if self._defaultInnerSep:  # it has been set by the user
            self.tikzPictureDefaults.innerSep = self.defaultInnerSep
        if self.defaultTextFamily:
            self.tikzPictureDefaults.textFamily = self.defaultTextFamily

        for gr in self.graphics:
            gr.setPositions()

    def getTikz(self):
        gm = ['Gram.getTikz()']
        ss = []

        if not self.haveStartedPyX:
            self.startPyX()

        for gr in self.graphics:
            try:
                #print(gr)
                ret = gr.getTikz()
                #print(ret)
                if not isinstance(ret, str):
                    gm.append('graphic %s' % gr)
                    gm.append('getTikz() returned %s' % ret)
                    raise GramError(gm)
                ss.append(ret)
            except:
                gm.append('getTikz() failed for graphic %s' % gr)
                raise GramError(gm)

        try:
            return '\n'.join(ss)
        except:
            gm.append('Bad tikz strings')
            gm.append('%s' % ss)
            raise GramError(gm)

    def getSvg(self):
        gm = ['Gram.getSvg()']
        ss = []

        for gr in self.graphics:
            ret = gr.getSvg()
            if not isinstance(ret, str):
                gm.append('graphic %s' % gr)
                gm.append('getSvg() returned %s' % ret)
                raise GramError(gm)
            ss.append(ret)
        try:
            return '\n'.join(ss)
        except:
            gm.append('Bad svg strings')
            gm.append('%s' % ss)
            raise GramError(gm)

    def svgPxForCmI(self, cm):  # Int version
        return int(round(cm * self.svgPxForCm, 0))

    def svgPxForCmF(self, cm):  # float version
        return (cm * self.svgPxForCm)

    def setSvgIdAndAddToDict(self, typeString):
        self.svgId = "%s-%i" % (typeString, self.svgIdCounter)
        self.svgIdCounter += 1
        self.svgGForIdDict[self.svgId] = self

    ###############################################################

    def render(self):
        # print("Gram.render() doing a render() on %s" % self)
        if self.engine == 'tikz':
            if not self.haveStartedPyX:
                self.startPyX()
            if not self.haveSetBuiltInStyles:
                self.setBuiltInStyles()
            self.haveSetBuiltInStyles = True
        elif self.engine == 'svg':
            # print "Gram.render() here, set for svg"
            if not self.haveSetBuiltInStyles:   # Is this needed for svg?  Yes, it is used.
                self.setBuiltInStyles()
            self.haveSetBuiltInStyles = True
            # pass
        self.setPositions()
        for gr in self.grams:
            gr.render()
        # TreeGram.render() and Plot.render() continue ...

    def startPyX(self):

        if self.haveStartedPyX:
            return
        gm = ['Gram.startPyX()']

        pyx.unit.set(defaultunit='pt')  # 'bp' no workee

        pyx.text.set(engine=pyx.text.LatexEngine, docclass="article", 
            docopt='%ipt' % self.documentFontSize)

        # construct pyxTextPreambleString, with latexUsePackages
        pyxTextPreambleString = self._makeFontLine()
        if pyxTextPreambleString:
            pyxTextPreambleString += "\n"

        #pyxTextPreambleString += "\\usepackage{tikz}\n"
        pyxTextPreambleString += "\\usepackage[svgnames]{xcolor}\n"
        #if self.useTikzPlotMarkLib:
        #    pyxTextPreambleString += r"\usetikzlibrary{plotmarks}"
        #    pyxTextPreambleString += "\n"

        pkgString = self._parseLatexUsePackages()
        pyxTextPreambleString += pkgString
        if pkgString:
            pyxTextPreambleString += "\n"

        for lopc in self.latexOtherPreambleCommands:
            pyxTextPreambleString += lopc

        # print("Gram.startPyX() pyxTextPreambleString is ---")
        # print(f"{pyxTextPreambleString}\n(end of pyxTextPreambleString)")

        pyx.text.preamble(pyxTextPreambleString)

        self.haveStartedPyX = True
        

    def _makeFontLine(self):
        ss = []
        if self.font == 'cm':
            pass
        elif self.font == 'helvetica':
            self.defaultTextFamily = "sffamily"
            # texStuffFontLine = r"\usepackage[scaled=.90]{helvet}"
            ss.append("\\usepackage{helvet}")
            ss.append(r"\usepackage{courier}")
            ss.append(r"\renewcommand{\familydefault}{\sfdefault}")
        elif self.font == 'palatino':
            self.defaultTextFamily = "rmfamily"
            ss.append(r"\usepackage[osf]{mathpazo}")    # this uses osf, old style figures
            ss.append(r"\usepackage[scaled=.95]{helvet}")
            ss.append(r"\usepackage{courier}")
        elif self.font == 'times':
            self.defaultTextFamily = "rmfamily"
            ss.append(r"\usepackage{mathptmx}")  # osf no workee
            ss.append(r"\usepackage[scaled=.95]{helvet}") 
            ss.append(r"\usepackage{courier}")

        if self.defaultTextFamily == "sffamily":
            if self.useSfMathIfSffamily:
                ss.append("\\usepackage{sfmath}")
            if self.font != "helvetica":  # helvetica already done, above
                ss.append(r"\renewcommand{\familydefault}{\sfdefault}")
        return '\n'.join(ss)

    def _parseLatexUsePackages(self):
        """returns a multi-line string"""
        ss = []
        for lup in self.latexUsePackages:
            # print lup
            if isinstance(lup, tuple):
                # its a usepackage with options, eg ('graphicx', ['dvips'])
                # making \usepackage[dvips]{graphicx}
                assert len(lup) == 2
                assert isinstance(lup[1], list), "Got lup[1] %s " % lup[1]
                myOptions = ','.join(lup[1])
                ss.append(r"\usepackage[%s]{%s}" % (myOptions, lup[0]))
            else:
                ss.append(r"\usepackage{%s}" % lup)
        return '\n'.join(ss)

    def setBuiltInStyles(self):
        pass

    def writeTikz(self):

        gm = ['Gram.writeTikz()']
        thisDir = os.getcwd()
        # -p here means no error if existing.
        os.system('mkdir -p %s' % self.dirName)
        os.chdir(self.dirName)

        outFileNameA = '%s.tikz.tex' % self.baseName

        fA = open(outFileNameA, 'w')
        # fA.write('%% This is a tikz file\n')
        # fA.write('\n')
        # fA.write('%% This file is set up to use %ipt %s font.\n' %
        #          (self.documentFontSize, self.font))

        # tikzset styles
        theKeys = list(self.styleDict.keys())
        if theKeys:
            fA.write('\\tikzset{')
            for tzs in theKeys[:-1]:
                # print(f"writeTikz() style {tzs}")
                fA.write(r'%s/.style=%s,' %
                         (tzs, self.styleDict[tzs].getDefString()))
                fA.write('\n')
            tzs = theKeys[-1]
            fA.write(r'%s/.style=%s}' %
                     (tzs, self.styleDict[tzs].getDefString()))
            fA.write('\n')

        fA.write('\\begin{tikzpicture}')

        if self.tikzPictureDefaults:
            theDefString = self.tikzPictureDefaults.getDefString()[1:-1]
            if theDefString:
                fA.write("[%s]" % theDefString)
        fA.write('\n')

        if 0:
            fA.write("\n\\draw[help lines] (0cm,0cm) grid (8cm,5cm);\n")

        tricks = self.getTikz()
        fA.write(tricks)
        fA.write('\n')

        if 0:
            fA.write(
                "\n\\path[ultra thin, draw=red] (current bounding box.south west) ")
            fA.write("rectangle (current bounding box.north east);\n")

        self.writeTikzOfEmbeddedGrams(fA)

        fA.write('\\end{tikzpicture}\n')
        fA.close()
        os.chdir(thisDir)
        # print("Gram.writeTikz().  finished.")

    def writeTikzOfEmbeddedGrams(self, fA):
        for gr in self.grams:
            if gr.gX or gr.gY:
                fA.write('\\begin{scope}[xshift=%.3fcm,yshift=%.3fcm]\n' % (gr.gX, gr.gY))
            tricks = gr.getTikz()
            fA.write(tricks)
            fA.write("\n")
            gr.writeTikzOfEmbeddedGrams(fA)
            if gr.gX or gr.gY:
                fA.write('\\end{scope}\n')


    def _writeTexStuff(self, flavour, inputTikzLine=None, geometryLine=None):

        # a4 is 20.99 by 29.70 cm, us letter paper is 21.59 by 27.94.  Assume a4.
        # If we make the margins 1 cm on each side, so thats [ 538.30897506  785.21109054] postscript points
        # If we make 7.5 mm margins, thats [ 552.48246045  799.38457593] postscript points.
        # 15 mm margins -> [ 509.96200429  756.86411976]
        # 20 mm margins -> [ 481.61503351  728.51714898]

        gm = ['Gram._writeTexStuff()']

        assert flavour in ['pdfPage', 'pdf']
        if flavour == 'pdfPage':
            assert inputTikzLine
            assert geometryLine
        if flavour == 'pdf':
            assert inputTikzLine

        texStuffFontLine = self._makeFontLine()
        # print("===== texStuffFontLine")
        # print(texStuffFontLine)
        # print("==================")

        f = open('Makefile', 'w')
        f.write("TEXFILEROOT = %s\n" % self.baseName)
        #f.write("JOBNAME=%s\n" % self.baseName)
        #f.write("OUTFILEROOT=%s\n" % self.baseName)
        if self.theGpdf:
            f.write("COMPOSITEROOT=c\n")
            f.write("COMPOSITEOUTFILEROOT=composite_%s\n" % self.baseName)
        f.write("PDFVIEWER=%s\n" % self.pdfViewer)
        if self.pdflatexOutputGoesToDevNull:
            f.write(makeStuff_2)
        else:
            f.write(makeStuff_2b)
        if self.theGpdf:
            f.write(makeStuff_3)
        f.write(makeStuff_4)
        f.close()

        f = open('%s.tex' % self.baseName, 'w')
        if flavour == 'pdfPage':
            # or scrartcl?
            f.write(
                r"\documentclass[%ipt,a4paper]{article}" % self.documentFontSize)
            f.write("\n%s" % geometryLine)
        elif flavour == 'pdf':
            f.write(
                r"\documentclass[%ipt]{standalone}" % self.documentFontSize)
        f.write("\n")
        if texStuffFontLine:
            f.write("%s\n" % texStuffFontLine)
        f.write(self._parseLatexUsePackages())
        f.write("\n")
        f.write("\\usepackage[svgnames]{xcolor}\n")
        f.write("\\usepackage{tikz}\n")
        if self.useTikzPlotMarkLib:
            f.write(r"\usetikzlibrary{plotmarks}")
            f.write("\n")
        for lopc in self.latexOtherPreambleCommands:
            f.write("%s\n" % lopc)
        # f.write("\\pgfrealjobname{t}\n")
        #f.write("%s\n" % geometryLine)
        # f.write(tTexStuff_2) # \renewcommand\floatpagefraction{1.0} etc

        f.write("\\begin{document}\n")
        if flavour == 'pdfPage':
            f.write("\\thispagestyle{empty}\n")
        f.write(inputTikzLine)
        f.write('\\end{document}\n')
        f.close()

        if self.theGpdf:
            f = open('c.tex', 'w')
            f.write(tTexStuff_5 % self.documentFontSize)
            f.write("\\begin{textblock}{1}(0,0)\n")
            #f.write("\\includegraphics[scale=1.0023]{%s.pdf}\n" % self.baseName)
            f.write("\\includegraphics{%s.pdf}\n" % self.baseName)
            f.write("\\end{textblock}\n")
            # f.write("\\begin{textblock}{1}(0,0)\n")
            #f.write("\\includegraphics{../%s}\n" % self.theGpdf.pdf_fName)
            # f.write("\\end{textblock}\n")

            # These next lines work, but the sizes are not exactly exact.  Can see it better in big overlays.
            # f.write("\\includepdf[offset=0.5mm -0.5mm, noautoscale=true, fitpaper=true]{../%s}\n" % (
            #        self.theGpdf.pdf_fName))
            f.write("\\includepdf[fitpaper=true]{../%s}\n" % (
                    self.theGpdf.pdf_fName))
            f.write(tTexStuff_4)
            f.close()

        # os.chdir(thisDir)

    #    a4 is 20.99 by 29.70 cm

    def pdfPage(self, maxWidth=19, maxHeight=27.7):
        gm = ['Gram.pdf()']
        self.render()
        theKeys = self.styleDict.keys()
        if theKeys:
            for k in theKeys:
                self.styleDict[k].setBB()
        self.tikzCalcBigBoundingBox()
        print("Gram.pdf(), bbb is now %s" % self.bbb)

        if maxWidth > 19:
            gm.append(
                'a4 is 21 cm wide, so the maxWidth has a 19 cm maximum.  Got %s' % maxWidth)
            raise GramError(gm)
        if maxHeight > 27.7:
            gm.append(
                'a4 is 29.7 cm tall, so the maxHeight has a 27.7 cm maximum.  Got %s' % maxHeight)
            raise GramError(gm)
        myWid = (self.bbb[2] - self.bbb[0])
        myHt = (self.bbb[3] - self.bbb[1])
        assert myWid > 0.0, self.bbb
        assert myHt > 0.0, self.bbb

        print("%s: maxWidth = %.2f, maxHeight = %.2f, myWid=%.2f, myHt=%.2f, %.3f, %.3f" % (
            gm[0], maxWidth, maxHeight, myWid, myHt, maxWidth / myWid, maxHeight / myHt))

        assert myWid > 0.0
        assert myHt > 0.0
        
        if myWid > maxWidth or myHt > maxHeight:
            # \usepackage[margin=3cm,noheadfoot]{geometry}
            theScale = [1.0] * 2  # width and height
            if myWid > maxWidth:
                xScale = float(maxWidth) / myWid
                if xScale < 1.0:
                    theScale[0] = xScale
            if myHt > maxHeight:
                yScale = float(maxHeight) / myHt
                if yScale < 1.0:
                    theScale[1] = yScale
            print("theScale = %s" % theScale)
            myScale = min(theScale)
            # print "myScale = %s" % myScale
            assert myScale < 1.0

        if 1:
            gm = ["Gram.pdf()"]
            self.writeTikz()
            assert self.dirName
            if os.path.isdir(self.dirName) and os.path.isfile("%s/%s.tikz.tex" % (self.dirName, self.baseName)):
                thisDir = os.getcwd()
                os.chdir(self.dirName)
                if myWid > maxWidth or myHt > maxHeight:
                    inputTikzLine = '\\scalebox{%.3f}{\\input{%s.tikz}}\n' % (
                        myScale, self.baseName)
                else:
                    inputTikzLine = '\\input{%s.tikz}\n' % self.baseName
                geometryLine = '\\usepackage[width=%.1fcm, height=%.1fcm,noheadfoot]{geometry}' % (
                    maxWidth, maxHeight)
                self._writeTexStuff(
                    'pdfPage', inputTikzLine=inputTikzLine, geometryLine=geometryLine)
                if 1:
                    oldFName = "%s.pdf" % self.baseName
                    if os.path.isfile(oldFName):
                        os.remove(oldFName)
                os.system('make pdfPage')
                os.chdir(thisDir)


    # def epdf(self):
    #     """For backward compatability.  Calls pdf()"""
    #     self.pdf()

    def pdf(self):
        assert self.documentFontSize in [10, 11, 12]

        if not self.haveStartedPyX:
            for k,v in self.htmlColorDict.items():
                print(k,v)
                myColorDef = r"\definecolor{%s}{HTML}{%s}" % (k, v)
                self.latexOtherPreambleCommands.append(myColorDef)

        self.render()
        theKeys = self.styleDict.keys()
        if theKeys:
            for k in theKeys:
                self.styleDict[k].setBB()

        assert self.dirName
        # print("Gram.pdf() about to do writeTikz()")
        self.writeTikz()
        # print("Gram.pdf() finished writeTikz()")
        if os.path.isdir(self.dirName) and os.path.isfile("%s/%s.tikz.tex" % (self.dirName, self.baseName)):
            #inputTikzLine = '\\input{%s.tikz}' % self.baseName
            #geometryLine  = '\\usepackage[width=%.1fcm, height=%.1fcm,noheadfoot]{geometry}' % (myWid+2, myHt+2)
            thisDir = os.getcwd()
            os.chdir(self.dirName)
            inputTikzLine = '\\input{%s.tikz}\n' % self.baseName
            self._writeTexStuff('pdf', inputTikzLine)
            if 1:
                oldFName = "%s.pdf" % self.baseName
                if os.path.isfile(oldFName):
                    os.remove(oldFName)
            if self.theGpdf and 1:
                oldFName = "composite_%s.pdf" % self.baseName
                if os.path.isfile(oldFName):
                    os.remove(oldFName)
            os.system('make pdf')
            if self.theGpdf and os.path.isfile("%s.pdf" % self.baseName):
                os.system('make composite')
            os.chdir(thisDir)

    def png(self, resolution=None):
        
        if not resolution:
            resolution = self.pngResolution
        pdfFileName = "%s/%s.pdf" % (self.dirName, self.baseName)
        #if not os.path.isfile(pdfFileName):

        # We want to re-make the pdf, in case there have been changes.
        # But we don't want to see it, so turn off pdfViewer
        savedPdfViewer = self.pdfViewer
        self.pdfViewer = 'ls'
        pdfFileName = "%s/%s.pdf" % (self.dirName, self.baseName)
        writeInColour("Making PDF file %s\n" % (pdfFileName), 'blue')
        self.pdf()
        self.pdfViewer = savedPdfViewer

        pngFileName = "%s/%s.png" % (self.dirName, self.baseName)
        writeInColour("Writing PNG file %s : resolution %i\n" % (pngFileName, resolution), 'blue')
        sys.stdout.flush()
        os.system("gs -dNOPAUSE -sDEVICE=pngalpha -r%i -dBATCH -sOutputFile=%s %s" % (
            resolution, pngFileName, pdfFileName))
        os.system("%s %s" % (self.pngViewer, pngFileName))
        
    def svg(self, extraMarginHack=1.0, writeWidthHeight=True):

        # This is a complex and ugly hack.
        # Together with calcBigBoundingBox() it should be re-written

        verbose = False
        if verbose:
            print("Gram.svg() start")
        self.engine = 'svg'

        # Leftover stuff from a previous call to this method causes
        # grief.  Not sure why.  It probably indicates a bug elsewhere.
        # Maybe it is not needed anymore?
        # So zero a couple of things.

        agt = self.getAllGramTexts()
        for gt in agt:
        #     print(f"fullHeight {gt.fullHeight}")
        #     gt.fullHeight = 0.0
        #     gt.underhang = 0.0
        #     gt.svgBaseline_cm = 0.0
        #     gt.rise = 0.0
            gt.svg_half_normal_x = 0.0

        # I probably should not have used class attributes here ...
        Gram._svgNormalsize_x = None
        Gram._svgHackDoRotate = False
        Gram._svgHack_x_Only = True

        if verbose:
            print("Gram.svg() first go, about to render")
        self.render()
        if verbose:
            print("Gram.svg() first go, about to calcBigBoundingBox")

        self.calcBigBoundingBox()
        if verbose:
            print("Gram.svg() finished first go")

        Gram._svgHackDoRotate = False
        Gram._svgHack_x_Only = False
        self.render()
        if verbose:
            print("Gram.svg() second go, about to calcBigBoundingBox")
        self.calcBigBoundingBox()

        Gram._svgHackDoRotate = True
        self.render()
        if verbose:
            print("Gram.svg() third go, about to calcBigBoundingBox")
        self.calcBigBoundingBox()

        # The final product.
        svgFName = "%s.svg" % self.baseName
        f = open(svgFName, 'w')
        writeInColour("Writing SVG file %s : svgPxForCm %.2f, extraMarginHack %.1f\n" % (
            svgFName, self.svgPxForCm, extraMarginHack), 'blue')
        sys.stdout.flush()
        self.svgWriteToOpenFile(f, self.bbb, doHackExtra=extraMarginHack, writeWidthHeight=writeWidthHeight)
        f.close()

        if self.svgViewer:
            os.system("%s %s" % (self.svgViewer, svgFName)) 
                  
    def svgWriteToOpenFile(self, flob, theBBB, doHackExtra=0.0, writeWidthHeight=True):
        gm = ['Gram.svgWriteToOpenFile()']
        myWid = (theBBB[2] - theBBB[0])
        myHt = (theBBB[3] - theBBB[1])
        assert myWid > 0.0
        assert myHt > 0.0

        #flob.write('<?xml-stylesheet type="text/css" href="/Users/peter/Write/Html/psvn1.css" ?>\n')
        flob.write('<svg version="1.1"\n  baseProfile="full"\n')
        hackExtraX = doHackExtra
        hackExtraY = doHackExtra
        if doHackExtra:
            wd = (myWid * self.svgPxForCm) + (2 * hackExtraX)
            ht = (myHt * self.svgPxForCm) + (2 * hackExtraY)
        else:
            wd = myWid * self.svgPxForCm
            ht = myHt * self.svgPxForCm

        if writeWidthHeight:
            flob.write('  width="%.2f" height="%.2f"\n' % (wd, ht))

        if doHackExtra:
            vb1 = (theBBB[0] * self.svgPxForCm) - hackExtraX
            vb2 = (theBBB[1] * self.svgPxForCm) - hackExtraY
            vb3 = (myWid * self.svgPxForCm) + (2 * hackExtraX)
            vb4 = (myHt * self.svgPxForCm) + (2 * hackExtraY)
        else:
            vb1 = (theBBB[0] * self.svgPxForCm)
            vb2 = (theBBB[1] * self.svgPxForCm)
            vb3 = (myWid * self.svgPxForCm)
            vb4 = (myHt * self.svgPxForCm)

        flob.write('  viewBox="%.2f %.2f %.2f %.2f"\n' % (vb1, vb2, vb3, vb4))
        flob.write('  xmlns="http://www.w3.org/2000/svg"\n')
        flob.write('  xmlns:xlink="http://www.w3.org/1999/xlink">\n')
        flob.write('\n')

        if self.font == 'cm':
            #raise GramError("Font cm does not work with svg")
            # print()
            # print("=" * 75)
            # print("Font is currently 'cm', Computer Modern, which won't work with SVG files.")
            # print("Switching to Helvetica.")
            # print("=" * 75, "\n")
            # self.font = 'helvetica'

            if self.defaultTextFamily == "sffamily":
                myFont = '"Latin Modern Sans", Helvetica, sans-serif'
            else:
                myFont = '"Latin Modern Roman", Times,serif'

        if self.font == 'helvetica':
            myFont = "Helvetica, sans-serif"
        elif self.font == "palatino":
            myFont = '"Palatino Linotype", "Book Antiqua", Palatino, serif'
        elif self.font == "times":
            myFont = '"Times New Roman",Times,serif'

        flob.write("<style>\n")
        if self.font == 'cm':
            flob.write(svgCss2 % (myFont, self.svgTextNormalWeight))
        else:
            flob.write(svgCss1 % (myFont, self.svgTextNormalWeight))
        flob.write("</style>\n")

        # Write markers in a <defs> </defs>  section.
        markersToWrite = []
        if hasattr(self, 'scatters'):
            for sc in self.scatters:
                markersToWrite.append(sc.marker)
        for gr in self.grams:
            if hasattr(gr, 'scatters'):
                for sc in gr.scatters:
                    markersToWrite.append(sc.marker)
        if markersToWrite:
            flob.write("<defs>\n")
            for mtw in markersToWrite:
                flob.write(mtw.getSvg())
            flob.write("</defs>\n")
        tricks = self.getSvg()
        flob.write(tricks)
        flob.write('\n')
        for gr in self.grams:
            if gr.gX or gr.gY:
                flob.write('<g transform="translate(%.2f, %.2f)">\n' %
                           (self.svgPxForCmF(gr.gX), -self.svgPxForCmF(gr.gY)))
            tricks = gr.getSvg()
            flob.write(tricks)
            flob.write("\n")
            if gr.gX or gr.gY:
                flob.write('</g>\n')
        flob.write('</svg>\n')


    def cat(self):
        assert self.dirName
        if 0:
            print("=========== %s/%s.tex =============" % (self.dirName, self.baseName))
            os.system('cat %s/%s.tex' % (self.dirName, self.baseName))
        if 1:
            if os.path.isfile("%s/%s.tikz.tex" % (self.dirName, self.baseName)):
                print("=========== %s.tikz.tex =============" % self.baseName)
                os.system('cat %s/%s.tikz.tex' % (self.dirName, self.baseName))

    def adjustBBBFromGraphicBB(self, g):
        if g.bb[0] < self.bbb[0]:
            self.bbb[0] = g.bb[0]
        if g.bb[1] < self.bbb[1]:
            self.bbb[1] = g.bb[1]
        if g.bb[2] > self.bbb[2]:
            self.bbb[2] = g.bb[2]
        if g.bb[3] > self.bbb[3]:
            self.bbb[3] = g.bb[3]

    def inkscape(self):
        gm = ["Gram.inkscape()"]
        print(gm[0], "Gram._svgHackDoRotate is %s, Gram._svgHack_x_Only is %s" % (
            Gram._svgHackDoRotate, Gram._svgHack_x_Only))
        flob = io.StringIO()
        self.svgWriteToOpenFile(flob, theBBB=[0., 0., 1., 1.])
        flob.seek(0)
        thisRet = flob.read().encode('utf-8')
        
        if 1:
            print("=+" * 20, "result of svgWriteToOpenFile()")
            # print(thisRet)
            splRet = thisRet.split(b"\n")
            for l in splRet:
                print(l)
            # print("thisRet type is %s" % type(thisRet))  # <class 'bytes'>
            flob.seek(0)
            print("-." * 20)

        p = Popen(['inkscape', '-S', '-p'],
                  stdout=PIPE, stdin=PIPE, stderr=PIPE)

        # In Py3 if I used a StringIO()  then read() gives a str, and 
        # TypeError: memoryview: a bytes-like object is required, not 'str'
        # So do theUnicodeStuff.encode('utf-8')
        ret = p.communicate(input=thisRet)
        if 0:
            print("======================== returned from inkscape")
            print(ret)
            print(type(ret[0])) # class 'bytes'
            print("-------------------------")

        flob.close()

        if not ret[0]:
            # f = open("debug.svg", "w")
            # self.svgWriteToOpenFile(f, theBBB=[0., 0., 1., 1.])
            # f.close()
            gm.append("No string returned from inkscape.")
            raise GramError(gm)
        if not ret[0].startswith(b"svg"):
            gm.append("Bad string returned from inkscape.  Got %s %s" % ret)
            raise GramError(gm)
        #print ret[0]
        ll = [l for l in ret[0].split(b'\n') if l]
        splL = ll[0].split(b',')
        #print("got splL: ", splL)
        assert splL[0].startswith(b'svg')
        for l in ll:
            print(l)

    def calcBigBoundingBox(self):
        if self.engine == 'tikz':
            print("Gram.calcBigBoundingBox() is turned off for tikz")
            #self.tikzCalcBigBoundingBox()
        else:
            assert self.engine == 'svg'
            self.svgCalcBigBoundingBox()

    def svgCalcBigBoundingBox(self):
        gm = ["Gram.svgCalcBigBoundingBox()"]
        #print(gm[0], "Gram._svgHackDoRotate is %s, Gram._svgHack_x_Only is %s" % (
        #    Gram._svgHackDoRotate, Gram._svgHack_x_Only))
        flob = io.StringIO()
        self.svgWriteToOpenFile(flob, theBBB=[0., 0., 1., 1.])
        flob.seek(0)
        thisRet = flob.read().encode('utf-8')

        if 0:
            fNm = f"debug{Gram._svgHackDoRotate}{Gram._svgHack_x_Only}.svg"
            f = open(fNm, "w")
            self.svgWriteToOpenFile(f, theBBB=[0., 0., 1., 1.])
            f.close()
        
        if 0:
            if Gram._svgHackDoRotate:
                if Gram._svgHack_x_Only:
                    print("=+" * 20, "result of svgWriteToOpenFile()")
                    splRet = thisRet.split(b"\n")
                    for aLine in splRet:
                        if aLine.startswith(b" <text"):
                            print(aLine)
                    # print(thisRet)
                    # print("thisRet type is %s" % type(thisRet))  # <class 'bytes'>
                    flob.seek(0)
                    print("-." * 20)

        # For inkscape version 1.0
        p = Popen(['inkscape', '-S', '-p'],
                  stdout=PIPE, stdin=PIPE, stderr=PIPE)

        # In Py3 if I used a StringIO()  then read() gives a str, and 
        # TypeError: memoryview: a bytes-like object is required, not 'str'
        # So do theUnicodeStuff.encode('utf-8')
        ret = p.communicate(input=thisRet)
        if 0:
            print("======================== svgCalcBigBoundingBox, returned from inkscape")
            print(ret)
            print(type(ret[0])) # class 'bytes'
            print("-------------------------")

        flob.close()

        if not ret[0]:
            # f = open("debug.svg", "w")
            # self.svgWriteToOpenFile(f, theBBB=[0., 0., 1., 1.])
            # f.close()
            gm.append("No string returned from inkscape.")
            raise GramError(gm)
        if not ret[0].startswith(b"svg"):
            gm.append("Bad string returned from inkscape.  Got %s %s" % ret)
            raise GramError(gm)
        #print ret[0]
        ll = [l for l in ret[0].split(b'\n') if l]
        splL = ll[0].split(b',')
        #print("got splL: ", splL)
        assert splL[0].startswith(b'svg')
        # pxPerCm = 35.43307   # official
        self.bbb[0] = float(splL[1]) / self.svgPxForCm
        self.bbb[1] = float(splL[2]) / self.svgPxForCm
        self.bbb[2] = self.bbb[0] + float(splL[3]) / self.svgPxForCm
        self.bbb[3] = self.bbb[1] + float(splL[4]) / self.svgPxForCm
        #print("svgCalcBigBoundingBox() got bbb:", self.bbb[0], self.bbb[1], self.bbb[2], self.bbb[3]) 

        #print("svgGForIdDict is now", self.svgGForIdDict)

        # For this hack, if Gram._svgHackDoRotate is turned on, then the text is
        # not rotated, and we can get the length from the inkscape bounding box.
        if not Gram._svgHackDoRotate:  # so any text is not rotated

            for l in ll[1:]:
                if l.startswith(b'text'):
                    splL = l.split(b',')
                    # print(splL)
                    #print("svgGForIdDict", self.svgGForIdDict)
                    g = self.svgGForIdDict.get(splL[0].decode("utf-8"))
                    assert g
                    if Gram._svgHack_x_Only:
                        
                        top = -(float(splL[2])) 
                        fullHeight = (float(splL[4]))
                        g.svgBaseline_cm = (top - fullHeight) / self.svgPxForCm
                        # print(f"""svgCalcBigBoundingBox() cd self.svgPxForCm: 
                        # {self.svgPxForCm}, top: {top}, fullHeight: {fullHeight} 
                        #  g.svgBaseline_cm: {g.svgBaseline_cm}""")
                    else:

                        # Get, for the un-rotated text, 
                        # - g.length
                        # - g.fullHeight
                        # - g.underhang # descent
                        # - g.rise      # ascent
                        g.length = float(splL[3]) / self.svgPxForCm
                        x1 = (float(splL[1])) / self.svgPxForCm
                        top = -(float(splL[2])) / self.svgPxForCm
                        x3 = x1 + (float(splL[3])) / self.svgPxForCm
                        g.fullHeight = (float(splL[4])) / self.svgPxForCm
                        y1 = top - g.fullHeight
                        g.underhang = g.svgBaseline_cm - y1  # can be zero
                        g.rise = top - g.svgBaseline_cm


        # Get Gram._svgNormalsize_x.  Need a new temporary text.
        # Then run inkscape again.  Then remove the temporary text.

        # Only do this next bit once, at the beginning, when Gram._svgNormalsize_x is still None
        # Add a text object of a single "x", and remove it when finished
        if  Gram._svgNormalsize_x == None:
            gx = self.text("x", 0,0)
            flob = io.StringIO()
            self.svgWriteToOpenFile(flob, theBBB=[0., 0., 1., 1.])
            flob.seek(0)
            thisRet = flob.read().encode('utf-8')
            p = Popen(['inkscape', '-S', '-p'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
            ret = p.communicate(input=thisRet)
            flob.close()
            ll = [l for l in ret[0].split(b'\n') if l]
            inkLine = None
            for l in ll[1:]:
                if l.startswith(b'text'):
                    splL = l.split(b',')
                    g = self.svgGForIdDict.get(splL[0].decode("utf-8"))
                    assert g
                    if g == gx:
                        inkLine = splL
                        break
            assert inkLine
            my_x = float(inkLine[4]) / self.svgPxForCm
            Gram._svgNormalsize_x = my_x
            
            # Clean up
            self.graphics.remove(gx)
            g = self.svgGForIdDict.pop(inkLine[0].decode("utf-8"))
            assert g == gx
                

    ##############################################################
    ##############################################################
    ##############################################################

    def code(self, theCode):
        GramCode(self, theCode)
        # The instantiation above puts it in ...?

    def grid(self, llx, lly, urx, ury, color='gray'):
        g = GramGrid(llx, lly, urx, ury, color=color)
        self.graphics.append(g)
        return g

    def text(self, theText, x, y):
        g = GramText(theText)
        g.cA = GramCoord(x, y)
        self.graphics.append(g)
        return g

    def line(self, x1, y1, x2, y2):
        cA = GramCoord(x1, y1)
        cB = GramCoord(x2, y2)
        # self.graphics.append(cA)
        # self.graphics.append(cB)
        g = GramLine(cA, cB)
        self.graphics.append(g)
        return g

    def rect(self, x1, y1, x2, y2):
        cA = GramCoord(x1, y1)
        cB = GramCoord(x2, y2)
        # self.graphics.append(cA)
        # self.graphics.append(cB)
        g = GramRect(cA, cB)
        self.graphics.append(g)
        return g

    def gpdf(self, pdf_fName):
        if self.theGpdf:
            raise GramError(
                "Gram.gpdf()  This week, we only allow one gpdf.  Already got one.")

        g = GramPdf(pdf_fName)
        self.theGpdf = g
        self.graphics.append(g)
        return g

    def jpeg(self, jpeg_fName, x, y, scale):
        cA = GramCoord(x, y)
        g = GramJpeg(jpeg_fName, cA, scale)
        self.graphics.append(g)
        return g

    ###########################################################

    def getAllGramTexts(self):
        """Does not recurse into self.grams"""
        agt = []
        for g in self.graphics:
            if isinstance(g, GramText):
                agt.append(g)
        #print("Got %i texts" % len(agt))
        return agt
        

    def fixTextOverlaps(self):
        tbb = self.getAllGramTexts()
        if len(tbb) < 2:
            return

        thisVerbose = False
        self.render()
        theMax = -1000000.
        theMin = 1000000.
        for g in tbb:
            # not g.getInnerSep(), so could be None
            g.savedInnerSep = g.innerSep
            g.innerSep = 0.0

            if self.engine == 'tikz':
                g.setBB()
            elif self.engine == 'svg':
                g.getSvg()
            else:
                raise GramError()

            g.lly = g.bb[1]
            if g.lly < theMin:
                theMin = g.lly
            if g.lly > theMax:
                theMax = g.lly
            g.overlaps = []
        theCenterY = theMin + (0.5 * (theMax - theMin))
        if 0:
            g = self.line(0, theCenterY, 3, theCenterY)
            g.color = 'blue'
            g.lineThickness = 'ultra thin'

        indices = range(len(tbb))

        tbb = func.sortListOfObjectsOnAttribute(tbb, 'lly')
        # tbb is ordered from lowest to highest
        if thisVerbose:
            for i in indices:
                tbNum = indices[-(i + 1)]
                print("%2i  %.3f  %s" % (tbNum, tbb[tbNum].lly, tbb[tbNum].rawText))
            print("theCenterY is %.2f" % theCenterY)

        safety = 0
        while 1:
            if thisVerbose:
                print("round %i ----" % safety)
            safety += 1
            hasOverlap = False
            if 1:
                # In this part, we go up from the lowest ones, moving the
                # lowest ones down.
                for tb in tbb:
                    tb.overlaps = []
                for i in indices[:-1]:
                    tbA = tbb[i]
                    if tbA.lly > theCenterY:
                        break
                    for j in indices[i + 1:]:
                        tbB = tbb[j]
                        # if thisVerbose:
                        # print "%i %s,   %i %s" % (i, tbA.rawText, j,
                        # tbB.rawText)
                        if bbOverlap(tbA.bb, tbB.bb):
                            if thisVerbose:
                                print("        '%s' overlaps with '%s'" % (tbA.rawText, tbB.rawText))
                            hasOverlap = True
                            moveDownBy = (tbA.bb[3] - tbB.bb[1])
                            assert moveDownBy >= 0.0
                            if tbA.yShift is None:
                                tbA.yShift = 0.0
                            tbA.yShift -= moveDownBy
                            tbA.bb[1] -= moveDownBy
                            tbA.bb[3] -= moveDownBy
                            tbA.lly -= moveDownBy
                            if thisVerbose:
                                print("        '%s' moving down by %.3f" % (tbA.rawText, moveDownBy))
                            tbB.overlaps.append(tbA)
                            for tb in tbA.overlaps:
                                tb.yShift -= moveDownBy
                                tb.bb[1] -= moveDownBy
                                tb.bb[3] -= moveDownBy
                                tb.lly -= moveDownBy
                                if thisVerbose:
                                    print("        '%s' moving down by %.3f" % (tb.rawText, moveDownBy))
                            break
                    # if hasOverlap:
                    #    break

            if 1:
                # In this part we go down from the highest ones, moving the
                # highest ones down.
                for tb in tbb:
                    tb.overlaps = []
                for i2 in indices[:-1]:
                    i = indices[-(i2 + 1)]
                    tbA = tbb[i]
                    if tbA.lly < theCenterY:
                        break
                    for j2 in indices[i2 + 1:]:
                        j = indices[-(j2 + 1)]
                        tbB = tbb[j]
                        # if thisVerbose:
                        # print "%i %s,   %i %s" % (i, tbA.rawText, j,
                        # tbB.rawText)
                        if bbOverlap(tbA.bb, tbB.bb):
                            if thisVerbose:
                                print("        '%s' overlaps with %s" % (tbA.rawText, tbB.rawText))
                            hasOverlap = True
                            moveUpBy = (tbB.bb[3] - tbA.bb[1])
                            assert moveUpBy >= 0.0
                            if tbA.yShift is None:
                                tbA.yShift = 0.0
                            tbA.yShift += moveUpBy
                            tbA.bb[1] += moveUpBy
                            tbA.bb[3] += moveUpBy
                            tbA.lly += moveUpBy
                            if thisVerbose:
                                print("        '%s' moving up by %.3f" % (tbA.rawText, moveUpBy))
                            tbB.overlaps.append(tbA)
                            for tb in tbA.overlaps:
                                tb.yShift += moveUpBy
                                tb.bb[1] += moveUpBy
                                tb.bb[3] += moveUpBy
                                tb.lly += moveUpBy
                                if thisVerbose:
                                    print("        '%s' moving up by %.3f" % (tb.rawText, moveUpBy))
                            break
                    # if hasOverlap:
                    #    break

            # break
            # print "safety=%i" % safety
            if not hasOverlap:
                if thisVerbose:
                    print("======== no more overlaps.  breaking out of loop")
                break
            if safety > 100:
                print("Gram.fixTextOverlaps() -- too many iterations -- quitting.")
                break

        for tb in tbb:
            tb.innerSep = tb.savedInnerSep
            del(tb.savedInnerSep)
            del(tb.overlaps)


class GramCoord(Gram):

    def __init__(self, xPosn=0.0, yPosn=0.0, name=None, comment=None):
        Gram.__init__(self)

        self.xPosn = xPosn
        self.yPosn = yPosn
        self.name = name
        self.comment = comment
        # self.topLevelGraphics.append(self)

    def getTikz(self):
        if self.name:
            ss = []
            ss.append('\coordinate')
            ss.append('(%s)' % self.name)
            ss.append('at (%.3f,%.3f);' % (self.xPosn, self.yPosn))
            if self.comment:
                ss.append("%% %s" % self.comment)
            return ' '.join(ss)


class GramCode(Gram):

    def __init__(self, mygram, code):
        Gram.__init__(self)
        # gram is a gram.gram.Gram object
        assert isinstance(mygram, Gram)
        self.code = code
        mygram.graphics.append(self)
                  
    def getTikz(self):
        return '%s' % self.code

    def getSvg(self):
        return '%s' % self.code
                  


class GramColor(Gram):
    def __init__(self):
        #self.svgColor = None
        #self.svgColorOpacity = None
        #self.tikzColor = None
        #self.tikzColorOpacity = None 
        self.color = None
        self.value = None
        self.type = None       # svg, base (ie latex), html
        self.transparent = True
        
    def setColorFromString(self, theColor):
        assert isinstance(theColor, str)
        gm = ['GramColor.setColorFromString(%s)' % theColor]

        # theColor string might be "red" or it might be "red!20".  First, split
        # off the number if it exists and put that in self.value.  The rest goes
        # into theColorNoValue.
        if "!" in theColor:
            splColor = theColor.split('!')
            assert len(splColor) == 2
            try:
                theNum = int(splColor[1])
            except ValueError:
                gm.append("Can't make sense of color '%s'" % theColor)
                raise GramError(gm)
            if theNum < 0 or theNum >= 100:
                gm.append("The number in the color should be from 0-99.  Got %i" % theNum)
                raise GramError(gm)
            self.value = "%.2f" % (0.01 * theNum)
            theColorNoValue = splColor[0]
        else:
            theColorNoValue = theColor

        # Now see if theColorNoValue is a base color (eg "red") or an svg color
        # (eg "Red") or an html color (eg 99ff33 or #FF00AA)
        if theColorNoValue in baseColors:
            self.type = "base"
        elif theColorNoValue in validSvgColorNames:
            self.type = 'svg'
        elif len(theColorNoValue) in [6,7]:
            if len(theColorNoValue) == 7:
                if not theColorNoValue.startswith("#"):
                    gm.append("HTML colour?  I don't understand this.")
                    raise GramError(gm)

                theColorNoValue = theColorNoValue[1:]

            # Make the hex value uppercase
            theColorNoValue = theColorNoValue.upper()

            # Check for only digits and uppercase A-F
            goods = string.digits + string.ascii_uppercase[:6]
            for c in theColorNoValue:
                if c not in goods:
                    gm.append("Got non-hex character '%s' " % c)
                    gm.append("problem with HTML? colour %s." % theColorNoValue)
                    raise GramError(gm)

            # Put it in the self.latexHtmlColorDefsDict, but first check if we have seen it before
            theKey = "gCol" + theColorNoValue
            ret = self.htmlColorDict.get(theKey)
            if ret:
                if ret != theColorNoValue:
                    gm.append("Duplicate key '%s' in GramColor.htmlColorDict" % theKey)
                    gm.append("Old value '%s', new value '%s'" % (ret, theColorNoValue))
                    raise GramError(gm)
                else:
                    pass
            else:
                self.htmlColorDict[theKey] = theColorNoValue
            theColorNoValue = theKey  # switcheroo, so self.color becomes gColXXXXXX
            self.type = 'html'
        else:
            gm.append("I don't understand the color '%s'" % theColorNoValue)
            print("This week, the colour should be based on base or svg names.  One of ---")
            print("%s" % baseColors)
            print("%s" % validSvgColorNames)
            raise GramError(gm)

        self.color = theColorNoValue
        


class GramTikzStyle(Gram):

    def __init__(self):
        Gram.__init__(self)
        self.name = None
        self._color = None
        #self._opacity = None
        self._draw = None
        self._fill = None
        self._textSize = None
        self._textFamily = None
        self._textSeries = None
        self._textShape = None
        self._anchor = None
        self._anchorOverRide = None
        self._xShift = None
        self._yShift = None
        self._rotate = None
        # Whether a box or a circle is drawn around the text.
        self._shape = None
        self._lineThickness = None
        self._cap = None
        self._lineStyle = None  # Dotted, dashed
        self._textHeight = None
        self._textDepth = None
        self._textWrapWidth = None
        self._textAlign = None
        self._innerSep = None
        self._roundedCorners = None

    def _getColor(self):
        return self._color

    def _setColor(self, theColor):
        if theColor is None:
            self._color = None
        else:
            if isinstance(theColor, GramColor):
                self._color = theColor
            elif isinstance(theColor, str):
                self._color = GramColor()
                self._color.setColorFromString(theColor)
            else:
                gm = ['GramTikzStyle._setColor()']
                gm.append("Can't set color to '%s'" % theColor)
                raise GramError(gm)

    def _delColor(self):
        self._color = None

    color = property(_getColor, _setColor, _delColor)
    colour = property(_getColor, _setColor, _delColor)

    def _getDraw(self):
        return self._draw

    def _setDraw(self, theDraw):
        # Default None.  Set to True or False, or the colour.  This is for text boxes
        if theDraw in [None, True, False]:
            self._draw = theDraw
        else:
            if isinstance(theDraw, GramColor):
                self._draw = theDraw
            elif isinstance(theDraw, str):
                self._draw = GramColor()
                self._draw.setColorFromString(theDraw)
            else:
                gm = ['GramTikzStyle._setDraw()']
                gm.append("Can't set color to '%s'" % theDraw)
                raise GramError(gm)

    def _delDraw(self):
        self._draw = None

    draw = property(_getDraw, _setDraw, _delDraw)

    def _getFill(self):
        return self._fill

    def _setFill(self, theColor):
        if theColor is None:
            self._fill = None
        else:
            if isinstance(theColor, GramColor):
                self._fill = theColor
            elif isinstance(theColor, str):
                self._fill = GramColor()
                self._fill.setColorFromString(theColor)
            else:
                gm = ['GramTikzStyle._setFill()']
                gm.append("Can't set color to '%s'" % theColor)
                raise GramError(gm)

    def _delFill(self):
        self._fill = None

    fill = property(_getFill, _setFill, _delFill)

    def _getTextSize(self):
        return self._textSize

    def _setTextSize(self, theSize):
        if theSize is None:
            self._textSize = None
        else:
            assert isinstance(theSize, str)
            gm = ['GramTikzStyle._setSize()']
            goodSizes = self.goodTextSizes
            if theSize not in goodSizes:
                gm.append("You can only set property 'size' to one of")
                gm.append("%s" % goodSizes)
                gm.append("Got attempt to set to '%s'" % theSize)
                raise GramError(gm)
            self._textSize = theSize

    def _delTextSize(self):
        self._textSize = None

    textSize = property(_getTextSize, _setTextSize, _delTextSize)

    #_goodTextFamilies = ['rmfamily', 'sffamily', 'ttfamily']
    def _getTextFamily(self):
        return self._textFamily

    def _setTextFamily(self, newVal):
        gm = ['GramTikzStyle._setTextFamily()']
        if newVal == None:
            self._textFamily = None
        else:
            try:
                assert isinstance(newVal, str)
            except AssertionError:
                gm.append(f"Got newVal {newVal}, type {type(newVal)}, should be a string")
                raise GramError(gm)
            lowVal = newVal.lower()
            goodVals = self.goodTextFamilies
            if lowVal not in goodVals:
                gm.append("You can only set property 'textFamily' to one of")
                gm.append("%s (or None, or y" % goodVals)
                gm.append("Got attempt to set to '%s'" % newVal)
                raise GramError(gm)
            if self.font == 'helvetica':
                # if lowVal != 'sffamily':
                #     print gm[0]
                #     print "  Ignoring request to set textFamily to '%s' -- it does not work with helvetica" % newVal
                #     print "does this work?"  # does not work with ttfamily
                self._textFamily = lowVal
            else:
                self._textFamily = lowVal

    def _delTextFamily(self):
        self._textFamily = None

    textFamily = property(_getTextFamily, _setTextFamily, _delTextFamily)

    #_goodTextSeries = ['bfseries']
    def _getTextSeries(self):
        return self._textSeries

    def _setTextSeries(self, newVal):
        gm = ['GramTikzStyle._setTextSeries()']
        if newVal == None:
            self._textSeries = None
        else:
            assert isinstance(newVal, str)
            lowVal = newVal.lower()
            goodVals = self.goodTextSeries
            if lowVal not in goodVals:
                gm.append("You can only set property 'textSeries' to one of")
                gm.append("%s (or None, or you can delete it)" % goodVals)
                gm.append("Got attempt to set to '%s'" % newVal)
                raise GramError(gm)
            else:
                self._textSeries = lowVal

    def _delTextSeries(self):
        self._textSeries = None

    textSeries = property(_getTextSeries, _setTextSeries, _delTextSeries)

    #_goodTextShapes = ['itshape', 'scshape']
    def _getTextShape(self):
        return self._textShape

    def _setTextShape(self, newVal):
        gm = ['GramTikzStyle._setTextShape()']
        if newVal == None:
            self._textShape = None
        else:
            assert isinstance(newVal, str)
            lowVal = newVal.lower()
            goodVals = self.goodTextShapes
            if lowVal not in goodVals:
                gm.append("You can only set property 'textShape' to one of")
                gm.append("%s (or None, or you can delete it)" % goodVals)
                gm.append("Got attempt to set to '%s'" % newVal)
                raise GramError(gm)
            else:
                self._textShape = lowVal

    def _delTextShape(self):
        self._textShape = None

    textShape = property(_getTextShape, _setTextShape, _delTextShape)

    def _getAnchor(self):
        return self._anchor

    def _setAnchor(self, theAnchor):
        if theAnchor not in self.goodAnchors:
            gm = ['GramTikzStyle._setAnchor()']
            gm.append("You can only set property 'anchor' to one of")
            gm.append("%s" % self.goodAnchors)
            gm.append("Got attempt to set to '%s'" % theAnchor)
            raise GramError(gm)
        self._anchor = theAnchor

    def _delAnchor(self):
        raise GramError("Don't delete propery anchor, ok?")

    anchor = property(_getAnchor, _setAnchor, _delAnchor)

    def _getAnchorOverRide(self):
        return self._anchorOverRide

    def _setAnchorOverRide(self, theAnchorOverRide):
        if theAnchorOverRide not in self.goodAnchors:
            gm = ['GramTikzStyle._setAnchorOverRide()']
            gm.append("You can only set property 'anchorOverRide' to one of")
            gm.append("%s" % self.goodAnchors)
            gm.append("Got attempt to set to '%s'" % theAnchorOverRide)
            if theAnchorOverRide.startswith('mid'):
                gm.append(
                    "(Anchors 'mid', 'mid east', and 'mid west' are turned off).")
            raise GramError(gm)
        self._anchorOverRide = theAnchorOverRide

    def _delAnchorOverRide(self):
        self._anchorOverRide = None

    anchorOverRide = property(_getAnchorOverRide,
                              _setAnchorOverRide, _delAnchorOverRide)

    def _setAnch(self, newVal):
        gm = ['GramTizStyle._setAnch()']
        gm.append("This is a read-only variable -- don't set it.")
        gm.append("Set anchor or anchorOverRide")
        raise GramError(gm)

    def _getAnch(self):
        if self.anchorOverRide:
            return self.anchorOverRide
        else:
            return self.anchor
    anch = property(_getAnch, _setAnch)

    def _getXShift(self):
        return self._xShift

    def _setXShift(self, theXShift):
        self._xShift = theXShift

    def _delXShift(self):
        self._xShift = None

    xShift = property(_getXShift, _setXShift, _delXShift)

    def _getYShift(self):
        return self._yShift

    def _setYShift(self, theYShift):
        self._yShift = theYShift

    def _delYShift(self):
        self._yShift = None

    yShift = property(_getYShift, _setYShift, _delYShift)

    def _getRotate(self):
        return self._rotate

    def _setRotate(self, theRotate):
        gm = ['GramTikzStyle._setRotate()']
        try:
            theRotate = float(theRotate)
        except:
            gm.append("The rotate, in degrees, should a number.")
            raise GramError(gm)
        if theRotate > 360 or theRotate < -360:
            gm.append("There is no point to having the rotate (%s)" %
                      theRotate)
            gm.append("more than one revolution around the circle, is there?")
            raise GramError(gm)
        self._rotate = theRotate

    def _delRotate(self):
        self._rotate = None

    rotate = property(_getRotate, _setRotate, _delRotate)

    def _getShape(self):
        return self._shape

    def _setShape(self, theShape):
        goodShapes = ['circle', 'rectangle']
        if theShape not in goodShapes:
            gm = ['GramGraphic._setShape()']
            gm.append("You can only set property 'shape' to one of")
            gm.append("%s" % goodShapes)
            gm.append("Got attempt to set to '%s'" % theShape)
            raise GramError(gm)
        self._shape = theShape

    def _delShape(self):
        self._shape = False

    shape = property(_getShape, _setShape, _delShape)

    def _getLineThickness(self):
        #if self._lineThickness is not None:
        return self._lineThickness
        #else:
        #    return self.defaultLineThickness

    def _setLineThickness(self, theLineThickness):
        gm = ['GramTikzStyle._setLineThickness()']
        isOk = False
        if theLineThickness in Gram._goodLineThicknesses:
            isOk = True
        if not isOk:
            try:
                theLineThickness = float(theLineThickness)
            except:
                gm.append('The lineThickness should be one of %s' %
                          Gram._goodLineThicknesses)
                gm.append(
                    "or the lineThickness should be a positive float, the width in postscript points")
                raise GramError(gm)
            if theLineThickness > 100.:
                gm.append(
                    "property 'lineThickness' has an arbitrary upper limit of 100 pt.")
                gm.append("Got attempt to set to '%s'" % theLineThickness)
                raise GramError(gm)

        self._lineThickness = theLineThickness

    def _delLineThickness(self):
        self._lineThickness = None

    lineThickness = property(
        _getLineThickness, _setLineThickness, _delLineThickness)

    def _checkCapVal(self, newVal):
        # goodEnds = ['', '<', '>', '<<', '>>', '|', '|*',
        #            '[', ']', '(', ')', 'o', '*', 'oo', '**',
        #            'c', 'cc', 'C', '|<', '>|', '|<*', '>|*']
        goodCaps = ['rect', 'butt', 'round']
        if newVal not in goodCaps:
            gm = ['GramTikzStyle._checkCapVal()']
            gm.append("You can only set the line cap to one of ")
            gm.append("%s" % goodCaps)
            gm.append("   %12s  %s" %
                      ('empty string, or butt', 'Flush square ends'))
            gm.append("   %12s  %s" % ('round', 'Extended, rounded'))
            gm.append("   %12s  %s" % ('rect', 'Square extended'))
            gm.append("Got %s" % newVal)
            raise GramError(gm)
        return True

    def _getCap(self):
        return self._cap

    def _setCap(self, newVal):
        if self._checkCapVal(newVal):
            self._cap = newVal
    cap = property(_getCap, _setCap)

    def _checkLineStyleVal(self, newVal):
        # goodLineStyles = [None, 'solid', 'dotted', 'densely dotted',
        #'loosely dotted', 'dashed', 'densely dashed', 'loosely dashed' ]
        if newVal not in self.goodLineStyles:
            gm = ['GramTikzStyle._checkLineStyleVal()']
            gm.append("You can only set the line style to one of ")
            gm.append("%s" % goodLineStyles)
            gm.append("Got %s" % newVal)
            raise GramError(gm)
        return True

    def _getLineStyle(self):
        return self._lineStyle

    def _setLineStyle(self, newVal):
        if self._checkLineStyleVal(newVal):
            self._lineStyle = newVal

    def _delLineStyle(self):
        self._lineStyle = None
    lineStyle = property(_getLineStyle, _setLineStyle, _delLineStyle)

    def _getTextHeight(self):
        return self._textHeight

    def _setTextHeight(self, newVal):
        self._textHeight = newVal

    def _delTextHeight(self):
        self._textHeight = None
    textHeight = property(_getTextHeight, _setTextHeight, _delTextHeight)

    def _getTextDepth(self):
        return self._textDepth

    def _setTextDepth(self, newVal):
        self._textDepth = newVal

    def _delTextDepth(self):
        self._textDepth = None
    textDepth = property(_getTextDepth, _setTextDepth, _delTextDepth)

    def _getTextWrapWidth(self):
        return self._textWrapWidth

    def _setTextWrapWidth(self, newVal):
        try:
            nV = float(newVal)
        except:
            if newVal is None:
                nV = newVal
            else:
                raise GramError(
                    "_setTextWrapWidth, should set to a float or None.")
        self._textWrapWidth = nV

    def _delTextWrapWidth(self):
        self._textWrapWidth = None
    textWrapWidth = property(_getTextWrapWidth, _setTextWrapWidth, _delTextWrapWidth)

    def _getTextAlign(self):
        return self._textAlign

    def _setTextAlign(self, newVal):
        if newVal not in Gram._goodTextAligns:
            gm = ["Set textAlign."]
            gm.append("Should be one of %s" % Gram._goodTextAligns)
            gm.append(f"Got '{newVal}'")
            raise GramError(gm)
        else:
            self._textAlign = newVal

    def _delTextAlign(self):
        self._textAlign = None
    textAlign = property(
        _getTextAlign, _setTextAlign, _delTextAlign)

    def _getInnerSep(self):
        return self._innerSep

    def _setInnerSep(self, newVal):
        #assert newVal.endswith('pt')
        self._innerSep = newVal

    def _delInnerSep(self):
        self._innerSep = None
    innerSep = property(_getInnerSep, _setInnerSep, _delInnerSep)

    def _getRoundedCorners(self):
        return self._roundedCorners

    def _setRoundedCorners(self, newVal):
        #assert newVal.endswith('pt')
        self._roundedCorners = newVal

    def _delRoundedCorners(self):
        self._roundedCorners = None
    roundedCorners = property(
        _getRoundedCorners, _setRoundedCorners, _delRoundedCorners)

    # def getTikz(self):
    #    return ''
    def getTikzOptions(self): # GramTikzStyle
        # print("  ------- GramTikzStyle.getTikzOptions()  self=%s" % self)
        options = []
        # or self.font=='helvetica':
        # extraSffamilyHasBeenWritten = False
        if self.textSize or self.textFamily or self.textSeries or self.textShape:
            fStr = 'font='
            if self.textSize:
                #print(f"getTikzOptions() Got textSize {self.textSize}")
                # if self.textFamily == "sffamily":
                #     fStr += '\\sffamily\\%s' % self.textSize
                #     extraSffamilyHasBeenWritten = True
                # elif self.defaultTextFamily == "sffamily":
                #     fStr += '\\sffamily\\%s' % self.textSize
                #     extraSffamilyHasBeenWritten = True
                # else:
                fStr += '\\%s' % self.textSize

            if self.textFamily:
                # print(f"getTikzOptions() Got textFamily {self.textFamily}")
                if self.textFamily != self.defaultTextFamily:
                    fStr += '\\%s' % self.textFamily
            if self.name == "tikzPictureDefaults":
                fStr += '\\%s' % self.defaultTextFamily
            if self.textSeries:
                # If default sffamily and bfseries, then we need to repeat sffamily 
                # if self.textFamily == "sffamily" and not extraSffamilyHasBeenWritten:
                #     fStr += '\\sffamily\\%s' % self.textSeries
                # elif self.defaultTextFamily == "sffamily" and not extraSffamilyHasBeenWritten:
                #     fStr += '\\sffamily\\%s' % self.textSeries
                # else:
                fStr += '\\%s' % self.textSeries
            if self.textShape:
                fStr += '\\%s' % self.textShape
            # print(f"style getTikzOptions() fStr is {fStr}")
            options.append(fStr)
        if self.color:
            assert isinstance(self.color, GramColor)
            # if self.color.value and not self.color.transparent:
            #     options.append("%s!%s" % (self.color.color, self.color.value[2:]))
            # else:
            #     options.append("%s" % self.color.color)
            # if self.color.transparent and self.color.value:
            #     options.append("opacity=%s" % self.color.value)

            if self.color.value:
                if self.color.transparent:
                    options.append("%s" % self.color.color)
                    options.append("opacity=%s" % self.color.value)
                else:
                    options.append("%s!%s" % (self.color.color, self.color.value[2:]))
            else:
                options.append("%s" % self.color.color)
            
        if self.draw:
            if self.draw is True:
                options.append("draw")
            else:
                assert isinstance(self.draw, GramColor)
                if self.draw.value:
                    if self.draw.transparent:
                        options.append("draw=%s" % self.draw.color)
                        # If we do not say "draw" in this next line, the node 
                        # text gets that opacity as well.
                        options.append("draw opacity=%s" % self.draw.value)
                        
                    else:
                        options.append("draw=%s!%s" % (self.draw.color, self.draw.value[2:]))
                else:
                    options.append("draw=%s" % self.draw.color)

        if self.fill:
            assert isinstance(self.fill, GramColor)
            # options.append("fill=%s" % self.fill.color)
            # if self.fill.transparent and self.fill.value:
            #     options.append("fill opacity=%s" % self.fill.value)

            if self.fill.value:
                if self.fill.transparent:
                    options.append("fill=%s" % self.fill.color)
                    options.append("fill opacity=%s" % self.fill.value)
                else:
                    options.append("fill=%s!%s" % (self.fill.color, self.fill.value[2:]))
            else:
                options.append("fill=%s" % self.fill.color)

            # Hack to overcome bug that makes text have the same opacity as fill opacity.
            if self.fill.value and self.fill.transparent:
                options.append("text opacity=1.0")


        if self.anch:
            options.append("anchor=%s" % self.anch)
        elif self.anchor:
            options.append("anchor=%s" % self.anchor)
        if self.xShift:
            options.append("xshift=%.3fcm" % self.xShift)
        if self.yShift:
            options.append('yshift=%.3fcm' % self.yShift)
        if self.rotate:
            options.append("rotate=%.1f" % self.rotate)
        if self.shape:
            options.append("shape=%s" % self.shape)
        if self.lineThickness is not None:
            if isinstance(self.lineThickness, str):
                options.append("%s" % self.lineThickness)
            else:
                options.append("line width=%spt" % self.lineThickness)
        if self.cap:
            options.append("line cap=%s" % self.cap)
        if self.lineStyle:
            options.append("%s" % self.lineStyle)
        if self.textHeight:
            options.append("text height=%.3fcm" % self.textHeight)
        if self.textDepth or self.textDepth == 0.0:  
            options.append("text depth=%.3fcm" % self.textDepth)
        if self.textWrapWidth:
            options.append("text width=%.3fcm" % self.textWrapWidth)
        if self.textAlign:
            options.append("align=%s" % self.textAlign)
        if self.innerSep is not None:
            options.append("inner sep=%scm" % self.innerSep)
        if self.roundedCorners is not None:
            options.append("rounded corners=%s" % self.roundedCorners)
        # print "GramTikzStyle.getTikzOptions() returning %s" % options
        return options

    def getSvgOptions(self):
        options = []
        # or self.font=='helvetica':
        if self.textSize or self.textFamily or self.textSeries or self.textShape:
            fStr = 'font='
            if self.textSize:
                fStr += '\\%s' % self.textSize
            if self.textFamily:  # or self.font=='helvetica':
                # if self.font == 'helvetica':
                #    fStr += '\\%s' % 'sffamily'
                # elif self.textFamily:
                fStr += '\\%s' % self.textFamily
            if self.textSeries:
                fStr += '\\%s' % self.textSeries
            if self.textShape:
                fStr += '\\%s' % self.textShape
            options.append(fStr)


        if self.color:
            #print("    SVG.getSvgOptions() self is %s,  self.color is %s" % (self, self.color))
            assert isinstance(self.color, GramColor)
            if self.color.value:
                if self.color.transparent:
                    options.append('stroke="%s"' % self.color.color)
                    options.append('stroke-opacity="%s"' % self.color.value)
                else:
                    # color.value, eg red!50, does not work for non-tranaparent svg 
                    options.append('stroke="%s"' % self.color.color) 
            else:
                options.append('stroke="%s"' % self.color.color)

        # color, above, implies draw, and we do not want both
        elif self.draw:
            if self.draw == True:
                options.append('stroke="black"')
            else:
                assert isinstance(self.draw, GramColor)
                if self.draw.value:
                    if self.draw.transparent:
                        options.append('stroke="%s"' % self.draw.color)
                        options.append('stroke-opacity="%s"' % self.draw.value)
                    else:
                        # color.value, eg red!50, does not work for non-tranaparent svg 
                        options.append('stroke="%s"' % self.draw.color) 
                else:
                    options.append('stroke="%s"' % self.draw.color)

        if self.fill:
            #print("    SVG.getSvgOptions() self is %s,  self.fill is %s" % (self, self.fill))
            if self.fill == True:
                options.append('fill="black"')
            else:
                assert isinstance(self.fill, GramColor)
                if self.fill.value:
                    if self.fill.transparent:
                        options.append('fill="%s"' % self.fill.color)
                        options.append('fill-opacity="%s"' % self.fill.value)
                    else:
                        # color.value, eg red!50, does not work for non-tranaparent svg 
                        options.append('fill="%s"' % self.fill.color) 
                else:
                    options.append('fill="%s"' % self.fill.color)
        elif self.fill == None:
            if isinstance(self, GramRect):
                options.append('fill="none"')
            elif isinstance(self, GramLine):
                pass
            else:
                options.append('fill="none"')
        
        #if self.anch:
        #    options.append('anchor=%s' % self.anch)
        #elif self.anchor:
        #    options.append('anchor=%s' % self.anchor)
        if self.xShift:
            options.append('xshift=%.3fcm' % self.xShift)
        if self.yShift:
            options.append('yshift=%.3fcm' % self.yShift)
        # if self.rotate:
        #     options.append('rotate=%.1f' % self.rotate)
        # if self.shape:
        #     options.append('shape=%s' % self.shape)
        if self.lineThickness is not None:
            #if isinstance(self.lineThickness, str):
            myLineThickness = cmForLineThickness(self.lineThickness)
            myLineThickness = self.svgPxForCmF(myLineThickness)
            options.append('stroke-width="%.2f"' % myLineThickness)
        else:
            if self.tikzPictureDefaults.lineThickness:
                myLineThickness = cmForLineThickness(self.tikzPictureDefaults.lineThickness)
            else:
                # TikZ default is thin, which is 0.4 pts
                myLineThickness = cmForLineThickness('thin')
            myLineThickness = self.svgPxForCmF(myLineThickness)
            options.append('stroke-width="%.2f"' % myLineThickness)

        if self.cap:
            # tikz caps ['rect', 'butt', 'round']
            # svg caps butt square round
            if self.cap:
                if self.cap == 'rect':
                    options.append('stroke-linecap="square"')
                else:
                    options.append('stroke-linecap="%s"' % self.cap)
        if self.lineStyle:
            myDashArray = svgDasharrayForLinestyle(self.lineStyle)
            options.append('stroke-dasharray="%s"' % myDashArray)
        # if self.textHeight:
        #     options.append('text height=%.3fcm' % self.textHeight)
        # if self.textDepth:
        #     options.append('text depth=%.3fcm' % self.textDepth)
        # if self.textWrapWidth:
        #     options.append('text width=%.3fcm' % self.textWrapWidth)
        # if self.innerSep is not None:
        #     options.append('inner sep=%scm' % self.innerSep)
        # if self.roundedCorners is not None:
        #     options.append('rounded corners=%s' % self.roundedCorners)
        # print 'GramTikzStyle.getSvgOptions() returning %s' % options
        return options

    def getDefString(self):
        assert self.name
        # print(f"getDefString() self.name is {self.name}")
        options = self.getTikzOptions()
        return "{%s}" % ','.join(options)

    def dump(self):
        print("GramTikzStyle.dump() here")
        import inspect
        myMembers = inspect.getmembers(self)
        # print myMembers    #2-tuples
        for it in myMembers:
            if it[0].startswith("_"):
                if it[0] == '__class__':
                    print("  CLASS: %s" % it[1])
            else:
                if inspect.ismethod(it[1]):
                    # print "method: %s" % it[0]
                    pass
                else:

                    it1 = getattr(self, it[0])
                    print("  %-20s   %s" % (it[0], it1))


class GramGraphic(GramTikzStyle):

    """Base class for Gram graphic objects."""

    def __init__(self):
        GramTikzStyle.__init__(self)
        # cA is the GramCoord where the Graphic is put.
        self.cA = None
        self.comment = None
        self.style = None
        self.myStyle = None
        self.bb = [0.0] * 4
        #self.svgBb = [0.0] * 4
        self.svgId = None

    def setPositions(self):
        for g in self.graphics:
            g.setPositions()

    def setBB(self):
        raise GramError("setBB() called.  self is %s" % self)

    def getTikzOptions(self):
        dbug = False
        if dbug:
            if hasattr(self, "rawText"):
                print("------- GramGraphic.getTikzOptions()  rawText=%s" % self.rawText)
            else:
                print(f"------- GramGraphic.getTikzOptions() {self}")
            print("    self.draw is %s" % self.draw)
        options = []

        # First get the style string.
        # style and myStyle are just strings.  They are keys to
        # self.styleDict, but often we do not need that.

        theStyleString = ''
        theStyleObject = None
        if self.style or self.myStyle:
            if self.myStyle:
                theStyleString = self.myStyle
            else:
                theStyleString = self.style

            # This next bit is the first part of a hack to avoid repetition of
            # sffamily.
            try:
                theStyleObject = self.styleDict[theStyleString]
            except KeyError:
                print(self.styleDict)
                print(self.styleDict.keys())
                print("styleDict can't find style '%s'" % theStyleString)
                raise
            # print " *** theStyleObject.textFamily is %s" % theStyleObject.textFamily
            # print("getTikzOptions()  A  theStyleObject.anchor is %s" % theStyleObject.anchor)
            options.append(theStyleString)
        if dbug:
            print("    getTikzOptions()  B  options from style = %s" % options)

        # Then get options not associated with the style from the style string.
        nonStyleOptions = GramTikzStyle.getTikzOptions(self)
        if dbug:
            print("    getTikzOptions()  C  nonStyleOptions = %s" % nonStyleOptions)

        # Avoid repetition of font=\sffamily and anchor
        booger = r'font=\sffamily'
        if theStyleObject and theStyleObject.textFamily == 'sffamily':
            if booger in nonStyleOptions:
                nonStyleOptions.remove(booger)
        
        # Here is a bit of a hack, to overcome what looks a lot like a bug.  If
        # the style says fill=white and the options include a color, then the
        # fill becomes that color, when I just wanted the text to be that color,
        # not the background.  So I have to add fill to the options.
        if theStyleObject:
            if theStyleObject.fill:
                if isinstance(theStyleObject.fill, GramColor):
                    nonStyleOptions.append("fill=%s" % theStyleObject.fill.color)

        # if theStyleObject and theStyleObject.anchor:
        #    booger = "anchor=%s" % theStyleObject.anchor
        #    if booger in nonStyleOptions:
        #        nonStyleOptions.remove(booger)

        options += nonStyleOptions
        if dbug:
            print("    getTikzOptions()  D  (final) options = %s" % options)
        return options

    def getSvgOptions(self):
        #print("------- GramGraphic.getSvgOptions()  self=%s" % self)
        options = []

        # First get the style string.
        # style and myStyle are just strings.  They are keys to
        # self.styleDict, but often we do not need that.

        theStyleString = ''
        theStyleObject = None
        if self.style or self.myStyle:
            if self.myStyle:
                theStyleString = self.myStyle
            else:
                theStyleString = self.style

            # This next bit is the first part of a hack to avoid repetition of
            # sffamily.  Is it still needed?
            try:
                theStyleObject = self.styleDict[theStyleString]
            except KeyError:
                print(self.styleDict)
                print(self.styleDict.keys())
                print("styleDict can't find style '%s'" % theStyleString)
                raise
            # print " *** theStyleObject.textFamily is %s" % theStyleObject.textFamily
            # print "getTikzOptions()  A  theStyleObject.anchor is %s" %
            # theStyleObject.anchor
            options.append(theStyleString)
        #print "getSvgOptions()  B  style (ie class) options = %s" % options

        # Then get options not associated with the style from the style string.
        nonStyleOptions = GramTikzStyle.getSvgOptions(self)
        #print("getSvgOptions()  C  nonStyleOptions = %s" % nonStyleOptions)

        # Avoid repetition of font=\sffamily and anchor
        booger = 'font=\\sffamily'
        if theStyleObject and theStyleObject.textFamily == 'sffamily':
            if booger in nonStyleOptions:
                nonStyleOptions.remove(booger)

        # if theStyleObject and theStyleObject.anchor:
        #    booger = "anchor=%s" % theStyleObject.anchor
        #    if booger in nonStyleOptions:
        #        nonStyleOptions.remove(booger)

        options += nonStyleOptions
        #print "getSvgOptions()  D  (final) options = %s" % options
        return options

    def getTikz(self):
        ss = []
        ss.append('%% This is from GramGraphic.getTikz()')
        if self.comment:
            ss.append("%% %s" % self.comment)
        for gr in self.graphics:
            ss.append(gr.getTikz())
        return '\n'.join(ss)

    def getSvg(self):
        ss = []
        #ss.append('%% This is from GramGraphic.getSvg()')
        if self.comment:
            ss.append("<!--  %s -->" % self.comment)
        for gr in self.graphics:
            ss.append(gr.getSvg())
        return '\n'.join(ss)

    def getDraw(self):
        ret = self.draw
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.draw
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.draw
        return ret

    def getTextSize(self):
        ret = self.textSize
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.textSize
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.textSize
        return ret

    def getTextFamily(self):
        ret = self.textFamily
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.textFamily
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.textFamily
        if ret is None and self.tikzPictureDefaults:
            ret = self.tikzPictureDefaults.textFamily
        if ret is None and self.defaultTextFamily:
            ret = self.defaultTextFamily
        return ret

    def getTextSeries(self):
        ret = self.textSeries
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.textSeries
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.textSeries
        return ret

    def getTextShape(self):
        ret = self.textShape
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.textShape
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.textShape
        return ret

    def getColor(self):
        ret = self.color
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.color
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.color
        return ret

    # def getDraw(self):
    #    pass

    def getFill(self):
        ret = self.fill
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.fill
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.fill
        return ret

    def getAnch(self):
        ret = self.anch
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.anch
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.anch
        return ret

    def getXShift(self):
        ret = self.xShift
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.xShift
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.xShift
        return ret

    def getYShift(self):
        ret = self.yShift
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.yShift
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.yShift
        return ret

    # def getShape(self):
    #    pass

    def getRotate(self):
        ret = self.rotate
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.rotate
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.rotate
        return ret

    def getLineThickness(self):
        ret = self.lineThickness
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.lineThickness
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.lineThickness
        if ret is None and self.tikzPictureDefaults:
            ret = self.tikzPictureDefaults.lineThickness
        if ret is None:
            ret = 'thin'
        return ret

    def getCap(self):
        ret = self.cap
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.cap
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.cap
        return ret

    def getLineStyle(self):
        ret = self.lineStyle
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.lineStyle
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.lineStyle
        return ret

    # def getTextHeight(self):
    #    pass
    # def getTextDepth(self):
    #    pass

    def getTextWrapWidth(self):
        ret = self.textWrapWidth
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.textWrapWidth
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.textWrapWidth
        return ret


    def getInnerSep(self):
        ret = self.innerSep
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.innerSep
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.innerSep
        if ret is None:
            assert self.defaultInnerSep is not None
            ret = self.defaultInnerSep
        if ret is None:
            gm = ["GramText.getInnerSep()"]
            gm.append("rawText %s" % self.rawText)
            gm.append("getInnerSep() is None")
            raise GramError(gm)
        return ret

class GramSvgMarker(GramGraphic):
    
    _counter = 0

    def __init__(self, markerShape, markerRelativeSize=None):
        GramGraphic.__init__(self)
        #assert markerShape in ['+', 'x', '*', '-', '|', 'o', 'asterisk',  ## 'star', 'oplus', 'oplus*',                
        #                       ##'otimes', 'otimes*', 
        #                        'square', 'square*', 'triangle',
        #                       'triangle*', 'diamond', 'diamond*' ##, 'pentagon', 'pentagon*']
        #assert markerShape in ['+', 'x', '*', 'asterisk']
        self.markerShape = markerShape
        self.markerRelativeSize = markerRelativeSize
        markerIdBaseDict = {
            '+': 'gmCross',
            'x': 'gmX',
            '*': 'gmCircF',
            '-': 'gmDash',
            '|': 'gmBar',
            'o': 'gmCirc',
            'asterisk': 'gmAsterisk',
            'square': 'gmSquare',
            'square*': 'gmSquareF',
            'triangle': 'gmTriangle',
            'triangle*': 'gmTriangleF',
            'diamond': 'gmDiamond',
            'diamond*': 'gmDiamondF',
        }
        self.markerId = markerIdBaseDict[self.markerShape]
        self.markerId += "_%i" % GramSvgMarker._counter
        GramSvgMarker._counter += 1
        #self.haveDoneResetMarkerId = False


    def getTikz(self):
        pass

    def getSvg(self):
        gm = ["GramSvgMarker.getSvg() markerShape %s, markerId %s, color %s, fill %s" % (
            self.markerShape, self.markerId, self.color, self.fill)]
        #print gm[0]
        if not self.color and not self.fill:
            self.fill = 'black'
            gm.append("... setting fill to black")
        elif self.color and not self.fill:
            self.fill = self.color
            gm.append("... setting fill to the color")
        elif self.fill and not self.color:
            self.color = 'black'
            gm.append("... setting the color to the fill")

        # if len(gm) == 2:
        #     print gm[1]

            
        
        #mySc = 0.035 * self.svgPxForCm
        mySc = 0.038 * self.svgPxForCm

        if self.markerRelativeSize:
            mySc *= self.markerRelativeSize

        mySc2 = mySc * 2
        mySc4 = mySc * 4
        myScR = mySc * 1.7
        ss = []
        ss.append('  <marker id="%s" markerWidth="%.2f" markerHeight="%.2f" refX="%.2f" refY="%.2f">' % (
            self.markerId, mySc4, mySc4, mySc2, mySc2))


        if self.markerShape == '*':   # filled circle
            ss2 = []
            ss2.append('    <circle cx="%.2f" cy="%.2f" r="%.2f"' % (
                mySc2, mySc2, myScR))
            # if self.color:
            #     ss2.append('stroke="%s"' % self.color.svgColor)
            #     if self.color.svgColorOpacity:
            #         ss2.append('stroke-opacity="%s"' % self.color.svgColorOpacity)
            # else:
            #     if not self.fill:
            #         #gm.append("No color (OK), but also no fill --- invisible?")
            #         #raise GramError(gm)
            #         #self.fill = 'black'
            #         pass
            #     #ss2.append('stroke="black"')
            # if self.fill:
            #     ss2.append('fill="%s"' % self.fill.svgColor)
            #     if self.fill.svgColorOpacity:
            #         ss2.append('fill-opacity="%s"' % self.fill.svgColorOpacity)
            # else:
            #     ss2.append('fill="black"')
            ss2 += self.getSvgOptions()
            ss2.append('/>')
            ss.append(' '.join(ss2))

        elif self.markerShape == '+':
            ss2 = []
            ss2.append('    <path d="M%.2f,0 L%.2f,%.2f M0,%.2f L%.2f,%.2f"' % (
                mySc2, mySc2, mySc4, mySc2, mySc4, mySc2))
            # if self.color:
            #     ss2.append('stroke="%s"' % self.color.svgColor)
            #     if self.color.svgColorOpacity:
            #         ss2.append('stroke-opacity="%s"' % self.color.svgColorOpacity)
            # else:
            #     ss2.append('stroke="black"')
            ss2 += self.getSvgOptions()
            ss2.append('/>')
            ss.append(' '.join(ss2))

        elif self.markerShape == 'x':
            mySc01 = mySc * 0.1
            mySc39 = mySc * 3.9
            ss2 = []
            ss2.append('    <path d="M %.2f,%.2f L %.2f,%.2f M %.2f,%.2f L %.2f,%.2f"' % (
                mySc01, mySc01, mySc39, mySc39, mySc39, mySc01, mySc01, mySc39))
            # if self.color:
            #     ss2.append('stroke="%s"' % self.color.svgColor)
            #     if self.color.svgColorOpacity:
            #         ss2.append('stroke-opacity="%s"' % self.color.svgColorOpacity)
            # else:
            #     ss2.append('stroke="black"')
            ss2 += self.getSvgOptions()
            ss2.append('/>')
            ss.append(' '.join(ss2))

        elif self.markerShape == '-':
            ss2 = []
            ss2.append('    <path d="M 0,%.2f L%.2f,%.2f"' % (
                mySc2, mySc4, mySc2))
            # if self.color:
            #     ss2.append('stroke="%s"' % self.color.svgColor)
            #     if self.color.svgColorOpacity:
            #         ss2.append('stroke-opacity="%s"' % self.color.svgColorOpacity)
            # else:
            #     ss2.append('stroke="black"')
            ss2 += self.getSvgOptions()
            ss2.append('/>')
            ss.append(' '.join(ss2))

        elif self.markerShape == '|':
            ss2 = []
            ss2.append('    <path d="M%.2f,0 L%.2f,%.2f"' % (
                mySc2, mySc2, mySc4))
            # if self.color:
            #     ss2.append('stroke="%s"' % self.color.svgColor)
            #     if self.color.svgColorOpacity:
            #         ss2.append('stroke-opacity="%s"' % self.color.svgColorOpacity)
            # else:
            #     ss2.append('stroke="black"')
            ss2 += self.getSvgOptions()
            ss2.append('/>')
            ss.append(' '.join(ss2))

        elif self.markerShape == 'o':   # empty circle
            ss2 = []
            ss2.append('    <circle cx="%.2f" cy="%.2f" r="%.2f"' % (
                mySc2, mySc2, myScR))
            if self.color:
                ss2.append('stroke="%s"' % self.color.color)
                if self.color.value and self.color.transparent:
                    ss2.append('stroke-opacity="%s"' % self.color.value)
            else:
                ss2.append('stroke="black"')
            ss2.append('fill="none"')
            # ss2 += self.getSvgOptions()
            ss2.append('/>')
            ss.append(' '.join(ss2))

        elif self.markerShape == 'asterisk':
            ss2 = []
            ss2.append('    <path d="M %.2f,%.2f L %.2f,%.2f M %.2f,%.2f L %.2f,%.2f M %.2f,%.2f L %.2f,%.2f"' % (
                mySc * 3.732, mySc, 
                mySc * 0.268, mySc * 3., 
                mySc2, 0, 
                mySc2, mySc4, 
                mySc * 0.268, mySc, 
                mySc * 3.732, mySc * 3.))
            # if self.color:
            #     ss2.append('stroke="%s"' % self.color.svgColor)
            #     if self.color.svgColorOpacity:
            #         ss2.append('stroke-opacity="%s"' % self.color.svgColorOpacity)
            # else:
            #     ss2.append('stroke="black"')
            ss2 += self.getSvgOptions()
            ss2.append('/>')
            ss.append(' '.join(ss2))

        elif self.markerShape.startswith('square'):
            mySc03 = mySc * 0.3
            mySc37 = mySc * 3.7
            ss2 = []
            ss2.append('    <path d="M%.2f,%.2f L%.2f,%.2f %.2f,%.2f %.2f,%.2f z"' % (
                mySc03, mySc03, mySc37, mySc03, mySc37, mySc37, mySc03, mySc37))
            if self.color:
                ss2.append('stroke="%s"' % self.color.color)
                if self.color.value and self.color.transparent:
                    ss2.append('stroke-opacity="%s"' % self.color.value)
            #else:
            #    ss2.append('stroke="black"')
            isFilled = False
            if self.markerShape.endswith('*'):
                isFilled = True
            if not self.color and not isFilled:
                ss2.append('stroke="black"')
            if isFilled:
                if self.fill:
                    ss2.append('fill="%s"' % self.fill.color)
                    if self.fill.value and self.fill.transparent:
                        ss2.append('fill-opacity="%s"' % self.fill.value)
                else:
                    ss2.append('fill="black"')
            else:
                ss2.append('fill="none"')
               
            ss2.append('/>')
            ss.append(' '.join(ss2))

        elif self.markerShape.startswith('triangle'):
            mySc37 = mySc * 3.7
            ss2 = []
            ss2.append('    <path d="M%.2f,0 L%.2f,%.2f 0,%.2f z"' % (
                mySc2, mySc4, mySc37, mySc37))
            if self.color:
                ss2.append('stroke="%s"' % self.color.color)
                if self.color.value and self.color.transparent:
                    ss2.append('stroke-opacity="%s"' % self.color.value)
            #else:
            #    ss2.append('stroke="black"')
            isFilled = False
            if self.markerShape.endswith('*'):
                isFilled = True
            if not self.color and not isFilled:
                ss2.append('stroke="black"')
            if isFilled:
                if self.fill:
                    ss2.append('fill="%s"' % self.fill.color)
                    if self.fill.value and self.fill.transparent:
                        ss2.append('fill-opacity="%s"' % self.fill.value)
                else:
                    ss2.append('fill="black"')
            else:
                ss2.append('fill="none"')
               
            ss2.append('/>')
            ss.append(' '.join(ss2))

        elif self.markerShape.startswith('diamond'):
            ss2 = []
            ss2.append('    <path d="M%.2f,0 L%.2f,%.2f %.2f,%.2f 0,%.2f z"' % (
                mySc2, mySc4, mySc2, mySc2, mySc4, mySc2))
            if self.color:
                ss2.append('stroke="%s"' % self.color.color)
                if self.color.value and self.color.transparent:
                    ss2.append('stroke-opacity="%s"' % self.color.value)
            #else:
            #    ss2.append('stroke="black"')
            isFilled = False
            if self.markerShape.endswith('*'):
                isFilled = True
            if not self.color and not isFilled:
                ss2.append('stroke="black"')
            if isFilled:
                if self.fill:
                    ss2.append('fill="%s"' % self.fill.color)
                    if self.fill.value and self.fill.transparent:
                        ss2.append('fill-opacity="%s"' % self.fill.value)
                else:
                    ss2.append('fill="black"')
            else:
                ss2.append('fill="none"')
               
            ss2.append('/>')
            ss.append(' '.join(ss2))



        ss.append('  </marker>\n')
        return '\n'.join(ss)

                 

class GramGrid(GramGraphic):

    def __init__(self, llx, lly, urx, ury, color='gray'):
        GramGraphic.__init__(self)
        assert isinstance(llx, int)
        assert isinstance(lly, int)
        assert isinstance(urx, int)
        assert isinstance(ury, int)

        assert urx > llx
        assert ury > lly

        self.llx = llx
        self.lly = lly
        self.urx = urx
        self.ury = ury
        self.color = color

    def getTikz(self):
        ss = []
        # if self.comment:
        #    ss.append("%% %s" % self.comment)
        ss.append("\draw[%s,very thin] (%i,%i) grid (%i,%i);" %
                  (self.color.color, self.llx, self.lly, self.urx, self.ury))
        for gr in self.graphics:
            ss.append(gr.getTikz())
        return '\n'.join(ss)

    def getSvg(self):
        ss = []
        ss.append("\n<!-- grid -->\n")
        if self.color.transparent:
            ss.append('<path stroke="%s" stroke-opacity="%s" stroke-width="0.5" d="' % (
                      self.color.color, self.color.value))
        else:
            ss.append('<path stroke="%s" stroke-width="0.5" d="' % self.color.color)
        for colNum in range(self.llx, self.urx + 1):
            ss.append('M %.1f %.1f L %.1f %.1f ' % (
                self.svgPxForCmF(colNum), -self.svgPxForCmF(self.lly),
                self.svgPxForCmF(colNum), -self.svgPxForCmF(self.ury)))
        for rowNum in range(self.lly, self.ury + 1):
            ss.append('M %.1f %.1f L %.1f %.1f ' % (
                self.svgPxForCmF(self.llx), -self.svgPxForCmF(rowNum),
                self.svgPxForCmF(self.urx), -self.svgPxForCmF(rowNum)))
        ss.append('"/>\n')
        for gr in self.graphics:
            ss.append(gr.getSvg())
        return ''.join(ss)

    def setBB(self):
        extra = 0.1
        self.bb = [self.llx - extra, self.lly - extra,
                   self.urx + extra, self.ury + extra]



###############################################################
###############################################################
#
# TEXT
#
###############################################################
###############################################################


class GramText(GramGraphic):

    def __init__(self, text):
        GramGraphic.__init__(self)

        # GramGraphic provides ---
        # self.cA = None
        # self.comment = None
        # self.style = None
        # self.myStyle = None
        # self.bb = [0.0] * 4
        # self.svgId = None
        # Plus all the stuff inherited from GramTikzStyle
        # That includes _textHeight and _textDepth, and GramTikzStyle properties textHeight and TextDepth

        
        #print("GramText.__init__(%s)" % text)
        self.rawText = text
        self.cookedText = None                 # with added modifiers like sffamily, bfseries, itshape, Large, etc
        if text.startswith(r"\begin{minipage}"):
            self.mpText = text
        else:
            self.mpText = None                     # wrapped in a minipage
        # self.name = f"l{self.labelIdCounter}"  
        # self.labelIdCounter += 1
        # self.labelGForIdDict[self.name] = self  # Gram-wide dictionary
        self.length = 0.1

        self.corners = None
        self.fullHeight = 0.0         # Note we also have self.textHeight, inherited, which is different
        self.tbb = [0.0] * 4

        # more text measurements for tikz/pyx 
        # inner sep is initially 0.3333em
        # em is the point size; it is not the width of an M (although maybe in history it was ...)
        # default inner sep is 0.3333em for normalsize text, regardless of text size
        # So for 10pt documents, inner sep is 3.333pt
        self.ex = 0.0         # vertical size of an x
        self.exWid = 0.0      # width of an x
        self.bigX = 0.0       # vertical size of a big X, cap height
        self.yuh = 0.0        # vertical underhang of a y
        self.half_normal_x = 0.0   # half vertical size of a normalsize x
        self.svg_half_normal_x = 0.0   # half vertical size of a normalsize x
        self.underhang = 0.0
        self.rise = 0.0
        self.svgBaseline_cm = 0.0   # Used to calculate underhang from inkscape bb
        # Gram._svgNormalsize_x = None  # vertical size, for mid anchor, measured by inkscape

         
        self.fontSizeMultiplierDict = {
            'tiny': 0.5,
            'scriptsize': 0.7,
            'footnotesize': 0.8,
            'small': 0.9,
            'normalsize': 1.,
            'large': 1.2,
            'Large': 1.44,
            'LARGE': 1.728,
            'huge': 2.074,
            'Huge': 2.488,
        }

        self.gX = 0.0
        self.gY = 0.0

    def dump(self):
        print("GramText.dump()")
        spacer = " " * 8
        print(f"{spacer} rawText: {self.rawText}")
        print(f"{spacer} cookedText: {self.cookedText}")
        # print(f"{spacer} name: {self.name}")
        print(f"{spacer} cA: {self.cA.xPosn:.3f},{self.cA.yPosn:.3f}")
        print(f"{spacer} anchor: {self.getAnch()}")
        print(f"{spacer} bb: {self.bb}")
        print(f"{spacer} length: {self.length:.5f}")
        print(f"{spacer} fullHeight: {self.fullHeight:.5f}")
        print(f"{spacer} innerSep: {self.getInnerSep()}")
        print(f"{spacer} lineThickness (cm): {cmForLineThickness(self.getLineThickness())}")
        print(f"{spacer} underhang (cm): {self.underhang}")
        print(f"{spacer} rise (cm): {self.rise}")
        print(f"{spacer} svgNormalsize_x (cm): {Gram._svgNormalsize_x}")
        print(f"{spacer} svgBaseline_cm (cm): {self.svgBaseline_cm}")
        # print(f"{spacer} ")
        # print(f"{spacer} ")


    def setCookedText(self):
        if self.mpText:
            self.cookedText = self.mpText
        else:
            self.cookedText = self.cookText(self.rawText)

    def cookText(self, rawText):
        """Add adjectives like sffamily, bfseries, itshape, Large, etc to rawText.
        """
        #_goodTextFamilies = ['rmfamily', 'sffamily', 'ttfamily']
        #_goodTextSeries = ['bfseries']
        #_goodTextShapes = ['itshape', 'scshape']

        if not rawText:
            return ''

        
        if rawText.startswith(r"\begin{minipage}"):
            raise GramError("programming error: cookText with minipage.")

        if 1:
            theText = func.fixCharsForLatex(rawText)
        else:
            theText = rawText
        # print("cookText() the raw text is %s" % rawText)
        # print("cookText() theText (a) is %s" % theText)
        theTextFamily = self.getTextFamily()
        theTextSeries = self.getTextSeries()
        theTextShape = self.getTextShape()
        theSize = self.getTextSize()

        if theTextShape:
            theText = r"\%s %s" % (theTextShape, theText)
        if theTextSeries:
            theText = r"\%s %s" % (theTextSeries, theText)
        if theTextFamily:
            theText = r"\%s %s" % (theTextFamily, theText)
        if theSize and theSize != 'normalsize':
            theText = r"\%s %s" % (theSize, theText)

        return theText

    def setTextLengthHeightAndMetrics(self):
        """This runs pyx on the cookedText, gets length and height
        
        and X, x, yuh measurements
        """

        # 1 PostScript point = 0.35277138 mm
        ptToCm = 0.035277138

        try:
            # print("just before pyx, cookedText is", self.cookedText)
            t = pyx.text.text(0.0, 0.0, self.cookedText)
        except:
            raise GramError("pyx gagged on '%s', which was cooked to '%s'" % (
                self.rawText, self.cookedText))

        tbb = t.bbox()
        self.tbb = [tbb.llx_pt * ptToCm, tbb.lly_pt * ptToCm, tbb.urx_pt * ptToCm, tbb.ury_pt * ptToCm]
        # print(f"GramText.setTextLengthAndMetrics().  self.tbb is {self.tbb} ")

        self.length = (tbb.urx_pt - tbb.llx_pt) * ptToCm

        # Width for wrapping, or None
        theTextWrapWidth = self.getTextWrapWidth()
        if 0 and theTextWrapWidth:
            theInnerSep = self.getInnerSep()
            # print("theTextWrapWidth", theTextWrapWidth, " theInnerSep", theInnerSep)
            if theInnerSep:
                self.length += theInnerSep

        self.fullHeight = (tbb.ury_pt - tbb.lly_pt) * ptToCm
        self.underhang = -tbb.lly_pt * ptToCm    # might be zero
        self.rise = tbb.ury_pt * ptToCm
        # print("setTextLengthHeightAndMetrics() The text '%s' is %.3f cm long, and %.3f cm  high" % (self.cookedText, self.length, self.fullHeight))
        # sys.exit()

        #self.length = 3.
        #self.fullHeight = 2.
        #self.underhang = 0.1
        #self.rise = 0.2

        cooked = self.cookText('X')
        t = pyx.text.text(0.0, 0.0, cooked)
        tbb = t.bbox()
        self.bigX = tbb.ury_pt * ptToCm

        cooked = self.cookText('x')
        t = pyx.text.text(0.0, 0.0, cooked)
        tbb = t.bbox()
        self.ex = tbb.ury_pt * ptToCm
        self.exWid = tbb.urx_pt * ptToCm

        cooked = self.cookText('y')
        t = pyx.text.text(0.0, 0.0, cooked)
        tbb = t.bbox()
        self.yuh = -tbb.lly_pt * ptToCm

        #cooked = 'M'
        #t = pyx.text.text(0.0, 0.0, cooked)
        #tbb = t.bbox()
        #self.normal_em = tbb.urx_pt * ptToCm

        cooked = 'x'
        t = pyx.text.text(0.0, 0.0, cooked)
        tbb = t.bbox()
        self.half_normal_x = 0.5 * tbb.ury_pt * ptToCm

    def getBiggestWidth(self):
        """This assumes a multi-line rawText, with newlines '\\' """
        # savedRawText = self.rawText
        #    1 PostScript point = 0.35277138 mm
        ptToCm = 0.035277138
        bits = self.rawText.split(r'\\')
        bits = [b.strip() for b in bits if b]
        #print(f"The bits are {bits}")
        #sys.exit()
        biggestWidth = 0.0
        for bit in bits:
            cookedText = self.cookText(bit)

            try:
                t = pyx.text.text(0.0, 0.0, cookedText)
            except IOError:
                raise GramError("pyx gagged on '%s', which was cooked to '%s'" % (
                    b, cookedText))

            tbb = t.bbox()
            thisWidth = (tbb.urx_pt - tbb.llx_pt) * ptToCm
            # print(f"getBiggestWidth() bit cookedText: {cookedText}, got width {thisWidth}")
            if thisWidth > biggestWidth:
                biggestWidth = thisWidth
        # print("getBiggestWidth: %.3fcm" % biggestWidth)

        if 1:
            # But note that we are using tbb, or tight bounding box.  This
            # seems to cause wrapping of the longest line.  So grow it.

            innerSep = self.getInnerSep()
            biggestWidth += (1 * innerSep)

        return biggestWidth

    def setBogusBB(self):

        if self.style:
            print("====== Turning off style for textbox '%s'" % self.rawText)
            self.style = None
        theAnch = self.getAnch()
        if theAnch == 'south west':
            self.bb[0] = self.cA.xPosn
            self.bb[1] = self.cA.yPosn
            self.bb[2] = self.cA.xPosn + 1.
            self.bb[3] = self.cA.yPosn + 1.

        elif theAnch == 'south':
            self.bb[0] = self.cA.xPosn - 0.5
            self.bb[1] = self.cA.yPosn
            self.bb[2] = self.cA.xPosn + 0.5
            self.bb[3] = self.cA.yPosn + 1.0

        elif theAnch == 'south east':
            self.bb[0] = self.cA.xPosn - 1.0
            self.bb[1] = self.cA.yPosn
            self.bb[2] = self.cA.xPosn
            self.bb[3] = self.cA.yPosn + 1.0

        elif theAnch == 'base east':
            self.bb[0] = self.cA.xPosn - 1.
            self.bb[1] = self.cA.yPosn - 0.35
            self.bb[2] = self.cA.xPosn
            self.bb[3] = self.cA.yPosn + 0.65

        elif theAnch == 'east':
            self.bb[0] = self.cA.xPosn - 1.0
            self.bb[1] = self.cA.yPosn - 0.5
            self.bb[2] = self.cA.xPosn
            self.bb[3] = self.cA.yPosn + 0.5

        elif theAnch == 'north east':
            self.bb[0] = self.cA.xPosn - 1.0
            self.bb[1] = self.cA.yPosn - 1.0
            self.bb[2] = self.cA.xPosn
            self.bb[3] = self.cA.yPosn

        elif theAnch == 'north':
            self.bb[0] = self.cA.xPosn - 0.5
            self.bb[1] = self.cA.yPosn - 1.0
            self.bb[2] = self.cA.xPosn + 0.5
            self.bb[3] = self.cA.yPosn

        elif theAnch == 'north west':
            self.bb[0] = self.cA.xPosn
            self.bb[1] = self.cA.yPosn - 1.0
            self.bb[2] = self.cA.xPosn + 1.0
            self.bb[3] = self.cA.yPosn

        elif theAnch == 'west':
            self.bb[0] = self.cA.xPosn
            self.bb[1] = self.cA.yPosn - 0.5
            self.bb[2] = self.cA.xPosn + 1.0
            self.bb[3] = self.cA.yPosn + 0.5

        elif theAnch == 'base west':
            self.bb[0] = self.cA.xPosn
            self.bb[1] = self.cA.yPosn - 0.35
            self.bb[2] = self.cA.xPosn + 1.0
            self.bb[3] = self.cA.yPosn + 0.65

        elif theAnch == 'base':
            self.bb[0] = self.cA.xPosn - 0.5
            self.bb[1] = self.cA.yPosn - 0.35
            self.bb[2] = self.cA.xPosn + 0.5
            self.bb[3] = self.cA.yPosn + 0.65

        elif theAnch == 'mid west':
            self.bb[0] = self.cA.xPosn
            self.bb[1] = self.cA.yPosn - 0.5
            self.bb[2] = self.cA.xPosn + 1.0
            self.bb[3] = self.cA.yPosn + 0.5

        elif theAnch == 'mid':
            self.bb[0] = self.cA.xPosn - 0.5
            self.bb[1] = self.cA.yPosn - 0.5
            self.bb[2] = self.cA.xPosn + 0.5
            self.bb[3] = self.cA.yPosn + 0.5

        elif theAnch == 'mid east':
            self.bb[0] = self.cA.xPosn - 1.0
            self.bb[1] = self.cA.yPosn - 0.5
            self.bb[2] = self.cA.xPosn
            self.bb[3] = self.cA.yPosn + 0.5

        elif theAnch == 'center' or theAnch is None:
            self.bb[0] = self.cA.xPosn - 0.5
            self.bb[1] = self.cA.yPosn - 0.5
            self.bb[2] = self.cA.xPosn + 0.5
            self.bb[3] = self.cA.yPosn + 0.5


        # ====================================

        else:
            raise GramError("GramText.setBogusBB().  anch '%s' not implemented." % theAnch)

        

    def setBB(self):    # GramText
        # print("GramText '%s'  setBB()" % self.rawText)
        
        if not self.cA:
            self.cA = GramCoord()

        assert self.engine == 'tikz'

        boogers = [r'\includegraphics', r'\parbox']
        hasBooger = False
        for booger in boogers:
            if booger in self.rawText:
                hasBooger = True
                break
        if hasBooger:
            self.setBogusBB()
            return


        #if self.font == 'helvetica':
        #    # This should not be needed, but it is!  Is it still?
        #    # self.textFamily = 'sffamily'
        #    pass

        self.setCookedText()
        self.setTextLengthHeightAndMetrics()

        if 0:
            print("a GramText.setBB() for '%s';" % self.rawText)  
            print("    self.length is %s, self.fullHeight is %s" % (self.length, self.fullHeight))
            print("    bb is %s" % self.bb)

        halfHeight = self.fullHeight / 2.0
        halfLength = self.length / 2.0
        # oneSep = (self.normal_em * 0.3333) + 0.009 # The 0.009 is a total
        # fudge, but it appears to be right.

        theAnch = self.getAnch()
        #print("xxy GramText.setBB() theAnch is %s" % theAnch)
        oneInnerSep = self.getInnerSep()
        #if oneInnerSep < 0.11:
        #    print(f"GramText.setBB() {theAnch}, innerSep {oneInnerSep}")
        if oneInnerSep is None:
            raise GramError("GramText.setBB(). %s getInnerSep() returned None." % self.rawText)

        theLineThickness = self.getLineThickness()
        # if oneInnerSep is None:
        #    oneInnerSep = self.defaultInnerSep
        twoInnerSep = 2 * oneInnerSep
        twoOuterSep = cmForLineThickness(theLineThickness)
        oneOuterSep = 0.5 * twoOuterSep
        # print "    oneInnerSep is %.3f" % oneInnerSep
        # print "    oneOuterSep is %.3f" % oneOuterSep
        # print "  %s theAnch is %s, length=%.5f, height=%s, halfHeight=%s" % (
        #    self.rawText, theAnch, self.length, self.fullHeight, halfHeight)
        # sys.exit()


        if theAnch == 'south west':
            self.tbb[0] = self.cA.xPosn + oneOuterSep + oneInnerSep
            self.tbb[1] = self.cA.yPosn + oneOuterSep + oneInnerSep
            self.tbb[2] = self.tbb[0] + self.length
            self.tbb[3] = self.tbb[1] + self.fullHeight

            self.bb[0] = self.cA.xPosn
            self.bb[1] = self.cA.yPosn
            self.bb[2] = self.cA.xPosn + self.length + twoInnerSep + twoOuterSep
            self.bb[3] = self.cA.yPosn + self.fullHeight + twoInnerSep + twoOuterSep



        elif theAnch == 'south':
            self.bb[0] = self.cA.xPosn - \
                (halfLength + oneInnerSep + oneOuterSep)
            self.bb[1] = self.cA.yPosn
            self.bb[2] = self.cA.xPosn + \
                (halfLength + oneInnerSep + oneOuterSep)
            self.bb[3] = self.cA.yPosn + \
                self.fullHeight + twoInnerSep + twoOuterSep

        elif theAnch == 'south east':
            self.bb[0] = self.cA.xPosn - \
                (self.length + twoInnerSep + twoOuterSep)
            self.bb[1] = self.cA.yPosn
            self.bb[2] = self.cA.xPosn
            self.bb[3] = self.cA.yPosn + \
                (self.fullHeight + twoInnerSep + twoOuterSep)

        elif theAnch == 'base east':
            # if self.textWrapWidth:
            if 0:
                self.bb[0] = self.cA.xPosn - \
                    (self.length + twoInnerSep + twoOuterSep)
                self.bb[1] = self.cA.yPosn - \
                    (self.fullHeight + oneInnerSep + oneOuterSep)
                self.bb[2] = self.cA.xPosn
                self.bb[3] = self.cA.yPosn + (oneInnerSep + oneOuterSep)
            else:
                self.bb[0] = self.cA.xPosn - (self.length + twoInnerSep + twoOuterSep)
                self.bb[1] = self.cA.yPosn - (self.underhang + oneInnerSep + oneOuterSep)
                self.bb[2] = self.cA.xPosn
                self.bb[3] = self.cA.yPosn + (self.rise + oneInnerSep + oneOuterSep)

        elif theAnch == 'east':
            self.bb[0] = self.cA.xPosn - (self.length + twoInnerSep + twoOuterSep)
            self.bb[1] = self.cA.yPosn - (halfHeight + oneInnerSep + oneOuterSep)
            self.bb[2] = self.cA.xPosn
            self.bb[3] = self.cA.yPosn + (halfHeight + oneInnerSep + oneOuterSep)

        elif theAnch == 'north east':
            self.bb[0] = self.cA.xPosn - \
                (self.length + twoInnerSep + twoOuterSep)
            self.bb[1] = self.cA.yPosn - \
                (self.fullHeight + twoInnerSep + twoOuterSep)
            self.bb[2] = self.cA.xPosn
            self.bb[3] = self.cA.yPosn

        elif theAnch == 'north':
            self.bb[0] = self.cA.xPosn - \
                (halfLength + oneInnerSep + oneOuterSep)
            self.bb[1] = self.cA.yPosn - \
                (self.fullHeight + twoInnerSep + twoOuterSep)
            self.bb[2] = self.cA.xPosn + \
                (halfLength + oneInnerSep + oneOuterSep)
            self.bb[3] = self.cA.yPosn

        elif theAnch == 'north west':
            self.bb[0] = self.cA.xPosn
            self.bb[1] = self.cA.yPosn - \
                (self.fullHeight + twoInnerSep + twoOuterSep)
            self.bb[2] = self.cA.xPosn + \
                (self.length + twoInnerSep + twoOuterSep)
            self.bb[3] = self.cA.yPosn

        elif theAnch == 'west':
            self.bb[0] = self.cA.xPosn
            self.bb[1] = self.cA.yPosn - \
                (halfHeight + oneInnerSep + oneOuterSep)
            self.bb[2] = self.cA.xPosn + \
                (self.length + twoInnerSep + twoOuterSep)
            self.bb[3] = self.cA.yPosn + \
                (halfHeight + oneInnerSep + oneOuterSep)

        elif theAnch == 'base west':
            # if self.textWrapWidth:
            if 0:
                self.bb[0] = self.cA.xPosn
                self.bb[1] = self.cA.yPosn - \
                    (self.fullHeight + oneInnerSep + oneOuterSep)
                self.bb[2] = self.cA.xPosn + \
                    (self.length + twoInnerSep + twoOuterSep)
                self.bb[3] = self.cA.yPosn + (oneInnerSep + oneOuterSep)
            else:
                self.bb[0] = self.cA.xPosn
                self.bb[1] = self.cA.yPosn - (self.underhang + oneInnerSep + oneOuterSep)
                self.bb[2] = self.cA.xPosn + (self.length + twoInnerSep + twoOuterSep)
                self.bb[3] = self.cA.yPosn + (self.rise + oneInnerSep + oneOuterSep)

        elif theAnch == 'base':
            # if self.textWrapWidth:
            if 0:
                self.bb[0] = self.cA.xPosn - \
                    (halfLength + oneInnerSep + oneOuterSep)
                self.bb[1] = self.cA.yPosn - \
                    (self.fullHeight + oneInnerSep + oneOuterSep)
                self.bb[2] = self.cA.xPosn + \
                    (halfLength + oneInnerSep + oneOuterSep)
                self.bb[3] = self.cA.yPosn + (oneInnerSep + oneOuterSep)
            else:
                self.bb[0] = self.cA.xPosn - (halfLength + oneInnerSep + oneOuterSep)
                self.bb[1] = self.cA.yPosn - (self.underhang + oneInnerSep + oneOuterSep)
                self.bb[2] = self.cA.xPosn + (halfLength + oneInnerSep + oneOuterSep)
                self.bb[3] = self.cA.yPosn + (self.rise + oneInnerSep + oneOuterSep)

        elif theAnch == 'center' or theAnch is None:
            self.bb[0] = self.cA.xPosn - (halfLength + oneInnerSep + oneOuterSep)
            self.bb[1] = self.cA.yPosn - (halfHeight + oneInnerSep + oneOuterSep)
            self.bb[2] = self.cA.xPosn + (halfLength + oneInnerSep + oneOuterSep)
            self.bb[3] = self.cA.yPosn + (halfHeight + oneInnerSep + oneOuterSep)

        # ====================================
        elif theAnch == 'mid west':
            if self.textWrapWidth:
                # self.bb[0] = self.cA.xPosn
                # self.bb[1] = self.cA.yPosn - (self.fullHeight + twoInnerSep + oneOuterSep)
                # self.bb[2] = self.cA.xPosn + (self.length + twoInnerSep + twoOuterSep)
                # # + (self.fullHeight + oneInnerSep + oneOuterSep)
                # self.bb[3] = self.cA.yPosn
                
                # Behaves like "west"
                self.bb[0] = self.cA.xPosn
                self.bb[1] = self.cA.yPosn - \
                    (halfHeight + oneInnerSep + oneOuterSep)
                self.bb[2] = self.cA.xPosn + \
                    (self.length + twoInnerSep + twoOuterSep)
                self.bb[3] = self.cA.yPosn + \
                    (halfHeight + oneInnerSep + oneOuterSep)
                
            else:
                self.bb[0] = self.cA.xPosn
                self.bb[1] = self.cA.yPosn - (self.underhang + self.half_normal_x + oneInnerSep + oneOuterSep)
                self.bb[2] = self.cA.xPosn + (self.length + twoInnerSep + twoOuterSep)
                self.bb[3] = self.cA.yPosn + ((self.rise - self.half_normal_x) + oneInnerSep + oneOuterSep)

        elif theAnch == 'mid east':
            if self.textWrapWidth:
                # self.bb[0] = self.cA.xPosn - (self.length + twoInnerSep + twoOuterSep)
                # self.bb[1] = self.cA.yPosn - (self.fullHeight + twoInnerSep + oneOuterSep)
                # self.bb[2] = self.cA.xPosn
                # # + (self.fullHeight + oneInnerSep + oneOuterSep)
                # self.bb[3] = self.cA.yPosn

                # This week it behaves like "east"
                self.bb[0] = self.cA.xPosn - (self.length + twoInnerSep + twoOuterSep)
                self.bb[1] = self.cA.yPosn - (halfHeight + oneInnerSep + oneOuterSep)
                self.bb[2] = self.cA.xPosn
                self.bb[3] = self.cA.yPosn + (halfHeight + oneInnerSep + oneOuterSep)

            else:
                self.bb[0] = self.cA.xPosn - (self.length + twoInnerSep + twoOuterSep)
                self.bb[1] = self.cA.yPosn - (self.underhang + self.half_normal_x + oneInnerSep + oneOuterSep)
                self.bb[2] = self.cA.xPosn
                self.bb[3] = self.cA.yPosn + ((self.rise - self.half_normal_x) + oneInnerSep + oneOuterSep)

        elif theAnch == 'mid':     # setBB
            if self.textWrapWidth:
                # self.bb[0] = self.cA.xPosn - (halfLength + oneInnerSep + oneOuterSep)
                # self.bb[1] = self.cA.yPosn - (self.fullHeight + twoInnerSep + oneOuterSep)
                # self.bb[2] = self.cA.xPosn + (halfLength + oneInnerSep + oneOuterSep)
                # self.bb[3] = self.cA.yPosn  # + (oneInnerSep + oneOuterSep)

                # This week it behaves like "center"
                self.bb[0] = self.cA.xPosn - (halfLength + oneInnerSep + oneOuterSep)
                self.bb[1] = self.cA.yPosn - (halfHeight + oneInnerSep + oneOuterSep)
                self.bb[2] = self.cA.xPosn + (halfLength + oneInnerSep + oneOuterSep)
                self.bb[3] = self.cA.yPosn + (halfHeight + oneInnerSep + oneOuterSep)
            else:
                self.bb[0] = self.cA.xPosn - (halfLength + oneInnerSep + oneOuterSep)
                self.bb[1] = self.cA.yPosn - (self.underhang + self.half_normal_x + oneInnerSep + oneOuterSep)
                self.bb[2] = self.cA.xPosn + (halfLength + oneInnerSep + oneOuterSep)
                self.bb[3] = self.cA.yPosn + ((self.rise - self.half_normal_x) + oneInnerSep + oneOuterSep)

        else:
            raise GramError("anch '%s' not implemented." % theAnch)

        #print("b GramText.setBB() for '%s';  self.length is %s, bb is %s" % (self.rawText, self.length, self.bb))


        # Get bb for rotated text  GramText.setBB
        theRotate = self.getRotate()
        if theRotate:
            # The textbox rotates around its anchor.
            # print "   *tb.bb %25s  %.2f %.2f %.2f %.2f " % (
            # self.rawText, self.bb[0], self.bb[1], self.bb[2], self.bb[3])
            corners = []
            corners.append([self.bb[0], self.bb[1]])
            corners.append([self.bb[2], self.bb[1]])
            corners.append([self.bb[2], self.bb[3]])
            corners.append([self.bb[0], self.bb[3]])
            # print "xPosn=%.1f, yPosn=%.1f" % (self.cA.xPosn,
            # self.cA.yPosn)
            for cNum in range(4):
                corner = corners[cNum]
                corner[0] -= self.cA.xPosn
                corner[1] -= self.cA.yPosn
            polarCorners = []
            for cNum in range(4):
                polarCorners.append(func.square2polar(corners[cNum]))
            # print "a polarCorners = ", polarCorners
            rads = (theRotate * math.pi) / 180.
            # print "theRotate %f is %f radians" % (theRotate, rads)
            for cNum in range(4):
                pCorner = polarCorners[cNum]
                pCorner[0] += rads
            # print "b polarCorners = ", polarCorners

            corners = []
            for cNum in range(4):
                corners.append(func.polar2square(polarCorners[cNum]))
            # print 'corners', corners
            for cNum in range(4):
                corner = corners[cNum]
                corner[0] += self.cA.xPosn
                corner[1] += self.cA.yPosn
            # print corners

            llx = 1000000.
            lly = 1000000.
            urx = -1000000.
            ury = -1000000.

            for cNum in range(4):
                corner = corners[cNum]
                if corner[0] < llx:
                    llx = corner[0]
                if corner[1] < lly:
                    lly = corner[1]
                if corner[0] > urx:
                    urx = corner[0]
                if corner[1] > ury:
                    ury = corner[1]
            self.bb = [llx, lly, urx, ury]
            # print "   @tb.bb %25s  %.2f %.2f %.2f %.2f " % (
            # self.rawText, self.bb[0], self.bb[1], self.bb[2], self.bb[3])
            self.corners = corners

        theXShift = self.getXShift()
        if theXShift:
            self.bb[0] += theXShift
            self.bb[2] += theXShift
            if self.corners:
                for cNum in range(4):
                    self.corners[cNum][0] += theXShift
        theYShift = self.getYShift()
        if theYShift:
            self.bb[1] += theYShift
            self.bb[3] += theYShift
            if self.corners:
                for cNum in range(4):
                    self.corners[cNum][1] += theYShift

    def wrapRawInMinipage(self):
        gm = ["GramText.wrapRawInMinipage()"]

        if self.textWrapWidth:
            widStr = "%.3fcm" % self.textWrapWidth
        else:
            gm.append("textWrapWidth needs to be set.")
            raise GramError(gm)

        
        alig = self.textAlign

        # Gram._goodTextAligns = [None, 'left', 'flush left', 'right', 'flush right', 
        #                    'center', 'flush center', 'justify', 'none']
        mpAlig = None
        if alig in [None, 'left', 'flush left', 'none']:
            mpAlig = "raggedright"
        elif alig in ["right", "flush right"]:
            mpAlig = "raggedleft"
        elif alig in ["center", "flush center"]:
            mpAlig = "centering"
        elif alig in ["justify"]:
            mpAlig = "justify"
        assert mpAlig


        # print(f"wrapRawInMinipage() widStr = {widStr}, mpAlig={mpAlig}")

        cookedText = self.cookText(self.rawText)

        myCmds = ""
        for it in [mpAlig]:
            if it:
                myCmds += r"\%s" % it
        # print(myCmds)

        self.mpText = r"\begin{minipage}{%s}%s %s \end{minipage}" % (widStr, myCmds, cookedText)

    def setPositions(self):
        gm = ['GramText.setPositions() rawText=%s' % self.rawText]
        
        if self.engine == "tikz":
            if not self.haveStartedPyX:
                self.startPyX()

            if self.mpText:    # a minipage
                pass
            else:
                # Is it to be wrapped, multi-line?
                # If so, put it in a minipage
                isWrapped = False
                if self.textWrapWidth:
                    isWrapped = True
                else:
                    if r"\\" in self.rawText:
                        isWrapped = True
                        self.textWrapWidth = self.getBiggestWidth()

                if isWrapped:
                    self.wrapRawInMinipage()

            self.setBB()

        elif self.engine == "svg":
            pass
            


    def getTikz(self):   # GramText
        gm = ['GramText.getTikz() rawText=%s' % self.rawText]
        # print(gm[0])

        self.setPositions()

        if self.mpText:
            theText = self.mpText
        else:
            # We don't want to use self.cookedText here, because we get tikz options, below.
            # However, we want to escape underscores and such.
            # But not in includegraphics filenames
            if self.rawText.startswith(r"\includegraphics"):
                theText = self.rawText
            else:
                theText = func.fixCharsForLatex(self.rawText)

        
        # print(f"GramText.getTikz()  self.rawText= {self.rawText}")
        # print(f"theText (after fixCharsForLatex(self.rawText))= {theText}")

        # Hack
        # if 1:
        #     if 'fcolorbox' in theText:
        #         print("------fixing ------", theText)
        #         splText = theText.split()
        #         for tNum in range(len(splText)):
        #             if splText[tNum].startswith("\\fcolorbox"):
        #                 splText[tNum] = "\\raisebox{1.5bp}{\\scalebox{0.5}{%s}}" % splText[
        #                     tNum]
        #         theText = ' '.join(splText)


        ss = []
        ss.append(r'\node')

        options = self.getTikzOptions()
        #print("%s, options %s" % (self.rawText, options))
        # If fill.value and fill.transparent, then fill-opacity is set to
        # fill.value (good) but the text gets that same opacity (bad).
        # Here is a hack fix.
        if self.fill and self.fill.value and self.fill.transparent:
            options.append("text opacity=1.0")

        if options:
            ss.append('[%s]' % ','.join(options))
        # if self.name:
        #    ss.append(f"({self.name})")
        if self.cA.name:
            ss.append('at (%s)' % self.cA.name)
        else:
            ss.append('at (%.3f,%.3f)' % (self.cA.xPosn, self.cA.yPosn))

        ss.append('{%s};' % theText)

        if 0:
            tbbLine = '\n'
            tbbLine += r"\draw [teal,ultra thin] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (
                self.tbb[0], self.tbb[1],
                self.tbb[2], self.tbb[3])
            # print tbbLine
            ss.append(tbbLine)


        if self.showTextBB:
            # bbLine = '\n'
            # bbLine += r"\draw [blue,ultra thin] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (
            #     self.tbb[0], self.tbb[1],
            #     self.tbb[2], self.tbb[3])
            # # print bbLine
            # ss.append(bbLine)

            bbLine = '\n'
            bbLine += r"\draw [red,ultra thin] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (
                self.bb[0], self.bb[1],
                self.bb[2], self.bb[3])
            # print bbLine
            ss.append(bbLine)

        if self.showTextAnchor:
            ss.append("\\draw [red] plot[only marks,mark=x] coordinates {(%.3f,%.3f)};" % (
                self.cA.xPosn, self.cA.yPosn))
        return ' '.join(ss)


    def svgDump(self):
        print("GramText.svgDump()")
        spacer = " " * 8
        print(f"{spacer} rawText: {self.rawText}")
        print(f"{spacer} cA: {self.cA.xPosn:.3f},{self.cA.yPosn:.3f}")
        print(f"{spacer} anchor: {self.getAnch()}")
        print(f"{spacer} length: {self.length:.5f}")
        print(f"{spacer} fullHeight: {self.fullHeight:.5f}")
        print(f"{spacer} underhang (cm): {self.underhang}")
        print(f"{spacer} rise (cm): {self.rise}")
        print(f"{spacer} Gram._svgNormalsize_x (cm): {Gram._svgNormalsize_x}")
        print(f"{spacer} svgBaseline_cm (cm): {self.svgBaseline_cm}")


    def getSvg(self):    # GramText
        gm = ['GramText.getSvg() rawText=%s' % self.rawText]
        # print(gm[0])
        if not self.cA:
            self.cA = GramCoord()
        if self.svgId:
            assert self.svgGForIdDict.get(self.svgId)
        else:
            self.setSvgIdAndAddToDict('text')
        # print gm[0], self.svgId, self.svgGForIdDict[self.svgId].rawText

        myClass = None
        myTextFamilyString = self.getTextFamily()
        if myTextFamilyString == 'ttfamily':
            myClass = 'ttfamily'
        elif myTextFamilyString == "sffamily":
            myClass = "sffamily"

        myTextSizeStr = self.getTextSize()
        #print(f"GramText.getSvg()  myTextSizeStr is {myTextSizeStr}")
        if myTextSizeStr is None or myTextSizeStr == 'normalsize':
            myTextSizeCm = self.svgTextNormalsize
        else:
            myTextSizeCm = self.fontSizeMultiplierDict[
                myTextSizeStr] * self.svgTextNormalsize
        
        #print(f"GramText.getSvg()  a myTextSizeStr is {myTextSizeStr}")
        #print(f"GramText.getSvg()  myTextSizeCm is {myTextSizeCm}")
        myTextSizeStr = "%.2f" % (myTextSizeCm * self.svgPxForCm)
        #print(f"GramText.getSvg()  b myTextSizeStr= {myTextSizeStr}")

        myAnch = self.getAnch()
        # print "GramText.getSvg()  myAnch=%s" % myAnch
        
        halfHeight = self.fullHeight / 2.
        #self.length = (self.bb[2] - self.bb[0])  no workee for rotated!
        halfLength = self.length/2.
        # print(f"GramText.getSvg() '{self.rawText}' length {self.length:.2} cm, height is {self.fullHeight:.2} cm")

        oneInnerSep = self.getInnerSep()
        #print("GramText.getSvg() Got oneInnerSep %.2f" % oneInnerSep)
        twoInnerSep = 2 * oneInnerSep

        # Get outer sep
        theLineThickness = self.getLineThickness()
        # print("a Got theLineThickness %s" % theLineThickness)
        twoOuterSep = cmForLineThickness(theLineThickness)
        oneOuterSep = 0.5 * twoOuterSep

        # For mid anchors, need half_normal_x
        if Gram._svgNormalsize_x:
            self.svg_half_normal_x = Gram._svgNormalsize_x / 2.
        # print(f"{gm[0]} svg_half_normal_x is {self.svg_half_normal_x}")
        


        # dx and dy are fine-tuning args for svg text, that modify the x and y positions. 
        # Eg <text id="text-1"  x="300.00" y="-300.00" font-size="108.00" dx="-93.29" dy="28.62" >acly</text> 
        # If they are zero, the text is placed at x,y as the start of the text, and the baseline
        # For a rect, the x,y is the top left corner, width goes right (as usual) and height goes down (unusual)
        # Eg <rect x="300.0" y="-300.0"  width="186.57" height="100.62" stroke="red" fill="none" stroke-width="0.5" /> 
        myDx = 0.0
        myDy = 0.0
        myDrDx = 0.0   # for the box, ie the "draw"
        myDrDy = 0.0
       
        if myAnch == 'west':
            myDx += oneInnerSep
            myDx += oneOuterSep
            myDy -= self.underhang
            myDy += halfHeight
            myDrDy += oneInnerSep
            myDrDy += oneOuterSep
            myDrDy += halfHeight
        elif myAnch == 'north west':
            myDx += oneInnerSep
            myDx += oneOuterSep
            myDy += oneInnerSep
            myDy += oneOuterSep
            myDy += self.rise
            myDrDy += self.fullHeight
            myDrDy += twoInnerSep
            myDrDy += twoOuterSep
        elif myAnch == 'north':
            myDx += -halfLength
            myDy += self.rise
            myDy += oneInnerSep
            myDy += oneOuterSep
            myDrDx += -halfLength
            myDrDx += -oneInnerSep
            myDrDx += -oneOuterSep
            myDrDy += self.fullHeight
            myDrDy += twoInnerSep
            myDrDy += twoOuterSep
        elif myAnch == 'north east':
            myDx += -self.length
            myDx += -oneInnerSep
            myDx += -oneOuterSep
            myDy += oneInnerSep
            myDy += oneOuterSep
            myDy += self.rise
            myDrDx += -self.length
            myDrDx += -twoInnerSep
            myDrDx += -twoOuterSep
            myDrDy += self.fullHeight
            myDrDy += twoInnerSep
            myDrDy += twoOuterSep
        elif myAnch == 'east':
            myDx += -self.length
            myDx += -oneInnerSep
            myDx += -oneOuterSep
            myDy -= self.underhang
            myDy += halfHeight
            myDrDx += -self.length
            myDrDx += -twoInnerSep
            myDrDx += -twoOuterSep
            myDrDy += oneInnerSep
            myDrDy += oneOuterSep
            myDrDy += halfHeight
        elif myAnch == 'base':
            myDx += -halfLength
            myDrDx += -halfLength
            myDrDx += -oneInnerSep
            myDrDx += -oneOuterSep
            myDrDy += oneInnerSep
            myDrDy += oneOuterSep
            myDrDy += self.underhang
        elif myAnch == 'base west':
            myDx += oneInnerSep
            myDx += oneOuterSep
            myDrDy += oneInnerSep
            myDrDy += oneOuterSep
            myDrDy += self.underhang
        elif myAnch == 'base east':
            myDx += -self.length
            myDx += -oneInnerSep
            myDx += -oneOuterSep
            myDrDx += -self.length
            myDrDx += -twoInnerSep
            myDrDx += -twoOuterSep
            myDrDy += oneInnerSep
            myDrDy += oneOuterSep
            myDrDy += self.underhang
        elif myAnch == 'mid':
            # print(f"mid: oneInnerSep: {oneInnerSep}, oneOuterSep {oneOuterSep}, underhang: {self.underhang}, svg_half_normal_x: {self.svg_half_normal_x}")
            myDx += -halfLength
            myDy  += self.svg_half_normal_x
            myDrDx += -halfLength
            myDrDx += -oneInnerSep
            myDrDx += -oneOuterSep
            myDrDy += oneInnerSep
            myDrDy += oneOuterSep
            # myDrDy += self.svg_half_normal_x
            myDrDy += self.underhang
        elif myAnch == 'mid west':
            myDx += oneInnerSep
            myDx += oneOuterSep
            myDy += self.svg_half_normal_x
            myDrDy += oneInnerSep
            myDrDy += oneOuterSep
            # myDrDy += self.svg_half_normal_x
            myDrDy += self.underhang
        elif myAnch == 'mid east':
            myDx += -self.length
            myDx += -oneInnerSep
            myDx += -oneOuterSep
            myDy += self.svg_half_normal_x
            myDrDx += -self.length
            myDrDx += -twoInnerSep
            myDrDx += -twoOuterSep
            myDrDy += oneInnerSep
            myDrDy += oneOuterSep
            # myDrDy += self.svg_half_normal_x
            myDrDy += self.underhang
        elif myAnch == 'south west':
            myDx += oneInnerSep
            myDx += oneOuterSep
            myDy += -oneInnerSep
            myDy += -oneOuterSep
            myDy += -self.underhang
            # myDx = 0.0
            # myDy = 0.0
        elif myAnch == 'south':
            myDx += -halfLength
            myDy += -oneInnerSep
            myDy += -oneOuterSep
            myDy += -self.underhang
            myDrDx += -halfLength
            myDrDx += -oneInnerSep
            myDrDx += -oneOuterSep
        elif myAnch == 'south east':
            myDx += -self.length
            myDx += -oneInnerSep
            myDx += -oneOuterSep
            myDy += -oneInnerSep
            myDy += -oneOuterSep
            myDy += -self.underhang
            myDrDx += -self.length
            myDrDx += -twoInnerSep
            myDrDx += -twoOuterSep
        elif myAnch == 'center' or myAnch is None:
            myDx += -halfLength
            myDy += -self.underhang
            myDy += halfHeight
            myDrDx += -halfLength
            myDrDx += -oneInnerSep
            myDrDx += -oneOuterSep
            myDrDy += oneInnerSep
            myDrDy += oneOuterSep
            myDrDy += halfHeight
        else:
            gm.append("Bad anchor %s" % myAnch)
            raise GramError(gm)

        # Calculate the tight bounding box self.tbb for svg for GramText
        # First for the un-rotated text box, and then rotate it if needed.
        # # rotatePointAroundPoint(pointToRotate, degrees, pivotPoint)

        # tbb is [llx, lly, urx, ury]
        
        if myAnch in ["mid", "mid east", "mid west"]:
            self.tbb[0] = self.cA.xPosn + myDx
            self.tbb[1] = self.cA.yPosn - self.underhang
            self.tbb[2] = self.tbb[0] + self.length
            self.tbb[3] = self.tbb[1] + self.fullHeight
        else:
            self.tbb[0] = self.cA.xPosn + myDx
            self.tbb[1] = self.cA.yPosn - self.underhang - myDy
            self.tbb[2] = self.tbb[0] + self.length
            self.tbb[3] = self.tbb[1] + self.fullHeight

        #     myRotate = self.getRotate()
        #     if myRotate:
        #         # ss.append('transform="rotate(%.2f, %.2f, %.2f)"' % (
        #         #    -myRotate, self.svgPxForCmF(self.cA.xPosn), -self.svgPxForCmF(self.cA.yPosn)))

        #         ll = (self.tbb[0], self.tbb[1])
        #         ur = (self.tbb[2], self.tbb[3])
        #         pivotPoint = (self.svgPxForCmF(self.cA.xPosn), -self.svgPxForCmF(self.cA.yPosn))
        #         (self.tbb[0], self.tbb[1]) = rotatePointAroundPoint(ll, -myRotate, pivotPoint)
        #         (self.tbb[2], self.tbb[3]) = rotatePointAroundPoint(ur, -myRotate, pivotPoint)

        # get self.bb

        self.bb[0] = self.tbb[0] - oneInnerSep - oneOuterSep
        self.bb[1] = self.tbb[1] - oneInnerSep - oneOuterSep
        self.bb[2] = self.tbb[2] + oneInnerSep + oneOuterSep
        self.bb[3] = self.tbb[3] + oneInnerSep + oneOuterSep


        theRotate = self.getRotate()
        if theRotate:
            # The textbox rotates around its anchor.
            corners = []
            corners.append([self.bb[0], self.bb[1]])
            corners.append([self.bb[2], self.bb[1]])
            corners.append([self.bb[2], self.bb[3]])
            corners.append([self.bb[0], self.bb[3]])
            # print("xPosn=%.1f, yPosn=%.1f" % (self.cA.xPosn,
            # self.cA.yPosn))
            for cNum in range(4):
                corner = corners[cNum]
                corner[0] -= self.cA.xPosn
                corner[1] -= self.cA.yPosn
            polarCorners = []
            for cNum in range(4):
                polarCorners.append(func.square2polar(corners[cNum]))
            # print("a polarCorners = ", polarCorners)
            rads = (theRotate * math.pi) / 180.
            # print "theRotate %f is %f radians" % (theRotate, rads)
            for cNum in range(4):
                pCorner = polarCorners[cNum]
                pCorner[0] += rads
            # print "b polarCorners = ", polarCorners

            corners = []
            for cNum in range(4):
                corners.append(func.polar2square(polarCorners[cNum]))
            # print 'corners', corners
            for cNum in range(4):
                corner = corners[cNum]
                corner[0] += self.cA.xPosn
                corner[1] += self.cA.yPosn
            # print corners

            llx = 1000000.
            lly = 1000000.
            urx = -1000000.
            ury = -1000000.

            for cNum in range(4):
                corner = corners[cNum]
                if corner[0] < llx:
                    llx = corner[0]
                if corner[1] < lly:
                    lly = corner[1]
                if corner[0] > urx:
                    urx = corner[0]
                if corner[1] > ury:
                    ury = corner[1]
            self.bb = [llx, lly, urx, ury]
            # print "   @tb.bb %25s  %.2f %.2f %.2f %.2f " % (
            # self.rawText, self.bb[0], self.bb[1], self.bb[2], self.bb[3])
            self.corners = corners

        theXShift = self.getXShift()
        if theXShift:
            self.bb[0] += theXShift
            self.bb[2] += theXShift
            if self.corners:
                for cNum in range(4):
                    self.corners[cNum][0] += theXShift
        theYShift = self.getYShift()
        if theYShift:
            self.bb[1] += theYShift
            self.bb[3] += theYShift
            if self.corners:
                for cNum in range(4):
                    self.corners[cNum][1] += theYShift
        


        myDx *= self.svgPxForCm
        myDy *= self.svgPxForCm

        myXShift = self.getXShift()
        if myXShift:
            myDx += myXShift * self.svgPxForCm
        myYShift = self.getYShift()
        if myYShift:
            myDy -= myYShift * self.svgPxForCm

        # print "%20s  %+.2f  %+6.2f" % (myAnch, myDx, myDy)

        #print("b GramText.getSvg() self.length is %s; svgHackDoRotate is %s" % (self.length, Gram._svgHackDoRotate))

 

        ss = []  # GramText.getSvg()

        # ss.append('\n<polygon points="FIXME"' % (
        #    self.tbb[0], self.tbb]1], self.

        myDraw = self.getDraw()
        myFill = self.getFill()
        #print("GramText.getSvg() for %s --- myDraw is %s, myFill is %s" % (self.rawText, myDraw, myFill))

        if myDraw or myFill:
            myDrDx *= self.svgPxForCm
            myDrDy *= self.svgPxForCm

            #myXShift = self.getXShift()
            if myXShift:
                myDrDx += myXShift * self.svgPxForCm
            #myYShift = self.getYShift()
            if myYShift:
                myDrDy -= myYShift * self.svgPxForCm

            if myDraw is True:
                myColor = self.getColor()    # rectangle outline is made to be the same color as the text color
            elif isinstance(myDraw, GramColor):
                myColor = myDraw
            else:
                myColor = None

            myDrHeight = ((self.fullHeight + twoInnerSep) * self.svgPxForCm)
            myDrX = ((self.cA.xPosn + oneOuterSep) * self.svgPxForCm)  + myDrDx
            myDrY = ((-self.cA.yPosn - oneOuterSep) * self.svgPxForCm) - myDrHeight + myDrDy
            myDrWid = ((self.length + twoInnerSep) * self.svgPxForCm)
            ss.append('<rect x="%.2f" y="%.2f"  width="%.2f" height="%.2f"' % (
                myDrX, myDrY, myDrWid, myDrHeight))
            # ss.append('stroke="black" fill="none" stroke-width="1" />\n')
            if myColor:
                ss.append('stroke="%s"' % myColor.color)
                if myColor.transparent:
                    ss.append('stroke-opacity="%s"' % myColor.value)
            else:
                if myDraw is True:
                    ss.append('stroke="black"')
                else:
                    ss.append('stroke="none"')
            if myFill:
                ss.append('fill="%s"' % myFill.color)
                if myFill.transparent:
                    ss.append('fill-opacity="%s"' % myFill.value)
            else:
                ss.append('fill="none"')
            if theLineThickness:
                myLineThickness = cmForLineThickness(theLineThickness)
                #print "b Got myLineThickness %s cm" % myLineThickness
                myLineThickness = self.svgPxForCmF(myLineThickness)
                #print "c Got myLineThickness %s px" % myLineThickness
                ss.append('stroke-width="%s"' % myLineThickness)

            myRotate = self.getRotate()
            if myRotate:
                ss.append('transform="rotate(%.2f, %.2f, %.2f)"' % (
                    -myRotate, self.svgPxForCmF(self.cA.xPosn), -self.svgPxForCmF(self.cA.yPosn)))

            ss.append('/>\n')
            
        ss.append('<text id="%s" ' % self.svgId)
        if myClass:
            ss.append('class="%s"' % myClass)

        myX = (self.svgPxForCmF(self.cA.xPosn))


        ss.append('x="%.2f" y="%.2f"' %
                  (myX, -self.svgPxForCmF(self.cA.yPosn)))
        #ss.append('dy="0.35em" dx="1ex"')
        ss.append('font-size="%s"' % myTextSizeStr)
        if myDx:
            ss.append('dx="%.2f"' % myDx)
        if myDy:
            ss.append('dy="%.2f"' % myDy)

        myTextShape = self.getTextShape()  #  ['itshape', 'scshape']
        if myTextShape == 'scshape':
            ss.append('font-variant="small-caps"')
        if myTextShape == 'itshape':
            if self.font == 'helvetica':
                ss.append('font-style="oblique"')
            elif self.font == 'cm':
                if myTextShape == 'scshape':
                    ss.append('font-style="oblique"')
                else:
                    ss.append('font-style="italic"')
            elif self.font in ['palatino', 'times']:
                ss.append('font-style="italic"')

        # Since font-weight is part of the style, I need to use "style=..."
        myTextSeries = self.getTextSeries()   # only 'bfseries'
        if myTextSeries == "bfseries":
            ss.append('style="font-weight:bold"')   # or a number?

        myColor = self.getColor()
        if myColor:
            ss.append('fill="%s"' % myColor.color)
            if myColor.transparent:
                ss.append('fill-opacity="%s"' % myColor.value)

        # print(f"GramText.getSvg() Gram._svgHackDoRotate is  {Gram._svgHackDoRotate}")
        if Gram._svgHackDoRotate:
            myRotate = self.getRotate()
            # print(f"GramText.getSvg() myRotate is  {myRotate}")
            if myRotate:
                ss.append('transform="rotate(%.2f, %.2f, %.2f)"' % (
                    -myRotate, self.svgPxForCmF(self.cA.xPosn), -self.svgPxForCmF(self.cA.yPosn)))

        if Gram._svgHack_x_Only:
            ss.append('>x</text>')
        else:
            ss.append('>%s</text>' % self.rawText)

        if self.showTextBB:
            # Tight bb first

            if myAnch in ["mid", "mid east", "mid west"]:
                ss.append('\n<rect x="%.2f" y="%.2f"  width="%.2f" height="%.2f"' % (
                    self.svgPxForCmF(self.cA.xPosn) + myDx,
                    -self.svgPxForCmF(self.cA.yPosn + self.fullHeight - self.underhang),
                    self.svgPxForCmF(self.length),
                    self.svgPxForCmF(self.fullHeight)))
            else:
                ss.append('\n<rect x="%.2f" y="%.2f"  width="%.2f" height="%.2f"' % (
                    self.svgPxForCmF(self.cA.xPosn) + myDx,
                    -self.svgPxForCmF(self.cA.yPosn + self.fullHeight - self.underhang) + myDy,
                    self.svgPxForCmF(self.length),
                    self.svgPxForCmF(self.fullHeight)))
            myRotate = self.getRotate()
            if myRotate:
                ss.append('transform="rotate(%.2f, %.2f, %.2f)"' % (
                    -myRotate, self.svgPxForCmF(self.cA.xPosn), -self.svgPxForCmF(self.cA.yPosn)))
            ss.append('stroke="blue" fill="none" stroke-width="0.5" />')


            # baseline
            ss.append('\n<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"' % (
                self.svgPxForCmF(self.cA.xPosn) + myDx,
                -self.svgPxForCmF(self.cA.yPosn) + myDy,
                self.svgPxForCmF(self.cA.xPosn + self.length) + myDx,
                -self.svgPxForCmF(self.cA.yPosn) + myDy))
            myRotate = self.getRotate()
            if myRotate:
                ss.append('transform="rotate(%.2f, %.2f, %.2f)"' % (
                    -myRotate, self.svgPxForCmF(self.cA.xPosn), -self.svgPxForCmF(self.cA.yPosn)))
            ss.append('stroke="red" fill="none" stroke-width="0.5" />')

            # ss.append('\n<rect x="%.2f" y="%.2f"  width="%.2f" height="%.2f"' % (
            #     self.bb[0] * self.svgPxForCm, -self.bb[3] * self.svgPxForCm,
            #     (self.bb[2] - self.bb[0]) * self.svgPxForCm, (self.bb[3] - self.bb[1]) * self.svgPxForCm))
            # ss.append('stroke="red" fill="none" stroke-width="0.5" />')

            # bb
            ss.append("\n\n<!-- bb -->\n")
            ss.append('\n<rect x="%.2f" y="%.2f"  width="%.2f" height="%.2f"' % (
                self.svgPxForCmF(self.bb[0]), 
                -self.svgPxForCmF(self.bb[3]), 
                self.svgPxForCmF(self.bb[2] - self.bb[0]), 
                self.svgPxForCmF(self.bb[3] - self.bb[1])))
            ss.append('stroke="red" fill="none" stroke-width="0.8" />')

        if self.showTextAnchor:
            ss.append('\n<circle cx="%.2f" cy="%.2f" r="2" stroke="none" fill="red"/>' % (
                self.svgPxForCmF(self.cA.xPosn), -self.svgPxForCmF(self.cA.yPosn)))
        ret = ' '.join(ss)
        # print ret
        return ret


class GramLine(GramGraphic):

    def __init__(self, cA, cB):
        GramGraphic.__init__(self)
        self.cA = cA
        self.cB = cB
        self.color = 'black'

    def getTikz(self):
        #gm = ['GramLine.getTikz()']
        ss = []
        ss.append('\draw')

        options = self.getTikzOptions()
        if options:
            ss.append('[%s]' % ','.join(options))

        if self.cA.name:
            ss.append('(%s)' % self.cA.name)
        else:
            ss.append('(%.3f,%.3f)' % (self.cA.xPosn, self.cA.yPosn))
        ss.append('--')
        if self.cB.name:
            ss.append('(%s);' % self.cB.name)
        else:
            ss.append('(%.3f,%.3f);' % (self.cB.xPosn, self.cB.yPosn))

        # For debugging.  Obviously this is not text.
        # if self.showTextAnchor:
        #    ss.append("\\draw [blue] plot[only marks,mark=*] coordinates {(%.3f,%.3f)};" % (self.cA.xPosn, self.cA.yPosn))
        #    ss.append("\\draw [green] plot[only marks,mark=*] coordinates {(%.3f,%.3f)};" % (self.cB.xPosn, self.cB.yPosn))
        return ' '.join(ss)


    def getSvg(self):
        gm = ['GramLine.getSvg()']
        ss = []
        ss.append('<line')

        ss.append('x1="%.1f" y1="%.1f"' % (
            self.svgPxForCmF(self.cA.xPosn), -self.svgPxForCmF(self.cA.yPosn)))
        ss.append('x2="%.1f" y2="%.1f"' % (
            self.svgPxForCmF(self.cB.xPosn), -self.svgPxForCmF(self.cB.yPosn)))

        options = self.getSvgOptions()
        ss += options

        ss.append('/>')
        return ' '.join(ss)

    def setBB(self):
        theLineThickness = cmForLineThickness(self.getLineThickness())
        halfLT = theLineThickness / 2.
        if self.cA.xPosn < self.cB.xPosn:
            self.bb[0] = self.cA.xPosn - halfLT
            self.bb[2] = self.cB.xPosn + halfLT
        else:
            self.bb[0] = self.cB.xPosn + halfLT
            self.bb[2] = self.cA.xPosn - halfLT

        if self.cA.yPosn < self.cB.yPosn:
            self.bb[1] = self.cA.yPosn - halfLT
            self.bb[3] = self.cB.yPosn + halfLT
        else:
            self.bb[1] = self.cB.yPosn + halfLT
            self.bb[3] = self.cA.yPosn - halfLT



class GramRect(GramLine):

    def __init__(self, cA, cB):
        GramLine.__init__(self, cA, cB)
        self.color = None
        self.draw = True

    def getTikz(self):
        ss = []

        #ss.append(r"\draw[gray,very thin] (0,0) grid (4,4);")

        #ss.append('\draw')
        ss.append('\path')

        options = self.getTikzOptions()
        if options:
            ss.append('[%s]' % ','.join(options))

        if self.cA.name:
            ss.append('(%s)' % self.cA.name)
        else:
            ss.append('(%.3f,%.3f)' % (self.cA.xPosn, self.cA.yPosn))
        ss.append('rectangle')
        if self.cB.name:
            ss.append('(%s);' % self.cB.name)
        else:
            ss.append('(%.3f,%.3f);' % (self.cB.xPosn, self.cB.yPosn))

        if 0:
            self.setBB()
            bbLine = '\n'
            bbLine += r"\draw [red,ultra thin] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (
                self.bb[0], self.bb[1],
                self.bb[2], self.bb[3])
            ss.append(bbLine)
        if 0:
            ss.append(
                "\\draw plot[only marks,mark=+] coordinates {(%.3f,%.3f)};" % (self.cA.xPosn, self.cA.yPosn))
            ss.append(
                "\\draw plot[only marks,mark=+] coordinates {(%.3f,%.3f)};" % (self.cB.xPosn, self.cB.yPosn))

        return ' '.join(ss)

    def getSvg(self):
        gm = ['GramRect.getSvg()']
        if self.svgId:
            assert self.svgGForIdDict.get(self.svgId)
        else:
            self.setSvgIdAndAddToDict('rect')
        # print gm[0], self.svgId

        ss = []
        ss.append('<rect id="%s" ' % self.svgId)
        ss.append('x="%.2f" y="%.2f"' % (
            self.svgPxForCmF(self.cA.xPosn), -self.svgPxForCmF(self.cB.yPosn)))
        ss.append('width="%.2f" height="%.2f"' % (
            self.svgPxForCmF(self.cB.xPosn - self.cA.xPosn),
            self.svgPxForCmF(self.cB.yPosn - self.cA.yPosn)))
        

        if 1:
            options = self.getSvgOptions()
            if 0:
                print("SVG options")
                for opti in options:
                    print("            %s" % opti)
            ss += options
            

        else:
            myLineThickness = self.getLineThickness()
            # print "GramLine.getSvg()  myLineThickness %s" % myLineThickness
            myLineThickness = cmForLineThickness(myLineThickness)
            myLineThickness = self.svgPxForCmF(myLineThickness)
            ss.append('stroke-width="%.1f"' % (myLineThickness))

            # cId is color object, fId is the fill object
            # Both are GramColor objects
            cId = self.getColor()
            if cId is None:
                pass
            else:
                assert isinstance(cId, GramColor), "Got %s, should be a GramColor instance." % cId

            fId = self.getFill()
            if fId is None:
                pass
            else:
                assert isinstance(fId, GramColor), "Got %s, should be a GramColor instance." % fId

            if cId and cId.color:
                ss.append('stroke="%s"' % cId.color)
                if cId.transparent:
                    ss.append('stroke-opacity="%s"' % cId.value)

            if fId is None:
                ss.append('fill="none"')
            elif fId and fId.color:
                ss.append('fill="%s"' % fId.color)
                if fId.transparent:
                    ss.append('fill-opacity="%s"' % fId.value)

        ss.append('/>')
        #print(' '.join(ss))
        return ' '.join(ss)


class GramPdf(GramGraphic):

    def __init__(self, pdf_fName):
        GramGraphic.__init__(self)
        gm = ['GramPdf.__init__()']

        self.jpegPxPerCm = 100

        if not os.path.isfile(pdf_fName):
            gm.append("Can't find pdf file '%s'" % pdf_fName)
            raise GramError(gm)
        self.pdf_fName = pdf_fName
        theBasename = os.path.basename(self.pdf_fName)
        gif_fName = '%s.gif' % theBasename
        # if os.path.exists(gif_fName):
        #    gm.append("The file %s exists.  It should not.  Get rid of it." % gif_fName)
        #    raise GramError(gm)
        self.gif_fName = gif_fName
        self.jpeg_fName = '%s.jpeg' % theBasename

        identifyLines = None
        if func.which('gm'):
            try:
                po = Popen(['gm', 'identify', '-verbose', '%s' %
                            self.pdf_fName], stdout=PIPE, stderr=PIPE)
            except OSError:
                gm.append(
                    "Could not find the gm (GraphicsMagick) 'identify' program.  Install it.")
                raise GramError(gm)
            ret_tup = po.communicate()
            # print "GramPdf init.  identify returns", ret_tup
            spl = None
            if ret_tup[0]:
                #spl = ret_tup[0].split()
                identifyLines = [l.strip() for l in ret_tup[0].split('\n')]
            else:
                if ret_tup[1]:
                    gm.append("Got stderr: %s" % ret_tup[1])
                gm.append("Could not 'identify' the pdf.")
                raise GramError(gm)
        elif func.which('identify'):
            try:
                po = Popen(
                    ['identify', '-verbose', '%s' % self.pdf_fName], stdout=PIPE, stderr=PIPE)
            except OSError:
                gm.append(
                    "Could not find the ImageMagick 'identify' program.  Install it.")
                raise GramError(gm)
            ret_tup = po.communicate()
            # print "GramPdf init.  (ImageMagick) identify returns", ret_tup
            if ret_tup[0]:
                identifyLines = [l.strip() for l in ret_tup[0].split('\n')]
            else:
                if ret_tup[1]:
                    gm.append("Got stderr: %s" % ret_tup[1])
                gm.append("Could not 'identify' the pdf.")
                raise GramError(gm)
        else:
            raise GramError(
                "Cant find GraphicsMagick identify or ImageMagick identify.")

        # print identifyLines
        # assert spl
        # if not spl or len(spl) < 2:
        #     gm.append('Idenfication of the pdf did not work.')
        #     raise GramError(gm)
        # if spl[1] != 'PDF':
        #     gm.append("This does not appear to be a pdf file.  Or maybe the file name has spaces in it?")
        #     raise GramError(gm)
        # theDim = spl[2]
        # splDim = spl[2].split('x')
        # self.pdfWid = int(splDim[0])
        # self.pdfHeight = int(splDim[1])

        self.pdfWid = None
        self.pdfHeight = None
        for iL in identifyLines:
            if iL.startswith("Geometry:"):
                spl_iL = iL.split()
                AxB = spl_iL[1].split('+')[0]
                spl_AxB = AxB.split('x')
                self.pdfWid = int(spl_AxB[0])
                self.pdfHeight = int(spl_AxB[1])

        # Hack!
        # print "GramPdf init.  Ugly hack.  Decreasing the pdfWid by 4"
        #self.pdfWid -= 4

        print("GramPdf init. Pdf width: %.2f pt, height %.2f pt" % (self.pdfWid, self.pdfHeight))
        # 1 PostScript point = 0.35277138 mm
        self.pdfWid_cm = self.pdfWid * 0.035277138
        self.pdfHeight_cm = self.pdfHeight * 0.035277138
        print("GramPdf init. The pdf is %.2f cm x %.2f cm." % (self.pdfWid_cm, self.pdfHeight_cm))

        self.gif_pi = None  # gif photoimage, used for tweakerDraw()

        # Make the jpeg
        if func.which('gm'):
            try:
                po = Popen(["gm", "convert", '-density', '%.2f' % (self.jpegPxPerCm * 2.54),
                            self.pdf_fName, self.jpeg_fName], stdout=PIPE, stderr=PIPE)
            except OSError:
                gm.append("Could not run the 'gm convert' program.")
                raise GramError(gm)
            ret_tup = po.communicate()
            if ret_tup[0] or ret_tup[1]:
                gm.append("Something wrong with gm convert.")
                gm.append("Here is what it said:")
                gm.append(ret_tup[0])
                gm.append(ret_tup[1])
                raise GramError(gm)
        elif func.which('convert'):
            try:
                po = Popen(["convert", '-density', '%.2f' % (self.jpegPxPerCm * 2.54),
                            self.pdf_fName, self.jpeg_fName], stdout=PIPE, stderr=PIPE)
            except OSError:
                gm.append("Could not run the 'convert' program.")
                raise GramError(gm)
            ret_tup = po.communicate()
            if ret_tup[0] or ret_tup[1]:
                gm.append("Something wrong with convert.")
                gm.append("Here is what it said:")
                gm.append(ret_tup)
                raise GramError(gm)
        else:
            raise GramError(
                "Cant find GraphicsMagick convert or ImageMagick convert.")

    def setBB(self):
        self.bb = [0.0, 0.0, self.pdfWid_cm, self.pdfHeight_cm]

    def getTikz(self):
        ss = []

        #ss.append(r"\draw[gray,very thin] (0,0) grid (4,4);")

        if 0:
            self.setBB()
            bbLine = '% GramPdf.getTikz() debug.  Adding a bounding box rectangle.\n'
            # bbLine += r"\draw [red,ultra thin] (%.3f,%.3f) rectangle
            # (%.3f,%.3f);" % (
            bbLine += r"\draw [red] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (
                self.bb[0], self.bb[1],
                self.bb[2], self.bb[3])
            ss.append(bbLine)
        if 0:
            ss.append(
                "\\draw plot[only marks,mark=+] coordinates {(%.3f,%.3f)};" % (self.bb[0], self.bb[1]))
            ss.append(
                "\\draw plot[only marks,mark=+] coordinates {(%.3f,%.3f)};" % (self.bb[2], self.bb[3]))

        return ' '.join(ss)



class GramJpeg(GramGraphic):

    def __init__(self, jpeg_fName, cA, scale):
        GramGraphic.__init__(self)
        gm = ['GramJpeg.__init__()']
        self.corners = None

        # x and y positions are put in self.cA, as usual
        self.cA = cA
        if not os.path.isfile(jpeg_fName):
            gm.append("Can't find jpeg file '%s'" % jpeg_fName)
            raise GramError(gm)
        self.jpeg_fName = jpeg_fName
        self.scale = scale

        identifyLines = None
        if func.which('gm'):
            try:
                po = Popen(['gm', 'identify', '-verbose', '%s' %
                            self.jpeg_fName], stdout=PIPE, stderr=PIPE)
            except OSError:
                gm.append(
                    "Could not find the gm (GraphicsMagick) 'identify' program.  Install it.")
                raise GramError(gm)
            ret_tup = po.communicate()
            # print "GramJpeg init.  gm (GraphicsMagick) identify returns",
            # ret_tup
            if ret_tup[0]:
                identifyLines = [l.strip() for l in ret_tup[0].split('\n')]
            else:
                if ret_tup[1]:
                    gm.append("Got stderr: %s" % ret_tup[1])
                gm.append("Could not identify the jpeg.")
                raise GramError(gm)
        elif func.which('identify'):
            try:
                po = Popen(
                    ['identify', '-verbose', '%s' % self.jpeg_fName], stdout=PIPE, stderr=PIPE)
            except OSError:
                gm.append(
                    "Could not find the ImageMagick 'identify' program.  Install it.")
                raise GramError(gm)
            ret_tup = po.communicate()
            print("GramJpeg init.  (ImageMagick) identify returns", ret_tup)
            if ret_tup[0]:
                identifyLines = [l.strip() for l in ret_tup[0].split('\n')]
            else:
                if ret_tup[1]:
                    gm.append("Got stderr: %s" % ret_tup[1])
                gm.append("Could not identify the jpeg.")
                raise GramError(gm)
        else:
            raise GramError(
                "Cant find GraphicsMagick identify or ImageMagick identify.")

        # print identifyLines

        # We want the geometry and the resolution.
        # GraphicsMagick:
        #   Geometry: 1518x1520
        #   Resolution: 254x254 pixels/inch
        # or
        #   Resolution: 118x118 pixels/centimeter
        # ImageMagick:
        #   Geometry: 1518x1520+0+0
        #   Resolution: 254x254

        self.jpegWid_px = None
        self.jpegHeight_px = None
        self.resolution_dpi = None

        for iL in identifyLines:
            if iL.startswith("Geometry:"):
                spl_iL = iL.split()
                AxB = spl_iL[1].split('+')[0]
                spl_AxB = AxB.split('x')
                self.jpegWid_px = int(spl_AxB[0])
                self.jpegHeight_px = int(spl_AxB[1])

            elif iL.startswith("Resolution:"):
                spl_iL = iL.split()

                # pixels/something
                theUnits = spl_iL[2]
                spl_units = theUnits.split('/')
                unitNumerator = spl_units[0]
                assert unitNumerator == 'pixels'
                unitDenominator = spl_units[1]

                AxB = spl_iL[1]
                spl_AxB = AxB.split('x')
                rA = int(round(float(spl_AxB[0])))
                rB = int(round(float(spl_AxB[1])))
                if rA != rB:
                    raise GramError(
                        "GramJpeg.  Odd -- the two resolutions of the jpg are not the same!")
                if unitDenominator == 'inch':
                    self.resolution_dpi = rA
                elif unitDenominator == 'centimeter':
                    self.resolution_dpi = int(round(float(spl_AxB[0]) * 2.54))
                else:
                    raise GramError(
                        "I don't know unitDenominator %s.  Fix me." % unitDenominator)

        if not self.resolution_dpi:
            # This in GraphicsMagick
            #    X Resolution: 4718592/65536
            #    Y Resolution: 4718592/65536
            #    Resolution Unit: 2
            for iL in identifyLines:
                if iL.startswith('X Resolution:'):
                    lastBit = iL.split()[2]
                    splLastBit = lastBit.split('/')
                    theFloat = float(splLastBit[0]) / float(splLastBit[1])
                    rA = int(theFloat)
                elif iL.startswith('Y Resolution:'):
                    lastBit = iL.split()[2]
                    splLastBit = lastBit.split('/')
                    theFloat = float(splLastBit[0]) / float(splLastBit[1])
                    rB = int(theFloat)
                elif iL.startswith('Resolution Unit:'):
                    lastBit = iL.split()[2]
                    resUnit = int(lastBit)
                    if resUnit != 2:
                        raise GramError(
                            "GramJpeg.  Not sure what is going on here.  Resolution Unit ?!?  Fix me")
            if not rA or not rB:
                raise GramError("GramJpeg.  Failed to get resolution")
            if rA != rB:
                raise GramError(
                    "GramJpeg.  Odd -- x res and y res are not the same.")
            self.resolution_dpi = rA

        if not self.jpegWid_px:
            raise GramError("GramJpeg.  Failed to get jpegWid_px")
        if not self.jpegHeight_px:
            raise GramError("GramJpeg.  Failed to get jpegHeight_px")
        if not self.resolution_dpi:
            raise GramError("GramJpeg.  Failed to get resolution_dpi")

        print("GramJpeg. Got wid_px %i, height_px %i, and resolution (dpi) %i" % (
            self.jpegWid_px, self.jpegHeight_px, self.resolution_dpi))

        self.jpegWid_cm = (
            (float(self.jpegWid_px) / self.resolution_dpi) * 2.54) * self.scale
        self.jpegHeight_cm = (
            (float(self.jpegHeight_px) / self.resolution_dpi) * 2.54) * self.scale
        print("GramJpeg.__init__()  Got jpegWid_cm %.2f, jpegHeight_cm %.2f" % (
            self.jpegWid_cm, self.jpegHeight_cm))


        self.gX = 0.0
        self.gY = 0.0

    def setBB(self):
        gm = ["GramJpeg() '%s'  setBB()" % self.jpeg_fName]
        if not self.cA:
            self.cA = GramCoord()

        theAnch = self.getAnch()
        if theAnch and theAnch not in ['west', 'north west', 'north', 'north east', 'east',
                                       'south west', 'south', 'south east',
                                       'center']:
            gm.append("anchor '%s' does not work for jpegs")
            raise GramError(gm)

        if 1:

            halfHeight = self.jpegHeight_cm / 2.0
            halfLength = self.jpegWid_cm / 2.0

            theAnch = self.getAnch()

            if theAnch == 'south west':
                self.bb[0] = self.cA.xPosn
                self.bb[1] = self.cA.yPosn
                self.bb[2] = self.cA.xPosn + self.jpegWid_cm
                self.bb[3] = self.cA.yPosn + self.jpegHeight_cm

            elif theAnch == 'south':
                self.bb[0] = self.cA.xPosn - halfLength
                self.bb[1] = self.cA.yPosn
                self.bb[2] = self.cA.xPosn + halfLength
                self.bb[3] = self.cA.yPosn + self.jpegHeight_cm

            elif theAnch == 'south east':
                self.bb[0] = self.cA.xPosn - self.jpegWid_cm
                self.bb[1] = self.cA.yPosn
                self.bb[2] = self.cA.xPosn
                self.bb[3] = self.cA.yPosn + self.jpegHeight_cm

            elif theAnch == 'east':
                self.bb[0] = self.cA.xPosn - self.jpegWid_cm
                self.bb[1] = self.cA.yPosn - halfHeight
                self.bb[2] = self.cA.xPosn
                self.bb[3] = self.cA.yPosn + halfHeight

            elif theAnch == 'north east':
                self.bb[0] = self.cA.xPosn - self.jpegWid_cm
                self.bb[1] = self.cA.yPosn - self.jpegHeight_cm
                self.bb[2] = self.cA.xPosn
                self.bb[3] = self.cA.yPosn

            elif theAnch == 'north':
                self.bb[0] = self.cA.xPosn - halfLength
                self.bb[1] = self.cA.yPosn - self.jpegHeight_cm
                self.bb[2] = self.cA.xPosn + halfLength
                self.bb[3] = self.cA.yPosn

            elif theAnch == 'north west':
                self.bb[0] = self.cA.xPosn
                self.bb[1] = self.cA.yPosn - self.jpegHeight_cm
                self.bb[2] = self.cA.xPosn + self.jpegWid_cm
                self.bb[3] = self.cA.yPosn

            elif theAnch == 'west':
                self.bb[0] = self.cA.xPosn
                self.bb[1] = self.cA.yPosn - halfHeight
                self.bb[2] = self.cA.xPosn + self.jpegWid_cm
                self.bb[3] = self.cA.yPosn + halfHeight

            elif theAnch == 'center' or theAnch is None:
                self.bb[0] = self.cA.xPosn - halfLength
                self.bb[1] = self.cA.yPosn - halfHeight
                self.bb[2] = self.cA.xPosn + halfLength
                self.bb[3] = self.cA.yPosn + halfHeight

            else:
                raise GramError("anch '%s' not implemented." % theAnch)

            theRotate = self.getRotate()
            if theRotate:
                # The picture rotates around its anchor.
                # print "   *jpeg.bb %.2f %.2f %.2f %.2f " % (
                #        self.bb[0], self.bb[1], self.bb[2], self.bb[3])
                corners = []
                corners.append([self.bb[0], self.bb[1]])
                corners.append([self.bb[2], self.bb[1]])
                corners.append([self.bb[2], self.bb[3]])
                corners.append([self.bb[0], self.bb[3]])
                # print "xPosn=%.1f, yPosn=%.1f" % (self.cA.xPosn,
                # self.cA.yPosn)
                for cNum in range(4):
                    corner = corners[cNum]
                    corner[0] -= self.cA.xPosn
                    corner[1] -= self.cA.yPosn
                polarCorners = []
                for cNum in range(4):
                    polarCorners.append(func.square2polar(corners[cNum]))
                # print "a polarCorners = ", polarCorners
                rads = (theRotate * math.pi) / 180.
                # print "theRotate %f is %f radians" % (theRotate, rads)
                for cNum in range(4):
                    pCorner = polarCorners[cNum]
                    pCorner[0] += rads
                # print "b polarCorners = ", polarCorners

                corners = []
                for cNum in range(4):
                    corners.append(func.polar2square(polarCorners[cNum]))
                # print 'corners', corners
                for cNum in range(4):
                    corner = corners[cNum]
                    corner[0] += self.cA.xPosn
                    corner[1] += self.cA.yPosn
                # print corners

                llx = 1000000.
                lly = 1000000.
                urx = -1000000.
                ury = -1000000.

                for cNum in range(4):
                    corner = corners[cNum]
                    if corner[0] < llx:
                        llx = corner[0]
                    if corner[1] < lly:
                        lly = corner[1]
                    if corner[0] > urx:
                        urx = corner[0]
                    if corner[1] > ury:
                        ury = corner[1]
                self.bb = [llx, lly, urx, ury]
                # print "   @tb.bb %.2f %.2f %.2f %.2f " % (
                #         self.bb[0], self.bb[1], self.bb[2], self.bb[3])
                self.corners = corners

            theXShift = self.getXShift()
            if theXShift:
                self.bb[0] += theXShift
                self.bb[2] += theXShift
                if self.corners:
                    for cNum in range(4):
                        self.corners[cNum][0] += theXShift
            theYShift = self.getYShift()
            if theYShift:
                self.bb[1] += theYShift
                self.bb[3] += theYShift
                if self.corners:
                    for cNum in range(4):
                        self.corners[cNum][1] += theYShift

    def getTikz(self):
        # self.setBB()  Is this needed here?
        ss = []
        ss.append(r'\node')

        options = self.getTikzOptions()
        if options:
            ss.append('[%s]' % ','.join(options))
        if self.cA.name:
            ss.append('at (%s)' % self.cA.name)
        else:
            ss.append('at (%.3f,%.3f)' % (self.cA.xPosn, self.cA.yPosn))

        ss.append(
            '{\\includegraphics[scale=%.3f]{../%s}};' % (self.scale, self.jpeg_fName))

        if 0:
            self.setBB()
            bbLine = '% GramPdf.getTikz() debug.  Adding a bounding box rectangle.\n'
            # bbLine += r"\draw [red,ultra thin] (%.3f,%.3f) rectangle
            # (%.3f,%.3f);" % (
            bbLine += r"\draw [red] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (
                self.bb[0], self.bb[1],
                self.bb[2], self.bb[3])
            ss.append(bbLine)
        if 0:
            ss.append(
                "\\draw plot[only marks,mark=+] coordinates {(%.3f,%.3f)};" % (self.bb[0], self.bb[1]))
            ss.append(
                "\\draw plot[only marks,mark=+] coordinates {(%.3f,%.3f)};" % (self.bb[2], self.bb[3]))

        return ' '.join(ss)



class GramError(Exception):

    """A class for exceptions in gram.

    You can raise this with a string, or a list of strings.  If its
    a single string, it gets wrapped.  If its a list of 2 strings, the
    first one is output flush and unwrapped, and the second is
    indented and wrapped."""

    def __init__(self, msg=''):
        myIndent = ' ' * 4
        if isinstance(msg, str):
            #self.msg = '\n\n' + textwrap.fill(msg, 70, initial_indent=myIndent, subsequent_indent=myIndent)
            try:
                if msg.startswith('\n\n'):
                    firstLine = '%s' % msg
                elif msg.startswith('\n'):
                    firstLine = '\n%s' % msg
                else:
                    firstLine = '\n\n%s' % msg
            except:
                firstLine = ''
            self.msg = firstLine

        elif isinstance(msg, list):
            try:
                if msg[0].startswith('\n\n'):
                    firstLine = '%s' % msg[0]
                elif msg[0].startswith('\n'):
                    firstLine = '\n%s' % msg[0]
                else:
                    firstLine = '\n\n%s' % msg[0]
            except:
                firstLine = ''
            niceMsgList = [firstLine]
            for i in range(len(msg))[1:]:
                if isinstance(msg[i], str):
                    #  If it is short, use it as is.  If it is long, wrap it.
                    if len(msg[i]) < 66:
                        niceMsgList.append(myIndent + msg[i])
                    else:
                        wLine = textwrap.fill(msg[i], 70, initial_indent=myIndent, subsequent_indent=myIndent)
                        niceMsgList.append(wLine)
                else:
                    pass

            self.msg = '\n'.join(niceMsgList)
        else:
            self.msg = ''
        Exception.__init__(self)

    def __str__(self):
        return self.msg


# makeStuff_1 =  """TEXFILEROOT = t
#EPS_TEXFILEROOT = t
#"""
# OUTFILEROOT goes here, between makeStuff_1 and makeStuff_2.
# No!, no more makeStuff_1

# The 'open' command on the mac opens the pdf with Preview.  If you
# are using linux you will want to change that to something more
# appropriate.  Evince? ggv?

makeStuff_2 = """

# For debugging, remove the '> /dev/null' bit, so you can see the error messages!
pdf: $(TEXFILEROOT).tex
\tpdflatex $(TEXFILEROOT).tex > /dev/null
\t$(PDFVIEWER) $(TEXFILEROOT).pdf &

pdfPage: $(TEXFILEROOT).tex
\tpdflatex $(TEXFILEROOT).tex > /dev/null
\t$(PDFVIEWER) $(TEXFILEROOT).pdf
"""

makeStuff_2b = """

pdf: $(TEXFILEROOT).tex
\tpdflatex $(TEXFILEROOT).tex
\t$(PDFVIEWER) $(TEXFILEROOT).pdf &

pdfPage: $(TEXFILEROOT).tex
\tpdflatex $(TEXFILEROOT).tex
\t$(PDFVIEWER) $(TEXFILEROOT).pdf
"""

makeStuff_3 = """
composite:$(COMPOSITEROOT).tex
\trm -f $(COMPOSITEOUTFILEROOT).pdf
\tpdflatex $(COMPOSITEROOT).tex
\tmv $(COMPOSITEROOT).pdf $(COMPOSITEOUTFILEROOT).pdf
\t$(PDFVIEWER) $(COMPOSITEOUTFILEROOT).pdf
"""

# makeStuff_4 = """

# ps: $(TEXFILEROOT).tex
# \tlatex $(TEXFILEROOT).tex
# \tdvips -Ppdf -o $(OUTFILEROOT).ps $(TEXFILEROOT)

# # making an eps with dvips -E might work, or might not ...
# eps: $(EPS_TEXFILEROOT).tex
# \tlatex $(EPS_TEXFILEROOT).tex
# \tdvips -Ppdf -E -o $(OUTFILEROOT).eps $(EPS_TEXFILEROOT)

# clean:
# \trm -f $(TEXFILEROOT).aux  $(TEXFILEROOT).dvi  $(TEXFILEROOT).log
# \trm -f $(EPS_TEXFILEROOT).aux  $(EPS_TEXFILEROOT).dvi  $(EPS_TEXFILEROOT).log
# \trm -f $(JOBNAME).aux $(JOBNAME).log


# """

makeStuff_4 = """
clean:
\trm -f $(TEXFILEROOT).aux  $(TEXFILEROOT).log

"""


# tTexStuff_1 = r"""\documentclass[%ipt]{standalone}
#\usepackage{tikz}
#"""
# tTexStuff_1 = r"""\documentclass[%ipt,a4paper]{scrartcl}
#\usepackage{tikz}
#"""
# tTexStuff_1 = r"""\documentclass[%ipt,a4paper,extrafontsizes]{memoir}
#\usepackage{tikz}
#"""


# texStuffExtras goes here

tTexStuff_2 = r"""\renewcommand\floatpagefraction{1.0}
\renewcommand\topfraction{1.0}
\renewcommand\bottomfraction{1.0}
\renewcommand\textfraction{0.0}
"""

# tTexStuff_3 = r"""\begin{document}
# \thispagestyle{empty}
# """
# tTexStuff_3 = r"""\begin{document}
# """
# # inputGramLine goes here

# tTexStuff_4 = r"""\end{document}

# """


tTexStuff_5 = r"""\documentclass[%ipt,a4paper]{scrartcl}
\usepackage{graphicx}
\usepackage{pdfpages}
\usepackage[absolute,overlay]{textpos}
%%\textblockorigin{0mm}{-0.3mm}
%%\textblockorigin{0.27mm}{0.32mm}
\textblockorigin{0mm}{-1.1mm}
\setlength{\parindent}{0pt}
\begin{document}
\thispagestyle{empty}
"""

# line {
#     stroke: black;
# }

svgCss1 = """text {
    font-family: %s;
    font-weight: %i;
}
text.sffamily {
    font-family: Helvetica, Arial, sans-serif;
}
text.ttfamily {
    font-family: "Courier New", Courier, monospace;
}
"""

svgCss2 = """
text {
    font-family: %s;
    font-weight: %i;
}
text.sffamily {
    font-family: "Latin Modern Sans", sans-serif;
}
text.ttfamily {
    font-family: "Latin Modern Mono", "Courier New", Courier, monospace;
}
"""


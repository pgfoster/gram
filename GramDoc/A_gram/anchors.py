from __future__ import print_function
from gram import Gram,GramCoord,GramGrid,GramText

Gram.pdflatexOutputGoesToDevNull = True

gr = Gram()
gr.pdfViewer = 'open'
gr.baseName = 'anchors'
gr.font = 'helvetica'
gr.defaultInnerSep = 0.1
g = GramGrid(0, 1, 8, 7)
gr.graphics.append(g)

##    _goodAnchors = ['west', 'north west', 'north', 'north east', 'east',
##                        'base', 'base west', 'base east',
##                        'south west', 'south', 'south east',
##                        #'mid', 'mid west', 'mid east',
##                        'center'] # center seems to be the default

nnDict = {}
nn = []
for i in range(3):
    for j in range(4):
        indx = (i * 4) + j
        refPt = gr.goodAnchors[indx]
        print(indx, refPt)
        n = GramCoord((2 * j) + 1,
                      (2 * i) + 1,
                      refPt)
        nnDict[refPt] = n
        nn.append(n)
        gr.graphics.append(n)

myStr = 'Xxy'
theTextSize = 'normalsize'
for i in range(12):
    anch = gr.goodAnchors[i]
    print("i=%i, anch=%s" % (i, anch))
    g = GramText(anch)
    g.cA = nnDict[anch]
    g.textAnchor = 'base'
    g.textSize = 'small'
    g.textFamily = 'ttfamily'
    g.yShift = 0.1
    gr.graphics.append(g)

    gB = GramText(myStr)
    gB.cA = GramCoord()
    gB.cA.xPosn = g.cA.xPosn
    gB.cA.yPosn = g.cA.yPosn + 1
    gB.anchor = anch
    gB.color = 'orange'
    gB.draw = 'blue'
    gB.lineThickness = 2
    #gB.draw = True
    gB.textSize = theTextSize
    gB.rotate = 0
    gr.graphics.append(gB)

    if 0:
        gB = GramText(myStr)
        gB.cA = GramCoord()
        gB.cA.xPosn = g.cA.xPosn
        gB.cA.yPosn = g.cA.yPosn + 1
        gB.anchor = anch
        gB.draw = True
        gB.textSize = theTextSize
        gB.rotate = 30
        gr.graphics.append(gB)

#gr.showTextBB = True
#print(gr.graphics)
#print(gr.getTikz())
gr.pdf()
#gr.png()
#gr.svg()

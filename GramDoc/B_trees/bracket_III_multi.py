from p4 import *
read("((A,B)89,C,(D,E)95);") 
t = var.trees[0]
n = t.node('A')
n.name = r'Ab{\textcolor{blue}{cde}}fgh {\textcolor{blue}{\ding{110}}}'
#n.name = r'Ab<tspan fill="blue">cde</tspan>fgh <tspan fill="blue"> &#x2B1B;</tspan>'
#n.name = r'Ab<tspan fill="blue">cde</tspan>fgh <tspan fill="blue"> &#xFFED;</tspan>'
t.draw()
from gram import TreeGram
tg = TreeGram(t, scale=None, showNodeNums=False, widthToHeight=0.67) 
tg.latexUsePackages.append('pifont')
tg.baseName = "multiBrackets"
#tg.showTextBB=True
#tg.showTextAnchor=True
#tg.pdflatexOutputGoesToDevNull=False
#tg.grid(0,0,4,4)
g = tg.setBracket(t.node('D').nodeNum,7, text="Bracket DE", rotated=True)
g = tg.setBracket(t.node('B').nodeNum,6, text="Bracket BCD", rotated=True)
g.rightExtra = 0.7
g = tg.setBracket(2,4, text="Bracket", rotated=False)
tg.bracketsLineUp = False
#tg.render()
#tg.styleDict['bracket label'].textSize = 'tiny'
tg.png()
n.label.rawText = r'Ab<tspan fill="blue">cde</tspan>fgh <tspan fill="blue"> &#x2B1B;</tspan>'
tg.svg()

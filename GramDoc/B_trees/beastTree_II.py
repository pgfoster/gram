from gram import TreeGram
var.nexus_getAllCommandComments = True
var.nexus_readBeastTreeCommandComments=True
read('treeannotatorOut')
t = var.trees[0]

# The two cBoxes on the left are too big, and dominate the figure.
# Make them text, as a node labels, instead.
n = t.root
n.name = "(%.1f, %.1f)" % (n.height_95_HPD[1], n.height_95_HPD[0])
n = t.node(1)
n.name = "(%.1f, %.1f)" % (n.height_95_HPD[1], n.height_95_HPD[0])

tg = TreeGram(t)
tg.font = 'palatino'
tg.documentFontSize = 10
tg.baseName = 'beastB'
for nNum in [3,4,6,9]:
    n = t.node(nNum)
    tg.setNodeConfidenceBox(n)

# Define a style
from gram import GramText
tg.render()
tb = GramText('myStyle')
tb.textWidth = 1.
tb.textSize = 'scriptsize'
tb.anchor = 'west'
tb.name = 'wrappedNode'
tg.styleDict['wrappedNode'] = tb

for nNum in [0,1]:
    n = t.node(nNum)
    n.label.myStyle = 'wrappedNode'

tg.png()
tg.svg()  # no wrapping in svg

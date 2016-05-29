from gram import TreeGramRadial
read('fancyTree.nex')
t = var.trees[0]
for n in t.iterInternalsNoRoot():
    if n.name:
        if n.name in ['0.22']:
            n.br.name = n.name
        else:
            n.br.uName = n.name
        n.name = None
tg = TreeGramRadial(t, maxLinesDim=6.,
                    rotate=120,
                    showNodeNums=False,
                    slopedBrLabels=True)
tg.baseName = 'smallRadialII'

# There are a two superimposed taxon names
# Either of these can be used to fix it.
if 1:
    tg.fixTextOverlaps()
else:
    t.node(11).label.yShift = -0.25
    t.node(12).label.yShift = 0.25
tg.setScaleBar(xOffset=-2.0, yOffset=3.0)
tg.pdf()
tg.svg()

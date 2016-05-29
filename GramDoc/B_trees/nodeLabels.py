from gram import TreeGram
read('((A, B)uvw, (C, D)xyz);')
t = var.trees[0]
tg = TreeGram(t.dupe(),showNodeNums=True)
tg.baseName = 'nodeLabels'
tgB = TreeGram(t.dupe())
tgB.tree.node(1).label.anchor = 'north east'
tgB.tree.node(4).label.anchor = 'west'
tgB.gX = 3.
tg.grams.append(tgB)
# tg.png()
tg.svg()


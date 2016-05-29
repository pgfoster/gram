from gram import TreeGram
read("((A,B)Wxy,(C,(D,E, F)Xyz)Vwxy);")
t = var.trees[0]
tg = TreeGram(t.dupe(),showNodeNums=True)
tg.baseName = 'stylesForInternalNodes'
tgB = TreeGram(t.dupe())
tgB.tree.node(1).label.myStyle = 'node lower left'
tgB.tree.node(4).label.myStyle = 'node right'
tgB.tree.node(6).label.myStyle = 'node lower right'
tgB.gX = 4.
tg.grams.append(tgB)
tg.svg()

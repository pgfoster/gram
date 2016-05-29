from gram import TreeGram
read('((A, B), (C, (D, E)));')
t = var.trees[0]
t.draw()
nB = t.node('B')
nB.name = """synonym 1, another synonym,
and a third synonym."""
nE = t.node('D')
nE.name = """synonym 1, synonym 2, 
yet another synonym, and synonym 4"""
tg = TreeGram(t, showNodeNums=False)
tg.wrapLeafLabelsAt = 'comma'
tg.baseName = 'wrapLeafLabelsAtComma'
tg.png()
# tg.svg() no workee

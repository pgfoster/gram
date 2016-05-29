from gram import TreeGram
read('tinyTree.nex')
t = var.trees[0]
tg = TreeGram(t)
tg.baseName = 'tinyII'
tg.setScaleBar(length=0.2, xOffset=0.0, yOffset=-0.7)
tg.pdf()
tg.svg()


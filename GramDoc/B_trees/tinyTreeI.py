from gram import TreeGram
read('tinyTree.nex')
t = var.trees[0]
tg = TreeGram(t)
tg.baseName = 'tinyI'
tg.setScaleBar()
tg.pdf()
tg.svg()


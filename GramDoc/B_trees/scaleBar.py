from gram import TreeGram
read("(((A, B), (C, D)));")
t = var.trees[0]
tg = TreeGram(t)
tg.baseName = 'scaleBar'
tg.grid(-1, -1, 3, 3)
tg.setScaleBar(length=0.1, yOffset=-0.0)
tg.pdf()
tg.svg()

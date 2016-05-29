from gram import TreeGram
read("((A, B), (C, D), (E, (F, G)));")
t = var.trees[0]
tg = TreeGram(t, showNodeNums=True)
tg.baseName = 'bracket1'
t.draw()
tg.setBracket(2, 3, text='these brackets line',
              leftNode=1)
tg.setBracket(6, 10, text='up with each other',
              leftNode=None, rotated=True)
tg.png()
tg.svg()

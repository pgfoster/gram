from gram import TreeGram
read("((A, B), (C, D), (E, (F, G)));")
t = var.trees[0]
tg = TreeGram(t, showNodeNums=False)
tg.font = 'palatino'
tg.baseName = 'bracket2'
t.draw()
longText1 = """A long note \
about this grouping of taxa, \
composed of A and B""" 
b = tg.setBracket(2, 3, text=longText1,
                  leftNode=None)
b.label.style=None
b.label.textSize='scriptsize'
b.label.anchor = 'west'
b.label.textWidth = 3.0
b.label.innerSep = 0.2
b = tg.setBracket(6, 10, text='Rotated label',
                  leftNode=None, rotated=True)
b.label.textSize='large'
tg.bracketsLineUp = False
#tg.showTextAnchor = True
tg.pdf()
tg.svg()

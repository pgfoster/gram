from gram import TreeGram
read("((A,B)89,C,(D,E)96);")
read("((H, I)73, (J, K)98, L);")
t = var.trees[0]
tg = TreeGram(t)
tg.font = 'palatino'
tg.documentFontSize = 10
tg.baseName = 'twoTrees'
t = var.trees[1]
tgB = TreeGram(t)
tgB.baseName = 'doesntMatter'
tgB.gX = 4.
tg.grams.append(tgB)
#tg.pdf()
tg.svg()

from gram import TreeGram
read("((A,B)89,C,(D,E)95);")
t = var.trees[0]
tg = TreeGram(t)
tg.font = 'cm'
tg.baseName = 'minimal_cm'
tg.png()

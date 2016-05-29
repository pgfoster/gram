from gram import TreeGramRadial
read('(chimp, gorilla, (human, (gibbon, orang)));')
t = var.trees[0]
tg = TreeGramRadial(t, maxLinesDim=2.,rotate=-50)
tg.baseName = 'radialTinyI'
tg.png()
tg.svg()

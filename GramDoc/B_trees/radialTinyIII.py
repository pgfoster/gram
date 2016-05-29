from gram import TreeGramRadial
read('tinyTree.nex')
t = var.trees[0]
tg = TreeGramRadial(t, maxLinesDim=2.,rotate=-50)
tg.baseName = 'radialTinyIII'
tg.png()
tg.svg()

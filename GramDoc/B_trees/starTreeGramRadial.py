from gram import TreeGramRadial
read("(Able,Baker,Charlie,Daphne,Estelle,Floxey,Gertrude,Harvey);")
t = var.trees[0]
tg = TreeGramRadial(t, maxLinesDim=1)
tg.baseName = 'starRadial'
tg.pdf()
tg.svg()

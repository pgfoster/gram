from gram import TreeGram
read("tinyTree.nex")
t = var.trees[0]
tg = TreeGram(t)
tg.baseName = 'brokenBranches'
tg.setBrokenBranch(1)
tg.setBrokenBranch(7)
tg.png()
tg.svg()

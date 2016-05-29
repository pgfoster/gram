from gram import TreeGram
read("(((A, B, (C, D)'a node label'):0.01, E, F)'another node label', G);")
t = var.trees[0]
tg = TreeGram(t.dupe())
tg.baseName = 'overlapping'
tgB = TreeGram(t.dupe())
tgB.fixTextOverlaps()
tgB.gX = 6
tg.grams.append(tgB)
#tg.png()
tg.svgPxForCm = 50.
tg.svg()

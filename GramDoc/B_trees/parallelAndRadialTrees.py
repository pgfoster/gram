from gram import TreeGram,TreeGramRadial

tString = "((A, (B, (C, ((D, E), F)))), G, H);"
read(tString)
t = var.trees[0]
t2 = t.dupe()

tg = TreeGram(t)
tg.baseName = 'parallelAndRadial'
#tg.grid(0,-2,10,6)

tgr = TreeGramRadial(t2, maxLinesDim=3.8)
tgr.gX = 5.0
tgr.gY = -1.0
tg.grams.append(tgr)

g = tg.text("Parallel, using the", 0.5, -1.)
g.anchor = 'west'
g = tg.text("TreeGram class", 0.5, -1.6)
g.anchor = 'west'

g = tg.text("Radial, using the", 6.5, -1.)
g.anchor = 'west'
g = tg.text("TreeGramRadial class", 6.5, -1.6)
g.anchor = 'west'

tg.png()
tg.svg()

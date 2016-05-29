from gram import TreeGramRadial
read('tinyTree.nex')  # with branch lengths and supports
t = var.trees[0]

# Delete the internal branch supports
for n in t.iterInternalsNoRoot():
    n.name = None

tg = TreeGramRadial(t, maxLinesDim=2.,rotate=-50)
tg.baseName = 'radialTinyII'
tg.png()
tg.svg()

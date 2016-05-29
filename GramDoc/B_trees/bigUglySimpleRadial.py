from gram import TreeGram,TreeGramRadial
read('bigTree.nex')
t = var.trees[0]

for n in t.iterInternalsNoRoot():
    if n.name:
        n.br.name = n.name
        n.name = None

tg = TreeGramRadial(t, maxLinesDim=30,
                    slopedBrLabels=True,
                    rotate=100, equalDaylight=False)

tg.font = 'helvetica'
tg.baseName = 'big_simpleRadial'
tg.fixTextOverlaps()
#tg.pdf()
tg.svg()

from gram import TreeGram
var.nexus_getAllCommandComments = True
var.nexus_readBeastTreeCommandComments = True
read('treeannotatorOut')
t = var.trees[0]
tg = TreeGram(t)
tg.baseName = 'beastA'
for n in t.iterNodes():
    if not n.isLeaf:
        tg.setNodeConfidenceBox(n)
tg.pdf()
#tg.svg()

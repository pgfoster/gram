from gram import TreeGram
read('easyTreeA.nex')
read('easyTreeB.nex')

tA = var.trees[0]
# make a duplicate tree, as tA is used again below
tg = TreeGram(tA.dupe())  
tg.baseName = 'combineSplitSupports'
tg.tree.node(8).label.myStyle = 'node upper right'
tg.tree.node(10).label.myStyle = 'node right'

tB = var.trees[1]
tgB = TreeGram(tB)
tgB.gY = -7.5
tg.grams.append(tgB)

tA.makeSplitKeys()
tB.makeSplitKeys()
nodeForSKDict = {}
for n in tB.iterInternalsNoRoot():
    nodeForSKDict[n.br.splitKey] = n
for n in tA.iterInternalsNoRoot():
    theNode = nodeForSKDict.get(n.br.splitKey)
    if theNode:
        n.name += '/%s' % theNode.name

tgX = TreeGram(tA, showNodeNums=False)
tgX.tree.node(8).label.myStyle = 'node upper right'
tgX.tree.node(10).label.myStyle = 'node right'
tgX.gY = -15.
tg.grams.append(tgX)
#tg.font = 'palatino'
#tg.grid(0, -16, 5, 7) 
#tg.pdf()
tg.svgPxForCm = 60.
tg.svg()
st = tg.styleDict['node upper left']

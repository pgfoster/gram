from gram import TreeGram
read('(A, (B, (C, (D, (E, F))85)));')
t = var.trees[0]
tg = TreeGram(t)
tg.font = 'helvetica'
tg.baseName = 'simplified'
tg.leafLabelSize = 'tiny'
tg.render()
tg.styleDict['bracket label'].textSize = 'Large'
for n in t.iterLeavesNoRoot():
    n.label.rawText = ' '
t.node(5).label.rawText = 'Euryarchaeota'
t.node(7).label.rawText = 'Crenarchaeota / eocytes'
t.node(6).label.anchor = 'north east'
g = tg.setBracket(1, 3, text='Bacteria', leftNode=0)
g.fill = 'blue!15'
g = tg.setBracket(5, 7, text='Archaea', leftNode=4)
g.fill = 'orange!20'
g = tg.setBracket(9, 10, text='Eukaryotes', leftNode=8)
g.fill = 'green!30'
tg.wrapLeafLabelsAt = 1.3     # svg can't do this
tg.pdf()
tg.wrapLeafLabelsAt = None
tg.svg()

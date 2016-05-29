from gram import TreeGram,TreeGramRadial,Gram
read("((A,B)ab,C,(D,E)de)m;")
t = var.trees[0]
t.node(1).br.uName = 'X'
t.node(5).br.uName = 'Y'
tg = TreeGram(t, scale=7.)
print "a", tg.internalNodeLabelSize
tg.baseName = 'twoTreesII'
t = t.dupe()
tgB = TreeGramRadial(t, scale=8.,
                     slopedBrLabels=True,
                     rotate=90)
print "b", tg.internalNodeLabelSize
tgB.tree.root.label.yShift = 0.1
tgB.gX = 4.8
tgB.gY = -1.5
gr = Gram()
g = gr.text(r'$\Longleftrightarrow$', 0, 0)  # LaTeX symbol
gr.text('equivalence', 0, 0.5)
gr.gX = 3.5
gr.gY = 1.0
tg.grams.append(tgB)
tg.grams.append(gr)
tg.png()
g.rawText = '&#x21D4;'       # unicode symbol
tg.svg()

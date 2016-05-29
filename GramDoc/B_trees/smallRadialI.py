from gram import TreeGramRadial
read("((A,B)ab,C,(D,E)de)m;")
t = var.trees[0]
t.node(1).br.uName = 'X'
t.node(5).br.name = 'Y'
tg = TreeGramRadial(t, scale=7.,
                    slopedBrLabels=True,
                    showNodeNums=False,
                    rotate=90)
tg.baseName = 'smallRadialI'
tg.font = 'palatino'

tg.png()
tg.svg()

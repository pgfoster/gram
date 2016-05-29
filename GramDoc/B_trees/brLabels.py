from gram import TreeGram
read("((A, B))root;")
t = var.trees[0]
t.node('A').br.name = 'label'
tg = TreeGram(t)
tg.scale = 8. # 7.035 otherwise, so a bit wider
tg.baseName = 'brLabels'
n = t.node('B')
tg.setBranchULabel(n, 'uLabel')
tg.png()
tg.svg()

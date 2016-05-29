from gram import TreeGram
read('tinyTree.nex')
t = var.trees[0]
tg = TreeGram(t)
tg.baseName = 'tinyIII'
# styleDict is empty until you render().
tg.render()
# Grab the leaf style ...
st = tg.styleDict['leaf']
# ... and change it
st.textShape = 'itshape'
#tg.pdf()
tg.svg()

from gram import TreeGram
read('tinyTree.nex')
t = var.trees[0]
tg = TreeGram(t,showNodeNums=True)
tg.baseName = 'tinyIV'
tg.font = 'helvetica'
if 1:
    # Make a new style, and put it in the
    # styleDict, with a name.
    from gram import GramText
    g = GramText("Xyx")
    g.textShape = 'itshape'
    g.textSize = 'small'
    g.color = 'white'
    g.draw = 'black'
    g.lineThickness = 'very thick'
    g.fill = 'blue!60'
    g.name = 'myleaf'
    g.anchor = 'west'
    tg.styleDict[g.name] = g

    # Apply the style to some of the leaves.
    for nNum in [1,4,5,7]:  # and one internal
        n = t.node(nNum)
        n.label.myStyle = 'myleaf'
tg.png()
tg.svg()

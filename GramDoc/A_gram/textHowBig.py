from gram import TreeGram
tString = "(('TreeGram needs to', 'know how big this':0.05, 'text is':0.5), (Boojum, Snark):0.03);"
t = func.readAndPop(tString)
t.draw()
tg = TreeGram(t)
# for nNum in [2,3,4]:
#     n = t.node(nNum)
#     n.label.draw = True
for nNum in [6,7]:
    n = t.node(nNum)
    n.label.textShape = 'itshape'
brText = "in order to place this bracket"
tg.setBracket(2,4, text=brText)

tg.baseName = 'textHowBig'
# tg.grid(0,0,5,4)
tg.pdf()
tg.svg()

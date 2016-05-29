from gram import TreeGramRadial
tA = func.readAndPop('((A, B), (C, D), (E, (F, (G, H))));')
tB = tA.dupe()

tg = TreeGramRadial(tA, maxLinesDim=3.,equalDaylight=True)
tg.baseName = 'equalDaylightAndSimpleRadialA'

tgB = TreeGramRadial(tB, maxLinesDim=3.,equalDaylight=False, rotate=70)
tgB.gX = 7.
tgB.gY = 2.6
tg.grams.append(tgB)

#tg.grid(0,0,8,8)
gA = tg.text("Equal Daylight", 0.5,0.5)
gB = tg.text("Simple radial", 5.5,0.5)
for g in [gA, gB]:
    g.anchor = 'west'
    g.textSize = 'normalsize'

#tg.pdf()
tg.svg()


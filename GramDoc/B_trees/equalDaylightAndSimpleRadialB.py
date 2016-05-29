# import string
# t = func.randomTree(taxNames=list(string.uppercase), seed=0)
# t.writeNexus('t26.nex')


from gram import TreeGramRadial
tA = func.readAndPop('t26.nex')
tA.reRoot(19)     # re-rooting can often help.
tB = tA.dupe()

tg = TreeGramRadial(tA, maxLinesDim=8.,equalDaylight=True)
tg.baseName = 'equalDaylightAndSimpleRadialB'

tgB = TreeGramRadial(tB, maxLinesDim=8.,equalDaylight=False)
tgB.gX = 5.
tgB.gY = -2.5
tg.grams.append(tgB)

#tg.grid(0,-10,10,10)
gA = tg.text("Equal Daylight", 0,3)
gB = tg.text("Simple radial", 0,-6.5)
for g in [gA, gB]:
    g.anchor = 'west'
    g.textSize = 'normalsize'
# gC = tg.text("(equalDaylight=False)", 0,-7.2)
# gC.textFamily = 'ttfamily'
# gC.anchor = 'west'

#tg.pdf()
tg.svg()


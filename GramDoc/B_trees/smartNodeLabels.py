#'node right'
#'node upper right'
#'node lower right'
#'node upper left'
#'node lower left'

my_gX = 4.0

from gram import TreeGram
myScale = 3.5
read('(((A, B)xy, (C, (D, E, F)wxyz, G))wxyz, (H, (I, J)xy)wxyz);')
t = var.trees[0]

tA = t.dupe()
tg = TreeGram(tA)
tg.baseName = 'smartNodeLabels'
tg.doSmartLabels = False # default True
tg.scale = myScale
#tg.png()
#tg.svg()

tB = t.dupe()
tgB = TreeGram(tB)
tgB.baseName = 'smart_semi'
tgB.doSmartLabels = 'semi' # default True
tgB.scale = myScale
#tgB.png()
#tgB.svg()
tg.grams.append(tgB)
tgB.gX = my_gX 

tC = t.dupe()
tgC = TreeGram(t)
tgC.baseName = 'smart_true'
tgC.doSmartLabels = True # default True
tgC.scale = myScale
#tgC.png()
#tgC.svg()
tg.grams.append(tgC)
tgC.gX = 2 * my_gX 

myTextSize = 'footnotesize'
#tg.grid(-1,-1, 6,6)
g = tg.text("doSmartLabels=False", -1.0, -1.0)
g.textFamily = 'ttfamily'
g.anchor = 'west'
g.textSize = myTextSize
g = tg.text("doSmartLabels='semi'", (-1.0 + my_gX), -1.0)
g.textFamily = 'ttfamily'
g.anchor = 'west'
g.textSize = myTextSize
g = tg.text("doSmartLabels=True", (-1.0 + (2. * my_gX)), -1.0)
g.textFamily = 'ttfamily'
g.anchor = 'west'
g.textSize = myTextSize
tg.png()
tg.svgPxForCm = 50.
tg.svg()

from gram import Gram
gr1 = Gram()
gr1.font = 'helvetica'
gr1.baseName = 'gramInGram'
gr1.text("Embedding gram", 0,0)
gr2 = Gram()
g = gr2.text("Embedded gram",0,0)
gr2.gX = 0.3
gr2.gY = 0.5
gr1.grams.append(gr2)
gr1.pdf()
gr1.svg()

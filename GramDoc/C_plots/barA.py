from gram import Plot
read("data2.py")
gp = Plot()
gp.font = 'helvetica'
gp.baseName = 'barA'
gp.bars(xx1, yy1)
gp.png()
gp.svg()

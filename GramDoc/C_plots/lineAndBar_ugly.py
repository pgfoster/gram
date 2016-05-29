from gram import Plot
read('data5.py')
gp = Plot()
gp.baseName = 'lineAndBar_ugly'
gp.bars(binNames,binVals)
gp.line(xx1, yy1, smooth=True)
gp.png()
gp.svg()

from gram import Plot
execfile("data1.py")
gp = Plot()
gp.baseName = 'line'
gp.line(xx1, yy1)
gp.png()
gp.svg()
   

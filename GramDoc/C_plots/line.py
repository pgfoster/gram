from gram import Plot
from data1 import xx1, yy1
gp = Plot()
gp.baseName = 'line'
gp.line(xx1, yy1)
gp.png()
gp.svg()
   

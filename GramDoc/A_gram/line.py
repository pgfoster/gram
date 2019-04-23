from gram import Gram
gr = Gram()
gr.baseName = 'line'
gr.font = 'Helvetica'
gr.grid(0,0,4,4)
g = gr.line(1,1,2,3)
g.colour = 'black!20'
g.colour.transparent = True
g.lineThickness = 28. # pts
g = gr.line(3, 3.5, 2, 1)
g.lineThickness = 'semithick'
g.lineStyle = 'dashed'
# A default, un-modified line
gr.line(1, 3, 1.5, 0.5)
g = gr.line(3.5, 1, 3.5, 2)
g.lineThickness = 10
g.cap = 'rect'  # default butt
g = gr.text('some lines', 3,3)
g.anchor = 'north west'
g.textSize = 'normalsize'
gr.png()
gr.svg()

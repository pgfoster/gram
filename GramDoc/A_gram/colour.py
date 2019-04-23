from gram import Gram
gr = Gram()
gr.baseName = 'colour'
gr.grid(0,0,6,4)

g = gr.rect(2.6, 2.6, 3.4, 3.4)
g.fill = "red!30"
g.draw = "blue!50"
g.lineThickness = 5

g = gr.rect(2.6, 1.6, 3.4, 2.4)
g.fill = "red!30"
g.draw = None

g = gr.rect(2.6, 0.6, 3.4, 1.4)
g.fill = None
g.draw = "blue!50"
g.lineThickness = 5

g = gr.text("default, transparent", 3.0, 3.75)
g.textSize = 'tiny'
g.fill = 'white'

g = gr.rect(4.6, 2.6, 5.4, 3.4)
g.fill = "red!30"
g.fill.transparent = False
g.draw = "blue!50"
g.draw.transparent = False
g.lineThickness = 5

g = gr.rect(4.6, 1.6, 5.4, 2.4)
g.fill = "red!30"
g.fill.transparent = False
g.draw = None

g = gr.rect(4.6, 0.6, 5.4, 1.4)
g.fill = None
g.draw = "blue!50"
g.draw.transparent = False
g.lineThickness = 5


g = gr.text("transparent=False", 5.0, 3.75)
g.textSize = 'tiny'
g.fill = 'white'

g = gr.text("with fill, with draw", 0.0, 3.0)
g.textSize = 'tiny'
g.anchor = 'west'
g.fill = 'white'

g = gr.text("with fill, no draw", 0.0, 2.0)
g.textSize = 'tiny'
g.anchor = 'west'
g.fill = 'white'

g = gr.text("no fill, with draw", 0.0, 1.0)
g.textSize = 'tiny'
g.anchor = 'west'
g.fill = 'white'

#gr.pdf()
gr.svg()

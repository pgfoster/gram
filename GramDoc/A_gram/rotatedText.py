from gram import Gram
gr = Gram()
gr.baseName = 'rotatedText'
gr.showTextBB = True
gr.showTextAnchor = True
g = gr.text("short", 1,2)
g.rotate = 30
g.draw = 'blue'
g.lineThickness = 'thick'
g = gr.grid(0,0, 3, 3)
g = gr.text("Another bit of text.", 2,3)
g.anchor = 'south west'
g.rotate = -120
g.draw = 'cyan'
gr.pdf()
gr.svg()

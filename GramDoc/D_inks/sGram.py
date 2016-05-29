from gram import Gram

gr = Gram()
gr.font = 'palatino'
gr.baseName = 'little'
g = gr.text("A bit of text.", 1,0)
g.draw = True
g = gr.text(r"$\sum \alpha\beta$", 2.5, 0)
g.anchor = 'west'
g = gr.text("0123456789", 3.5, 0)
g.anchor = 'west'
gr.png()

gr = Gram()
gr.font = 'palatino'
gr.baseName = 'little'
g = gr.text("A bit of text.", 1,0)
g.draw = True
g = gr.text('&#x2211;<tspan style="font-style: italic;">&#x03b1;&#x03b2;</tspan>', 2.5, 0)
g.anchor = 'west'
g = gr.text("0123456789", 3.5, 0)
g.anchor = 'west'
gr.svg()

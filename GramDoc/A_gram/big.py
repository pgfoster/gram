from gram import Gram
gr = Gram()
gr.font = 'helvetica'
gr.baseName = 'big'

ox = 35
oy = 20
x = ox + 10
y = oy + 55

gr.grid(ox,oy,x,y)

g = gr.text("Bottom left", ox,oy)
g.anchor = 'south west'

g = gr.text("Top right", x, y)
g.anchor = 'north east'

gr.pdf()
gr.svg()

    

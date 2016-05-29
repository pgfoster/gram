from gram import Gram,GramCoord,GramText
gr = Gram()
gr.font = 'times'
gr.baseName = 'style'

g = GramText('xXy')
g.cA = GramCoord()
g.textSize = 'Huge'
g.textShape = 'itshape'
g.color = 'green'
g.rotate = '30'
g.name = 'st1'
g.anchor = 'north west'
gr.styleDict[g.name] = g

g = GramText('xXy')
g.cA = GramCoord()
g.textSize = 'footnotesize'
g.textFamily = 'sffamily'
g.color = 'blue'
g.draw = 'violet'
g.name = 'st2'
g.anchor = 'center'
gr.styleDict[g.name] = g

for i in range(5):
    g = gr.text("Howdy!", 1, i)
    g.style = 'st1'

g = gr.styleDict['st2']
g.draw = 'orange'
for i in range(5):
    g = gr.text("Howdy!", 5, i)
    g.style = 'st2'

g = GramText('xXy')
g.cA = GramCoord()
g.textSize = 'Large'
g.textFamily = 'rmfamily'
g.textShape = 'scshape'
g.color = 'red'
g.draw = None
g.anchor = 'base'
g.rotate = 180.
g.name = 'st3'
gr.styleDict['st3'] = g


for i in range(5):
    g = gr.text("Howdy!", 9, i)
    g.style = 'st2'
    g.myStyle = 'st3'  # overrides style
    
if 1:
    #gr.pdf()
    #gr.cat()
    gr.svg()

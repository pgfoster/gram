from gram import Gram

tt = "xxx xxX xXy xyy".split()
xx = [i for i in range(1,5)]
gr = Gram()
gr.baseName = 'textVerticalAlignment'
gr.grid(0,0,5,5)
for i in range(4):
    gr.code(r"\node [anchor=west] at (%.1f,4.0) {%s};" % (xx[i], tt[i]))
    g = gr.text(tt[i],xx[i],3)
    g.anchor = 'west'
    gr.code(r"\node [anchor=west,draw] at (%.1f,2.0) {%s};" % (xx[i], tt[i]))
    g = gr.text(tt[i],xx[i],1)
    g.anchor = 'west'
    g.draw = True

gr.png()
# gr.svg()  tikz code does not work here


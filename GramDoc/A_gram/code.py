from gram import Gram,GramCode
gr = Gram()
gr.svgPxForCm = 100
gr.baseName = 'code'
gr.grid(0,0,3,3)
gr.code("% some tikz code")
gr.code(r"""\draw [->] (1,1) .. controls
(1.5,3) and (2,0) .. (2.5,2);""")
gr.code(r"""\draw [thick, gray, ->] (0,2)
parabola bend (0.5, 1)  (1, 2.5);""")
gr.png()

# Wipe out the tikz code
toRemove = [g for g in gr.graphics if isinstance(g, GramCode)]
for g in toRemove:
    gr.graphics.remove(g)

gr.code(r'<path d="M100 -100 C 150 -300 200 0 250 -200" stroke="black" fill="none" />')
gr.code(r'<path d="M 0 -200 Q 50 20 100 -250" stroke="grey" stroke-width="4px" fill="none" />')

gr.svg()

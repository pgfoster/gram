from gram import Gram
gr = Gram()
gr.baseName = 'fontWeight'
gr.font = 'helvetica'
gr.grid(-2,-1, 2, 1)
myText = "This is some text"
#gr.text("This is a PNG", 0,0)
gr.text(myText, 0,0)
gr.png()

gr.graphics.pop()
gr.text(myText, 0, 0)
#gr.text("This is SVG, weight 300", 0, 0)
gr.svgTextNormalWeight = 300
gr.baseName = 'fontWeight300'
gr.svg()

gr.graphics.pop()
gr.text(myText, 0, 0)
#gr.text("This is SVG, weight 400", 0, 0)
gr.svgTextNormalWeight = 400
gr.baseName = 'fontWeight400'
gr.svg()


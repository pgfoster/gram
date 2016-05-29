from gram import Gram
gr = Gram()
gr.font = 'helvetica'
gr.baseName = 'rect'
gr.grid(2,2,6,5)
g = gr.rect(2,3,5,4)
g.lineThickness = 5
g.color = 'teal'
g.fill = 'cyan!10'
g = gr.text("xXy", 4,5)
g.textSize = 'Large'
gr.pdf()
gr.svg()
    

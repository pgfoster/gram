from gram import Gram

gr = Gram()
gr.font = 'helvetica'
gr.baseName = 'size'
gr.pngResolution = 90
gr.svgPxForCm = 35.43307
gr.grid(0,0,1,1,color='black')
gr.png()
gr.svg()

gr.baseName = 'sizeB'
gr.pngResolution = 200
gr.svgPxForCm = 100
gr.png()
gr.svg()





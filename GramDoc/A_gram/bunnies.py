from gram import Gram
gr = Gram()
# gr.defaultInnerSep = 0.0
gr.grid(0,-1,4,2)
gr.font = 'palatino'
gr.baseName = 'bunnies'

# Define a couple of styles
from gram import GramText
st = GramText('Xy')
st.name = 'bunny1'
st.textShape = 'scshape'
st.color = 'violet'
gr.styleDict[st.name] = st

st = GramText('Xy')
st.name = 'bunny2'
st.rotate = 45
st.color = 'darkgray'
st.textSize = 'small'
st.draw = True
#st.shape='circle'
gr.styleDict[st.name] = st

g = gr.text("Flopsy", 1,1.2)
g.style = 'bunny1'

g = gr.text("Mopsy", 3,1.2)
g.style = 'bunny1'

g = gr.text("Cottontail", 1,0)
g.style = 'bunny1'
g.myStyle = 'bunny2'

g = gr.text("Peter", 3, 0)
g.style = 'bunny1'
g.anchor = 'south west'
g.textShape = 'itshape'
g.draw = True
g.color = 'blue!85'
g.fill = 'cyan!10'
g.textSize = 'Large'

# gr.showTextBB = True
# gr.showTextAnchor = True

gr.png()
gr.svg()

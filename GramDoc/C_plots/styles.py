from gram import Plot
gp = Plot()
gp.baseName = 'styles'
gp.line([-1,3,6],[-2,5,0], smooth=True)
# At this point, the styleDict is empty.
# The styleDict is filled by render().  Calling
# render() is usually automatic and hidden,
# called by eg png(), but it can be called by
# itself, and it does not hurt to call it
# more than once.
gp.render()
st = gp.styleDict['tickLabel']
st.textFamily = 'ttfamily'
st.textSize = 'large'
st = gp.styleDict['axisLabel']
st.textFamily = 'ttfamily'
st.textShape = 'itshape'
st.textSize = 'huge'
gp.xAxis.title = 'x'
gp.yAxis.title = 'f(x)'
gp.png()
gp.svg()


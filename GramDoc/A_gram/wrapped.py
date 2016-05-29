from gram import Gram
gr = Gram()
gr.baseName = 'wrapped'
gr.font = 'palatino'
myText = r"""This is a bit of text, with a
\texttt{textWidth}, to show wrapping.  You
can also set the \texttt{textJustification},
although this one does not, and so uses the
default \texttt{ragged} justification."""
g = gr.text(myText, 1,2.5)
g.textWidth = 4.0
gr.text(r'''This text is not wrapped, as
it has no \texttt{textWidth}''', 0,0)
gr.png()

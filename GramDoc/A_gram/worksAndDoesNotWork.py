from gram import Gram
myText = r"""This is some\\ multi-line text that
does not work so well.\\ With $\alpha$  unusual $\beta$ characters."""

if 0:  # This works
    gr = Gram()
    gr.baseName = 'minipage'
    stuff = r"\begin{minipage}{12cm}%s\end{minipage}" % myText
    g = gr.text(stuff, 1,2)
    g.anchor = 'south west'
    gr.pdflatexOutputGoesToDevNull = False
    gr.pdf()

if 0:  # This does not work
    gr = Gram()
    gr.baseName = 'varwidth'
    stuff = r"\begin{varwidth}{12cm}%s\end{varwidth}" % myText
    g = gr.text(stuff, 1,2)
    g.anchor = 'south west'
    gr.latexUsePackages.append("varwidth")
    gr.pdflatexOutputGoesToDevNull = False
    gr.pdf()

if 0:  # This does not work
    gr = Gram()
    gr.baseName = 'pbox'
    stuff = r"\pbox{12cm}{%s}" % myText
    g = gr.text(stuff, 1,2)
    g.anchor = 'south west'
    gr.latexUsePackages.append("pbox")
    gr.pdflatexOutputGoesToDevNull = False
    gr.pdf()

if 0:  # This does not work
    gr = Gram()
    gr.baseName = 'verbatim'
    gr.latexUsePackages.append('fancyvrb')
    print("appended fancyvrb")
    stuff = r"""\begin{Verbatim}This is some verbatim.\end{Verbatim}"""
    #stuff = myText
    g = gr.text(stuff, 1,2)
    gr.pdflatexOutputGoesToDevNull = False
    gr.pdf()

if 0:  # This does not work
    gr = Gram()
    gr.baseName = 'shortverbatim'
    gr.latexUsePackages.append('fancyvrb')
    print("appended fancyvrb")
    stuff = r"""This is |short verbatim|"""
    #stuff = myText
    g = gr.text(stuff, 1,2)
    gr.pdflatexOutputGoesToDevNull = False
    gr.pdf()


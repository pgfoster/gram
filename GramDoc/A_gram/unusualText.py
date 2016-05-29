t1 = """This is
some
usual
text.
"""

t2 = r"""\parbox{150pt}{\raggedright This \\ is
some \\ text in a parbox
with
line endings.}
"""

t3 = r"""\begin{minipage}{100pt} This is some
text that is put
in a minipage
that is 100 pt wide. \end{minipage}
"""

t3x = r"""\begin{minipage}{120pt}
\begin{enumerate*}
\item This is the first item of a mdw
enumerate* list, in a minipage
\item This is the second item
\item And the third.
\end{enumerate*}
\end{minipage}
"""

t4 = r"""\begin{minipage}{170pt}
\begin{center}
\begin{tabular}{@{}llr@{}} \toprule 
\multicolumn{2}{c}{Item} \\ \cmidrule(r){1-2} 
Animal & Description & Price (\$)\\ \midrule 
Gnat & per gram & 13.65 \\ 
& each & 0.01 \\ 
Gnu & stuffed & 92.50 \\ 
Emu & stuffed & 33.33 \\ 
Armadillo & frozen & 8.99 \\ \addlinespace
Total &           & 56.23 \\ \bottomrule 
\end{tabular}
\end{center}
\end{minipage}
"""

t5 = r"""\includegraphics[scale = 0.25, angle=32]
{../../frownie_tongue.png}"""

from gram import Gram
gr = Gram()
gr.font = "palatino"
gr.latexUsePackages.append('mdwlist')
gr.latexUsePackages.append('booktabs')
gr.latexUsePackages.append('graphicx')

bNames = ['t1', 't2', 't3', 't3x', 't4', 't5']
tt = [t1, t2, t3, t3x, t4, t5]

for dNum in range(6):
    gr.graphics = []
    gr.baseName = bNames[dNum]
    gr.text(tt[dNum],0,0)
    print "about to do %s" % tt[dNum]
    gr.png()

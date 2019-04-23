from gram import TreeGram
read('((A, (B, C)), (D, (E, (F, G))));')
t = var.trees[0]
t.draw()
nB = t.node('B')
nB.name = """This is the very long name
of the node that used to be `B'.  It needs
to have the text wrapped, but that affects
the spacing of the leaf taxa.  Both
wrapping and spacing are handled by setting
\\texttt{wrapLeafLabelsAt}."""
nE = t.node('E')
thePng = "../../frownie_tongue.png"
nE.name = r"\includegraphics[scale=0.3]{%s}" % thePng
tg = TreeGram(t, showNodeNums=False)
tg.font = 'palatino'
tg.latexUsePackages.append('graphicx')
tg.wrapLeafLabelsAt = 3.5
tg.baseName = 'fatTaxa'
#tg.grid(0,0,5,6)

# The style gets in the way, so it is
# auto-deleted.  With no style, the default
# anchor is center, so change that.
nE.label.anchor = 'west'
tg.extraYSpaceAtNode(nE, extra=1.1)
b = tg.setBracket(4, 5, text='A bracket',
                  leftNode=None, rotated=True)
bText = r"""Since the size of the picture is
unknown to Gram, it needed to have its
\texttt{extraYSpaceAtNode} set explicitly.
This bracket also needed to have its
\texttt{topOverRide} and
\texttt{rigthOverRide} set to some
appropriate values in order to
work; use a grid to get those values."""
b = tg.setBracket(9, 11, text=bText,
                  leftNode=None, rotated=True)
b.topOverRide = 2.8
b.rightOverRide = 4.3
b.label.style = None
b.label.textWidth = 2.5
b.label.textSize = 'scriptsize'
b.label.anchor = 'north'
b.label.rotate = 90
b.label.textJustification = 'badly centered'
tg.bracketsLineUp = False
tg.pdf()
# tg.svg()  # no workee, svg does not do wrapping

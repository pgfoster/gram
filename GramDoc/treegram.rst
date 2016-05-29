========
TreeGram
========


.. contents::



The TreeGram and TreeGramRadial classes
---------------------------------------

TreeGram is a subclass of Gram. 
TreeGram makes drawings of phylogenetic trees in the style where the
root of the tree is on the left and the lines are parallel and go
right, and the branch lengths are usually meaningful.  
The TreeGram subclass TreeGramRadial draws trees in a 'radial'
style.

.. _fig:parallel:

.. figure:: ./B_trees/Gram/parallelAndRadial.png

    Parallel style and radial style trees.


A minimal TreeGram script might be something like this ---

.. code-block:: python

    from gram import TreeGram
    read("((A,B)89,C,(D,E)95);")
    t = var.trees[0]
    tg = TreeGram(t)
    tg.baseName = 'minimal'
    tg.png()

TreeGram needs `p4 <http://p4.nhm.ac.uk>`_ for its Tree class, for reading and manipulating
phylogenetic trees, so if you saved the script above in a file ``minimal.py``, it
could be run by

::

    p4 minimal.py

This would make 

- a PDF file ``Gram/minimal.pdf``,

- a PNG file ``Gram/minimal.png`` made from that PDF file, like this

.. image:: ./B_trees/Gram/minimal.png


Actually you don't really need the ``baseName`` line --- ``tg`` is the default ``baseName``.  

Output files
------------

Here are the output files, and how to get them.

.. table::

    +---------------------------+-------------+
    | file type                 | method name |
    +===========================+=============+
    | PDF                       | ``pdf()``   |
    +---------------------------+-------------+
    | PDF, and PNG made from it | ``png()``   |
    +---------------------------+-------------+
    | SVG                       | ``svg()``   |
    +---------------------------+-------------+

Some things possible with PDF and PNG output do not work for SVG, and some
things possible with SVG do not work for PDF or PNG output.

The PDF files that are produced by ``pdf()`` are meant to be included
in an enclosing document without changing their sizes.
Font sizes and line thicknesses are chosen assuming that the diagram
will be unscaled, and any scaling will affect those sizes, usually
badly.  However, sometimes the tree is too big to fit on a page
without scaling it down.

If you want to simply print a tree on a single sheet of paper without
an enclosing document, that could be done with the ``pdfPage()`` method.

::

    tg.pdfPage()

Fonts
-----

Some user defaults, including the font, can be set via the ``conf`` files.  The default font is Helvetica.  In
the example that is
what I get.  Computer Modern does not work
with ``svg`` output.  You may also want to set the ``documentFontSize``, and the
``pdfViewer``.  You can over-ride any of these gram defaults and user defaults in
individual ``gram`` scripts.  Ideally you would want to match the font and font
size that is used in the diagram with that in the enclosing document.

Here is the same tree with Computer Modern font (as a png)

.. image:: ./B_trees/Gram/minimal_cm.png

and here is the same tree using Palatino (as an ``svg``).  

.. image:: ./B_trees/minimal_palatino.svg

The ``pdf`` or ``png`` using Palatino uses old style figures.

.. image:: ./B_trees/Gram/minimal_palatino.png

Startup
-------

You can read in a tree with the ``read()`` function from ``p4``.  Your tree would
generally be in a Nexus or Phylip (Newick) file, or in some simple cases such as
the previous example you can read in the tree from its Newick description
directly.  If the tree that you want to draw is in a file, you use the ``read()``
command with a file name, as

.. code-block:: python

    from Gram import TreeGram
    read('myTreeFile.nex')
    t = var.trees[0]
    tg = TreeGram(t)

As explained in the p4 documentation, the rationale for this somewhat awkward
construction above is that a tree file might contain more than one tree, and so
saying something like

.. code-block:: python

    t = read('myMultiTreeFile.nex') # does not work

would not work.  If there are multiple trees in the file,
they all get put in the ``var.trees`` list, and you can specify and get
a Tree object from that list as shown above.

If you are sure that you only have one tree in your file, you can save a few
keystrokes with this idiom ---

.. code-block:: python

    t = func.readAndPop('mySingleTreeFile.nex') 


When you instantiate a TreeGram instance with ``tg = TreeGram(t)``, there are various other arguments that you can invoke.  With
their defaults, they are

``scale=None``
    The horizontal scale, in cm.  If the scale is 1, then a branch length of 1 makes a horizontal line 1 cm long.  The default is None, and then TreeGram uses ``widthToHeight`` to calculate an appropriate scale.  However if you do specify a scale, that scale over-rides the ``widthToHeight``, and so you can make two TreeGrams have the same scale.

``yScale=0.7``
    The vertical scale, in cm.  This is the spacing between leaves.  

``showNodeNums=False`` 
    You can turn this on to put little numbers on the nodes, to help you in composition or debugging.

``widthToHeight=0.67``
    For the lines part of the tree drawing, excluding leaf labels, this is the width to height ratio, given the ``yScale``.  A suitable scale is calculated to achieve this ratio.  If you specify a scale, then that specified scale over-rides this. 

Tree arrays
-----------

You can add entire Gram objects to other Gram objects, and that
includes TreeGram objects --- so you can include a TreeGram in another
TreeGram.  To do that, you put the embedded TreeGram in the enclosing
TreeGram's ``grams`` list.

.. code-block:: python

    from gram import TreeGram
    read("((A,B)89,C,(D,E)96);")
    read("((H, I)73, (J, K)98, L);")
    t = var.trees[0]
    tg = TreeGram(t)
    tg.font = 'palatino'
    tg.documentFontSize = 10
    tg.baseName = 'twoTrees'
    t = var.trees[1]
    tgB = TreeGram(t)
    tgB.baseName = 'doesntMatter'
    tgB.gX = 4.
    tg.grams.append(tgB)
    #tg.pdf()
    tg.svg()

.. image:: ./B_trees/twoTrees.svg


You can include other kinds of Gram objects, as

.. code-block:: python

    from gram import TreeGram,TreeGramRadial,Gram
    read("((A,B)ab,C,(D,E)de)m;")
    t = var.trees[0]
    t.node(1).br.uName = 'X'
    t.node(5).br.uName = 'Y'
    tg = TreeGram(t, scale=7.)
    print "a", tg.internalNodeLabelSize
    tg.baseName = 'twoTreesII'
    t = t.dupe()
    tgB = TreeGramRadial(t, scale=8.,
                         slopedBrLabels=True,
                         rotate=90)
    print "b", tg.internalNodeLabelSize
    tgB.tree.root.label.yShift = 0.1
    tgB.gX = 4.8
    tgB.gY = -1.5
    gr = Gram()
    g = gr.text(r'$\Longleftrightarrow$', 0, 0)  # LaTeX symbol
    gr.text('equivalence', 0, 0.5)
    gr.gX = 3.5
    gr.gY = 1.0
    tg.grams.append(tgB)
    tg.grams.append(gr)
    tg.png()
    g.rawText = '&#x21D4;'       # unicode symbol
    tg.svg()

Here is the png ---

.. image:: ./B_trees/Gram/twoTreesII.png

... and the svg.

.. image:: ./B_trees/twoTreesII.svg

Scale bar
---------

A scale bar can be incorporated by the ``setScaleBar()`` method; usually
the default position is good, but in the example that follows it is
not -- it is badly placed.

.. code-block:: python

    from gram import TreeGram
    read('tinyTree.nex')
    t = var.trees[0]
    tg = TreeGram(t)
    tg.baseName = 'tinyI'
    tg.setScaleBar()
    tg.pdf()
    tg.svg()

.. image:: ./B_trees/tinyI.svg


The length of the scale bar is
chosen automatically; if you don't like the choice you can choose
another value in the ``setScaleBar()`` method.  The position of the
scale bar can be adjusted with offsets (in cm), as

::

    tg.setScaleBar(length=0.2, xOffset=0.0, yOffset=-0.6)


.. image:: ./B_trees/tinyII.svg

Node labels
-----------

TreeGram, as does the Tree class in ``p4``, distinguishes between node names and
branch names.  Leaf names are node names, usually representing taxon names.
Newick tree descriptions allow for internal node names, but do not accommodate
branch names as such.  The root node can have a name, but of course the root has
no branch.  Things like bootstrap support are most appropriately properties of
the branch, but nonetheless are usually given as internal node labels, because
they are given in Newick tree descriptions.

We usually have names for leaf nodes, but we may also have names for
internal nodes, and possibly for the root.  You can specify these
internal node names in Newick and Nexus tree descriptions.  The node
name, a string, is accessible in a p4 Tree for node ``n`` as ``n.name``.  This
is made into a Gram text object and attached to the node as ``n.label``.
As such, you can modify it, as for example


.. code-block:: python

    n.label.textShape = 'itshape'
    n.label.color = 'red!50'
    n.label.textSize = 'tiny'

Text sizes
^^^^^^^^^^

Relative to the ``documentFontSize``.

.. table::

    +--------------+-------+
    | tiny         | large |
    +--------------+-------+
    | scriptsize   | Large |
    +--------------+-------+
    | footnotesize | LARGE |
    +--------------+-------+
    | small        | huge  |
    +--------------+-------+
    | normalsize   | Huge  |
    +--------------+-------+

Other text attributes
^^^^^^^^^^^^^^^^^^^^^

.. table::

    +------------+----------+
    | textFamily | rmfamily |
    +------------+----------+
    | \          | sffamily |
    +------------+----------+
    | \          | ttfamily |
    +------------+----------+
    | textSeries | bfseries |
    +------------+----------+
    | textShape  | itshape  |
    +------------+----------+
    | \          | scshape  |
    +------------+----------+

Leaf labels of course go on the right of the leaf nodes.  The root
label, if it exists, generally goes on the left of the root, although
if you want it to go on the right you can set the TreeGram attribute
``rootLabelLeft=False``.  

Other internal node labels can be located in various positions near
the nodes that they are associated with.  In a busy tree, these
positions affect legibility.  These positions are affected by, or can be adjusted by

- The ``doSmartLabels`` attribute (``True`` by default), for automatic placement

- The ``fixTextOverlaps()`` method, to adjust labels up or down so that they do not overlap

- Setting the ``anchor`` of the label

- Changing the style of the label with the ``myStyle`` attribute of the label

By default, ``doSmartLabels`` is turned on, which attempts a smart
placement of labels.  This week, the rules are:

::

    The label goes on top of the branch, just to the left of the node,
    unless the label is too long to fit on the branch.

    If the label is too long, then where it goes depends on the
    node.  If the node is the left child of its parent, then the
    (too long) label stays on top of the branch anyway.  If the
    node is a rightmost child then the (too long) label gets put
    under the line, just behind the node.  For other nodes, that
    are not rightmost children, the (too long) label gets put on
    the right of the node.  In that case, if there are an odd
    number of children then it is nudged up a little to avoid
    being put directly on top of a line.  See 
    Figure `fig:smartLabels`_.


.. _fig:smartLabels:

.. figure:: ./B_trees/smartNodeLabels.svg

    This shows the effect of ``doSmartLabels`` settings on automatic internal node placement.  The default setting is ``True``.




The effect of the ``fixTextOverlaps()`` method can be seen in the
following pair of examples.  The method was called for the tree on the
right, but not for the tree on the left.


.. image:: ./B_trees/overlapping.svg

Labels and styles
-----------------

Some text sizes are specified by TreeGram variables.  For example, the
size of leaf labels is given by ``leafLabelSize``, which by default is
``normalsize``.  You can change the ``leafLabelSize`` or the
``internalNodeLabelSize`` or the ``branchLabelSize`` to change all the
text sizes that use those definitions.  You could do that, by, for
example,

.. code-block:: python

    tg = TreeGram(t)
    tg.leafLabelSize = 'footnotesize' # default normalsize
    tg.internalNodeLabelSize = 'tiny' # default scriptsize
    tg.branchLabelSize = 'scriptsize' # default tiny

Various *styles* for text items are defined, so that you can use the
same style for all leaf labels, all node labels, and so on.  Here are
some styles that are in use ---

``branch``
    a style for text on branch (not node) labels, either above or below the branch

``leaf``
    a style for non-root leaf labels

``root``
    a style for the root node label

``bracket label``
    a style for the text in bracket labels

In addition, there are 5 styles for internal node labels

- ``node right``

- ``node upper right``

- ``node lower right``

- ``node upper left``

- ``node lower left``

Besides changing the ``label.textSize`` and other attributes of an individual text box,
another way to change the attributes of the font is to redefine or over-ride
the style as described below.  For example, the default leaf label font style is upright.  But let's
say that you want leaf labels to be italic.  One way to do that is to
modify the leaf style, by

.. code-block:: python

    from gram import TreeGram
    read('tinyTree.nex')
    t = var.trees[0]
    tg = TreeGram(t)
    tg.baseName = 'tinyIII'
    # styleDict is empty until you render().
    tg.render()
    # Grab the leaf style ...
    st = tg.styleDict['leaf']
    # ... and change it
    st.textShape = 'itshape'
    #tg.pdf()
    tg.svg()

.. image:: ./B_trees/tinyIII.svg


Another way you could change the style of text is to define your own
style.  You could do that like this ---

.. code-block:: python

    from gram import TreeGram
    read('tinyTree.nex')
    t = var.trees[0]
    tg = TreeGram(t,showNodeNums=True)
    tg.baseName = 'tinyIV'
    tg.font = 'helvetica'
    if 1:
        # Make a new style, and put it in the
        # styleDict, with a name.
        from gram import GramText
        g = GramText("Xyx")
        g.textShape = 'itshape'
        g.textSize = 'small'
        g.color = 'white'
        g.draw = 'black'
        g.lineThickness = 'very thick'
        g.fill = 'blue!60'
        g.name = 'myleaf'
        g.anchor = 'west'
        tg.styleDict[g.name] = g

        # Apply the style to some of the leaves.
        for nNum in [1,4,5,7]:  # and one internal
            n = t.node(nNum)
            n.label.myStyle = 'myleaf'
    tg.png()
    tg.svg()


.. image:: ./B_trees/tinyIV.svg

Re-positioning internal node labels
-----------------------------------

You can re-position internal node labels in a few ways ---  

- You can change the ``anchor``,
  for example

  .. code-block:: python

      n.label.anchor = 'north east'

- You can over-ride the style with a ``myStyle`` with a different anchor,
  for example

  .. code-block:: python

      n.label.myStyle = 'node upper right'

- You can adjust the ``xShift`` and ``yShift``,
  for example

  .. code-block:: python

      n.label.xShift = 0.5  # cm
      n.label.yShift = -0.2

These are the anchors ---

.. table::

    +----------------+----------------+----------------+
    | ``west``       | ``north west`` | ``north``      |
    +----------------+----------------+----------------+
    | ``north east`` | ``east``       | ``base``       |
    +----------------+----------------+----------------+
    | ``base west``  | ``base east``  | ``south west`` |
    +----------------+----------------+----------------+
    | ``south``      | ``south east`` | ``center``     |
    +----------------+----------------+----------------+

The default is '``center``'.  


You can set the ``anchor`` of a text box (label) as follows.  Here the
default anchor for these short labels (dependent on ``doSmartLabels``)
would be with an anchor of '``south east``'.

.. code-block:: python

    from gram import TreeGram
    read('((A, B)uvw, (C, D)xyz);')
    t = var.trees[0]
    tg = TreeGram(t.dupe(),showNodeNums=True)
    tg.baseName = 'nodeLabels'
    tgB = TreeGram(t.dupe())
    tgB.tree.node(1).label.anchor = 'north east'
    tgB.tree.node(4).label.anchor = 'west'
    tgB.gX = 3.
    tg.grams.append(tgB)
    # tg.png()
    tg.svg()

.. image:: ./B_trees/nodeLabels.svg


.. code-block:: python

    from gram import TreeGram
    read("((A,B)Wxy,(C,(D,E, F)Xyz)Vwxy);")
    t = var.trees[0]
    tg = TreeGram(t.dupe(),showNodeNums=True)
    tg.baseName = 'stylesForInternalNodes'
    tgB = TreeGram(t.dupe())
    tgB.tree.node(1).label.myStyle = 'node lower left'
    tgB.tree.node(4).label.myStyle = 'node right'
    tgB.tree.node(6).label.myStyle = 'node lower right'
    tgB.gX = 4.
    tg.grams.append(tgB)
    tg.svg()


.. image:: ./B_trees/stylesForInternalNodes.svg

Branch labels
-------------

In addition to labelling internal nodes, branches (or edges) may be
also be labelled, either above or below the line. There is no facility
to specify that in Newick or Nexus tree descriptions.  Branch labels
may be added later, in 2 ways.

- You can set ``n.br.name`` before you instantiate a TreeGram object, or

- you can tell the TreeGram object to ``setBranchLabel(n, 'a label')``.

(And similarly for ``uName`` and ``setBranchULabel()``).  
The following shows both ways ---

.. code-block:: python

    from gram import TreeGram
    read("((A, B))root;")
    t = var.trees[0]
    t.node('A').br.name = 'label'
    tg = TreeGram(t)
    tg.scale = 8. # 7.035 otherwise, so a bit wider
    tg.baseName = 'brLabels'
    n = t.node('B')
    tg.setBranchULabel(n, 'uLabel')
    tg.png()
    tg.svg()

.. image:: ./B_trees/brLabels.svg


These labels are available as GramText objects ``n.br.label`` and
``n.br.uLabel``, and can be modified further as usual.

Broken branches
---------------

Branches that are too long are often not drawn to scale, indicated by
a "broken branch".  You can draw a broken branch as shown here.  

.. code-block:: python

    from gram import TreeGram
    read("tinyTree.nex")
    t = var.trees[0]
    tg = TreeGram(t)
    tg.baseName = 'brokenBranches'
    tg.setBrokenBranch(1)
    tg.setBrokenBranch(7)
    tg.png()
    tg.svg()

.. image:: ./B_trees/brokenBranches.svg

Grouping taxa with brackets
---------------------------

What we often want to do is to group some taxa together with a bracket
on the right, with a label.  This can be done with the ``setBracket()``
method.  The top and bottom nodes are given to define the bracket, and
if a ``leftNode`` is also given then a shaded box is drawn.  If there is
more than one bracket then by default they line up with each other.

.. code-block:: python

    from gram import TreeGram
    read("((A, B), (C, D), (E, (F, G)));")
    t = var.trees[0]
    tg = TreeGram(t, showNodeNums=True)
    tg.baseName = 'bracket1'
    t.draw()
    tg.setBracket(2, 3, text='these brackets line',
                  leftNode=1)
    tg.setBracket(6, 10, text='up with each other',
                  leftNode=None, rotated=True)
    tg.png()
    tg.svg()

.. image:: ./B_trees/bracket1.svg

The brackets need not line up with each other; it is under the control of the ``bracketsLineUp`` attribute, which is ``True`` by default.  The label can have wrapped text when using TikZ, turned on with ``textWidth``.

.. code-block:: python

    from gram import TreeGram
    read("((A, B), (C, D), (E, (F, G)));")
    t = var.trees[0]
    tg = TreeGram(t, showNodeNums=False)
    tg.font = 'palatino'
    tg.baseName = 'bracket2'
    t.draw()
    longText1 = """A long note \
    about this grouping of taxa, \
    composed of A and B""" 
    b = tg.setBracket(2, 3, text=longText1,
                      leftNode=None)
    b.label.style=None
    b.label.textSize='scriptsize'
    b.label.anchor = 'west'
    b.label.textWidth = 3.0
    b.label.innerSep = 0.2
    b = tg.setBracket(6, 10, text='Rotated label',
                      leftNode=None, rotated=True)
    b.label.textSize='large'
    tg.bracketsLineUp = False
    #tg.showTextAnchor = True
    tg.png()
    tg.svg()

.. image:: ./B_trees/Gram/bracket2.png

We can have multiple brackets.

.. code-block:: python

    from p4 import *
    read("((A,B)89,C,(D,E)95);") 
    t = var.trees[0]
    n = t.node('A')
    n.name = r'Ab{\textcolor{blue}{cde}}fgh {\textcolor{blue}{\ding{110}}}'
    #n.name = r'Ab<tspan fill="blue">cde</tspan>fgh <tspan fill="blue"> &#x2B1B;</tspan>'
    #n.name = r'Ab<tspan fill="blue">cde</tspan>fgh <tspan fill="blue"> &#xFFED;</tspan>'
    t.draw()
    from gram import TreeGram
    tg = TreeGram(t, scale=None, showNodeNums=False, widthToHeight=0.67) 
    tg.latexUsePackages.append('pifont')
    tg.baseName = "multiBrackets"
    #tg.showTextBB=True
    #tg.showTextAnchor=True
    #tg.pdflatexOutputGoesToDevNull=False
    #tg.grid(0,0,4,4)
    g = tg.setBracket(t.node('D').nodeNum,7, text="Bracket DE", rotated=True)
    g = tg.setBracket(t.node('B').nodeNum,6, text="Bracket BCD", rotated=True)
    g.rightExtra = 0.7
    g = tg.setBracket(2,4, text="Bracket", rotated=False)
    tg.bracketsLineUp = False
    #tg.render()
    #tg.styleDict['bracket label'].textSize = 'tiny'
    tg.png()
    n.label.rawText = r'Ab<tspan fill="blue">cde</tspan>fgh <tspan fill="blue"> &#x2B1B;</tspan>'
    tg.svg()

Here is the PNG ---

.. image:: ./B_trees/Gram/multiBrackets.png

And here is the SVG ---

.. image:: ./B_trees/multiBrackets.svg

Firefox shows me a blue square ding, but Safari shows me a black highlighted ding.

Here is another example, showing more colour.

.. code-block:: python

    from gram import TreeGram
    read('(A, (B, (C, (D, (E, F))85)));')
    t = var.trees[0]
    tg = TreeGram(t)
    tg.font = 'helvetica'
    tg.baseName = 'simplified'
    tg.leafLabelSize = 'tiny'
    tg.render()
    tg.styleDict['bracket label'].textSize = 'Large'
    for n in t.iterLeavesNoRoot():
        n.label.rawText = ' '
    t.node(5).label.rawText = 'Euryarchaeota'
    t.node(7).label.rawText = 'Crenarchaeota / eocytes'
    t.node(6).label.anchor = 'north east'
    g = tg.setBracket(1, 3, text='Bacteria', leftNode=0)
    g.fill = 'blue!15'
    g = tg.setBracket(5, 7, text='Archaea', leftNode=4)
    g.fill = 'orange!20'
    g = tg.setBracket(9, 10, text='Eukaryotes', leftNode=8)
    g.fill = 'green!30'
    tg.wrapLeafLabelsAt = 1.3     # svg can't do this
    tg.pdf()
    tg.wrapLeafLabelsAt = None
    tg.svg()

.. image:: ./B_trees/simplified.svg

Fat taxa
--------

Some taxa take up a lot of vertical space, perhaps because the taxon
name is actually a graphic, or perhaps because the name is very long
and is wrapped to two or more lines.  These can be accommodated in
TreeGram -- the latter automatically, and the former by some settings.

.. code-block:: python

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
    tg.png()
    # tg.svg()  # no workee

.. image:: ./B_trees/Gram/fatTaxa.png

Wrapping leaf labels at commas
------------------------------

I have occasionally had to work with datasets with some taxa that had
identical sequences, where I analyse them with the identical sequences
collapsed into a single sequence, but where I want to present the
final tree with all the identical taxa names included.  It is more
clear if each name is on a line by itself, separated by commas, rather
than if the list of identical taxa is wrapped like a paragraph.  To do
that, invoke 

::

    wrapLeafLabelsAt = 'comma'

.. code-block:: python

    from gram import TreeGram
    read('((A, B), (C, (D, E)));')
    t = var.trees[0]
    t.draw()
    nB = t.node('B')
    nB.name = """synonym 1, another synonym,
    and a third synonym."""
    nE = t.node('D')
    nE.name = """synonym 1, synonym 2, 
    yet another synonym, and synonym 4"""
    tg = TreeGram(t, showNodeNums=False)
    tg.wrapLeafLabelsAt = 'comma'
    tg.baseName = 'wrapLeafLabelsAtComma'
    tg.png()
    # tg.svg() no workee

.. image:: ./B_trees/Gram/wrapLeafLabelsAtComma.png

Node confidence boxes
---------------------

Sometimes you have some idea of the confidence range that you have in
the (horizontal) position of nodes.  For example, you might have a
confidence interval for dates in a molecular dating tree; BEAST uses
that.  P4 can read BEAST trees made by the TreeAnnotator program, and
draw confidence boxes like FigTree.  The confidence box uses the
``height_95_HPD`` doublet.

.. code-block:: python

    from gram import TreeGram
    var.nexus_getAllCommandComments = True
    var.nexus_readBeastTreeCommandComments = True
    read('treeannotatorOut')
    t = var.trees[0]
    tg = TreeGram(t)
    tg.baseName = 'beastA'
    for n in t.iterNodes():
        if not n.isLeaf:
            tg.setNodeConfidenceBox(n)
    tg.png()
    tg.svg()

.. image:: ./B_trees/Gram/beastA.png

Another example

.. code-block:: python

    from gram import TreeGram
    var.nexus_getAllCommandComments = True
    var.nexus_readBeastTreeCommandComments=True
    read('treeannotatorOut')
    t = var.trees[0]

    # The two cBoxes on the left are too big, and dominate the figure.
    # Make them text, as a node labels, instead.
    n = t.root
    n.name = "(%.1f, %.1f)" % (n.height_95_HPD[1], n.height_95_HPD[0])
    n = t.node(1)
    n.name = "(%.1f, %.1f)" % (n.height_95_HPD[1], n.height_95_HPD[0])

    tg = TreeGram(t)
    tg.font = 'palatino'
    tg.documentFontSize = 10
    tg.baseName = 'beastB'
    for nNum in [3,4,6,9]:
        n = t.node(nNum)
        tg.setNodeConfidenceBox(n)

    # Define a style
    from gram import GramText
    tg.render()
    tb = GramText('myStyle')
    tb.textWidth = 1.
    tb.textSize = 'scriptsize'
    tb.anchor = 'west'
    tb.name = 'wrappedNode'
    tg.styleDict['wrappedNode'] = tb

    for nNum in [0,1]:
        n = t.node(nNum)
        n.label.myStyle = 'wrappedNode'

    tg.png()
    tg.svg()  # no wrapping in svg

.. image:: ./B_trees/Gram/beastB.png

Radial trees
------------

TreeGramRadial, a subclass of TreeGram, is used to make radial trees.

By default it uses ``drawtree`` from the Phylip package to get the shape of the
trees, using the equal daylight algorithm (TreeGramRadial argument ``equalDaylight=True`` by default).  
Optionally it can use a simpler algorithm where the slope of the leaf branches increase evenly over the circle.  You can turn off equal daylight and turn on the simpler algorithm by

::

    tg = TreeGramRadial(t, equalDaylight=False)

Here is an example of each ---

.. code-block:: python

    from gram import TreeGramRadial
    tA = func.readAndPop('((A, B), (C, D), (E, (F, (G, H))));')
    tB = tA.dupe()

    tg = TreeGramRadial(tA, maxLinesDim=3.,equalDaylight=True)
    tg.baseName = 'equalDaylightAndSimpleRadialA'

    tgB = TreeGramRadial(tB, maxLinesDim=3.,equalDaylight=False, rotate=70)
    tgB.gX = 7.
    tgB.gY = 2.6
    tg.grams.append(tgB)

    #tg.grid(0,0,8,8)
    gA = tg.text("Equal Daylight", 0.5,0.5)
    gB = tg.text("Simple radial", 5.5,0.5)
    for g in [gA, gB]:
        g.anchor = 'west'
        g.textSize = 'normalsize'

    #tg.pdf()
    tg.svg()

.. image:: ./B_trees/equalDaylightAndSimpleRadialA.svg

With the pair above, the equal daylight version seems better.  However sometimes, as shown below, the equal daylight algorithm gets confused, and the simple algorithm does better.

.. code-block:: python

    # import string
    # t = func.randomTree(taxNames=list(string.uppercase), seed=0)
    # t.writeNexus('t26.nex')


    from gram import TreeGramRadial
    tA = func.readAndPop('t26.nex')
    tA.reRoot(19)     # re-rooting can often help.
    tB = tA.dupe()

    tg = TreeGramRadial(tA, maxLinesDim=8.,equalDaylight=True)
    tg.baseName = 'equalDaylightAndSimpleRadialB'

    tgB = TreeGramRadial(tB, maxLinesDim=8.,equalDaylight=False)
    tgB.gX = 5.
    tgB.gY = -2.5
    tg.grams.append(tgB)

    #tg.grid(0,-10,10,10)
    gA = tg.text("Equal Daylight", 0,3)
    gB = tg.text("Simple radial", 0,-6.5)
    for g in [gA, gB]:
        g.anchor = 'west'
        g.textSize = 'normalsize'
    # gC = tg.text("(equalDaylight=False)", 0,-7.2)
    # gC.textFamily = 'ttfamily'
    # gC.anchor = 'west'

    #tg.pdf()
    tg.svg()

.. image:: ./B_trees/equalDaylightAndSimpleRadialB.svg


In this next example, the TreeGramRadial is instantiated with a tree with no
branch length information, and no internal node names. The ``maxLinesDim``
argument gives the maximum dimension of the "lines" part of the diagram,
excluding the leaf labels.

.. code-block:: python

    from gram import TreeGramRadial
    read('(chimp, gorilla, (human, (gibbon, orang)));')
    t = var.trees[0]
    tg = TreeGramRadial(t, maxLinesDim=2.,rotate=-50)
    tg.baseName = 'radialTinyI'
    tg.png()
    tg.svg()

.. image:: ./B_trees/radialTinyI.svg

The tree diagram above seems clear enough.  However if we add in branch length information it becomes harder to read.

.. code-block:: python

    from gram import TreeGramRadial
    read('tinyTree.nex')  # with branch lengths and supports
    t = var.trees[0]

    # Delete the internal branch supports
    for n in t.iterInternalsNoRoot():
        n.name = None

    tg = TreeGramRadial(t, maxLinesDim=2.,rotate=-50)
    tg.baseName = 'radialTinyII'
    tg.png()
    tg.svg()

.. image:: ./B_trees/radialTinyII.svg

We can additionally add in internal node support. 
Notice that the internal node names are not very well
placed.  Sometimes the programmatic placement is all right, but often not.
not.  

.. code-block:: python

    from gram import TreeGramRadial
    read('tinyTree.nex')
    t = var.trees[0]
    tg = TreeGramRadial(t, maxLinesDim=2.,rotate=-50)
    tg.baseName = 'radialTinyIII'
    tg.png()
    tg.svg()

.. image:: ./B_trees/radialTinyIII.svg

A quick tweak of the SVG file with Inkscape gives this ---

.. image:: ./B_trees/radialTinyIII_ink.svg


Often it is better to use branch labels rather than node labels
for radial trees.  The following is an example, with both branch labels and internal node labels.  Internal branch lengths are sufficiently long, so it is all clear enough (although too busy).  This example also uses sloped branch
labels, which seem to work well.  

.. code-block:: python

    from gram import TreeGramRadial
    read("((A,B)ab,C,(D,E)de)m;")
    t = var.trees[0]
    t.node(1).br.uName = 'X'
    t.node(5).br.name = 'Y'
    tg = TreeGramRadial(t, scale=7.,
                        slopedBrLabels=True,
                        showNodeNums=False,
                        rotate=90)
    tg.baseName = 'smallRadialI'
    tg.font = 'palatino'

    tg.png()
    tg.svg()

.. image:: ./B_trees/smallRadialI.svg

In this next example the tree has numerical internal node names representing support, and in the first part of the script they are all transferred to the branches, which makes it much more legible.

.. code-block:: python

    from gram import TreeGramRadial
    read('fancyTree.nex')
    t = var.trees[0]
    for n in t.iterInternalsNoRoot():
        if n.name:
            if n.name in ['0.22']:
                n.br.name = n.name
            else:
                n.br.uName = n.name
            n.name = None
    tg = TreeGramRadial(t, maxLinesDim=6.,
                        rotate=120,
                        showNodeNums=False,
                        slopedBrLabels=True)
    tg.baseName = 'smallRadialII'

    # There are a two superimposed taxon names
    # Either of these can be used to fix it.
    if 1:
        tg.fixTextOverlaps()
    else:
        t.node(11).label.yShift = -0.25
        t.node(12).label.yShift = 0.25
    tg.setScaleBar(xOffset=-2.0, yOffset=3.0)
    tg.pdf()
    tg.svg()

.. image:: ./B_trees/smallRadialII.svg

Combining split supports
------------------------

A common task is to combine the results from two different analyses of
the same data onto one summary tree.  The two analyses each have a set
of input trees (MCMC samples or bootstrap analyses), and so each
analysis has a consensus tree and a list of split supports.

What is commonly done is to choose one consensus tree as the master
tree, and put the support from the second consensus tree on the
master.  This example shows one way to do that.  In this example the
master tree and the second consensus tree are identical in topology,
which makes things easy.  SplitKeys are made for every branch in both
trees.  For the second consensus tree the nodes corresponding to each
splitKey are made easy to get using a dictionary.  From there it is
easy to associate one splitKey in the second consensus tree with the
same splitKey from the master tree.

The second consensus tree might be the same topology with different
support values, or it might be a different topology with some shared
splits.  If you use the second consensus tree as the source of support
values, then if the master tree and the second tree are the same
topology then you can get a corresponding second support value from
every split in the master consensus tree (the example following is
like that).  However, if the second consensus tree differs, and you
use it as the source of support values, then there will be missing
values --- there will be some splits in the master that will not have
a corresponding support value in the second consensus tree.  This can
be improved somewhat if the second list of split supports is used as
the source of second supports, rather than using the second consensus
tree -- then you will have split supports available that did not make
it into the second consensus.

The following example shows two possible input trees, ``easyTreeA.nex``
and ``easyTreeB.nex``, where the former is used as the master tree.  The
two trees have identical splits, and so it is straightforward to
combine the support values, as shown in the third tree below.

.. code-block:: python

    from gram import TreeGram
    read('easyTreeA.nex')
    read('easyTreeB.nex')

    tA = var.trees[0]
    # make a duplicate tree, as tA is used again below
    tg = TreeGram(tA.dupe())  
    tg.baseName = 'combineSplitSupports'
    tg.tree.node(8).label.myStyle = 'node upper right'
    tg.tree.node(10).label.myStyle = 'node right'

    tB = var.trees[1]
    tgB = TreeGram(tB)
    tgB.gY = -7.5
    tg.grams.append(tgB)

    tA.makeSplitKeys()
    tB.makeSplitKeys()
    nodeForSKDict = {}
    for n in tB.iterInternalsNoRoot():
        nodeForSKDict[n.br.splitKey] = n
    for n in tA.iterInternalsNoRoot():
        theNode = nodeForSKDict.get(n.br.splitKey)
        if theNode:
            n.name += '/%s' % theNode.name

    tgX = TreeGram(tA, showNodeNums=False)
    tgX.tree.node(8).label.myStyle = 'node upper right'
    tgX.tree.node(10).label.myStyle = 'node right'
    tgX.gY = -15.
    tg.grams.append(tgX)
    #tg.font = 'palatino'
    #tg.grid(0, -16, 5, 7) 
    #tg.pdf()
    tg.svgPxForCm = 60.
    tg.svg()
    st = tg.styleDict['node upper left']

.. image:: ./B_trees/combineSplitSupports.svg

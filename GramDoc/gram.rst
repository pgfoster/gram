==============
The Gram Class
==============


.. contents::

This page contains far too much poorly-explained detail.  It is mostly notes to myself about how it works.  By all means skip it.

Hello World!
------------

A minimum Hello World! script would be 

.. code-block:: python

    from gram import Gram
    gr = Gram()
    gr.baseName = 'helloWorld'
    gr.text("Hello World!", 0, 0)
    gr.png()
    gr.svg()

Here is the PNG, made from the PDF ---

.. image:: ./A_gram/Gram/helloWorld.png

And here is the SVG

.. image:: ./A_gram/helloWorld.svg

Actually, you don't need the ``baseName`` line --- if you don't use it, Gram uses
the default ``gram`` as the ``baseName``.  The ``baseName`` affects naming of files
that result.  For PDF and PNG output it makes a Gram directory in which it
places various files.  The directory name is ``Gram`` by default, but that
directory name can be set by the user, via the ``dirName`` attribute of Gram
instances (and of course instances of its subclasses TreeGram, and Plot).  In
this example, with ``baseName='helloWorld``', the files are

``Makefile``     
    This allows re-making of the PDF (``make pdf``). 

``helloWorld.tex``        
    A short 'main' tex file, into which the TikZ file is input 

``helloWorld.tikz.tex``
    A human readable and editable TikZ file.  This file is input into ``helloWorld.tex`` 

``helloWorld.pdf``       
    The picture, either page sized or a small PDF. 

In addition we have ``helloWorld.aux`` and ``helloWorld.log``, which are PDFLaTeX
leftovers.  These intermediate files are plain text files, and they can
sometimes be useful, not least for debugging.  They are independent of Gram
(another design decision), and readable, editable, and usable by the user.
Using these files, you can re-make the PDF file, perhaps after a bit of editing,
without the gram package.

When making your final document for print, if you are using PDFLaTeX you can
embed the resulting small PDF file in your document with the ``includegraphics``
command from the ``graphicx`` package.  Another option is to include content of
the TikZ file in your LaTeX document, or ``\input`` the ``tikz.tex`` file.

What is it for?
---------------

If you want to make a one-off drawing, you might want to just use the very
capable TikZ rather than using Gram.  However, if you find yourself needing to
make the same sort of simple drawing repeatedly, then it might be worthwhile use
Gram, or to subclass Gram, to help you do that.  Gram is a base class; it was
meant to be subclassed.  You might find the Plot and TreeGram subclasses to be
useful; but the raw Gram class as such is possibly less so.

Making Gram graphics
--------------------

To draw a Gram, you instantiate a Gram object as was done in the 'Hello World!' example, and then use one of a very few methods to add primitive graphics objects to it, and then make a graphics output file (PDF, PDF+PNG, or SVG).  The methods are

``grid``
    This makes a grid, with cm spacing, to help with the layout of the diagram.  You call this method specifying the lower left and upper right corners.

``text``
    This makes a text box.

``line``
    This makes a straight line

``rect``
    This makes a simple rectangle

``code``
    This allows you to add raw TikZ or SVG code to your Gram.

These methods are called as 

- ``grid(llx, lly, urx, ury)``

- ``text(theText, x, y)``

- ``line(x1, y1, x2, y2)``

- ``rect(x1, y1, x2, y2)``

- ``code(theCode)``

The graphics are positioned in centimetre units.  The ``text``, ``line``, and 
``rect`` methods return the graphic objects that they make, allowing
further modification, as for example


.. code-block:: python

    g = text('my text', 0,0)
    g.color = 'orange'

How to make a Gram
------------------

1. Instantiate a ``Gram`` object

   .. code-block:: python

       gr = Gram()

2. Add some GramGraphics, such as text, lines, and so on, by calling the methods 

   .. code-block:: python

       gr.text(...)
       gr.line(...)
       gr.rect(...)

   and so on …

3. Make a graphics output file, such as a PDF, ``gr.pdf()``

   .. code-block:: python

       gr.pdf()

   or a PNG

   .. code-block:: python

       gr.png()

   or an SVG

   .. code-block:: python

       gr.svg()

Fonts
-----

These fonts are available

.. table::

    +----------------------+-------------+-----+
    | \                    | PDF and PNG | SVG |
    +======================+=============+=====+
    | Computer Modern (cm) | Yes         | No  |
    +----------------------+-------------+-----+
    | Helvetica            | Yes         | Yes |
    +----------------------+-------------+-----+
    | Palatino             | Yes         | Yes |
    +----------------------+-------------+-----+
    | Times                | Yes         | Yes |
    +----------------------+-------------+-----+


Setting the font is case insensitive.  Font sizes are as used in LaTeX, that is
``normalsize``, ``small``, ``large``, and so on.  And as in LaTeX, the size of
``normalsize`` can be set -- in gram it is set via the ``documentFontSize``
attribute of Gram, TreeGram, and Plot instances.  When using PDF output you will
probably want to make the ``documentFontSize`` of the Grams the same as the
enclosing document.  When using TikZ, you can use different text styles, such as
small caps, italics, and sans serif text.  Using Palatino or Times font
specifies Helvetica as its sans serif font.

Grams within Grams
------------------

A Gram can be embedded in another Gram.  To do that you put the embedded gram in
the list of an enclosing Gram's list of ``grams``.  You can shift entire Gram
objects with ``gX`` and ``gY``.

.. code-block:: python

    from gram import Gram
    gr1 = Gram()
    gr1.font = 'helvetica'
    gr1.baseName = 'gramInGram'
    gr1.text("Embedding gram", 0,0)
    gr2 = Gram()
    g = gr2.text("Embedded gram",0,0)
    gr2.gX = 0.3
    gr2.gY = 0.5
    gr1.grams.append(gr2)
    gr1.pdf()
    gr1.svg()

And here is the SVG ---

.. image:: ./A_gram/gramInGram.svg

Class data attributes of the Gram Class
---------------------------------------

Here I am distinguishing class data attributes from instance data attributes.

``font``
    Computer Modern is the default.  Otherwise Palatino, Times, and Helvetica.

``documentFontSize``
    The default is 11, for ``11pt``.  This is the size of ``normalsize`` font, as you would set it in LaTeX in the ``\documentclass``.  This should match the font size for the intended enclosing document.

``pdfViewer``
    Default ``ls``, which is a useless but safe choice.  Set it to ``open`` on the Mac, and your favourite PDF viewer on Linux.

``styleDict``
    Default in raw Gram is empty, but in subclasses Plot and TreeGram it has some useful styles.

Other class attributes that are useful for debugging
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``showTextBB``
    Default False.  A Boolean, saying whether to draw what Gram thinks is the bounding box around a TextBox.

``showTextAnchor``
    Default False.  A Boolean saying whether to put a mark where the TextBox is anchored.

``pdflatexOutputGoesToDevNull``
    Default True.  A Boolean.

Since the attibutes above are class attributes, they are universal, and so for example anything in Gram can set the font, and everything, including every instance of GramText, has immediate access to the font.

Debugging PDFLaTeX generation
-----------------------------

One of the more common places for gram to have problems is in PDFLaTeX
generation.  You might see it hang there, without an error message.  You can
kill it from another terminal, as usual.  The reason there is no error message
is that since the printout of PDFLaTeX is so verbose, by default Gram sends that
output to ``/dev/null``, and so it is not seen (possibly a bad design decision).
You can make PDFLaTeX verbose again for debugging by

::

    gm = Gram()
    gm.pdflatexOutputGoesToDevNull = False # default True

This affects lines in the ``Makefile`` (mentioned above) that calls PDFLaTeX.  To get the same effect, you could just edit that ``Makefile``.   Sometimes you can see the problem when you can see that output. 

Instance data attributes of the Gram class
------------------------------------------

``dirName``
    By default ``Gram``.  Where the LaTeX, TikZ, and PNG files get put.  SVG files are written to the current directory

``baseName``
    By default ``gram``.  

``latexUsePackages``
    By default an empty list.  If you use a LaTeX package, put it in here, *eg* 

    ::

        gr.latexUsePackages.append('booktabs')
        gr.latexUsePackages.append('pifont')

``latexOtherPreambleCommands``
    By default an empty list.  If you need some LaTeX commands for your diagram, put them in here.

``graphics``
    By default an empty list.  Whenever you make a Gram graphic via ``line()``, ``text()``, and so on, the graphic gets put in this list.  

``grams``
    By default an empty list.  You can put entire Gram objects in here, as described above.

``gX``, ``gY``
    By default 0.0.  The xShift and yShift of Gram objects in the ``grams``.

The GramGraphic class
---------------------

GramGraphic instances have

``color``
    By default ``None``, implying black.  Set to one of '``red``', '``green``', '``blue``', '``cyan``', '``magenta``', '``yellow``', '``black``', '``gray``', '``white``', '``darkgray``', '``lightgray``',
    '``brown``', '``orange``', '``purple``', '``violet``', '``lime``', '``olive``', '``pink``', and '``teal``'.  This uses the LaTeX ``xcolor`` package, so you can also say, for example '``red!20``' for a light pink, or '``black!10``' for a light gray. 

``colour``
    Same as color.

``fill``
    By default ``None``.  For rectangles or text box outlines, the fill colour.  Set to a colour.

``anchor``
    By default ``None``, implying '``center``'.  See below in the section on anchors.

``anchorOverRide``
    By default ``None``.  If the anchor of something is set programmatically, you can over-ride it with this.

``anch``
    Use this in conjunction with ``anchorOverRide``.  This is read only --- it can't be set.  If ``anchorOverRide`` is set, return it.  Otherwise return ``anchor``.

``xShift``
    By default 0.0.

``yShift``
    By default 0.0.

``rotate``
    By default ``None``.  Rotation in degrees.

``lineThickness``
    By default ``None``, implying '``thin``'.  Set to one of the standard line thicknesses ('``thick``', '``very thin``' and so on) or to a thickness in postscript points (bp in TeX).

``cap``
    By default None, implying '``butt``'.  Line endings.  Set to one of '``rect``', '``butt``', or '``round``'.

``lineStyle``
    By default ``None``.  Set to one of ``None``, '``solid``', '``dotted``', '``densely dotted``', '``loosely dotted``', '``dashed``', '``densely dashed``', '``loosely dashed``'.

``roundedCorners``
    By default ``None``.

``cA (and ~cB``)
    By default ``None``.  This is for a GramCoord instance.  GramCoord instances have ``xPosn`` and ``yPosn`` attributes.

``style``
    By default ``None``.  

``myStyle``
    By default ``None``.  If it exists, this will over-ride the ``style``.

``bb``
    The bounding box, as calculated by Gram

Often both ``style`` and ``myStyle`` are ``None``.  Gram (or rather TreeGram) might programmatically set ``style``, in which case you can set ``myStyle`` to over-ride it.

GramLine
--------

For GramLines, the ``lineThickness`` is given either in ``pt`` or in words as in TikZ.  
One PostScript point is exactly 1/72 of an inch, and so is 0.035277138 cm.  See `lineThickness`_ for line thicknesses using words.
For example,

.. code-block:: python

    from gram import Gram
    gr = Gram()
    gr.baseName = 'line'
    gr.font = 'Helvetica'
    gr.grid(0,0,4,4)
    g = gr.line(1,1,2,3)
    g.colour = 'black!20'
    g.lineThickness = 28. # pts
    g = gr.line(3, 3.5, 2, 1)
    g.lineThickness = 'semithick'
    g.lineStyle = 'dashed'
    # A default, un-modified line
    gr.line(1, 3, 1.5, 0.5)
    g = gr.line(3.5, 1, 3.5, 2)
    g.lineThickness = 10
    g.cap = 'rect'  # default butt
    g = gr.text('some lines', 3,3)
    g.anchor = 'north west'
    g.textSize = 'normalsize'
    gr.png()
    gr.svg()

Here is the SVG ---

.. image:: ./A_gram/line.svg

lineThickness
-------------

The default is ``None``, which gives 0.4 pt.  

You can set the ``lineThickness`` to some number of points, or to one of 

.. table::

    +-------------------+-----+
    | \                 |  pt |
    +-------------------+-----+
    | '``ultra thin``'  | 0.1 |
    +-------------------+-----+
    | '``very thin``'   | 0.2 |
    +-------------------+-----+
    | '``thin``'        | 0.4 |
    +-------------------+-----+
    | '``semithick``'   | 0.6 |
    +-------------------+-----+
    | '``thick``'       | 0.8 |
    +-------------------+-----+
    | '``very thick``'  | 1.2 |
    +-------------------+-----+
    | '``ultra thick``' | 1.6 |
    +-------------------+-----+

GramRect
--------

You can draw a rectangle as

.. code-block:: python

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

.. image:: ./A_gram/rect.svg

GramCode
--------

Adding raw TikZ or SVG code is also possible, which would allow you to do things that Gram cannot do on its own, such as drawing curves.

.. code-block:: python

    from gram import Gram,GramCode
    gr = Gram()
    gr.svgPxForCm = 100
    gr.baseName = 'code'
    gr.grid(0,0,3,3)
    gr.code("% some tikz code")
    gr.code(r"""\draw [->] (1,1) .. controls
    (1.5,3) and (2,0) .. (2.5,2);""")
    gr.code(r"""\draw [thick, gray, ->] (0,2)
    parabola bend (0.5, 1)  (1, 2.5);""")
    gr.png()

    # Wipe out the tikz code
    toRemove = [g for g in gr.graphics if isinstance(g, GramCode)]
    for g in toRemove:
        gr.graphics.remove(g)

    gr.code(r'<path d="M100 -100 C 150 -300 200 0 250 -200" stroke="black" fill="none" />')
    gr.code(r'<path d="M 0 -200 Q 50 20 100 -250" stroke="grey" stroke-width="4px" fill="none" />')

    gr.svg()

.. image:: ./A_gram/Gram/code.png

.. image:: ./A_gram/code.svg

Text
----

The remainder of this description of the Gram class is given over to a
description of Gram text.  Text is most capable using PDFLaTeX and TikZ, but you
can do things with text with SVG as well.

Text in Gram closely follows text in TikZ, so Gram text will be explained via
TikZ text, with examples stolen from the TikZ manual.  In TikZ, one of the ways
that you can place text on the page is as a *node*, and that is the way
that Gram does it.  In TikZ, one of the ways to specify where something goes is
to use *coordinates*, and that is the way that Gram does it.  In raw TikZ
you could say

.. code-block:: latex

    \begin{tikzpicture}
    \coordinate  (n1) at (-1,1);
    \coordinate  (n2) at (-.5,2);
    \node [draw] at (n1) {here};
    \node [draw] at (n2) {there};
    \end{tikzpicture}

.. image:: ./TikZPix/here_there.png


The "anchor" of the text is placed at the coordinate --- by default the anchor
is the center of the text.  The rectangle around the text is made because
``[draw]`` was specified.  The distance from the text to the middle of the line
that makes the rectangle is the ``inner sep``.  In TikZ the default ``inner sep`` is
``0.3333em``; in Gram it is ``0.1cm`` by default, which is about ``3pt``.  The
following is raw TikZ again, and so the default there is ``0.3333em``.  The gram
default really should not be absolute --- it should depend on the font size (eg
using ``em``), and this can be considered a bug.

.. code-block:: latex

    \begin{tikzpicture} 
    \draw (0cm,6em) node[draw] {default for TikZ}
    (0cm,4em) node[inner sep=5pt,draw] {loose}
    (0,2em) node[inner sep=0pt,draw] {tight}
    (0,0) node[inner sep=0.1cm,draw] {default for gram}; 
    \end{tikzpicture} 

.. image:: ./TikZPix/innerSep.png

Anchors
-------

The anchor is a spot on the text box.  The text is placed such that its anchor
is at the coordinate that is specified.  The default anchor is in the center of
the text.  Alternatively the text might be anchored on the baseline of the text,
or on the periphery (usually a rectangle) of the text box, which need not have
its peripheral shape drawn -- the anchor can be there anyway.  Anchors can be on
one of the four corners of the periphery, or on the top, bottom, left, or right.
These anchors are given compass names, so the anchor at the top of the text box
is ``north``, and the anchor at the left is ``west``, and so on.  Additionally,
there is an anchor on the text baseline, at the west, center, and east.  The
following shows the 12 anchors that are used by Gram.  TikZ has in addition
``mid``, ``mid east``, and ``mid west``, but they are not used in Gram.

Here is the SVG ---

.. image:: ./A_gram/anchors.svg

The GramText class
------------------

GramText inherits from  GramGraphic.

Generally you would make a text box using the Gram ``text()`` method.

You can change various properties of the GramText object, as

``draw``
    By default ``None``, implying ``False``.  For text boxes, it says whether to draw something (limited to a rectangle or circle in Gram --- much more capable and interesting in TikZ) around the text, and if so, what colour to make it --- by default black.  Set to ``True``, ``False``, ``None``, or a colour.

``fill``
    Whether the box is filled.  Specify a colour.

textSize]  Default ``None``, which gives '``normalsize``'.  Set to one of '``tiny``', '``scriptsize``', '``footnotesize``', '``small``', '``normalsize``', '``large``', '``Large``', '``LARGE``', '``huge``', or '``Huge``', or you can delete it.

``textFamily``
    Default ``None``, , implying ``sffamily`` when using Helvetica, and ``rmfamily`` otherwise.    Set to one of '``rmfamily``', '``sffamily``', or '``ttfamily``'. 

``textSeries``
    By default None, implying regular weight font.  You can set it to bold with '``bfseries``', or you can delete it.

``textShape``
    By default None, implying regular upright shape.  You can set it to '``itshape``' for italics, or '``scshape``' for small caps, or you can delete it.

``anchor``
    Default ``None``, which is '``center``'.  Set to one of '``west``', '``north west``', '``north``', '``north east``', '``east``', '``base``', '``base west``', '``base east``', '``south west``', '``south``', '``south east``', or   '``center``'   ('mid', 'mid west', 'mid east' turned off)

``anchorOverRide``
    This is useful to over-ride a programmatically assigned anchor.

``xShift``
    A distance in cm.

``yShift``
    A distance in cm.

``rotate``
    An angle in degrees.  Can be negative.  

``shape``
    By default ``None``, implying '``rectangle``'.  Whether a box or a circle is drawn around the text.  Set to '``circle``' or '``rectangle``'

``lineThickness``
    The thickness of line of the box.  The default is ``None``, which gives '``thin``', 0.4 pt.  You can set it to some number of points, or to one of '``ultra thin``', '``very thin``', '``thin``', '``semithick``', '``thick``', '``very thick``', or '``ultra thick``', which are 0.1, 0.2, 0.4, 0.6, 0.8, 1.2, and 1.6 pt, respectively.  Gram converts these measurements to cm.

``textHeight``
    See the explanation above.  For aligning text in different boxes.

``textDepth``
    See the explanation above.  For aligning text in different boxes.

``textWidth``
    Width of the box.  This allows text wrapping.

``textJustification``
    By default ``None``, implying '``ragged``'.  Set to one of '``justified``', '``ragged``', '``badly ragged``', '``centered``', or '``badly centered``'.

``innerSep``
    The default in Gram is 0.1cm, which is about 3 pt.  1 PostScript point = 0.35277138 mm

Text styles
-----------

The text properties tabulated above can be set for individual GramText objects.
However to set several text box objects all to the same style it is convenient
to define a ``style`` and use it instead.

For example this is done programmatically in TreeGram, where the TreeGram class
has a ``style`` for leaf labels.  In such a case where the ``style`` is
programmatically assigned it is therefore out of your immediate control.  If you
want to then change some or all the the tree leaf text, the simplest way to
over-ride the built-in ``style`` is to simply set all the attributes of the
GramText one by one.  Another way to over-ride a ``style`` is to define a
``myStyle`` and use it.  This is illustrated in the following, where I define two
styles, bunny1 and bunny2, and then make 4 text objects where each is assigned
bunny1 as its ``style``.  I then over-ride that style both ways.

First I define two styles.  GramText is a subclass of GramTikzStyle, and
GramText is appropriate to use to define a style here.

In the following the names of a family of four rabbits are all given the style
``bunny1``.  For the first two, I leave the style as is, for the third
(Cottontail) I over-ride with a ``myStyle``, and for the fourth (Peter) I
over-ride with specific attributes.  In the latter case, you can optionally set
the ``style`` to None to get rid of it completely; in the example given here that
was not done, and so ``bunny1`` remains in the option list for the 'Peter' node.
In other examples, leaving the ``style`` defined might cause problems.  In the
output files the styles are given in a ``tikzset`` command.

.. code-block:: python

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

The resulting ``bunnies.tikz.tex`` file is

.. code-block:: latex

    %% This is a tikz file

    % This file is set up to use 10pt palatino font.
    \tikzset{bunny2/.style={font=\small,darkgray,draw,rotate=45.0,text height=0.223cm,text depth=0.089cm},
    bunny1/.style={font=\scshape,violet,text height=0.248cm,text depth=-0.000cm}}
    \begin{tikzpicture}[inner sep=0.1cm]
    \draw[gray,very thin] (0,-1) grid (4,2);
    \node [bunny1,text height=0.248cm] at (1.000,1.200) {Flopsy};
    \node [bunny1,text height=0.248cm] at (3.000,1.200) {Mopsy};
    \node [bunny2,text height=0.223cm,text depth=0.089cm] at (1.000,0.000) {Cottontail};
    \node [bunny1,font=\Large\itshape,blue!85,draw,fill=cyan!10,anchor=south west,text height=0.348cm,text depth=0.140cm] at (3.000,0.000) {Peter};
    \end{tikzpicture}

.. image:: ./A_gram/Gram/bunnies.png

Unusual text
------------

Using TikZ, you can have text in the form of other LaTeX constructs, including graphics.
Note that these might require using LaTeX packages, and so they will need to be imported.

.. code-block:: python

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

.. image:: ./A_gram/Gram/t1.png

.. image:: ./A_gram/Gram/t2.png

.. image:: ./A_gram/Gram/t3.png

.. image:: ./A_gram/Gram/t3x.png

.. image:: ./A_gram/Gram/t4.png

.. image:: ./A_gram/Gram/t5.png

Text can also be rotated, as shown here.  In this example, the bounding box and anchor are shown, via

::

    gr.showTextBB = True 
    gr.showTextAnchor = True

.. code-block:: python

    from gram import Gram
    gr = Gram()
    gr.baseName = 'rotatedText'
    gr.showTextBB = True
    gr.showTextAnchor = True
    g = gr.text("short", 1,2)
    g.rotate = 30
    g.draw = 'blue'
    g.lineThickness = 'thick'
    g = gr.grid(0,0, 3, 3)
    g = gr.text("Another bit of text.", 2,3)
    g.anchor = 'south west'
    g.rotate = -120
    g.draw = 'cyan'
    gr.pdf()
    gr.svg()

.. image:: ./A_gram/rotatedText.svg

Summary of text attributes
--------------------------

Text sizes 

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

Colours

Set to one of '``red``', '``green``', '``blue``', '``cyan``', '``magenta``', '``yellow``',
                           '``black``', '``gray``', '``white``', '``darkgray``', '``lightgray``',
                           '``brown``', '``orange``', '``purple``', '``violet``', '``lime``', '``olive``', '``pink``', '``teal``'  

This uses the LaTeX ``xcolor`` package, so you can also say, for example '``red!20``' for a light pink, or '``black!10``' for a light gray.

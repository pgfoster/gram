=========
Gram Plot
=========

    :Author: Peter Foster

.. contents::



You probably want better software
---------------------------------

The plots made by gram are very simple.  There's lots better plot making software out there, for example ---

- `R <http://www.r-graph-gallery.com/>`_

- `gnuplot <http://www.gnuplot.info/>`_

- `matplotlib <http://matplotlib.org/>`_

- `pgfplots <http://pgfplots.sourceforge.net/>`_

(On the other hand, if you like simplicity, this may be useful sometimes.)

.. _gram-plot:

The Plot class in the gram package
----------------------------------

The Plot class in the gram package is for making simple line, scatter, and bar
plots.  It tries to make clear plots with a minimum of scripting.

To make a plot, you import Plot from gram, and then make a Plot instance, as

.. code-block:: python

    from gram import Plot
    gp = Plot()


and then call the following methods.  You can call the same method more than once.  


.. table::

    +-------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | ``line(xx, yy, smooth=False)``                  | For making line plots. The lines go from point to point, either jagged or smooth.  The x-value points need not be strictly increasing.  This method only shows the line -- if you want to also show the dots, then superimpose a ``scatter()`` with the same data. |
    +-------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | ``scatter(xx, yy, plotMark='next')``            | For making scatter plots.   This shows the dots.  If you want a line as well, superimpose a ``line()``.                                                                                                                                                            |
    +-------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | ``bars(barNames, counts)``                      | For making bar plots                                                                                                                                                                                                                                               |
    +-------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | ``xYText(x, y, theText)``                       | For placing text at a particular point in the context of a line or scatter plot                                                                                                                                                                                    |
    +-------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | ``barsText(barNum, val, theText)``              | For placing text at a particular point in the context of a bar plot                                                                                                                                                                                                |
    +-------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | ``lineFromSlopeAndIntercept(slope, intercept)`` | For placing a straight line, such as a linear fit or an assymptote, on a line or scatter plot.  If you need to place a curve, generate points for it and use a ``line()``.                                                                                         |
    +-------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | ``verticalLine(x, y=None)``                     | For placing a vertical line on a plot.                                                                                                                                                                                                                             |
    +-------------------------------------------------+--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+



When you call these methods, they return an object, which you will often want to
keep and give a name to so that you can to refer to it in subsequent lines.

.. code-block:: python

    g = gp.line(xx, yy)
    g.color = 'red'
    g = gp.xYText(x, y, theText)
    g.textSize = 'huge'

Simple line and scatter plots
-----------------------------

Lets say that we have some x-y points that we want to plot as a jagged
line plot.  We need the data as separate Python lists, here ``xx1`` and
``yy1``. 

.. code-block:: python

    from gram import Plot
    execfile("data1.py")
    gp = Plot()
    gp.baseName = 'line'
    gp.line(xx1, yy1)
    gp.png()
    gp.svg()

This gives the following, with some default axis titles ---

.. image:: ./C_plots/line.svg


Obviously here we would want to adjust the axes titles, but we also would want to
adjust the range of the x and y axes.  Lets say that we want the
x-axis to start at zero, and we want the y-axis to have an increased
range.  Also, we now think it will look better as a scatter plot
rather than a line plot.

.. code-block:: python

    from gram import Plot
    read("data1.py")
    gp = Plot()
    gp.svgPxForCm = 100
    gp.baseName = 'scatter'
    gp.scatter(xx1, yy1)
    gp.yAxis.title = 'scratches'
    gp.xAxis.title = 'itches'
    gp.minXToShow = 0
    gp.maxXToShow = 12
    gp.minYToShow = 0.
    gp.maxYToShow = 34
    gp.png()
    gp.svg()


.. image:: ./C_plots/scatter.svg

Multiple datasets on a plot
---------------------------

Here is an example imitating one of the figures in the `Wikipedia article on hyperbolas <https://en.wikipedia.org/wiki/Hyperbola>`_.  
It shows a few things ---

- Two datasets, making two curved lines in green; these are then drawn again switching x and y values, making the two blue curves.

- It uses TikZ/PDF/PNG, and so the equations can be nicely typeset.  Such fancy typesetting is awkward in SVG.

- In this example, the ``sig`` of the y-axis is changed from its  default, needlessly forcing the tick labels to  have a single decimal place.

.. code-block:: python

    import math
    xx1 = [x/100. for x in range(-400, 401)]
    yy1a = [math.sqrt(1. + (x * x)) for x in xx1]
    yy1b = [-y for y in yy1a]

    from gram import Plot
    gp = Plot()
    g = gp.line(xx1, yy1a)
    g.colour = 'green'
    g = gp.line(xx1, yy1b)
    g.colour = 'green'

    g = gp.line(yy1a, xx1)
    g.colour = 'blue'
    g = gp.line(yy1b, xx1)
    g.color = 'blue'

    g = gp.line([-4, 4], [-4, 4])
    g.color = 'red'
    g = gp.line([-4, 4], [4, -4])
    g.colour = 'red'

    myTextSize = 'tiny'
    l1 = r'$y^2 + x^2 = 1$'
    g = gp.xYText(-2, 2.5, l1)
    g.anchor = 'west'
    g.textSize = myTextSize

    l1 = r'$x^2 - y^2 = 1$'
    g = gp.xYText(1.5, 1., l1)
    g.anchor = 'west'
    g.textSize = myTextSize

    howBig = 3.5
    gp.contentSizeX = howBig
    gp.contentSizeY = howBig
    gp.xAxis.title = None
    gp.yAxis.title = None
    gp.yAxis.sig = '%.1f'
    gp.baseName = 'hyperbolas'
    gp.png()
    #gp.svg()

.. image:: ./C_plots/Gram/hyperbolas.png


In this next example we want to make a scatter plot from two sets of data (``xx1``, ``yy1``, and
``xx2``, ``yy2``), and for each superimpose a linear regression, each defined
by a slope and intercept (``s1``, ``m1``, and ``s2``, ``m2``).  Both the SVG and PNG figures are shown.  

.. code-block:: python

    from gram import Plot
    read("data3.py")
    gp = Plot()
    gp.baseName = 'scatterB'
    g = gp.scatter(xx1, yy1)
    g.color = 'blue'
    gp.lineFromSlopeAndIntercept(s1, m1)
    g = gp.scatter(xx2, yy2, plotMark='*')
    g.color = "orange"
    g.fill = 'blue!30'
    g = gp.lineFromSlopeAndIntercept(s2, m2)
    g.lineStyle = 'densely dotted'
    g.lineThickness = 'very thick'
    gp.xAxis.title = None
    gp.yAxis.title = None
    gp.minYToShow = 0.0
    gp.maxYToShow = 60.
    gp.png()
    gp.svg()

.. image:: ./C_plots/scatterB.svg

A simple bar plot
-----------------

When doing a bar plot, the data come in the form of a list of bar names, and a
corresponding list of values.  In this example following, the names are in ``xx1``
and the values are in ``yy1``.

.. code-block:: python

    from gram import Plot
    read("data2.py")
    gp = Plot()
    gp.baseName = 'barA'
    gp.bars(xx1, yy1)
    gp.png()
    gp.svg()

This gives the following not very pretty plot ---


.. image:: ./C_plots/barA.svg


This obviously needs adjustment.  We put in a proper bar value axis title.  The
bar name axis is self explanatory, so we set the bar name axis title to be
blank.  We adjust the range of the value axis to something more suitable, as
before.  We swivel the names of the bar names so that they can be read.  After
trying out colour fill in the plot we decide that the default of no fill is best
for this plot.

.. code-block:: python

    from gram import Plot
    read("data2.py")
    gp = Plot()
    gp.baseName = 'barB'
    c = gp.bars(xx1, yy1)
    # c.barSets[0].fillColor = 'violet!20'
    gp.barValAxis.title = 'gnat infestations'
    gp.barNameAxis.title = None
    #gp.barValAxis.position = 'r'
    #gp.barNameAxis.position = 't'
    gp.minBarValToShow = 0.
    gp.maxBarValToShow = 80.
    gp.barNameAxis.textRotate = 44
    # gp.png()
    gp.png()
    gp.svg()

This gives the following ---


.. image:: ./C_plots/barB.svg

More than one data set in a bar plot
------------------------------------

Below we make a bar plot with two sets of numbers.  The bar names are
the same for both.  The bar values are a list of the individual value
lists, so the outer list is the number of bar sets, and each inner
list is as long as the list of bar names.  If we do this

.. code-block:: python

    from gram import Plot
    read("data4.py")

    # Prepare the numbers, using p4.Numbers.  Make the padMin and padMax
    # the same for both data, so that the histo lists are the same size.
    n1 = Numbers(nv1)
    n1.binSize = 1
    n1.histo(verbose=False,padMin=-3, padMax=15.)

    n2 = Numbers(nv2)
    n2.binSize = 1
    n2.histo(verbose=False, padMin=-3, padMax=15.)

    # prepare the binNames, and extract the histo values into separate
    # lists.
    binNames = []
    vals1 = []
    vals2 = []
    for bNum in range(n1.nBins - 1):
        binNames.append('%i' % int(n1.bins[bNum][0]))
        vals1.append(float(n1.bins[bNum][1]))
        vals2.append(float(n2.bins[bNum][1]))
    assert len(binNames) == len(vals1)
    assert len(vals1) == len(vals2)

    gp = Plot()
    gp.baseName = 'twoBarsA'
    gp.bars(binNames, [vals1, vals2])
    gp.barValAxis.title = None
    gp.barNameAxis.title = None
    gp.png()
    gp.svg()

then we get this ---

.. image:: ./C_plots/twoBarsA.svg


We can tweak the axes labels of the plot above by --

.. code-block:: python

    gp.baseName = 'twoBarsB'
    gp.bars(binNames, [vals1, vals2])
    gp.barValAxis.title = None
    gp.barNameAxis.title = None
    gp.maxBarValToShow = 800.
    gp.barNameAxis.barLabelsEvery = 2
    gp.barNameAxis.barLabelsSkipFirst = 1
    gp.barNameAxis.textRotate = 90
    gp.png()
    gp.svg()

then we get better looking axes, 

.. image:: ./C_plots/twoBarsB.svg

The frame and the content box
-----------------------------

There are two boxes, one within the other -- the 'frame', and the 'content'.
The frame is the box that the axes sit on, and on which the lines on the other
two sides of the box are drawn.  The content box does not have a line around it,
and by default is slightly smaller than the frame box.  You can change the size
and position of the boxes by specifying

.. code-block:: python

    gp.contentSizeX  # default 3.5
    gp.contentSizeY  # default 2.65


If you want to make the content box sit tightly against the frame box, you can specify ---

.. code-block:: python

    gp.frameToContent_llx = 0 # default 0.175
    gp.frameToContent_lly = 0 # default 0.175
    gp.frameToContent_urx = 0 # default 0.175
    gp.frameToContent_ury = 0 # default 0.175

Axes
----

The ``xAxis`` and ``yAxis`` are only applicable to line and scatter plots -- bars
have a ``barNameAxis`` and ``barValAxis``.  The ``xAxis`` can be on the top or the
bottom of the frame, and the ``yAxis`` can be on the left or the right.  The
position can be specified by the attribute ``position``, as in ---

.. code-block:: python

    gp.yAxis.position = 'r'  # r for right


The ``barNameAxis`` and the ``barValAxis`` are for bar plots.  The ``barValAxis`` can
be on the left or right, but the ``barNameAxis``, due to lazy programming, can
only be on the bottom.

You can turn off labels, or turn off both ticks and labels, by
setting, for example,

.. code-block:: python

    gp.yAxis.styles.remove('labels') 
    gp.xAxis.styles.remove('ticks')  

When you turn off the ticks, you turn off the labels as well.

You can turn off the frame line for any of the four sides (T, B, L,
R).  For example, to turn off the top and right frame lines, say ---

.. code-block:: python

    tp.frameT = None
    tp.frameR = None


So if we want to turn off everything except the content, we can say ---

.. code-block:: python

    from gram import Plot
    read("data1.py")
    gp = Plot()
    gp.baseName = 'noFrame'
    gp.line(xx1, yy1)
    gp.yAxis.title = None
    gp.xAxis.title = None
    gp.yAxis.styles.remove('ticks')
    gp.xAxis.styles.remove('ticks')
    gp.frameT = None
    gp.frameB = None
    gp.frameL = None
    gp.frameR = None
    gp.png()
    gp.svg()


which makes this SVG ---

.. image:: ./C_plots/noFrame.svg

A line plot and a bar plot in one frame
---------------------------------------

It is possible to superimpose a line plot on a bar plot.  If we just use the defaults, as ---

.. code-block:: python

    from gram import Plot
    read('data5.py')
    gp = Plot()
    gp.baseName = 'lineAndBar_ugly'
    gp.bars(binNames,binVals)
    gp.line(xx1, yy1, smooth=True)
    gp.png()
    gp.svg()

then the results are not pretty, as shown below.


.. image:: ./C_plots/lineAndBar_ugly.svg



If we adjust the axes and axes titles, as ---

.. code-block:: python

    from gram import Plot
    read('data5.py')
    gp = Plot()
    gp.baseName = 'lineAndBar_better'
    c = gp.bars(binNames,binVals)
    c.barSets[0].fillColor = 'black!10'
    gp.minBarValToShow = 0.0
    gp.barNameAxis.title = None
    gp.barValAxis.title = 'frequency'
    gp.barNameAxis.barLabelsEvery = 2

    gp.line(xx1, yy1, smooth=True)
    gp.xAxis.position = 't'
    gp.yAxis.position = 'r'
    gp.xAxis.title = None
    gp.xAxis.tickLabelsEvery = 2
    gp.yAxis.title = 'density'
    gp.png()
    gp.svg() # line plot is not smooth

then the results are better, as shown below, but something is wrong ---


.. image:: ./C_plots/lineAndBar_better.svg

The problem is that the x-axis scale of the line and the bars do not line up.
One solution is to do something like ---

.. code-block:: python

    gp.maxXToShow = 4.0

That makes the x-scale of the line plot and the bar plot commensurate.
Here is the PNG, which does a better job of making smooth lines.

.. image:: ./C_plots/Gram/lineAndBar_good.png

A scatter with a fitted line
----------------------------

In this example there are some x-y data that are plotted as a scatter plot.  A
degree-3 polynomial curve is fitted through the points using R, and the
coefficients are used to generate 101 points for a smooth line.

.. code-block:: python

    from gram import Plot
    read("data6.py")
    read("data6b.py")
    gp = Plot()
    gp.baseName = 'regression'
    gp.scatter(xx1, yy1, plotMark='square')
    g = gp.line(xx2, yy2, smooth=True)
    g.lineThickness = 'thick'
    gp.maxYToShow=100
    gp.minXToShow=-2
    gp.xAxis.title = None
    gp.yAxis.title = None
    gp.png()
    gp.svg()

.. image:: ./C_plots/regression.svg

Plot marks for scatter plots
----------------------------

.. code-block:: python

    from gram import Plot

    markerShapes = ['+', 'x', '*', '-', '|', 'o', 'asterisk',
                    'square', 'square*', 'triangle',
                    'triangle*', 'diamond', 'diamond*']

    gp = Plot()
    gp.baseName = 'plotMarks'
    for mShNum in range(len(markerShapes)):
        xx = [5]
        yy = [len(markerShapes) - mShNum]
        myMarker = markerShapes[mShNum]
        gp.scatter(xx, yy, plotMark=myMarker)
        g = gp.xYText(0, yy[0], myMarker)
        g.textFamily = 'ttfamily'
        g.anchor = 'west'

        xx = [6]
        g = gp.scatter(xx, yy, plotMark=myMarker)
        g.color = 'red'

        xx = [7]
        g = gp.scatter(xx, yy, plotMark=myMarker)
        g.fill = 'red'

        xx = [8]
        g = gp.scatter(xx, yy, plotMark=myMarker)
        g.color = 'blue'
        g.fill = 'yellow'

    gp.line([4.5,8.5], [14, 14])

    colorY = 16
    gp.xYText(3, colorY, "color")
    gp.xYText(5, colorY, "-")
    gp.xYText(6, colorY, "+")
    gp.xYText(7, colorY, "-")
    gp.xYText(8, colorY, "+")

    fillY = 15
    gp.xYText(3, fillY, "fill")
    gp.xYText(5, fillY, "-")
    gp.xYText(6, fillY, "-")
    gp.xYText(7, fillY, "+")
    gp.xYText(8, fillY, "+")



    gp.yAxis.title = None
    gp.xAxis.title = None
    gp.yAxis.styles.remove('ticks')
    gp.xAxis.styles.remove('ticks')
    gp.frameT = None
    gp.frameB = None
    gp.frameL = None
    gp.frameR = None
    gp.contentSizeX = 4.0
    gp.contentSizeY = 7.0
    gp.minXToShow = 0
    gp.maxYToShow = 16

    gp.png()
    gp.svg()

.. image:: ./C_plots/plotMarks.svg

Line styles
-----------

In this example the various line styles are shown.  They are 

::

    None # (the default, which gives 'solid') 
    'solid' 
    'dotted' 
    'densely dotted'
    'loosely dotted' 
    'dashed' 
    'densely dashed' 
    'loosely dashed'

.. code-block:: python

    import math

    upper = int(round(25. * math.pi * 2.))
    rr = [0.04 * r for r in range(upper)]
    xxx = []
    yyy = []
    j = 0
    for rev in range(8):
        xx = []
        yy = []
        for i in range(len(rr)):
            r = rr[i]
            h = 0.0005 * j
            h += 0.5
            j += 1
            pt = func.polar2square([r,h])
            xx.append(pt[0])
            yy.append(pt[1])
        xxx.append(xx)
        yyy.append(yy)

    from gram import Plot
    gp = Plot()
    gp.baseName = 'spiral'
    for rev in range(8):
        xx = xxx[rev]
        yy = yyy[rev]
        g = gp.line(xx,yy,smooth=True)
        g.lineStyle = gp.goodLineStyles[rev]
        print g.lineStyle
    gp.contentSizeX = 4.5
    gp.contentSizeY = gp.contentSizeX
    gp.xAxis.title = None
    gp.yAxis.title = None
    gp.yAxis.styles.remove('ticks') 
    gp.xAxis.styles.remove('ticks') 
    gp.frameT = None
    gp.frameB = None
    gp.frameL = None
    gp.frameR = None
    gp.png()
    gp.svg()

.. image:: ./C_plots/spiral.svg

Text in the plot
----------------

.. code-block:: python

    from gram import Plot
    xx1 = [2,4,7,3,9]
    yy1 = [4,5,1,7,4]
    gp = Plot()
    gp.contentSizeX = 2
    gp.contentSizeY = 1.5
    gp.baseName = 'textInPlot'
    gp.scatter(xx1, yy1, plotMark='asterisk')
    c = gp.xYText(7, 1.2, r'$\Downarrow$')
    c.anchor = 'south'
    c = gp.xYText(3.3, 7,
          r'$\leftarrow$\ Ignore this point')
    c.textSize = 'tiny'
    c.anchor = 'west'
    gp.xAxis.title = None
    gp.yAxis.title = None
    gp.png()
    # gp.svg()  # looks bad, the latex text is not rendered


.. image:: ./C_plots/Gram/textInPlot.png

Lines in the plot
-----------------

.. code-block:: python

    from gram import Plot
    xx1 = [2,4,7,3,9]
    yy1 = [4,5,1,7,4]
    gp = Plot()
    gp.baseName = 'linesInPlot'
    gp.scatter(xx1, yy1, plotMark='diamond')
    gp.minXToShow = 0.0
    g = gp.lineFromSlopeAndIntercept(1, 2)
    g.lineThickness = 'thick'
    gp.verticalLine(x=3, y=4)
    c = gp.verticalLine(8)
    c.colour = 'gray'
    c.lineThickness = 'very thick'
    gp.xAxis.title = None
    gp.yAxis.title = None
    gp.png()
    gp.svg()


.. image:: ./C_plots/Gram/linesInPlot.png

An array of plots
-----------------

You can put a plot in another plot's ``grams``, *eg*

.. code-block:: python

    plot1 = Plot()
    plot2 = Plot()
    plot2.gX = 4.
    plot2.gY = 0.
    plot1.grams.append(plot2)


Here is an example with two plots.  On the plot on the right, the y-axis has been moved over to the right.  On the left plot, the line is ``smooth``; this does not work with SVG, and so the PNG is shown.  The smoothing is done by TikZ, and in this case it looks a bit wonky.

.. code-block:: python

    from gram import Plot

    xx1 = [2.3, 3.5, 7.]
    yy1 = [3.3, 1.2, 5.6]

    xx2 = [-19.3, -14.3, -10.5]
    yy2 = [-2.6, -15.9, -9.3]

    gp = Plot()
    gp.baseName = 'plotArrayB'
    gp.line(xx1, yy1, smooth=True)
    gp.scatter(xx1, yy1)
    gp.yAxis.title = 'widgets'
    gp.xAxis.title = 'time (hours)'
    gp.minXToShow = 0.0

    gp2 = Plot()
    gp2.line(xx2, yy2, smooth=False)
    gp2.scatter(xx2, yy2)
    gp2.yAxis.title = 'spin'
    gp2.yAxis.position = 'r'
    gp2.xAxis.title = 'impetus'
    gp2.gX = 4.3
    gp2.gY = 0.

    gp.grams.append(gp2)
    gp.png()
    gp.svg()  # smooth line plots do not work in svg

.. image:: ./C_plots/Gram/plotArrayB.png



Here is another example.  Here four plots are made, where three are embedded in the first.  You do not need a ``baseName`` for the embedded plots.

.. code-block:: python

    import random
    from gram import Plot
    plotmarks = ['o', 'square',
                 'triangle', 'diamond']
    gg = []
    for i in [0,1]:
        for j in [0,1]:
            xx1 = []
            yy1 = []
            for k in range(23):
                xx1.append(random.random())
                yy1.append(random.random())

            gp = Plot()
            gp.contentSizeX = 2.5
            gp.contentSizeY = 2.
            thePlotMark = plotmarks[(2 * i) +j]
            c = gp.scatter(xx1, yy1,
                           plotMark=thePlotMark)
            gp.minXToShow = 0.0
            gp.minYToShow = 0.0
            gp.maxXToShow = 1.0
            gp.maxYToShow = 1.0
            theText = '[%i.%i]' % (i, j)
            c = gp.xYText(0.5, 0.5, theText)
            c.colour = 'blue'

            if i == 0:
                gp.xAxis.title = None
                gp.xAxis.styles.remove('ticks') 
            else:
                gp.xAxis.title = 'xx1'
            if j == 0:
                gp.yAxis.title = 'yy1'
            else:
                gp.yAxis.title = None
                gp.yAxis.styles.remove('ticks')
            gp.gX = j * 3.2
            gp.gY = i * -2.7
            gg.append(gp)

    gr = gg[0]
    gr.baseName = 'plotArray'
    gr.grams += gg[1:]
    #gr.png()
    gr.svg()

Here is the SVG.  Notice that the inner ticks and axes labels have been removed.

.. image:: ./C_plots/plotArray.svg

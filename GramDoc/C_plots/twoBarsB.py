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

from gram import GramTikzStyle
tzs = GramTikzStyle()
tzs.name = 'foo'
s = tzs.getDefString()
print "s is now '%s'" % s
tzs.innerSep = 0.1
s = tzs.getDefString()
print "s is now '%s'" % s

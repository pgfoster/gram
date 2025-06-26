# I need p4 for p4.Tree, and for a few functions in p4.func
from p4 import func
import os
import math
import string
import sys
import io
from subprocess import Popen, PIPE
import textwrap
import copy
import configparser
from collections import UserDict
import colorsys

# I got these definitions of points from the web somewhere.
# The didot system originated in France but was used in most of Europe.
# 1 didot point = 0.376065 mm
# = 1.07007 pica point
# = 0.0148057 inch
# 1 cicero equals 12 didot points.

# Pica points
# This system was developed in England and is used in Great-Britain and the US.
# 1 pica point = 0.35146 mm
# = 0.93457 didot point
# = 0.013837 inch
# 1 pica equals 12 pica points.

# PostScript points
# When Adobe created PostScript, they added their own system of points. There are exactly 72 PostScript points in 1 inch.
# 1 PostScript point = 0.35277138 mm
# = 1.00375001 pica point
# = 0.01388888 inch

# US Letter paper is 21.59 by 27.94 cm = 612.011 by 792.014 postscript points
# A4 paper is 20.99 by 29.70 cm        = 595.003 by 842.905 postscript
# points (I get 841.905)

# Dvips gives %%BoundingBox: 0 0 596 842 for a4

# I found the following on the web somewhere.  I don't think they are correct, tho.  But I use them anyway.
# Command	Nominal Point Size	Exact Point Size
# \tiny                  5                    5
# \scriptsize            7                    7
# \footnotesize          8                    8
# \small                 9                    9
# \normalsize           10                   10
# \large                12                   12
# \Large                14                   14.40
# \LARGE                18                   17.28
# \huge                 20                   20.74
# \Huge                 24                   24.88

# SVG UNITS
# See here https://pythonhosted.org/svgwrite/overview.html#units
# | unit | identifier description                                                   |
# |------+--------------------------------------------------------------------------|
# | px   | one px unit is defined to be equal to one user unit                      |
# | em   | font-size (actual font height)                                           |
# | ex   | x-height (height of letter x of actual font)                           |
# | pt   | point 1pt equals 1.25px (and therefore 1.25 user units)              |
# | pc   | pica 1pc equals 15px (and therefore 15 user units)                   |
# | mm   | millimeter 1mm would be 3.543307px (3.543307 user units)             |
# | cm   | centimeter 1cm equals 35.43307px (and therefore 35.43307 user units) |
# | in   | inch 1in equals 90px (and therefore 90 user units)                   |

# svg colors, from the svgnames option of the LaTeX xcolor package.
# Duplicate colors: Aqua = Cyan, Fuchsia = Magenta; Navy = NavyBlue; Gray = Grey, DarkGray = DarkGrey, LightGray = LightGrey, SlateGray = SlateGrey, DarkSlateGray = DarkSlateGrey, LightSlateGray = LightSlateGrey, DimGray = DimGrey.
# HTML4 color keyword subset: Aqua, Black, Blue, Fuchsia, Gray, Green, Lime, Maroon, Navy, Olive, Purple, Red, Silver, Teal, White, Yellow.
# Colors taken from Unix/X11: LightGoldenrod, LightSlateBlue, NavyBlue, VioletRed -- these are not in CSS4_COLORS below

validSvgColorNames = ['AliceBlue', 'AntiqueWhite', 'Aqua', 'Aquamarine', 'Azure', 'Beige', 'Bisque', 'Black', 'BlanchedAlmond', 'Blue', 'BlueViolet', 'Brown', 'BurlyWood', 'CadetBlue', 'Chartreuse', 'Chocolate', 'Coral', 'CornflowerBlue', 'Cornsilk', 'Crimson', 'Cyan', 'DarkBlue', 'DarkCyan', 'DarkGoldenrod', 'DarkGray', 'DarkGreen', 'DarkGrey', 'DarkKhaki', 'DarkMagenta', 'DarkOliveGreen', 'DarkOrange', 'DarkOrchid', 'DarkRed', 'DarkSalmon', 'DarkSeaGreen', 'DarkSlateBlue', 'DarkSlateGray', 'DarkSlateGrey', 'DarkTurquoise', 'DarkViolet', 'DeepPink', 'DeepSkyBlue', 'DimGray', 'DimGrey', 'DodgerBlue', 'FireBrick', 'FloralWhite', 'ForestGreen', 'Fuchsia', 'Gainsboro', 'GhostWhite', 'Gold', 'Goldenrod', 'Gray', 'Green', 'GreenYellow', 'Grey', 'Honeydew', 'HotPink', 'IndianRed', 'Indigo', 'Ivory', 'Khaki', 'Lavender', 'LavenderBlush', 'LawnGreen', 'LemonChiffon', 'LightBlue', 'LightCoral', 'LightCyan', 'LightGoldenrod', 'LightGoldenrodYellow', 'LightGray', 'LightGreen', 'LightGrey', 'LightPink', 'LightSalmon', 'LightSeaGreen', 'LightSkyBlue', 'LightSlateBlue', 'LightSlateGray', 'LightSlateGrey', 'LightSteelBlue', 'LightYellow', 'Lime', 'LimeGreen', 'Linen', 'Magenta', 'Maroon', 'MediumAquamarine', 'MediumBlue', 'MediumOrchid', 'MediumPurple', 'MediumSeaGreen', 'MediumSlateBlue', 'MediumSpringGreen', 'MediumTurquoise', 'MediumVioletRed', 'MidnightBlue', 'MintCream', 'MistyRose', 'Moccasin', 'NavajoWhite', 'Navy', 'NavyBlue', 'OldLace', 'Olive', 'OliveDrab', 'Orange', 'OrangeRed', 'Orchid', 'PaleGoldenrod', 'PaleGreen', 'PaleTurquoise', 'PaleVioletRed', 'PapayaWhip', 'PeachPuff', 'Peru', 'Pink', 'Plum', 'PowderBlue', 'Purple', 'Red', 'RosyBrown', 'RoyalBlue', 'SaddleBrown', 'Salmon', 'SandyBrown', 'SeaGreen', 'Seashell', 'Sienna', 'Silver', 'SkyBlue', 'SlateBlue', 'SlateGray', 'SlateGrey', 'Snow', 'SpringGreen', 'SteelBlue', 'Tan', 'Teal', 'Thistle', 'Tomato', 'Turquoise', 'Violet', 'VioletRed', 'Wheat', 'White', 'WhiteSmoke', 'Yellow', 'YellowGreen']

baseColors = ['black',
 'darkgray',
 'blue',
 'gray',
 'brown',
 'green',
 'cyan',
 'lightgray',
 'lime',
 'magenta',
 'olive',
 'orange',
 'pink',
 'purple',
 'red',
 'teal',
 'violet',
 'white',
 'yellow']

# black #000000
# white #FFFFFF
# blue  #0000FF

svgLowColorsNotInCSS4 = ["lightgoldenrod", "lightslateblue", "navyblue", "violetred"]

# From matplotlib.colors module.
# It had lowercase names, and hex values.
# I added rgb values on range zero-1.0, as
# h = v.lstrip("#")
# r,g,b = tuple([int(h[i:i+2], 16)/255. for i in (0, 2, 4)])
CSS4_COLORS = {'aliceblue': ('#F0F8FF', (0.9411764705882353, 0.9725490196078431, 1.0), 'AliceBlue'), 'antiquewhite': ('#FAEBD7', (0.9803921568627451, 0.9215686274509803, 0.8431372549019608), 'AntiqueWhite'), 'aqua': ('#00FFFF', (0.0, 1.0, 1.0), 'Aqua'), 'aquamarine': ('#7FFFD4', (0.4980392156862745, 1.0, 0.8313725490196079), 'Aquamarine'), 'azure': ('#F0FFFF', (0.9411764705882353, 1.0, 1.0), 'Azure'), 'beige': ('#F5F5DC', (0.9607843137254902, 0.9607843137254902, 0.8627450980392157), 'Beige'), 'bisque': ('#FFE4C4', (1.0, 0.8941176470588236, 0.7686274509803922), 'Bisque'), 'black': ('#000000', (0.0, 0.0, 0.0), 'Black'), 'blanchedalmond': ('#FFEBCD', (1.0, 0.9215686274509803, 0.803921568627451), 'BlanchedAlmond'), 'blue': ('#0000FF', (0.0, 0.0, 1.0), 'Blue'), 'blueviolet': ('#8A2BE2', (0.5411764705882353, 0.16862745098039217, 0.8862745098039215), 'BlueViolet'), 'brown': ('#A52A2A', (0.6470588235294118, 0.16470588235294117, 0.16470588235294117), 'Brown'), 'burlywood': ('#DEB887', (0.8705882352941177, 0.7215686274509804, 0.5294117647058824), 'BurlyWood'), 'cadetblue': ('#5F9EA0', (0.37254901960784315, 0.6196078431372549, 0.6274509803921569), 'CadetBlue'), 'chartreuse': ('#7FFF00', (0.4980392156862745, 1.0, 0.0), 'Chartreuse'), 'chocolate': ('#D2691E', (0.8235294117647058, 0.4117647058823529, 0.11764705882352941), 'Chocolate'), 'coral': ('#FF7F50', (1.0, 0.4980392156862745, 0.3137254901960784), 'Coral'), 'cornflowerblue': ('#6495ED', (0.39215686274509803, 0.5843137254901961, 0.9294117647058824), 'CornflowerBlue'), 'cornsilk': ('#FFF8DC', (1.0, 0.9725490196078431, 0.8627450980392157), 'Cornsilk'), 'crimson': ('#DC143C', (0.8627450980392157, 0.0784313725490196, 0.23529411764705882), 'Crimson'), 'cyan': ('#00FFFF', (0.0, 1.0, 1.0), 'Cyan'), 'darkblue': ('#00008B', (0.0, 0.0, 0.5450980392156862), 'DarkBlue'), 'darkcyan': ('#008B8B', (0.0, 0.5450980392156862, 0.5450980392156862), 'DarkCyan'), 'darkgoldenrod': ('#B8860B', (0.7215686274509804, 0.5254901960784314, 0.043137254901960784), 'DarkGoldenrod'), 'darkgray': ('#A9A9A9', (0.6627450980392157, 0.6627450980392157, 0.6627450980392157), 'DarkGray'), 'darkgreen': ('#006400', (0.0, 0.39215686274509803, 0.0), 'DarkGreen'), 'darkgrey': ('#A9A9A9', (0.6627450980392157, 0.6627450980392157, 0.6627450980392157), 'DarkGrey'), 'darkkhaki': ('#BDB76B', (0.7411764705882353, 0.7176470588235294, 0.4196078431372549), 'DarkKhaki'), 'darkmagenta': ('#8B008B', (0.5450980392156862, 0.0, 0.5450980392156862), 'DarkMagenta'), 'darkolivegreen': ('#556B2F', (0.3333333333333333, 0.4196078431372549, 0.1843137254901961), 'DarkOliveGreen'), 'darkorange': ('#FF8C00', (1.0, 0.5490196078431373, 0.0), 'DarkOrange'), 'darkorchid': ('#9932CC', (0.6, 0.19607843137254902, 0.8), 'DarkOrchid'), 'darkred': ('#8B0000', (0.5450980392156862, 0.0, 0.0), 'DarkRed'), 'darksalmon': ('#E9967A', (0.9137254901960784, 0.5882352941176471, 0.47843137254901963), 'DarkSalmon'), 'darkseagreen': ('#8FBC8F', (0.5607843137254902, 0.7372549019607844, 0.5607843137254902), 'DarkSeaGreen'), 'darkslateblue': ('#483D8B', (0.2823529411764706, 0.23921568627450981, 0.5450980392156862), 'DarkSlateBlue'), 'darkslategray': ('#2F4F4F', (0.1843137254901961, 0.30980392156862746, 0.30980392156862746), 'DarkSlateGray'), 'darkslategrey': ('#2F4F4F', (0.1843137254901961, 0.30980392156862746, 0.30980392156862746), 'DarkSlateGrey'), 'darkturquoise': ('#00CED1', (0.0, 0.807843137254902, 0.8196078431372549), 'DarkTurquoise'), 'darkviolet': ('#9400D3', (0.5803921568627451, 0.0, 0.8274509803921568), 'DarkViolet'), 'deeppink': ('#FF1493', (1.0, 0.0784313725490196, 0.5764705882352941), 'DeepPink'), 'deepskyblue': ('#00BFFF', (0.0, 0.7490196078431373, 1.0), 'DeepSkyBlue'), 'dimgray': ('#696969', (0.4117647058823529, 0.4117647058823529, 0.4117647058823529), 'DimGray'), 'dimgrey': ('#696969', (0.4117647058823529, 0.4117647058823529, 0.4117647058823529), 'DimGrey'), 'dodgerblue': ('#1E90FF', (0.11764705882352941, 0.5647058823529412, 1.0), 'DodgerBlue'), 'firebrick': ('#B22222', (0.6980392156862745, 0.13333333333333333, 0.13333333333333333), 'FireBrick'), 'floralwhite': ('#FFFAF0', (1.0, 0.9803921568627451, 0.9411764705882353), 'FloralWhite'), 'forestgreen': ('#228B22', (0.13333333333333333, 0.5450980392156862, 0.13333333333333333), 'ForestGreen'), 'fuchsia': ('#FF00FF', (1.0, 0.0, 1.0), 'Fuchsia'), 'gainsboro': ('#DCDCDC', (0.8627450980392157, 0.8627450980392157, 0.8627450980392157), 'Gainsboro'), 'ghostwhite': ('#F8F8FF', (0.9725490196078431, 0.9725490196078431, 1.0), 'GhostWhite'), 'gold': ('#FFD700', (1.0, 0.8431372549019608, 0.0), 'Gold'), 'goldenrod': ('#DAA520', (0.8549019607843137, 0.6470588235294118, 0.12549019607843137), 'Goldenrod'), 'gray': ('#808080', (0.5019607843137255, 0.5019607843137255, 0.5019607843137255), 'Gray'), 'green': ('#008000', (0.0, 0.5019607843137255, 0.0), 'Green'), 'greenyellow': ('#ADFF2F', (0.6784313725490196, 1.0, 0.1843137254901961), 'GreenYellow'), 'grey': ('#808080', (0.5019607843137255, 0.5019607843137255, 0.5019607843137255), 'Grey'), 'honeydew': ('#F0FFF0', (0.9411764705882353, 1.0, 0.9411764705882353), 'Honeydew'), 'hotpink': ('#FF69B4', (1.0, 0.4117647058823529, 0.7058823529411765), 'HotPink'), 'indianred': ('#CD5C5C', (0.803921568627451, 0.3607843137254902, 0.3607843137254902), 'IndianRed'), 'indigo': ('#4B0082', (0.29411764705882354, 0.0, 0.5098039215686274), 'Indigo'), 'ivory': ('#FFFFF0', (1.0, 1.0, 0.9411764705882353), 'Ivory'), 'khaki': ('#F0E68C', (0.9411764705882353, 0.9019607843137255, 0.5490196078431373), 'Khaki'), 'lavender': ('#E6E6FA', (0.9019607843137255, 0.9019607843137255, 0.9803921568627451), 'Lavender'), 'lavenderblush': ('#FFF0F5', (1.0, 0.9411764705882353, 0.9607843137254902), 'LavenderBlush'), 'lawngreen': ('#7CFC00', (0.48627450980392156, 0.9882352941176471, 0.0), 'LawnGreen'), 'lemonchiffon': ('#FFFACD', (1.0, 0.9803921568627451, 0.803921568627451), 'LemonChiffon'), 'lightblue': ('#ADD8E6', (0.6784313725490196, 0.8470588235294118, 0.9019607843137255), 'LightBlue'), 'lightcoral': ('#F08080', (0.9411764705882353, 0.5019607843137255, 0.5019607843137255), 'LightCoral'), 'lightcyan': ('#E0FFFF', (0.8784313725490196, 1.0, 1.0), 'LightCyan'), 'lightgoldenrodyellow': ('#FAFAD2', (0.9803921568627451, 0.9803921568627451, 0.8235294117647058), 'LightGoldenrodYellow'), 'lightgray': ('#D3D3D3', (0.8274509803921568, 0.8274509803921568, 0.8274509803921568), 'LightGray'), 'lightgreen': ('#90EE90', (0.5647058823529412, 0.9333333333333333, 0.5647058823529412), 'LightGreen'), 'lightgrey': ('#D3D3D3', (0.8274509803921568, 0.8274509803921568, 0.8274509803921568), 'LightGrey'), 'lightpink': ('#FFB6C1', (1.0, 0.7137254901960784, 0.7568627450980392), 'LightPink'), 'lightsalmon': ('#FFA07A', (1.0, 0.6274509803921569, 0.47843137254901963), 'LightSalmon'), 'lightseagreen': ('#20B2AA', (0.12549019607843137, 0.6980392156862745, 0.6666666666666666), 'LightSeaGreen'), 'lightskyblue': ('#87CEFA', (0.5294117647058824, 0.807843137254902, 0.9803921568627451), 'LightSkyBlue'), 'lightslategray': ('#778899', (0.4666666666666667, 0.5333333333333333, 0.6), 'LightSlateGray'), 'lightslategrey': ('#778899', (0.4666666666666667, 0.5333333333333333, 0.6), 'LightSlateGrey'), 'lightsteelblue': ('#B0C4DE', (0.6901960784313725, 0.7686274509803922, 0.8705882352941177), 'LightSteelBlue'), 'lightyellow': ('#FFFFE0', (1.0, 1.0, 0.8784313725490196), 'LightYellow'), 'lime': ('#00FF00', (0.0, 1.0, 0.0), 'Lime'), 'limegreen': ('#32CD32', (0.19607843137254902, 0.803921568627451, 0.19607843137254902), 'LimeGreen'), 'linen': ('#FAF0E6', (0.9803921568627451, 0.9411764705882353, 0.9019607843137255), 'Linen'), 'magenta': ('#FF00FF', (1.0, 0.0, 1.0), 'Magenta'), 'maroon': ('#800000', (0.5019607843137255, 0.0, 0.0), 'Maroon'), 'mediumaquamarine': ('#66CDAA', (0.4, 0.803921568627451, 0.6666666666666666), 'MediumAquamarine'), 'mediumblue': ('#0000CD', (0.0, 0.0, 0.803921568627451), 'MediumBlue'), 'mediumorchid': ('#BA55D3', (0.7294117647058823, 0.3333333333333333, 0.8274509803921568), 'MediumOrchid'), 'mediumpurple': ('#9370DB', (0.5764705882352941, 0.4392156862745098, 0.8588235294117647), 'MediumPurple'), 'mediumseagreen': ('#3CB371', (0.23529411764705882, 0.7019607843137254, 0.44313725490196076), 'MediumSeaGreen'), 'mediumslateblue': ('#7B68EE', (0.4823529411764706, 0.40784313725490196, 0.9333333333333333), 'MediumSlateBlue'), 'mediumspringgreen': ('#00FA9A', (0.0, 0.9803921568627451, 0.6039215686274509), 'MediumSpringGreen'), 'mediumturquoise': ('#48D1CC', (0.2823529411764706, 0.8196078431372549, 0.8), 'MediumTurquoise'), 'mediumvioletred': ('#C71585', (0.7803921568627451, 0.08235294117647059, 0.5215686274509804), 'MediumVioletRed'), 'midnightblue': ('#191970', (0.09803921568627451, 0.09803921568627451, 0.4392156862745098), 'MidnightBlue'), 'mintcream': ('#F5FFFA', (0.9607843137254902, 1.0, 0.9803921568627451), 'MintCream'), 'mistyrose': ('#FFE4E1', (1.0, 0.8941176470588236, 0.8823529411764706), 'MistyRose'), 'moccasin': ('#FFE4B5', (1.0, 0.8941176470588236, 0.7098039215686275), 'Moccasin'), 'navajowhite': ('#FFDEAD', (1.0, 0.8705882352941177, 0.6784313725490196), 'NavajoWhite'), 'navy': ('#000080', (0.0, 0.0, 0.5019607843137255), 'Navy'), 'oldlace': ('#FDF5E6', (0.9921568627450981, 0.9607843137254902, 0.9019607843137255), 'OldLace'), 'olive': ('#808000', (0.5019607843137255, 0.5019607843137255, 0.0), 'Olive'), 'olivedrab': ('#6B8E23', (0.4196078431372549, 0.5568627450980392, 0.13725490196078433), 'OliveDrab'), 'orange': ('#FFA500', (1.0, 0.6470588235294118, 0.0), 'Orange'), 'orangered': ('#FF4500', (1.0, 0.27058823529411763, 0.0), 'OrangeRed'), 'orchid': ('#DA70D6', (0.8549019607843137, 0.4392156862745098, 0.8392156862745098), 'Orchid'), 'palegoldenrod': ('#EEE8AA', (0.9333333333333333, 0.9098039215686274, 0.6666666666666666), 'PaleGoldenrod'), 'palegreen': ('#98FB98', (0.596078431372549, 0.984313725490196, 0.596078431372549), 'PaleGreen'), 'paleturquoise': ('#AFEEEE', (0.6862745098039216, 0.9333333333333333, 0.9333333333333333), 'PaleTurquoise'), 'palevioletred': ('#DB7093', (0.8588235294117647, 0.4392156862745098, 0.5764705882352941), 'PaleVioletRed'), 'papayawhip': ('#FFEFD5', (1.0, 0.9372549019607843, 0.8352941176470589), 'PapayaWhip'), 'peachpuff': ('#FFDAB9', (1.0, 0.8549019607843137, 0.7254901960784313), 'PeachPuff'), 'peru': ('#CD853F', (0.803921568627451, 0.5215686274509804, 0.24705882352941178), 'Peru'), 'pink': ('#FFC0CB', (1.0, 0.7529411764705882, 0.796078431372549), 'Pink'), 'plum': ('#DDA0DD', (0.8666666666666667, 0.6274509803921569, 0.8666666666666667), 'Plum'), 'powderblue': ('#B0E0E6', (0.6901960784313725, 0.8784313725490196, 0.9019607843137255), 'PowderBlue'), 'purple': ('#800080', (0.5019607843137255, 0.0, 0.5019607843137255), 'Purple'), 'rebeccapurple': ('#663399', (0.4, 0.2, 0.6), 'NO_VALID_SVG_NAME'), 'red': ('#FF0000', (1.0, 0.0, 0.0), 'Red'), 'rosybrown': ('#BC8F8F', (0.7372549019607844, 0.5607843137254902, 0.5607843137254902), 'RosyBrown'), 'royalblue': ('#4169E1', (0.2549019607843137, 0.4117647058823529, 0.8823529411764706), 'RoyalBlue'), 'saddlebrown': ('#8B4513', (0.5450980392156862, 0.27058823529411763, 0.07450980392156863), 'SaddleBrown'), 'salmon': ('#FA8072', (0.9803921568627451, 0.5019607843137255, 0.4470588235294118), 'Salmon'), 'sandybrown': ('#F4A460', (0.9568627450980393, 0.6431372549019608, 0.3764705882352941), 'SandyBrown'), 'seagreen': ('#2E8B57', (0.1803921568627451, 0.5450980392156862, 0.3411764705882353), 'SeaGreen'), 'seashell': ('#FFF5EE', (1.0, 0.9607843137254902, 0.9333333333333333), 'Seashell'), 'sienna': ('#A0522D', (0.6274509803921569, 0.3215686274509804, 0.17647058823529413), 'Sienna'), 'silver': ('#C0C0C0', (0.7529411764705882, 0.7529411764705882, 0.7529411764705882), 'Silver'), 'skyblue': ('#87CEEB', (0.5294117647058824, 0.807843137254902, 0.9215686274509803), 'SkyBlue'), 'slateblue': ('#6A5ACD', (0.41568627450980394, 0.35294117647058826, 0.803921568627451), 'SlateBlue'), 'slategray': ('#708090', (0.4392156862745098, 0.5019607843137255, 0.5647058823529412), 'SlateGray'), 'slategrey': ('#708090', (0.4392156862745098, 0.5019607843137255, 0.5647058823529412), 'SlateGrey'), 'snow': ('#FFFAFA', (1.0, 0.9803921568627451, 0.9803921568627451), 'Snow'), 'springgreen': ('#00FF7F', (0.0, 1.0, 0.4980392156862745), 'SpringGreen'), 'steelblue': ('#4682B4', (0.27450980392156865, 0.5098039215686274, 0.7058823529411765), 'SteelBlue'), 'tan': ('#D2B48C', (0.8235294117647058, 0.7058823529411765, 0.5490196078431373), 'Tan'), 'teal': ('#008080', (0.0, 0.5019607843137255, 0.5019607843137255), 'Teal'), 'thistle': ('#D8BFD8', (0.8470588235294118, 0.7490196078431373, 0.8470588235294118), 'Thistle'), 'tomato': ('#FF6347', (1.0, 0.38823529411764707, 0.2784313725490196), 'Tomato'), 'turquoise': ('#40E0D0', (0.25098039215686274, 0.8784313725490196, 0.8156862745098039), 'Turquoise'), 'violet': ('#EE82EE', (0.9333333333333333, 0.5098039215686274, 0.9333333333333333), 'Violet'), 'wheat': ('#F5DEB3', (0.9607843137254902, 0.8705882352941177, 0.7019607843137254), 'Wheat'), 'white': ('#FFFFFF', (1.0, 1.0, 1.0), 'White'), 'whitesmoke': ('#F5F5F5', (0.9607843137254902, 0.9607843137254902, 0.9607843137254902), 'WhiteSmoke'), 'yellow': ('#FFFF00', (1.0, 1.0, 0.0), 'Yellow'), 'yellowgreen': ('#9ACD32', (0.6039215686274509, 0.803921568627451, 0.19607843137254902), 'YellowGreen')}


def cmForLineThickness(lt):
    pts = ptsForLineThickness(lt)
    cmPerPt = 0.035277138
    cm = pts * cmPerPt
    return cm


def ptsForLineThickness(lt):
    if lt is None:  # assume 'thin'
        pts = 0.4
    elif isinstance(lt, str):
        if lt == 'ultra thin':
            pts = 0.1
        elif lt == 'very thin':
            pts = 0.2
        elif lt == 'thin':
            pts = 0.4
        elif lt == 'semithick':
            pts = 0.6
        elif lt == 'thick':
            pts = 0.8
        elif lt == 'very thick':
            pts = 1.2
        elif lt == 'ultra thick':
            pts = 1.6
        else:
            raise GramError(
                "cmForLineThickness(), unknown string thickness %s" % lt)
    else:
        try:
            pts = float(lt)
        except ValueError:
            raise GramError(
                "cmForLineThickness(), unknown non-string thickness %s" % lt)
    assert pts
    return pts


def bbOverlap(bb1, bb2):
    # print "      bb1  %.1f %.1f %.1f %.1f" % tuple(bb1)
    # print "      bb2  %.1f %.1f %.1f %.1f" % tuple(bb2)

    bl1 = (bb1[0], bb1[1])
    tl1 = (bb1[0], bb1[3])
    br1 = (bb1[2], bb1[1])
    tr1 = (bb1[2], bb1[3])
    bl2 = (bb2[0], bb2[1])
    tl2 = (bb2[0], bb2[3])
    br2 = (bb2[2], bb2[1])
    tr2 = (bb2[2], bb2[3])
    for corner in [bl1, tl1, br1, tr1]:
        if isInside(corner, bb2):
            return True
    for corner in [bl2, tl2, br2, tr2]:
        if isInside(corner, bb1):
            return True


def isInside(point, bb):
    if point[0] > bb[0] and point[0] < bb[2] and point[1] > bb[1] and point[1] < bb[3]:
        return True

def svgDasharrayForLinestyle(theLS):
    if theLS in [None, 'solid']:
        return None
    elif theLS == 'dotted':
        return "2 4"
    elif theLS == 'densely dotted':
        return "2 2"
    elif theLS == 'loosely dotted':
        return "2 8"
    elif theLS == 'dashed':
        return "10 8"
    elif theLS == "densely dashed":
        return "10 4"
    elif theLS == "loosely dashed":
        return "10 16"

def writeInColour(theString, colour='blue'):
    goodColours = [
        'red', 'RED', 'blue', 'BLUE', 'cyan', 'CYAN', 'violet', 'VIOLET']
    if colour not in goodColours:
        raise P4Error(
            "func.printColour().  The colour should be one of %s" % goodColours)
    codeDict = {
        'red': '\033[0;31m',
        'RED': '\033[1;31m',
        'blue': '\033[0;34m',
        'BLUE': '\033[1;34m',
        'cyan': '\033[0;36m',
        'CYAN': '\033[1;36m',
        'violet': '\033[0;35m',
        'VIOLET': '\033[1;35m',
    }
    backToBlackCode = '\033[m'
    sys.stdout.write("%s%s%s" % (codeDict[colour], theString, backToBlackCode))


def setTerminalColour(theColour):
    goodTerminalColours = [
        'red', 'RED', 'blue', 'BLUE', 'cyan', 'CYAN', 'violet', 'VIOLET']
    terminalColourCodeDict = {
        'red': '\033[0;31m',
        'RED': '\033[1;31m',
        'blue': '\033[0;34m',
        'BLUE': '\033[1;34m',
        'cyan': '\033[0;36m',
        'CYAN': '\033[1;36m',
        'violet': '\033[0;35m',
        'VIOLET': '\033[1;35m',
    }
    #self.terminalBackToBlackCode = '\033[m'

    assert theColour in goodTerminalColours, "The colour must be one of %s" % goodTerminalColours
    sys.stdout.write(terminalColourCodeDict[theColour])


def unsetTerminalColour():
    sys.stdout.write('\033[m')

# Color and colour.
writeInColor = writeInColour
setTerminalColor = setTerminalColour
unsetTerminalColor = unsetTerminalColour

def fixUnderscores(theText):
    """Check and fix underscores.

    Semi-smart in knowing math mode.  It can distinguish "x_y" from "$x_y$".

    It is too stupid to know other kinds of math mode.
    """

    #raise GramError
    fixed = []
    isEscaped = False
    inMaths = False

    for c in theText:
        #print(f"fixUnderscores --- theText={theText} |{c}|")
        if c == "$":
            if isEscaped:
                pass
            elif not inMaths:
                inMaths = True
            elif inMaths:
                inMaths = False
            fixed.append(c)

        elif c == "_":
            if inMaths:
                fixed.append(c)
            elif isEscaped:
                fixed.append(c)
            else:
                writeInColour(f"fixUnderscores({theText}) Underscore not escaped -- adding backslash\n", colour="CYAN")
                fixed.append("\\" + c)
        elif c.startswith("\\"):
            if isEscaped:           # ie \\
                isEscaped = False
            elif inMaths:
                pass
            else:
                isEscaped = True
            fixed.append(c)
            continue
        else:
            if isEscaped:
                # print(r"Got escaped char %s not in maths." % c)
                pass
            fixed.append(c)
        isEscaped = False
    return "".join(fixed)

class GDict(UserDict):
    def dump(self):
        kk = self.keys()
        for k in kk:
            g = self[k]
            clas = ""
            if isinstance(g, GramText):
                clas = "GramText"
                print(f"  {k:10} {clas:12} {g.rawText[:30]}")
            else:
                print(f"  {k:10}")



###################################################################

class Gram(object):

    _font = 'helvetica'
    # _defaultTextFamily = None #  'sffamily'  rmfamily ttfamily; appears to be not required or used
    _engine = 'tikz'  # or 'svg'
    _documentFontSize = 10   # 10, 11, or 12
    _pdfViewer = 'ls'
    _pngViewer = 'ls'
    _svgViewer = 'ls'
    _pngResolution = 300       # was 140

    _config = None
    _configAttrs = """font documentFontSize pdfViewer pngViewer svgViewer
                              pngResolution svgPxForCm svgTextNormalWeight""".split()

    _goodLineThicknesses = [
        'ultra thin', 'very thin', 'thin', 'semithick', 'thick', 'very thick', 'ultra thick']
    _goodTextFamilies = ['rmfamily', 'sffamily', 'ttfamily']
    _goodTextSeries = ['bfseries', 'mdseries']
    _goodTextShapes = ['itshape', 'scshape', "upshape"]   # plus "slshape"?
    _goodTextSizes = ['tiny', 'scriptsize', 'footnotesize', 'small', 'normalsize', 'large',
                      'Large', 'LARGE', 'huge', 'Huge']

    _goodAnchors = ['west', 'north west', 'north', 'north east', 'east',
                    'base', 'base west', 'base east',
                    'mid', 'mid west', 'mid east',
                    'south west', 'south', 'south east',
                    'center']  # center is the default

    #_goodShapes = ['rounded rectangle']
    _goodLineStyles = [None, 'solid', 'dotted', 'densely dotted', 'loosely dotted',
                       'dashed', 'densely dashed', 'loosely dashed']

    _goodTextAligns = [None, 'left', 'flush left', 'right', 'flush right',
                       'center', 'flush center', 'justify', 'none']
    _styleDict = {}
    _tikzPictureDefaults = None
    _htmlColorDict = {}
    _svgTextMetricsUses = "inkscape"  # inkscape or "rsvg"


    _useTikzPlotMarkLib = False
    _xRecenter = 1.
    _yRecenter = 1.
    _recenterExtra = 0.1

    _showTextBB = False
    _showTextAnchor = False
    _latexOutputGoesToDevNull = True

    _svgPxForCm = 55.  # 70.86614  # 35.43307
    #_svgTextNormalsize = 0.34
    _svgTextNormalsize = 0.36      # estimate
    _defaultInnerSep = None
    _gIdCounter = 1
    _gForGIdDict = GDict()
    _svgHackDoRotate = False
    _svgHack_x_Only = False
    _svgNormalsize_x = None
    _svgTextNormalWeight = "normal"
    _svgTextPreserveWhitespace = False # True adds xml:space="preserve" to a text


    def __init__(self):
        self._dirName = 'Gram'
        self._baseName = 'gram'
        self.latexUsePackages = []
        self.latexOtherPreambleCommands = []
        self.bbb = [0.0] * 4  # big bounding box, ie of the whole gram
        self.useSfMathIfSffamily = True      # sometimes roman math is wanted

        self.graphics = []
        self.grams = []
        self.gX = 0.0  # the xShift of an included gram
        self.gY = 0.0  # the yShift

        self.theGpdf = None
        self.latexMetricsFileName = "grOut.txt"

        if not Gram._config:
            #config = configparser.SafeConfigParser()
            config = configparser.ConfigParser()
            Gram._config = config
            config.optionxform = str
            filesRead = config.read([os.path.expanduser('~/.gram.conf'), 'gram.conf'])
            if filesRead:
                writeInColor("... read conf files %s\n" % filesRead)
                theSections = config.sections()
                if theSections:
                    assert len(theSections) == 1
                    assert theSections[0] == 'Gram'

                    # theOpts = config.options('Gram')
                    # for anOpt in theOpts:
                    #     ret = config.get('Gram', anOpt)
                    #     print anOpt, ret, type(ret)

                    for myAttr in self.configAttrs:
                        try:
                            ret = config.get('Gram', myAttr)
                            if ret:
                                if myAttr in "documentFontSize pngResolution svgTextNormalWeight".split():
                                    try:
                                        ret = int(ret)
                                    except ValueError:
                                        raise GramError("Bad value '%s' for '%s' in conf file." %\
                                                        (ret, myAttr))
                                writeInColor("conf file: Setting Gram %s to %s" % (myAttr, ret)) # no \n
                                sys.stdout.flush()   # Get rid of the colour
                                print()                # line ending, finally
                                setattr(self, myAttr, ret)
                        except configparser.NoOptionError:
                            pass



    def _getDirName(self):
        return self._dirName

    def _setDirName(self, theDirName):
        gm = ['Gram._setDirName()']
        assert isinstance(theDirName, str)
        if ' ' in theDirName:
            gm.append("The dirName should not have any spaces.")
            raise GramError(gm)
        self._dirName = theDirName

    def _delDirName(self):
        gm = ['Gram._delDirName()']
        gm.append(
            "Caught an attempt to delete self.dirName-- Set it to something else, but don't delete it, ok?")
        raise GramError(gm)

    dirName = property(_getDirName, _setDirName, _delDirName)

    def _getBaseName(self):
        return self._baseName

    def _setBaseName(self, theBaseName):
        gm = ['Gram._setBaseName()']
        assert isinstance(theBaseName, str)
        if ' ' in theBaseName:
            gm.append("The baseName should not have any spaces.")
            raise GramError(gm)
        self._baseName = theBaseName

    def _delBaseName(self):
        gm = ['Gram._delBaseName()']
        gm.append(
            "Caught an attempt to delete self.baseName-- Set it to something else, but don't delete it, ok?")
        raise GramError(gm)

    baseName = property(_getBaseName, _setBaseName, _delBaseName)

    def _getFont(self):
        return Gram._font
    def _setFont(self, theFont):
        gm = ['Gram._setFont()']
        assert isinstance(theFont, str)
        lowFont = theFont.lower()
        goodFonts = ['lmr', 'lms', 'helvetica', 'palatino', 'times', "fira"]
        if lowFont not in goodFonts:
            gm.append("You can only set property 'font' to one of")
            gm.append("%s" % goodFonts)
            gm.append("Got attempt to set to '%s'" % theFont)
            raise GramError(gm)
        Gram._font = lowFont

    def _delFont(self):
        gm = ['Gram._delFont()']
        gm.append("Caught an attempt to delete self.font-- don't do that.")
        raise GramError(gm)
    font = property(_getFont, _setFont, _delFont)

    # def _getDefaultTextFamily(self):
    #     return Gram._defaultTextFamily
    # def _setDefaultTextFamily(self, theDefaultTextFamily):
    #     gm = ['Gram.defaultTextFamily']
    #     gm.append("Gram.defaultTextFamily is set by the font, not user-settable")
    #     raise Gram.error(gm)
    # defaultTextFamily = property(_getDefaultTextFamily, _setDefaultTextFamily)

    def _getEngine(self):
        return Gram._engine
    def _setEngine(self, theEngine):
        engines = ['tikz', 'svg']
        if theEngine not in engines:
            gm = ['Gram._setEngine()']
            gm.append("engine should be one of %s" % engines)
            raise GramError(gm)
        Gram._engine = theEngine
    def _delEngine(self):
        gm = ['Gram._delEngine()']
        gm.append("Caught an attempt to delete self.engine -- don't do that.")
        raise GramError(gm)
    engine = property(_getEngine, _setEngine, _delEngine)

    def _getDocumentFontSize(self):
        return Gram._documentFontSize
    def _setDocumentFontSize(self, theDocumentFontSize):
        gm = ['Gram._setDocumentFontSize()']
        gm.append('The documentFontSize should be an integer, 10-12')
        if not isinstance(theDocumentFontSize, int):
            raise GramError(gm)
        if theDocumentFontSize < 10 or theDocumentFontSize > 12:
            gm.append(f"Got attempt to set to {theDocumentFontSize}")
            raise GramError(gm)
        Gram._documentFontSize = theDocumentFontSize
    documentFontSize = property(_getDocumentFontSize, _setDocumentFontSize)

    def _getPdfViewer(self):
        return Gram._pdfViewer
    def _setPdfViewer(self, thePdfViewer):
        Gram._pdfViewer = thePdfViewer
    pdfViewer = property(_getPdfViewer, _setPdfViewer)

    def _getPngViewer(self):
        return Gram._pngViewer
    def _setPngViewer(self, thePngViewer):
        Gram._pngViewer = thePngViewer
    pngViewer = property(_getPngViewer, _setPngViewer)

    def _getSvgViewer(self):
        return Gram._svgViewer
    def _setSvgViewer(self, theSvgViewer):
        Gram._svgViewer = theSvgViewer
    svgViewer = property(_getSvgViewer, _setSvgViewer)

    def _getPngResolution(self):
        return Gram._pngResolution
    def _setPngResolution(self, thePngResolution):
        Gram._pngResolution = int(thePngResolution)
    pngResolution = property(_getPngResolution, _setPngResolution)

    def _getConfigAttrs(self):
        return Gram._configAttrs
    configAttrs = property(_getConfigAttrs)

    def _getGoodTextFamilies(self):
        return Gram._goodTextFamilies
    goodTextFamilies = property(_getGoodTextFamilies)

    def _getGoodTextSeries(self):
        return Gram._goodTextSeries
    goodTextSeries = property(_getGoodTextSeries)

    def _getGoodTextShapes(self):
        return Gram._goodTextShapes
    goodTextShapes = property(_getGoodTextShapes)

    def _getGoodTextSizes(self):
        return Gram._goodTextSizes
    goodTextSizes = property(_getGoodTextSizes)

    def _getGoodAnchors(self):
        return Gram._goodAnchors
    goodAnchors = property(_getGoodAnchors)

    def _getGoodLineStyles(self):
        return Gram._goodLineStyles
    goodLineStyles = property(_getGoodLineStyles)

    def _getStyleDict(self):
        return Gram._styleDict

    def _setStyleDict(self, newVal):
        raise GramError("Don't set styleDict, just modify it.")
    styleDict = property(_getStyleDict, _setStyleDict)

    def _getTikzPictureDefaults(self):
        if not Gram._tikzPictureDefaults:
            Gram._tikzPictureDefaults = GramTikzStyle()
            Gram._tikzPictureDefaults.name = 'tikzPictureDefaults'
        return Gram._tikzPictureDefaults

    def _setTikzPictureDefaults(self, newVal):
        Gram._tikzPictureDefaults = newVal
    tikzPictureDefaults = property(
        _getTikzPictureDefaults, _setTikzPictureDefaults)

    def _getHtmlColorDict(self):
        return Gram._htmlColorDict

    def _setHtmlColorDict(self, newVal):
        raise GramError("Don't set htmlColorDict, just modify it.")
    htmlColorDict = property(_getHtmlColorDict, _setHtmlColorDict)


    def _getSvgTextMetricsUses(self):
        return Gram._svgTextMetricsUses

    def _setSvgTextMetricsUses(self, newVal):
        if newVal in ["inkscape", "rsvg"]:
            Gram._svgTextMetricsUses = newVal
        else:
            raise GramError("Set svgTextMetricsUses to inkscape or rsvg, only (got %s)" % newVal)
    svgTextMetricsUses = property(_getSvgTextMetricsUses, _setSvgTextMetricsUses)

    def _getDefaultInnerSep(self):
        if Gram._defaultInnerSep is not None:  # ie it has been set by the user, eg to 0.0
            return Gram._defaultInnerSep
        else:
            if Gram._engine == "tikz":
                cmPerPt = 0.035277138
                myDocumentFontSize = self.documentFontSize  # pts
                myDocumentFontSize *= cmPerPt
                return myDocumentFontSize * 0.3333
            else:
                return self.svgTextNormalsize * 0.3333  # cm

    def _setDefaultInnerSep(self, newVal):
        try:
            nV = float(newVal)
            Gram._defaultInnerSep = nV
        except ValueError:
            raise GramError(
                "_setDefaultInnerSep().  newVal should be a float.")
        assert Gram._defaultInnerSep >= 0.0
    defaultInnerSep = property(_getDefaultInnerSep, _setDefaultInnerSep)

    def _getUseTikzPlotMarkLib(self):
        return Gram._useTikzPlotMarkLib

    def _setUseTikzPlotMarkLib(self, newVal):
        if newVal in [True, False]:
            Gram._useTikzPlotMarkLib = newVal
        else:
            raise GramError(
                "Set useTikzPlotMarkLib to True or False, only (got %s)" % newVal)
    useTikzPlotMarkLib = property(
        _getUseTikzPlotMarkLib, _setUseTikzPlotMarkLib)


    def _get_xRecenter(self):
        return Gram._xRecenter

    def _set_xRecenter(self, newVal):
        try:
            nV = float(newVal)
        except ValueError:
            raise GramError("_set_xRecenter().  newVal should be a float.")
        Gram._xRecenter = nV
    xRecenter = property(_get_xRecenter, _set_xRecenter)

    def _get_yRecenter(self):
        return Gram._yRecenter

    def _set_yRecenter(self, newVal):
        try:
            nV = float(newVal)
        except ValueError:
            raise GramError("_set_yRecenter().  newVal should be a float.")
        # print "Gram setting class var yRecenter to %.2f" % nV
        Gram._yRecenter = nV
    yRecenter = property(_get_yRecenter, _set_yRecenter)

    def _get_recenterExtra(self):
        return Gram._recenterExtra

    def _set_recenterExtra(self, newVal):
        try:
            nV = float(newVal)
        except ValueError:
            raise GramError("_set_recenterExtra().  newVal should be a float.")
        Gram._recenterExtra = nV
    recenterExtra = property(_get_recenterExtra, _set_recenterExtra)

    def _get_showTextBB(self):
        return Gram._showTextBB

    def _set_showTextBB(self, newVal):
        Gram._showTextBB = newVal
    showTextBB = property(_get_showTextBB, _set_showTextBB)

    def _get_showTextAnchor(self):
        return Gram._showTextAnchor

    def _set_showTextAnchor(self, newVal):
        Gram._showTextAnchor = newVal
    showTextAnchor = property(_get_showTextAnchor, _set_showTextAnchor)

    def _get_latexOutputGoesToDevNull(self):
        return Gram._latexOutputGoesToDevNull

    def _set_latexOutputGoesToDevNull(self, newVal):
        Gram._latexOutputGoesToDevNull = newVal
    latexOutputGoesToDevNull = property(
        _get_latexOutputGoesToDevNull, _set_latexOutputGoesToDevNull)

    def _get_svgPxForCm(self):
        return Gram._svgPxForCm

    def _set_svgPxForCm(self, newVal):
        Gram._svgPxForCm = float(newVal)
    svgPxForCm = property(_get_svgPxForCm, _set_svgPxForCm)

    def _get_svgTextNormalsize(self):
        return Gram._svgTextNormalsize

    def _set_svgTextNormalsize(self, newVal):
        Gram._svgTextNormalsize = float(newVal)
    svgTextNormalsize = property(
        _get_svgTextNormalsize, _set_svgTextNormalsize)

    def _get_gIdCounter(self):
        return Gram._gIdCounter

    def _set_gIdCounter(self, newVal):
        Gram._gIdCounter = int(newVal)
    gIdCounter = property(_get_gIdCounter, _set_gIdCounter)

    def _get_gForGIdDict(self):
        return Gram._gForGIdDict

    def _set_gForGIdDict(self, newVal):
        raise GramError("Don't set gForGIdDict, just read it.")
    gForGIdDict = property(_get_gForGIdDict, _set_gForGIdDict)

    def _get_svgTextNormalWeight(self):
        return Gram._svgTextNormalWeight

    def _set_svgTextNormalWeight(self, newVal):
        goodTextVals = ["normal", "bold", "light"]
        try:
            Gram._svgTextNormalWeight = int(newVal)
        except ValueError:
            assert newVal in goodTextVals, "weight as a string should be one of %s" % goodTextVals
            Gram._svgTextNormalWeight = newVal

    svgTextNormalWeight = property(_get_svgTextNormalWeight, _set_svgTextNormalWeight)

    def _get_svgTextPreserveWhitespace(self):
        return Gram._svgTextPreserveWhitespace

    def _set_svgTextPreserveWhitespace(self, newVal):
        if newVal in [True, False]:
            Gram._svgTextPreserveWhitespace = newVal
        else:
            raise GramError(
                "Set svgTextPreserveWhitespace to True or False, only (got %s)" % newVal)

    svgTextPreserveWhitespace = property(_get_svgTextPreserveWhitespace, _set_svgTextPreserveWhitespace)


    ##################################

    def setPositionsBeforeTextMetrics(self):
        for g in self.graphics:
            g.setPositionsBeforeTextMetrics()
        for gr in self.grams:
            gr.setPositionsBeforeTextMetrics()

    def setPositions(self):
        if self._defaultInnerSep is not None:  # it has been set by the user, maybe to zero
            self.tikzPictureDefaults.innerSep = self.defaultInnerSep

        for g in self.graphics:
            g.setPositions()
        for gr in self.grams:
            gr.setPositions()

    def getTikz(self):
        gm = ['Gram.getTikz()']
        ss = []

        for gr in self.graphics:
            try:
                #print(gr)
                ret = gr.getTikz()
                #print(ret)
                if not isinstance(ret, str):
                    gm.append('graphic %s' % gr)
                    gm.append('getTikz() returned %s' % ret)
                    raise GramError(gm)
                ss.append(ret)
            except:
                gm.append('getTikz() failed for graphic %s' % gr)
                raise GramError(gm)

        try:
            return '\n'.join(ss)
        except:
            gm.append('Bad tikz strings')
            gm.append('%s' % ss)
            raise GramError(gm)

    def getSvg(self):
        gm = ['Gram.getSvg()']
        ss = []

        for gr in self.graphics:
            ret = gr.getSvg()
            if not isinstance(ret, str):
                gm.append('graphic %s' % gr)
                gm.append('getSvg() returned %s' % ret)
                raise GramError(gm)
            ss.append(ret)
        try:
            return '\n'.join(ss)
        except:
            gm.append('Bad svg strings')
            gm.append('%s' % ss)
            raise GramError(gm)

    def svgPxForCmI(self, cm):  # Int version
        return int(round(cm * self.svgPxForCm, 0))

    def svgPxForCmF(self, cm):  # float version
        return (cm * self.svgPxForCm)

    ###############################################################


    def getLatexFontDefString(self):
        gm = ["Gram.getLatexFontDefString()"]
        assert self.engine == 'tikz'

        ss = []
        if self.font == "lmr":
            #self.defaultTextFamily = "rmfamily"
            ss.append(r"\usepackage{fontspec}")
            ss.append(r"\usepackage{unicode-math}")
            ss.append(r"\setmainfont[SmallCapsFont={Latin Modern Roman Caps}]{Latin Modern Roman}")
            ss.append(r"\setsansfont{Latin Modern Sans}")
            ss.append(r"\setmonofont{Latin Modern Mono}")
            ss.append(r"\setmathfont{Latin Modern Math}")  # OldStyle figures does not work here.
            # not mathastext

        elif self.font == "lms":
            # Latin modern sans
            ss.append(r"\usepackage[no-math]{fontspec}")
            ss.append(r"\usepackage{unicode-math}")
            ss.append(r"\setmainfont{Latin Modern Sans}")  # no small caps
            ss.append(r"\setsansfont{Latin Modern Sans}")
            ss.append(r"\setmonofont{Latin Modern Mono}")
            ss.append(r"%\setmathfont{Latin Modern Math}")
            ss.append(r"\setmathfont{Fira Math Regular}")
            ss.append(r"\usepackage[italic]{mathastext}")

        elif self.font == 'helvetica':
            # Helvetica.  No good maths font; use Fira math
            ss.append(r"\usepackage[no-math]{fontspec}")
            ss.append(r"\usepackage{unicode-math}")
            # ss.append(r"\setmainfont{Helvetica}")
            # ss.append(r"\setsansfont{Helvetica}")
            ss.append(r"\setmainfont{Tex Gyre Heros}")
            ss.append(r"\setsansfont{Tex Gyre Heros}")
            ss.append(r"\setmonofont{Fira Mono}")
            ss.append(r"\setmathfont{Fira Math Regular}")
            ss.append(r"\usepackage{mathastext}")

        elif self.font == 'palatino':
            # Palatino
            ss.append(r"\usepackage{fontspec}")
            ss.append(r"\usepackage{unicode-math}")
            ss.append(r"\setmainfont{TeX Gyre Pagella}")
            ss.append(r"\setsansfont{Optima Regular}")
            ss.append(r"\setmonofont{Fira Mono}")
            ss.append(r"\setmathfont{TeX Gyre Pagella Math}")

        elif self.font == 'times':
            ss.append(r"\usepackage{fontspec}")
            ss.append(r"\usepackage{unicode-math}")
            ss.append(r"\setmainfont{TeX Gyre Termes}")
            ss.append(r"\setsansfont{Tex Gyre Heros}")
            ss.append(r"\setmonofont{Fira Mono}")
            ss.append(r"\setmathfont{TeX Gyre Termes Math}")

        elif self.font == "fira":
            ss.append(r"\usepackage{fontspec}")
            ss.append(r"\usepackage{unicode-math}")
            ss.append(r"\setmainfont[BoldFont={Fira Sans Bold}, ItalicFont={Fira Sans Italic}, BoldItalicFont={Fira Sans Bold Italic}]{Fira Sans Regular}")
            ss.append(r"\setsansfont{Fira Sans Regular}")
            ss.append(r"\setmonofont{Fira Mono}")
            ss.append(r"\setmathfont{Fira Math Regular}")



        else:
            gm.append("got %s, not implemented" % self.font)
            raise GramError(gm)

        # if self.defaultTextFamily == "sffamily":
        #     if self.useSfMathIfSffamily:
        #         ss.append("\\usepackage{sfmath}")
        #     if self.font != "helvetica":  # helvetica already done, above
        #         ss.append(r"\renewcommand{\familydefault}{\sfdefault}")
        return '\n'.join(ss)

    def _parseLatexUsePackages(self):
        """returns a multi-line string"""
        ss = []
        for lup in self.latexUsePackages:
            # print lup
            if isinstance(lup, tuple):
                # its a usepackage with options, eg ('graphicx', ['dvips'])
                # making \usepackage[dvips]{graphicx}
                assert len(lup) == 2
                assert isinstance(lup[1], list), "Got lup[1] %s " % lup[1]
                myOptions = ','.join(lup[1])
                ss.append(r"\usepackage[%s]{%s}" % (myOptions, lup[0]))
            else:
                ss.append(r"\usepackage{%s}" % lup)
        return '\n'.join(ss)


    def writeTikz(self):     # Gram
        gm = ['Gram.writeTikz()']

        thisDir = os.getcwd()
        # -p here means no error if existing.
        os.system('mkdir -p %s' % self.dirName)
        os.chdir(self.dirName)

        outFileNameA = '%s.tikz.tex' % self.baseName

        fA = open(outFileNameA, 'w')
        # fA.write('%% This is a tikz file\n')
        # fA.write('\n')
        # fA.write('%% This file is set up to use %ipt %s font.\n' %
        #          (self.documentFontSize, self.font))

        # tikzset styles
        theKeys = list(self.styleDict.keys())
        if theKeys:
            fA.write('\\tikzset{')
            for tzs in theKeys[:-1]:
                # print(f"writeTikz() style {tzs}")
                fA.write(r'%s/.style=%s,' %
                         (tzs, self.styleDict[tzs].getDefString()))
                fA.write('\n')
            tzs = theKeys[-1]
            fA.write(r'%s/.style=%s}' %
                     (tzs, self.styleDict[tzs].getDefString()))
            fA.write('\n')

        fA.write('\\begin{tikzpicture}')

        if self.tikzPictureDefaults:
            theDefString = self.tikzPictureDefaults.getDefString()[1:-1]
            # print(gm[0], f'tikzPictureDefaults is "{theDefString}"')
            if theDefString:
                fA.write("[%s]" % theDefString)
        fA.write('\n')

        if 0:
            fA.write("\n\\draw[help lines] (0cm,0cm) grid (8cm,5cm);\n")

        tricks = self.getTikz()
        fA.write(tricks)
        fA.write('\n')

        if 0:
            fA.write("\n\\path[ultra thin, draw=red] (current bounding box.south west) ")
            fA.write("rectangle (current bounding box.north east);\n")

        self.writeTikzOfEmbeddedGrams(fA)

        fA.write('\\end{tikzpicture}\n')
        fA.close()
        os.chdir(thisDir)

    def writeTikzOfEmbeddedGrams(self, fA):
        for gr in self.grams:
            if gr.gX or gr.gY:
                fA.write('\\begin{scope}[xshift=%.3fcm,yshift=%.3fcm]\n' % (gr.gX, gr.gY))
            tricks = gr.getTikz()
            fA.write(tricks)
            fA.write("\n")
            gr.writeTikzOfEmbeddedGrams(fA)
            if gr.gX or gr.gY:
                fA.write('\\end{scope}\n')



    def _writeTexStuff(self, flavour, inputTikzLine=None, geometryLine=None):
        # a4 is 20.99 by 29.70 cm, us letter paper is 21.59 by 27.94.  Assume a4.
        # If we make the margins 1 cm on each side, so thats [ 538.30897506  785.21109054] postscript points
        # If we make 7.5 mm margins, thats [ 552.48246045  799.38457593] postscript points.
        # 15 mm margins -> [ 509.96200429  756.86411976]
        # 20 mm margins -> [ 481.61503351  728.51714898]

        gm = ['Gram._writeTexStuff()']

        assert flavour in ['pdfPage', 'pdf']
        if flavour == 'pdfPage':
            assert inputTikzLine
            assert geometryLine
        if flavour == 'pdf':
            assert inputTikzLine

        texStuffFontLine = self.getLatexFontDefString()
        # print("===== texStuffFontLine")
        # print(texStuffFontLine)
        # print("==================")

        f = open('%s.tex' % self.baseName, 'w')
        if flavour == 'pdfPage':
            # or scrartcl?
            f.write(
                r"\documentclass[%ipt,a4paper]{article}" % self.documentFontSize)
            f.write("\n%s" % geometryLine)
        elif flavour == 'pdf':
            f.write(
                r"\documentclass[%ipt]{standalone}" % self.documentFontSize)
        f.write("\n")
        if texStuffFontLine:
            f.write("%s\n" % texStuffFontLine)
        f.write(self._parseLatexUsePackages())
        f.write("\n")
        f.write("\\usepackage{varwidth}\n")
        f.write("\\usepackage[svgnames]{xcolor}\n")
        f.write("\\usepackage{graphicx}\n")
        f.write("\\usepackage{tikz}\n")
        if self.useTikzPlotMarkLib:
            f.write(r"\usetikzlibrary{plotmarks}")
            f.write("\n")
        for lopc in self.latexOtherPreambleCommands:
            f.write("%s\n" % lopc)
        # f.write("\\pgfrealjobname{t}\n")
        #f.write("%s\n" % geometryLine)
        # f.write(tTexStuff_2) # \renewcommand\floatpagefraction{1.0} etc

        f.write("\\begin{document}\n")
        if flavour == 'pdfPage':
            f.write("\\thispagestyle{empty}\n")
        f.write(inputTikzLine)
        f.write('\\end{document}\n')
        f.close()

        if self.theGpdf:
            f = open('c.tex', 'w')
            f.write(tTexStuff_5 % self.documentFontSize)
            f.write("\\begin{textblock}{1}(0,0)\n")
            #f.write("\\includegraphics[scale=1.0023]{%s.pdf}\n" % self.baseName)
            f.write("\\includegraphics{%s.pdf}\n" % self.baseName)
            f.write("\\end{textblock}\n")
            # f.write("\\begin{textblock}{1}(0,0)\n")
            #f.write("\\includegraphics{../%s}\n" % self.theGpdf.pdf_fName)
            # f.write("\\end{textblock}\n")

            # These next lines work, but the sizes are not exactly exact.  Can see it better in big overlays.
            # f.write("\\includepdf[offset=0.5mm -0.5mm, noautoscale=true, fitpaper=true]{../%s}\n" % (
            #        self.theGpdf.pdf_fName))
            f.write("\\includepdf[fitpaper=true]{../%s}\n" % (
                    self.theGpdf.pdf_fName))
            f.write(tTexStuff_4)
            f.close()

        # os.chdir(thisDir)

    def pdfPage(self, maxWidth=19, maxHeight=27.7):
        #    a4 is 20.99 by 29.70 cm
        gm = ['Gram.pdfPage()']
        self.setPostionsBeforeTextMetrics()
        theKeys = self.styleDict.keys()
        if theKeys:
            for k in theKeys:
                self.styleDict[k].setBB()
        self.tikzCalcBigBoundingBox()
        print("Gram.pdfPage(), bbb is now %s" % self.bbb)

        if maxWidth > 19:
            gm.append(
                'a4 is 21 cm wide, so the maxWidth has a 19 cm maximum.  Got %s' % maxWidth)
            raise GramError(gm)
        if maxHeight > 27.7:
            gm.append(
                'a4 is 29.7 cm tall, so the maxHeight has a 27.7 cm maximum.  Got %s' % maxHeight)
            raise GramError(gm)
        myWid = (self.bbb[2] - self.bbb[0])
        myHt = (self.bbb[3] - self.bbb[1])
        assert myWid > 0.0, self.bbb
        assert myHt > 0.0, self.bbb

        print("%s: maxWidth = %.2f, maxHeight = %.2f, myWid=%.2f, myHt=%.2f, %.3f, %.3f" % (
            gm[0], maxWidth, maxHeight, myWid, myHt, maxWidth / myWid, maxHeight / myHt))

        assert myWid > 0.0
        assert myHt > 0.0

        if myWid > maxWidth or myHt > maxHeight:
            # \usepackage[margin=3cm,noheadfoot]{geometry}
            theScale = [1.0] * 2  # width and height
            if myWid > maxWidth:
                xScale = float(maxWidth) / myWid
                if xScale < 1.0:
                    theScale[0] = xScale
            if myHt > maxHeight:
                yScale = float(maxHeight) / myHt
                if yScale < 1.0:
                    theScale[1] = yScale
            print("theScale = %s" % theScale)
            myScale = min(theScale)
            # print "myScale = %s" % myScale
            assert myScale < 1.0

        if 1:
            gm = ["Gram.pdfPage()"]
            self.writeTikz()
            assert self.dirName
            if os.path.isdir(self.dirName) and os.path.isfile("%s/%s.tikz.tex" % (self.dirName, self.baseName)):
                thisDir = os.getcwd()
                os.chdir(self.dirName)
                if myWid > maxWidth or myHt > maxHeight:
                    inputTikzLine = '\\scalebox{%.3f}{\\input{%s.tikz}}\n' % (
                        myScale, self.baseName)
                else:
                    inputTikzLine = '\\input{%s.tikz}\n' % self.baseName
                geometryLine = '\\usepackage[width=%.1fcm, height=%.1fcm,noheadfoot]{geometry}' % (
                    maxWidth, maxHeight)
                self._writeTexStuff(
                    'pdfPage', inputTikzLine=inputTikzLine, geometryLine=geometryLine)
                if 1:
                    oldFName = "%s.pdf" % self.baseName
                    if os.path.isfile(oldFName):
                        os.remove(oldFName)
                os.system('make pdfPage')
                os.chdir(thisDir)


    def pdf(self, fixTextOverlaps=False):
        assert self.documentFontSize in [10, 11, 12]
        assert self.dirName
        self.engine = "tikz"
        self.pdfUsingLatex(fixTextOverlaps=fixTextOverlaps)

    def render(self):
        if self.engine == "tikz":
            self.setPositionsBeforeTextMetrics()
            self.tikzSetTextMetricsUsingLatex()
            self.setPositions()
        elif self.engine == "svg":
            self.svgRender()

    def pdfUsingLatex(self, fixTextOverlaps=False):
        # TODO Need to deal with self.htmlColorDict

        self.render()
        if fixTextOverlaps:
            self.fixTextOverlaps()

        self.writeTikz()
        assert os.path.isdir(self.dirName)
        thisDir = os.getcwd()
        os.chdir(self.dirName)
        inputTikzLine = '\\input{%s.tikz}\n' % self.baseName
        self._writeTexStuff('pdf', inputTikzLine)
        if 1:
            oldFName = "%s.pdf" % self.baseName
            if os.path.isfile(oldFName):
                os.remove(oldFName)
        #os.system('make pdf')
        if self.latexOutputGoesToDevNull:
            os.system(f'lualatex {self.baseName} > /dev/null')
        else:
            os.system(f'lualatex {self.baseName}')
        os.system(f"{self.pdfViewer} {self.baseName}.pdf")
        os.chdir(thisDir)

    def png(self, resolution=None):
        if not resolution:
            resolution = self.pngResolution
        pdfFileName = "%s/%s.pdf" % (self.dirName, self.baseName)
        #if not os.path.isfile(pdfFileName):

        # We want to re-make the pdf, in case there have been changes.
        # But we don't want to see it, so turn off pdfViewer
        savedPdfViewer = self.pdfViewer
        self.pdfViewer = 'ls'
        pdfFileName = "%s/%s.pdf" % (self.dirName, self.baseName)
        writeInColour("Making PDF file %s\n" % (pdfFileName), 'blue')
        self.pdf()
        self.pdfViewer = savedPdfViewer

        pngFileName = "%s/%s.png" % (self.dirName, self.baseName)
        writeInColour("Writing PNG file %s : resolution %i\n" % (pngFileName, resolution), 'blue')
        sys.stdout.flush()
        myCmd = "gs -dNOPAUSE -sDEVICE=pngalpha -r%i -dBATCH -sOutputFile=%s %s" % (
            resolution, pngFileName, pdfFileName)
        print(myCmd)
        os.system(myCmd)
        os.system("%s %s" % (self.pngViewer, pngFileName))

    def svgRender(self):
        gm = ["Gram.svgRender()"]
        verbose = False
        if verbose:
            print(f"{gm[0]} start")
        assert self.engine == 'svg'

        # Leftover stuff from a previous call to this method causes
        # grief.  Not sure why.  It probably indicates a bug elsewhere.
        # Maybe this fix is not needed anymore?
        # So zero a couple of things.

        kk = [k for k in self.gForGIdDict.keys() if k.startswith("text")]
        for k in kk:
            g = self.gForGIdDict.get(k)
            g.svg_half_normal_x = 0.0
            #g.dump()

        # Should these be class attributes here? ...
        Gram._svgNormalsize_x = None
        Gram._svgHackDoRotate = False
        Gram._svgHack_x_Only = True

        if verbose:
            print(f"{gm[0]} first go, about to setPositionsBeforeTextMetrics")
        self.setPositionsBeforeTextMetrics()
        if verbose:
            print(f"{gm[0]} first go, about to setTextMetrics")

        self.setTextMetrics()
        # Do I need setPositions() here?
        # self.setPositions()
        if verbose:
            print(f"{gm[0]} finished first go")

        Gram._svgHackDoRotate = False
        Gram._svgHack_x_Only = False
        self.setPositionsBeforeTextMetrics()
        if verbose:
            print(f"{gm[0]} second go, about to setTextMetrics")
        self.setTextMetrics()
        self.setPositions()
        if verbose:
            print(f"{gm[0]} finished second go")

        Gram._svgHackDoRotate = True
        self.setPositionsBeforeTextMetrics()
        if verbose:
            print(f"{gm[0]} third go, about to setTextMetrics")
        self.setTextMetrics()

        self.setPositions()


    def svg(self, extraMarginHack=1.0, writeWidthHeight=False, fixTextOverlaps=False):
        self.engine = 'svg'

        self.svgRender()
        if fixTextOverlaps:
            self.fixTextOverlaps()

        # The final product.
        svgFName = "%s.svg" % self.baseName
        if writeWidthHeight:
            writeInColour("Writing SVG file %s, writing width and height : svgPxForCm %.2f, extraMarginHack %.1f\n" % (
                svgFName, self.svgPxForCm, extraMarginHack), 'blue')
        else:
            writeInColour("Writing SVG file %s, not writing width and height : extraMarginHack %.1f\n" % (
                svgFName, extraMarginHack), 'blue')

        sys.stdout.flush()
        f = open(svgFName, 'w')
        self.svgWriteToOpenFile(f, self.bbb, doHackExtra=extraMarginHack, writeWidthHeight=writeWidthHeight)
        f.close()

        if self.svgViewer:
            os.system("%s %s" % (self.svgViewer, svgFName))

    def svgWriteToOpenFile(self, flob, theBBB, doHackExtra=0.0, writeWidthHeight=True):
        gm = ['Gram.svgWriteToOpenFile() doHackExtra=%f, writeWidthHeight %s' % (
            doHackExtra, writeWidthHeight)]
        # print(gm[0])
        #print("theBBB = %.3f %.3f %.3f %.3f" % (theBBB[0], theBBB[1], theBBB[2], theBBB[3]))

        myWid = (theBBB[2] - theBBB[0])
        myHt = (theBBB[3] - theBBB[1])
        assert myWid > 0.0, f"Got BBB wid {myWid}"
        assert myHt > 0.0, f"Got BBB ht {myHt}"
        # print(f"wid {myWid:.3f}  Ht {myHt:.3f}")

        flob.write('<svg\n')
        hackExtraX = doHackExtra
        hackExtraY = doHackExtra
        if doHackExtra:
            wd = (myWid * self.svgPxForCm) + (2 * hackExtraX)
            ht = (myHt * self.svgPxForCm) + (2 * hackExtraY)
        else:
            wd = myWid * self.svgPxForCm
            ht = myHt * self.svgPxForCm

        if writeWidthHeight:
            flob.write('  width="%.2f"\n' % wd)
            flob.write('  height="%.2f"\n' % ht)

        if doHackExtra:
            vb1 = (theBBB[0] * self.svgPxForCm) - hackExtraX
            vb2 = (theBBB[1] * self.svgPxForCm) - hackExtraY
            vb3 = (myWid * self.svgPxForCm) + (2 * hackExtraX)
            vb4 = (myHt * self.svgPxForCm) + (2 * hackExtraY)
        else:
            vb1 = (theBBB[0] * self.svgPxForCm)
            vb2 = (theBBB[1] * self.svgPxForCm)
            vb3 = (myWid * self.svgPxForCm)
            vb4 = (myHt * self.svgPxForCm)

        flob.write('  viewBox="%.2f %.2f %.2f %.2f"\n' % (vb1, vb2, vb3, vb4))
        # See https://developer.mozilla.org/en-US/docs/Web/SVG/Namespaces_Crash_Course
        flob.write('  xmlns="http://www.w3.org/2000/svg"\n')

        if self.svgTextPreserveWhitespace:
            # xml:space is deprecated; use the white-space CSS property.
            # https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/xml:space
            # https://developer.mozilla.org/en-US/docs/Web/CSS/white-space
            # However, I think it is needed for inkscape
            flob.write('  xmlns:xlink="http://www.w3.org/1999/xlink"\n')
            flob.write('  xml:space="preserve"\n')
        # else:

        # flob.write('  xmlns:xlink="http://www.w3.org/1999/xlink">\n')
        flob.write('>\n')

        # it looks like inkscape does not do external style sheets.  Dang.
        if 0:
            # link css file (s) containing font-face defs
            flob.write('    <link\n')
            flob.write('      xmlns="http://www.w3.org/1999/xhtml"\n')
            flob.write('      rel="stylesheet"\n')
            flob.write('      href="/Volumes/Vork/H/GitLab/g23/public/css11/peter11lmodern.css"\n')
            flob.write('      type="text/css" />\n')


        # a temporary default
        mySCTextFontStack = None
        if self.font == "lmr":
            myTextFontStack = '"Latin Modern Roman", serif'
            myRmFontStack = '"Latin Modern Roman", serif'
            mySFTextFontStack = '"Latin Modern Sans", sans-serif'
            myTTTextFontStack = '"Latin Modern Mono", monospace';
            mySCTextFontStack = '"Latin Modern Roman Caps", serif'
        elif self.font == "lms":
            myTextFontStack = '"Latin Modern Sans", sans-serif'
            myRmFontStack = '"Latin Modern Roman", serif'
            mySFTextFontStack = '"Latin Modern Sans", sans-serif'
            myTTTextFontStack = '"Latin Modern Mono", monospace'
            mySCTextFontStack = '"Latin Modern Roman Caps", serif'
        elif self.font == "helvetica":
            myTextFontStack = 'Helvetica, sans-serif'
            myRmFontStack = '"Latin Modern Roman", serif'
            mySFTextFontStack = 'Helvetica, sans-serif'
            myTTTextFontStack = '"Lucida Console", monospace';
            mySCTextFontStack = '"Helvetica", serif'
        elif self.font == "palatino":
            myTextFontStack = 'Palatino, serif'
            mySFTextFontStack = 'Helvetica, sans-serif'
            myTTTextFontStack = '"Lucida Console", monospace';
        elif self.font == "times":
            myTextFontStack = '"Times New Roman", serif'
            mySFTextFontStack = 'Helvetica, sans-serif'
            myTTTextFontStack = 'Courier, monospace';
        elif self.font == "fira":
            myTextFontStack = '"Fira Sans Regular", sans-serif'
            mySFTextFontStack = '"Fira Sans Regular", sans-serif'
            myTTTextFontStack = '"Lucida Console", monospace';
        else:
            gm.append("font %s is not implemented" % self.font)
            raise GramError(gm)


        # LMS with font-variant: small-caps does not work well with inkscape
        if self.font in ["lms"]:  
            svgCss = """
                text,tspan {
                    font-family: %s;
                    font-size: %s;
                }
                text.rmfamily,tspan.rmfamily {
                    font-family: %s;
                }
                text.sffamily,tspan.sffamily {
                    font-family: %s;
                }
                text.ttfamily,tspan.ttfamily {
                    font-family: %s;
                }
                text.scshape,tspan.scshape {
                    font-family: %s;
                }
                """ % (myTextFontStack, "30px", 
                       myRmFontStack, mySFTextFontStack, myTTTextFontStack, mySCTextFontStack)

        elif self.font in ["helvetica"]:
            svgCss = """
                text,tspan {
                    font-family: %s;
                    font-size: %s;
                }
                text.rmfamily,tspan.rmfamily {
                    font-family: %s;
                }
                text.sffamily,tspan.sffamily {
                    font-family: %s;
                }
                text.ttfamily,tspan.ttfamily {
                    font-family: %s;
                }
                text.scshape,tspan.scshape {
                    font-family: %s;
                    font-variant: small-caps;
                } """ % (myTextFontStack, "30px", 
                       myRmFontStack, mySFTextFontStack, myTTTextFontStack, mySCTextFontStack)


        elif self.font in ["lmr"]:
            svgCss = """
                text,tspan {
                    font-family: %s;
                    font-size: %s;
                }
                text.rmfamily,tspan.rmfamily {
                    font-family: %s;
                }
                text.sffamily,tspan.sffamily {
                    font-family: %s;
                }
                text.ttfamily,tspan.ttfamily {
                    font-family: %s;
                }
                text.scshape,tspan.scshape {
                    font-family: %s;
                    font-variant: normal;
                } """ % (myTextFontStack, "30px", 
                       myRmFontStack, mySFTextFontStack, myTTTextFontStack, mySCTextFontStack)
        styleStuff = None
        if self.font == "lms":
            myTextFontStack = '"Latin Modern Sans", sans-serif'
            styleStuff = svgLMStyleFF % myTextFontStack
        elif self.font == "lmr":
            myTextFontStack = '"Latin Modern Roman", serif'
            styleStuff = svgLMStyleFF % myTextFontStack
        elif self.font == "helvetica":
            styleStuff = svgHelveticaStyle
        elif self.font == "palatino":
            styleStuff = svgPalatinoStyle
        elif self.font == "times":
            styleStuff = svgTimesStyle
        elif self.font == "fira":
            styleStuff = svgFiraStyle
        assert styleStuff

        flob.write("\n<style>")
        flob.write(styleStuff)
        flob.write("\n</style>\n\n")

 

        if 0:
            # external style does not work with inkscape?!?  True, it does not
            flob.write("<style>\n")


            # link css file (s) containing defs for text,tspan, and classes 
            # text.rmfamily, text.sffamily, text.scshape, etc
            flob.write('    <link\n')
            flob.write('      xmlns="http://www.w3.org/1999/xhtml"\n')
            flob.write('      rel="stylesheet"\n')
            flob.write('      href="/Volumes/Vork/H/GitLab/g23/public/css11/peter11svglms.css"\n')
            flob.write('      type="text/css" />\n')

            flob.write("</style>\n")

        # Write markers in a <defs> </defs>  section.
        markersToWrite = []
        if hasattr(self, 'scatters'):
            for sc in self.scatters:
                markersToWrite.append(sc.marker)
        for gr in self.grams:
            if hasattr(gr, 'scatters'):
                for sc in gr.scatters:
                    markersToWrite.append(sc.marker)
        if markersToWrite:
            flob.write("<defs>\n")
            for mtw in markersToWrite:
                flob.write(mtw.getSvg())
            flob.write("</defs>\n")
        tricks = self.getSvg()
        flob.write(tricks)
        flob.write('\n')
        self.svgWriteEmbeddedGramsToOpenFile(flob)
        flob.write('</svg>\n')

    def svgWriteEmbeddedGramsToOpenFile(self, flob):
        for gr in self.grams:
            if gr.gX or gr.gY:
                flob.write('<g transform="translate(%.2f, %.2f)">\n' %
                           (self.svgPxForCmF(gr.gX), -self.svgPxForCmF(gr.gY)))
            tricks = gr.getSvg()
            flob.write(tricks)
            flob.write("\n")
            gr.svgWriteEmbeddedGramsToOpenFile(flob)  # recurse
            if gr.gX or gr.gY:
                flob.write('</g>\n')

    def cat(self):
        if self.engine == "tikz":
            assert self.dirName
            if 1:
                print("=========== %s/%s.tex =============" % (self.dirName, self.baseName))
                os.system('cat %s/%s.tex' % (self.dirName, self.baseName))
            if 0:
                print("=========== %s/foo.tex =============" % (self.dirName))
                os.system('cat %s/foo.tex' % (self.dirName))
            if 1:
                if os.path.isfile("%s/%s.tikz.tex" % (self.dirName, self.baseName)):
                    print("=========== %s.tikz.tex =============" % self.baseName)
                    os.system('cat %s/%s.tikz.tex' % (self.dirName, self.baseName))
        elif self.engine == "svg":
            if 1:
                print("=========== %s.svg =============" % self.baseName)
                os.system('cat %s.svg' % self.baseName)


    def adjustBBBFromGraphicBB(self, g):
        if g.bb[0] < self.bbb[0]:
            self.bbb[0] = g.bb[0]
        if g.bb[1] < self.bbb[1]:
            self.bbb[1] = g.bb[1]
        if g.bb[2] > self.bbb[2]:
            self.bbb[2] = g.bb[2]
        if g.bb[3] > self.bbb[3]:
            self.bbb[3] = g.bb[3]

    def inkscape(self):
        """Not used.  Only for testing."""

        gm = ["Gram.inkscape()"]
        print(gm[0], "Gram._svgHackDoRotate is %s, Gram._svgHack_x_Only is %s" % (
            Gram._svgHackDoRotate, Gram._svgHack_x_Only))
        flob = io.StringIO()
        self.svgWriteToOpenFile(flob, theBBB=[0., 0., 1., 1.])
        flob.seek(0)
        thisRet = flob.read().encode('utf-8')

        if 1:
            print("=+" * 20, "result of svgWriteToOpenFile()")
            # print(thisRet)
            splRet = thisRet.split(b"\n")
            for l in splRet:
                print(l)
            # print("thisRet type is %s" % type(thisRet))  # <class 'bytes'>
            flob.seek(0)
            print("-." * 20)

        p = Popen(['inkscape', '-S', '-p'],
                  stdout=PIPE, stdin=PIPE, stderr=PIPE)

        # In Py3 if I used a StringIO()  then read() gives a str, and
        # TypeError: memoryview: a bytes-like object is required, not 'str'
        # So do theUnicodeStuff.encode('utf-8')
        ret = p.communicate(input=thisRet)
        if 0:
            print("======================== returned from inkscape")
            print(ret)
            print(type(ret[0])) # class 'bytes'
            print("-------------------------")

        flob.close()

        if not ret[0]:
            # f = open("debug.svg", "w")
            # self.svgWriteToOpenFile(f, theBBB=[0., 0., 1., 1.])
            # f.close()
            gm.append("No string returned from inkscape.")
            raise GramError(gm)
        if not ret[0].startswith(b"svg"):
            gm.append("Bad string returned from inkscape.  Got %s %s" % ret)
            raise GramError(gm)
        #print ret[0]
        ll = [l for l in ret[0].split(b'\n') if l]
        splL = ll[0].split(b',')
        #print("got splL: ", splL)
        assert splL[0].startswith(b'svg')
        for l in ll:
            print(l)

    def setTextMetrics(self):        # Gram
        if self.engine == 'tikz':
            self.tikzSetTextMetricsUsingLatex()
        else:
            assert self.engine == 'svg'
            self.svgSetTextMetrics()

    def tikzSetTextMetricsUsingLatex(self):
        gm = ["Gram.tikzSetTextMetricsUsingLatex()"]
        # print(f"{gm[0]} here")

        # Get
        # - width
        # - fullHeight
        # - underhang
        # - rise
        # - half_normal_x

        # If there are any files referred to relatively, then they
        # should be relative to the dirName directory.  For example,
        # if I am doing \includegraphics{../../myGraphic.png}, that
        # should be relative to the dirName directory, often Gram, and
        # not relative to the current directory.  So I need to
        # possibly make that directory, and cd to it, and then back
        # out of it at the end.

        thisDir = os.getcwd()
        # -p here means no error if existing.
        os.system('mkdir -p %s' % self.dirName)
        os.chdir(self.dirName)


        kk = [k for k in self.gForGIdDict.keys() if k.startswith("text")]
        for k in kk:
            g = self.gForGIdDict.get(k)

            if 1:
                ret = fixUnderscores(g.rawText)
                g.rawText = ret
            else:
                # print(f"k={k} g.rawText={g.rawText} fixUnderscores")
                beforeT = g.rawText
                ret = fixUnderscores(g.rawText)
                g.rawText = ret
                afterT = g.rawText
                # print(f"tikzSetTextMetricsUsingLatex() fixUnderscores() before {beforeT}, after {afterT}")
            if 0:
                if "_" in g.rawText:
                    print(f"tikzSetTextMetricsUsingLatex() text: {g.rawText}")
                    print("  has underscore, but fixUnderscores() is turned off")
            #print(f"tikzSetTextMetricsUsingLatex() {k}: {g.rawText}")

            # This next one does parts, and wraps in a minipage or varwidth.
            # It does not do setCookedText or setBB()
            g.setTextPartsTikz()
            g.setMpTextTikz()
            #g.dump()

        fontLines = self.getLatexFontDefString()

        # I usepackage varwidth, [svgnames]xcolor, graphicx, and tikz for all, by default.
        # Any extras would be put in self.latexUsePackages
        # and self.latexOtherPreambleCommands

        # This should make the same output as in self._writeTextStuff()

        pkgString = self._parseLatexUsePackages()

        # otherPreambleCommands = ""
        # if self.latexOtherPreambleCommands:

        otherPreamble = []
        if self.useTikzPlotMarkLib:
            otherPreamble.append(r"\usetikzlibrary{plotmarks}")
        for lopc in self.latexOtherPreambleCommands:
            otherPreamble.append(lopc)
        otherPreamble = "\n".join(otherPreamble)

        texLines = [
            r"\documentclass{article}",
            fontLines,
            pkgString,
            r"\usepackage{varwidth}",
            r"\usepackage[svgnames]{xcolor}",
            r"\usepackage{graphicx}",
            r"\usepackage{tikz}",
            r"\newsavebox{\mysbox}",
            r"\newcommand{\myStr}{}",
            r"\newwrite\myotherfile",
            otherPreamble,
            r"\begin{document}",
            r"\immediate\openout\myotherfile=%s" % self.latexMetricsFileName,
        ]

        for k in kk:
            g = self.gForGIdDict[k]
            if 1:
                if g.mpText:
                    myStr = g.mpText
                else:
                    g.setCookedText()
                    myStr = g.cookedText
                # print("ltx Gram.tikzSetTextMetricsUsingLatex() ", end=" ")
                # print(f"raw: {g.rawText} cooked: {g.cookedText} myStr: {myStr}")

            if 0:
                ss = []
                ss.append(r'\tikz\node')
                options = g.getTikzOptions()
                if options:
                    ss.append('[%s]' % ','.join(options))
                    ss.append('at (0.0,0.0)')

                ss.append('{%s};' % g.rawText)
                myStr = "".join(ss)

            texLines.append(r"\renewcommand{\myStr}{%s}" % myStr)
            texLines.append(r"\sbox{\mysbox}{\myStr}")
            texLines.append(r"\immediate\write\myotherfile{%s\space\the\wd\mysbox\space\the\ht\mysbox\space\the\dp\mysbox}" % k)
            if 0:
                # makes pdf for debugging (turn off draftmode)
                texLines.append(r"\myStr")
            texLines.append(r"\renewcommand{\myStr}{x}")
            texLines.append(r"\sbox{\mysbox}{\myStr}")
            texLines.append(r"\immediate\write\myotherfile{%s\space x\space\the\ht\mysbox}" % k)

        texLines.append(r"\immediate\closeout\myotherfile")
        texLines.append(r"\end{document}")
        texLines.append("")

        if 0:
            print("Gram.tikzSetTextMetricsUsingLatex() debug; writing to foo.tex")
            fout = open("foo.tex", "w")
            fout.write("\n".join(texLines))
            fout.close()
            sys.exit()

        # run it in memory
        flob = io.BytesIO()
        for prt in texLines:
            flob.write(str.encode(prt))
        flob.seek(0, 0)  # Go to the beginning of the flob
        
        # Here below it writes foo.aux, foo.log, foo.pdf (always empty?) and grOut.txt
        # How do I prevent that writing?  It should be all in memory.
        p = Popen(["lualatex", "--jobname=foo", "--draftmode"], stdin=PIPE, stdout=PIPE, stderr=PIPE)
        ret = p.communicate(input=flob.getvalue())

        isBad = False
        if b"Undefined control sequence" in ret[0]:
            isBad = True
        elif b"Emergency stop" in ret[0]:
            isBad = True
        elif b"Fatal error occurred" in ret[0]:
            isBad = True

        if isBad:
            print(ret)
            gm.append("There was a problem with lualatex used for getting text sizes.")
            gm.append(r"It may be an underscore that needs escaping eg xx_yy -> xx\_yy ?")
            gm.append(r"or missing math mode with something like \alpha -> $\alpha$ ?")
            gm.append(r'To escape use literal =r"single\_backslash"= or ="double\\_backslash"=') 
            raise GramError(gm)

        assert os.path.isfile(self.latexMetricsFileName)  # grOut.txt
        ll = [l for l in open(self.latexMetricsFileName)]

        # 1 PostScript point = 0.35277138 mm
        ptToCm = 0.035277138

        for l in ll:
            sl = l.split()
            g = self.gForGIdDict.get(sl[0])
            if not g:
                for it in self.gForGIdDict.items():
                    print(f"{it[0]:10}  {it[1].rawText[:30]}")
                gm.append("could not get GramGraphic with gId %s" % sl[0])
                raise GramError(gm)
            assert isinstance(g, GramText)
            assert g.gId == sl[0]
            if len(sl) == 4:
                # first number is wd, g.width
                assert sl[1].endswith("pt")
                myNum = float(sl[1][:-2])
                # print(sl[0], sl[1], myNum)
                g.width = myNum * ptToCm

                # second number is ht, g.rise
                assert sl[2].endswith("pt")
                myNum = float(sl[2][:-2])
                # print(sl[0], sl[2], myNum)
                g.rise = myNum * ptToCm

                # third number is dp, g.underhang
                assert sl[3].endswith("pt")
                myNum = float(sl[3][:-2])
                # print(sl[0], sl[3], myNum)
                g.underhang = myNum * ptToCm

                g.fullHeight = g.underhang + g.rise

                if 0:
                    print(f"ltx {g.gId:8} width:{g.width:5.2f}cm ", end=" ")
                    print(f" fullHeight:{g.fullHeight:5.2f}cm     {g.rawText[:30]}")

            elif len(sl) == 3:
                assert sl[1] == "x"
                assert sl[2].endswith("pt")
                myNum = float(sl[2][:-2])
                # print(sl[0], sl[2], myNum)
                g.half_normal_x = myNum  * ptToCm * 0.5

        # chdir out of the dirName directory, back to the "script" directory
        os.chdir(thisDir)
        # print(f"{gm[0]} finished")


    def svgSetTextMetrics(self):
        gm = ["Gram.svgSetTextMetrics()"]
        #print(gm[0], "Gram._svgHackDoRotate is %s, Gram._svgHack_x_Only is %s" % (
        #    Gram._svgHackDoRotate, Gram._svgHack_x_Only))
        flob = io.StringIO()
        self.svgWriteToOpenFile(flob, theBBB=[0., 0., 1., 1.])
        flob.seek(0)
        thisRet = flob.read().encode('utf-8')

        if 0:
            fNm = f"debug{Gram._svgHackDoRotate}{Gram._svgHack_x_Only}.svg"
            print(f"writing debug svg file {fNm}")
            f = open(fNm, "w")
            self.svgWriteToOpenFile(f, theBBB=[0., 0., 1., 1.])
            f.close()
            #sys.exit()

        if 0:
            if Gram._svgHackDoRotate:
                #if Gram._svgHack_x_Only:
                    print("=+" * 20, "result of svgWriteToOpenFile()")
                    splRet = thisRet.split(b"\n")
                    for aLine in splRet:
                        if aLine.startswith(b" <text"):
                            print(aLine)
                    # print(thisRet)
                    # print("thisRet type is %s" % type(thisRet))  # <class 'bytes'>
                    flob.seek(0)
                    print("-." * 20)

        # For inkscape version 1.3
        #   -S, --query-all       Print bounding boxes of all objects
        #   -p, --pipe            Read input file from standard input (stdin)
        p = Popen(['inkscape', '-S', '-p'],
                  stdout=PIPE, stdin=PIPE, stderr=PIPE)

        # In Py3 if I used a StringIO()  then read() gives a str, and
        # TypeError: memoryview: a bytes-like object is required, not 'str'
        # So do theUnicodeStuff.encode('utf-8')
        ret = p.communicate(input=thisRet)
        if 0:
            print("======================== svgSetTextMetrics, returned from inkscape")
            print(ret)
            # print(type(ret[0])) # class 'bytes'
            print("-------------------------")

        flob.close()

        if not ret[0]:
            # f = open("debug.svg", "w")
            # self.svgWriteToOpenFile(f, theBBB=[0., 0., 1., 1.])
            # f.close()
            gm.append("No string returned from inkscape.")
            raise GramError(gm)
        if not ret[0].startswith(b"svg"):
            gm.append("Bad string returned from inkscape.  Got %s %s" % ret)
            raise GramError(gm)
        #print ret[0]
        ll = [l for l in ret[0].split(b'\n') if l]

        if 0:
            print()
            print("-" * 50, "svgSetTextMetrics().  lines returned from inkscape")
            for l in ll:
                #print(l)
                sl = l.split(b",")
                for i in range(5):
                    print("%10s" % sl[i], end=" ")
                print()
            print("-" * 50)
            print()



        splL = ll[0].split(b',')
        # print("got splL: ", splL)
        assert splL[0].startswith(b'svg')
        # pxPerCm = 35.43307   # official
        self.bbb[0] = float(splL[1]) / self.svgPxForCm
        self.bbb[1] = float(splL[2]) / self.svgPxForCm
        self.bbb[2] = self.bbb[0] + float(splL[3]) / self.svgPxForCm
        self.bbb[3] = self.bbb[1] + float(splL[4]) / self.svgPxForCm

        #print("svgSetTextMetrics() got bbb:", self.bbb[0], self.bbb[1], self.bbb[2], self.bbb[3])

        # print("gForGIdDict is now", self.gForGIdDict)

        # For this hack, if Gram._svgHackDoRotate is turned off, then the text is
        # not rotated, and we can get the width from the inkscape bounding box.
        if not Gram._svgHackDoRotate:  # so any text is not rotated

            for l in ll[1:]:
                if l.startswith(b'text'):
                    #print(l)
                    splL = l.split(b',')
                    # print(splL)
                    #print("gForGIdDict", self.gForGIdDict)
                    g = self.gForGIdDict.get(splL[0].decode("utf-8"))
                    if not g:
                        self.gForGIdDict.dump()
                        gm.append("could not get graphic for gId %s" % splL[0].decode("utf-8"))
                        raise GramError(gm)
                    if Gram._svgHack_x_Only:
                        top = -(float(splL[2]))
                        fullHeight = (float(splL[4]))
                        g.svgBaseline_cm = (top - fullHeight) / self.svgPxForCm
                        if 0:
                            print(f"""svgSetTextMetrics() cd self.svgPxForCm:
                            {self.svgPxForCm}, top: {top}, fullHeight: {fullHeight}
                            g.svgBaseline_cm: {g.svgBaseline_cm}""")
                    else:
                        # Get, for the un-rotated text,
                        # - g.width
                        # - g.fullHeight
                        # - g.underhang # descent
                        # - g.rise      # ascent
                        g.width = float(splL[3]) / self.svgPxForCm
                        x1 = (float(splL[1])) / self.svgPxForCm
                        top = -(float(splL[2])) / self.svgPxForCm
                        x3 = x1 + (float(splL[3])) / self.svgPxForCm
                        g.fullHeight = (float(splL[4])) / self.svgPxForCm
                        y1 = top - g.fullHeight
                        g.underhang = g.svgBaseline_cm - y1  # can be zero
                        g.rise = top - g.svgBaseline_cm

                        if 0:
                            print(f"svgSetTextMetrics: {g.rawText} width:{g.width:.2f}cm")


        # Get Gram._svgNormalsize_x.  Need a new temporary text.
        # Then run inkscape again.  Then remove the temporary text.

        # Only do this next bit once, at the beginning, when Gram._svgNormalsize_x is still None
        # Add a text object of a single "x", and remove it when finished
        if  Gram._svgNormalsize_x == None:
            gx = self.text("x", 0,0)
            #print(f"{gm[0]} made gx, gId {gx.gId}")
            flob = io.StringIO()
            self.svgWriteToOpenFile(flob, theBBB=[0., 0., 1., 1.])
            flob.seek(0)
            thisRet = flob.read().encode('utf-8')
            if 0:
                print()
                print("self is", self)
                print("graphics")
                for g in self.graphics:
                    if isinstance(g, GramText):
                        print(f"GramText {g.rawText} {g.gId}")
                print()
                print("gForGIdDict")
                for k,v in self.gForGIdDict.items():
                    print(k,v.rawText)
                print()
                print("send to inkscape:")
                print(thisRet)
                sys.exit()
            p = Popen(['inkscape', '-S', '-p'], stdout=PIPE, stdin=PIPE, stderr=PIPE)
            ret = p.communicate(input=thisRet)
            flob.close()
            ll = [l for l in ret[0].split(b'\n') if l]
            inkLine = None
            if 0:
                for l in ll:
                    print(l)
                print()
                for k,v in self.gForGIdDict.items():
                    print(k,v)

                    # print(k,v.rawText)
            for l in ll[1:]:
                if l.startswith(b'text'):
                    splL = l.split(b',')
                    g = self.gForGIdDict.get(splL[0].decode("utf-8"))
                    assert g
                    if g == gx:
                        inkLine = splL
                        break
            assert inkLine
            # print(f"svgSetTextMetrics() got inkLine for normalsize x {inkLine}")
            my_x = float(inkLine[4]) / self.svgPxForCm
            Gram._svgNormalsize_x = my_x
            # print(f"svgSetTextMetrics() got Gram._svgNormalsize_x {Gram._svgNormalsize_x}")

            # Clean up
            self.graphics.remove(gx)
            g = self.gForGIdDict.pop(inkLine[0].decode("utf-8"))
            assert g == gx

    ##############################################################
    ##############################################################
    ##############################################################

    def code(self, theCode):
        GramCode(self, theCode)
        # The instantiation above puts it in ...?

    def grid(self, llx, lly, urx, ury, color='gray'):
        g = GramGrid(llx, lly, urx, ury, color=color)
        self.graphics.append(g)
        return g

    def text(self, theText, x, y):
        g = GramText(theText)
        g.cA = GramCoord(x, y)
        self.graphics.append(g)
        return g

    def line(self, x1, y1, x2, y2):
        cA = GramCoord(x1, y1)
        cB = GramCoord(x2, y2)
        # self.graphics.append(cA)
        # self.graphics.append(cB)
        g = GramLine(cA, cB)
        self.graphics.append(g)
        return g

    def rect(self, x1, y1, x2, y2):
        cA = GramCoord(x1, y1)
        cB = GramCoord(x2, y2)
        # self.graphics.append(cA)
        # self.graphics.append(cB)
        g = GramRect(cA, cB)
        self.graphics.append(g)
        return g

    def gpdf(self, pdf_fName):
        if self.theGpdf:
            raise GramError(
                "Gram.gpdf()  This week, we only allow one gpdf.  Already got one.")

        g = GramPdf(pdf_fName)
        self.theGpdf = g
        self.graphics.append(g)
        return g

    def jpeg(self, jpeg_fName, x, y, scale):
        cA = GramCoord(x, y)
        g = GramJpeg(jpeg_fName, cA, scale)
        self.graphics.append(g)
        return g

    ###########################################################

    def getAllGramTexts(self, agt):
        """Recurses into self.grams"""

        for g in self.graphics:
            if isinstance(g, GramText):
                agt.append(g)
        for gr in self.grams:
            gr.getAllGramTexts(agt)
        #print("Got %i texts" % len(agt))
        return agt

    def fixTextOverlaps(self):
        """not working for rotated text"""
        gm = ["Gram.fixTextOverlaps()"]
        thisVerbose = True
        tbb = []
        tbb = self.getAllGramTexts(tbb)
        if thisVerbose:
            print(f"fixTextOverlaps() engine is '{self.engine}'")
            print(f"fixTextOverlaps() got {len(tbb)} texts")
        if len(tbb) < 2:
            return

        theMax = -1000000.
        theMin = 1000000.
        for g in tbb:
            # not g.getInnerSep(), so could be None
            g.savedInnerSep = g.innerSep
            g.innerSep = 0.0

            if self.engine == 'tikz':
                g.setBB()
            elif self.engine == 'svg':
                g.getSvg()
            else:
                raise GramError()

            print(f"g.bb {g.bb}  {g.rawText}")
            g.lly = g.bb[1]
            if g.lly < theMin:
                theMin = g.lly
            if g.lly > theMax:
                theMax = g.lly
            g.overlaps = []
        theCenterY = theMin + (0.5 * (theMax - theMin))
        if 0:
            g = self.line(0, theCenterY, 3, theCenterY)
            g.color = 'blue'
            g.lineThickness = 'ultra thin'
            # return

        indices = range(len(tbb))

        tbb = func.sortListOfObjectsOnAttribute(tbb, 'lly')
        # tbb is ordered from lowest to highest
        if thisVerbose:
            for i in indices:
                tbNum = indices[-(i + 1)]
                print("%2i  %.3f  %s" % (tbNum, tbb[tbNum].lly, tbb[tbNum].rawText))
            print("theCenterY is %.2f" % theCenterY)

        safety = 0
        while 1:
            if thisVerbose:
                print("round %i ----" % safety)
            safety += 1
            hasOverlap = False
            if 1:
                # In this part, we go up from the lowest ones, moving the
                # lowest ones down.
                for tb in tbb:
                    tb.overlaps = []
                for i in indices[:-1]:
                    tbA = tbb[i]
                    if tbA.lly > theCenterY:
                        break
                    for j in indices[i + 1:]:
                        tbB = tbb[j]
                        # if thisVerbose:
                        # print "%i %s,   %i %s" % (i, tbA.rawText, j,
                        # tbB.rawText)
                        if bbOverlap(tbA.bb, tbB.bb):
                            if thisVerbose:
                                print("        '%s' overlaps with '%s'" % (tbA.rawText, tbB.rawText))
                            hasOverlap = True
                            moveDownBy = (tbA.bb[3] - tbB.bb[1])
                            assert moveDownBy >= 0.0
                            if tbA.yShift is None:
                                tbA.yShift = 0.0
                            tbA.yShift -= moveDownBy
                            tbA.bb[1] -= moveDownBy
                            tbA.bb[3] -= moveDownBy
                            tbA.lly -= moveDownBy
                            if thisVerbose:
                                print("        '%s' moving down by %.3f" % (tbA.rawText, moveDownBy))
                            tbB.overlaps.append(tbA)
                            for tb in tbA.overlaps:
                                tb.yShift -= moveDownBy
                                tb.bb[1] -= moveDownBy
                                tb.bb[3] -= moveDownBy
                                tb.lly -= moveDownBy
                                if thisVerbose:
                                    print("        '%s' moving down by %.3f" % (tb.rawText, moveDownBy))
                            break
                    # if hasOverlap:
                    #    break

            if 1:
                # In this part we go down from the highest ones, moving the
                # highest ones down.
                for tb in tbb:
                    tb.overlaps = []
                for i2 in indices[:-1]:
                    i = indices[-(i2 + 1)]
                    tbA = tbb[i]
                    if tbA.lly < theCenterY:
                        break
                    for j2 in indices[i2 + 1:]:
                        j = indices[-(j2 + 1)]
                        tbB = tbb[j]
                        # if thisVerbose:
                        # print "%i %s,   %i %s" % (i, tbA.rawText, j,
                        # tbB.rawText)
                        if bbOverlap(tbA.bb, tbB.bb):
                            if thisVerbose:
                                print("        '%s' overlaps with %s" % (tbA.rawText, tbB.rawText))
                            hasOverlap = True
                            moveUpBy = (tbB.bb[3] - tbA.bb[1])
                            assert moveUpBy >= 0.0
                            if tbA.yShift is None:
                                tbA.yShift = 0.0
                            tbA.yShift += moveUpBy
                            tbA.bb[1] += moveUpBy
                            tbA.bb[3] += moveUpBy
                            tbA.lly += moveUpBy
                            if thisVerbose:
                                print("        '%s' moving up by %.3f" % (tbA.rawText, moveUpBy))
                            tbB.overlaps.append(tbA)
                            for tb in tbA.overlaps:
                                tb.yShift += moveUpBy
                                tb.bb[1] += moveUpBy
                                tb.bb[3] += moveUpBy
                                tb.lly += moveUpBy
                                if thisVerbose:
                                    print("        '%s' moving up by %.3f" % (tb.rawText, moveUpBy))
                            break
                    # if hasOverlap:
                    #    break

            # break
            # print "safety=%i" % safety
            if not hasOverlap:
                if thisVerbose:
                    print("======== no more overlaps.  breaking out of loop")
                break
            if safety > 100:
                print("Gram.fixTextOverlaps() -- too many iterations -- quitting.")
                break

        for tb in tbb:
            tb.innerSep = tb.savedInnerSep
            del(tb.savedInnerSep)
            del(tb.overlaps)
        for gr in self.grams:
            gr.fixTextOverlaps()


class GramCoord(Gram):

    def __init__(self, xPosn=0.0, yPosn=0.0, name=None, comment=None):
        Gram.__init__(self)

        self.xPosn = xPosn
        self.yPosn = yPosn
        self.name = name
        self.comment = comment
        # self.topLevelGraphics.append(self)

    def dump(self):
        if self.name:
            print(f"GramCoord.dump() name {self.name} xPosn {self.xPosn} yPosn {self.yPosn}")
        else:
            print(f"GramCoord.dump() xPosn {self.xPosn} yPosn {self.yPosn}")

    def getTikz(self):
        if self.name:
            ss = []
            ss.append(r'\coordinate')
            ss.append('(%s)' % self.name)
            ss.append('at (%.3f,%.3f);' % (self.xPosn, self.yPosn))
            if self.comment:
                ss.append("%% %s" % self.comment)
            return ' '.join(ss)


class GramCode(Gram):

    def __init__(self, mygram, code):
        Gram.__init__(self)
        # gram is a gram.gram.Gram object
        assert isinstance(mygram, Gram)
        self.code = code
        mygram.graphics.append(self)

    def getTikz(self):
        return '%s' % self.code

    def getSvg(self):
        return '%s' % self.code

class GramColor(Gram):
    def __init__(self):
        self.color = None
        self._value = None
        #self.type = None       # svg, base (ie latex), hex
        self._transparent = False

    def _getValue(self):
        return self._value

    def _setValue(self, theValue):
        gm = ['Gram._setValue()']
        assert isinstance(theValue, str)
        if ' ' in theValue:
            gm.append("The value should not have any spaces.")
            raise GramError(gm)

        try:
            fVal = float(theValue)
        except ValueError:
            gm.append("color value should be a number between 0 and 1.0")
            gm.append("but not equal to either zero or 1.0")
            gm.append(f"Got {theValue}")
            raise GramError(gm)

        if (fVal == 0.0) or (fVal == 1.0):
            gm.append("color value should be a number between 0 and 1.0")
            gm.append("but not equal to either zero or 1.0")
            gm.append(f"Got {theValue}")
            raise GramError(gm)

        self._value = theValue

    def _delValue(self):
        gm = ['Gram._delValue()']
        gm.append(
            "Caught an attempt to delete self.value-- Set it to something else, or None, but don't delete it, ok?")
        raise GramError(gm)

    value = property(_getValue, _setValue, _delValue)

    def _getTransparent(self):
        return self._transparent

    def _setTransparent(self, theTransparent):
        gm = ['Gram._setTransparent()']
        assert isinstance(theTransparent, bool)
        if theTransparent:
            if not self.value:
                gm.append("Setting a color to transparent without setting aColor.value does not work.")
                raise GramError(gm)
        self._transparent = theTransparent

    def _delTransparent(self):
        gm = ['Gram._delTransparent()']
        gm.append("Can't delete property GramColor.transparent")
        raise GramError(gm)

    transparent = property(_getTransparent, _setTransparent, _delTransparent)

    def dump(self):
        print("GramColor.dump()")
        print(f"    color={self.color}, value={self.value}, transparent={self.transparent}")

    def setColorFromString(self, theColor):
        assert isinstance(theColor, str)
        gm = ['GramColor.setColorFromString(%s)' % theColor]

        # theColor string might be "red" or it might be "red!20".  First, split
        # off the number if it exists and put that in self.value.  The rest goes
        # into theColorNoValue.
        if "!" in theColor:
            splColor = theColor.split('!')
            assert len(splColor) == 2
            try:
                theNum = int(splColor[1])
            except ValueError:
                gm.append("Can't make sense of color '%s'" % theColor)
                raise GramError(gm)
            if theNum <= 0 or theNum >= 100:
                gm.append("The 'value' in the color (eg in blue!50) should be from 1-99.  Got %i" % theNum)
                raise GramError(gm)
            self.value = "%.2f" % (0.01 * theNum)
            theColorNoValue = splColor[0]
        else:
            theColorNoValue = theColor

        theColorNoValue = theColorNoValue.lower()

        # Now see if theColorNoValue is a base color (eg "red") or an svg color
        # (eg "Red") or a hex color (eg 99ff33 or #FF00AA)
        if theColorNoValue in baseColors:
            # self.type = "base"
            pass
        elif theColorNoValue in CSS4_COLORS:
            #self.type = 'svg'
            pass
            if theColorNoValue == "rebeccapurple":
                writeInColour(f"Warning: Colour rebeccapurple is a valid CSS (for SVG) color, but not for Latex/Tikz\n",
                              colour='violet')
        elif theColorNoValue.startswith("#") and len(theColorNoValue) == 7:
            #self.type = "hex"
            pass
        elif theColorNoValue in svgLowColorsNotInCSS4:
            # gm.append(f"got color {theColorNoValue}")
            # gm.append("It is a valid SVG color, but is not in CSS4")
            writeInColour(f"Warning: Colour {theColorNoValue} is a valid SVG color, but not in CSS4 for SVG\n",
                          colour='violet')
        else:
            gm.append("I don't understand the color '%s'" % theColorNoValue)
            print("This week, the colour should be based on base or svg/html names.  One of ---")
            print("%s" % baseColors)
            print("%s" % CSS4_COLORS.keys())
            raise GramError(gm)

        self.color = theColorNoValue

    def getSvgOptions(self, stroke=None):    # GramColor
        gm = [f"GramColor.getSvgOptions(color:{self.color}, value:{self.value}, stroke:{stroke})"]
        #print(gm[0])
        # self.dump()

        if self.value:
            fValue = float(self.value)
            if fValue == 0.0:
                gm.append("Got colour value of zero.  Does that work?")
                raise GramError(gm)
            elif fValue == 1.0:
                gm.append("Got colour value of 1.0.  Does that make sense?")
                raise GramError(gm)

        # if self.transparent:
        #     if not self.value:
        #         gm.append(f"If the color (here {self.color}) is transparent (which it is)")
        #         gm.append(f"then it should have a 'value', usually given by eg 'thecolor!30'")
        #         raise GramError(gm)

        options = []
        if self.value and fValue > 0.0 and fValue < 1.0:
            if self.transparent:
                if stroke == "fill":
                    options.append('fill="%s"' % self.color)
                    options.append('fill-opacity="%s"' % self.value)
                else:
                    options.append('stroke="%s"' % self.color)
                    options.append('stroke-opacity="%s"' % self.value)
            else:
                # For cases when we have color.value, eg from red!50,
                # with non-transparent svg,
                # we should not put the self.value in stroke-opacity.

                # Rather, need to decrease the color saturation.
                # Do that by
                # 1a. either converting hex to rgb, or
                # 1b. looking up the rgb from the named color
                # 2.  converting to hsv
                # 3.  decreasing s by fValue
                # 4.  converting back to rgb
                # 5.  converting rgb to hex

                if self.color.startswith("#"):
                    r,g,b = self.getRgbFromHex(self.color)
                elif self.color in CSS4_COLORS:
                    ret = CSS4_COLORS.get(self.color)
                    assert ret
                    r,g,b = ret[1]
                    #print(f"rgb {r} {g} {b}; {r * 255} {g * 255} {b * 255}")
                h,s,v = colorsys.rgb_to_hsv(r,g,b)
                #print(f"GramColor.getSvgOptions() color:{self.color} value:{self.value}, {h},{s},{v}")
                if s == 0.0:    # black.  This looks like a bug to me.
                    r,g,b = (1.0 - fValue, 1.0 - fValue, 1.0 - fValue)
                else:
                    s *= fValue

                    # Hack alert.  This is not quite right, but not as bad as ignoring it.
                    newV = v + ((1.0 - fValue) * (1.0 - v))
                    assert newV >= 0.0
                    assert newV <= 1.0
                    r,g,b = colorsys.hsv_to_rgb(h,s,newV)
                newHex = self.getHexFromRgb((r,g,b))
                if stroke == "fill":
                    options.append('fill="%s"' % newHex)
                else:
                    options.append('stroke="%s"' % newHex)
        else:
            if stroke == "fill":
                options.append('fill="%s"' % self.color)
            else:
                options.append('stroke="%s"' % self.color)

        return options


    def getRgbFromHex(self, theHex):
        h = theHex.lstrip('#')
        r,g,b = tuple([int(h[i:i+2], 16)/255. for i in (0, 2, 4)])
        # print(f"GramColor.getRgbFromHex({theHex}): {r:.4f}  {g:.4f}  {b:.4f}")
        return (r,g,b)

    def getHexFromRgb(self, theRgb):
        h = "#"
        assert len(theRgb) == 3
        for indx in [0,1,2]:
            v = theRgb[indx]
            assert isinstance(v, float)
            assert v >= 0.0 and v <= 1.0
            hPart = hex(round(v * 255))
            #print(f"GramColor.getHexFromRgb()  {v} {hPart}")
            if len(hPart) == 3:
                h += "0"
                h += hPart[2]
            elif len(hPart) == 4:
                h += hPart[2:]
            else:
                raise GramError(f"unexpected getHexFromRgb from {v}; got {hPart}")
        assert len(h) == 7
        return h

class GramTikzStyle(Gram):

    def __init__(self):
        Gram.__init__(self)
        self.name = None
        self._color = None
        #self._opacity = None
        self._draw = None
        self._fill = None
        self._textSize = None
        self._textFamily = None
        self._textSeries = None
        self._textShape = None  # "upshape"
        self._anchor = None
        self._anchorOverRide = None
        self._xShift = None
        self._yShift = None
        self._rotate = None
        # Whether a box or a circle is drawn around the text.
        self._shape = None
        self._lineThickness = None
        self._cap = None
        self._lineStyle = None  # Dotted, dashed
        self._textHeight = None
        self._textDepth = None
        self._textWrapWidth = None
        self._textAlign = None
        self._innerSep = None
        self._roundedCorners = None

    def _getColor(self):
        return self._color

    def _setColor(self, theColor):
        # print(f"color being set to {theColor}")
        if theColor in [None, True, False]:
            self._color = theColor
        elif isinstance(theColor, GramColor):
            self._color = theColor
        elif isinstance(theColor, str):
            self._color = GramColor()
            self._color.setColorFromString(theColor)
        else:
            gm = ['GramTikzStyle._setColor()']
            gm.append("Can't set color to '%s'" % theColor)
            raise GramError(gm)

    def _delColor(self):
        self._color = None

    color = property(_getColor, _setColor, _delColor)
    colour = property(_getColor, _setColor, _delColor)

    def _getDraw(self):
        return self._draw

    def _setDraw(self, theDraw):
        # Default None.  Set to True or False, or the colour.  This is for text boxes
        if theDraw in [None, True, False]:
            self._draw = theDraw
        elif isinstance(theDraw, GramColor):
            self._draw = theDraw
        elif isinstance(theDraw, str):
            self._draw = GramColor()
            self._draw.setColorFromString(theDraw)
        else:
            gm = ['GramTikzStyle._setDraw()']
            gm.append("Can't set color to '%s'" % theDraw)
            raise GramError(gm)

    def _delDraw(self):
        self._draw = None

    draw = property(_getDraw, _setDraw, _delDraw)

    def _getFill(self):
        return self._fill

    def _setFill(self, theFill):
        if theFill in [None, True, False]:
            self._fill = theFill
        elif isinstance(theFill, GramColor):
            self._fill = theFill
        elif isinstance(theFill, str):
            self._fill = GramColor()
            self._fill.setColorFromString(theFill)
        else:
            gm = ['GramTikzStyle._setFill()']
            gm.append("Can't set the fill to '%s'" % theFill)
            raise GramError(gm)

    def _delFill(self):
        self._fill = None

    fill = property(_getFill, _setFill, _delFill)

    def _getTextSize(self):
        return self._textSize

    def _setTextSize(self, theSize):
        if theSize is None:
            self._textSize = None
        else:
            assert isinstance(theSize, str)
            gm = ['GramTikzStyle._setSize()']
            goodSizes = self.goodTextSizes
            if theSize not in goodSizes:
                gm.append("You can only set property 'size' to one of")
                gm.append("%s" % goodSizes)
                gm.append("Got attempt to set to '%s'" % theSize)
                raise GramError(gm)
            self._textSize = theSize

    def _delTextSize(self):
        self._textSize = None

    textSize = property(_getTextSize, _setTextSize, _delTextSize)

    #_goodTextFamilies = ['rmfamily', 'sffamily', 'ttfamily']
    def _getTextFamily(self):
        return self._textFamily

    def _setTextFamily(self, newVal):
        gm = ['GramTikzStyle._setTextFamily()']
        if newVal == None:
            self._textFamily = None
        else:
            try:
                assert isinstance(newVal, str)
            except AssertionError:
                gm.append(f"Got newVal {newVal}, type {type(newVal)}, should be a string")
                raise GramError(gm)
            lowVal = newVal.lower()
            goodVals = self.goodTextFamilies
            if lowVal not in goodVals:
                gm.append("You can only set property 'textFamily' to one of")
                gm.append("%s (or None, or y" % goodVals)
                gm.append("Got attempt to set to '%s'" % newVal)
                raise GramError(gm)
            if self.font == 'helvetica':
                # if lowVal != 'sffamily':
                #     print gm[0]
                #     print "  Ignoring request to set textFamily to '%s' -- it does not work with helvetica" % newVal
                #     print "does this work?"  # does not work with ttfamily
                self._textFamily = lowVal
            else:
                self._textFamily = lowVal

    def _delTextFamily(self):
        self._textFamily = None

    textFamily = property(_getTextFamily, _setTextFamily, _delTextFamily)

    #_goodTextSeries = ['bfseries']
    def _getTextSeries(self):
        return self._textSeries

    def _setTextSeries(self, newVal):
        gm = ['GramTikzStyle._setTextSeries()']
        if newVal == None:
            self._textSeries = None
        else:
            assert isinstance(newVal, str)
            lowVal = newVal.lower()
            goodVals = self.goodTextSeries
            if lowVal not in goodVals:
                gm.append("You can only set property 'textSeries' to one of")
                gm.append("%s (or None, or you can delete it)" % goodVals)
                gm.append("Got attempt to set to '%s'" % newVal)
                raise GramError(gm)
            else:
                self._textSeries = lowVal

    def _delTextSeries(self):
        self._textSeries = None

    textSeries = property(_getTextSeries, _setTextSeries, _delTextSeries)

    #_goodTextShapes = ['itshape', 'scshape', "upshape"]          # and "slshape"?
    def _getTextShape(self):
        return self._textShape

    def _setTextShape(self, newVal):
        gm = ['GramTikzStyle._setTextShape()']
        if newVal == None:
            self._textShape = "upshape"
        else:
            assert isinstance(newVal, str)
            lowVal = newVal.lower()
            goodVals = self.goodTextShapes
            if lowVal not in goodVals:
                gm.append("You can only set property 'textShape' to one of")
                gm.append("%s (or None, or you can delete it)" % goodVals)
                gm.append("Got attempt to set to '%s'" % newVal)
                raise GramError(gm)
            else:
                self._textShape = lowVal

    def _delTextShape(self):
        self._textShape = None

    textShape = property(_getTextShape, _setTextShape, _delTextShape)

    def _getAnchor(self):
        return self._anchor

    def _setAnchor(self, theAnchor):
        if theAnchor not in self.goodAnchors:
            gm = ['GramTikzStyle._setAnchor()']
            gm.append("You can only set property 'anchor' to one of")
            gm.append("%s" % self.goodAnchors)
            gm.append("Got attempt to set to '%s'" % theAnchor)
            raise GramError(gm)
        self._anchor = theAnchor

    def _delAnchor(self):
        raise GramError("Don't delete propery anchor, ok?")

    anchor = property(_getAnchor, _setAnchor, _delAnchor)

    def _getAnchorOverRide(self):
        return self._anchorOverRide

    def _setAnchorOverRide(self, theAnchorOverRide):
        if theAnchorOverRide not in self.goodAnchors:
            gm = ['GramTikzStyle._setAnchorOverRide()']
            gm.append("You can only set property 'anchorOverRide' to one of")
            gm.append("%s" % self.goodAnchors)
            gm.append("Got attempt to set to '%s'" % theAnchorOverRide)
            if theAnchorOverRide.startswith('mid'):
                gm.append(
                    "(Anchors 'mid', 'mid east', and 'mid west' are turned off).")
            raise GramError(gm)
        self._anchorOverRide = theAnchorOverRide

    def _delAnchorOverRide(self):
        self._anchorOverRide = None

    anchorOverRide = property(_getAnchorOverRide,
                              _setAnchorOverRide, _delAnchorOverRide)

    def _setAnch(self, newVal):
        gm = ['GramTizStyle._setAnch()']
        gm.append("This is a read-only variable -- don't set it.")
        gm.append("Set anchor or anchorOverRide")
        raise GramError(gm)

    def _getAnch(self):
        if self.anchorOverRide:
            return self.anchorOverRide
        else:
            return self.anchor
    anch = property(_getAnch, _setAnch)

    def _getXShift(self):
        return self._xShift

    def _setXShift(self, theXShift):
        self._xShift = theXShift

    def _delXShift(self):
        self._xShift = None

    xShift = property(_getXShift, _setXShift, _delXShift)

    def _getYShift(self):
        return self._yShift

    def _setYShift(self, theYShift):
        self._yShift = theYShift

    def _delYShift(self):
        self._yShift = None

    yShift = property(_getYShift, _setYShift, _delYShift)

    def _getRotate(self):
        return self._rotate

    def _setRotate(self, theRotate):
        gm = ['GramTikzStyle._setRotate()']
        try:
            theRotate = float(theRotate)
        except:
            gm.append("The rotate, in degrees, should a number.")
            raise GramError(gm)
        if theRotate > 360 or theRotate < -360:
            gm.append("There is no point to having the rotate (%s)" %
                      theRotate)
            gm.append("more than one revolution around the circle, is there?")
            raise GramError(gm)
        self._rotate = theRotate

    def _delRotate(self):
        self._rotate = None

    rotate = property(_getRotate, _setRotate, _delRotate)

    def _getShape(self):
        return self._shape

    def _setShape(self, theShape):
        goodShapes = ['circle', 'rectangle']
        if theShape not in goodShapes:
            gm = ['GramGraphic._setShape()']
            gm.append("You can only set property 'shape' to one of")
            gm.append("%s" % goodShapes)
            gm.append("Got attempt to set to '%s'" % theShape)
            raise GramError(gm)
        self._shape = theShape

    def _delShape(self):
        self._shape = False

    shape = property(_getShape, _setShape, _delShape)

    def _getLineThickness(self):
        #if self._lineThickness is not None:
        return self._lineThickness
        #else:
        #    return self.defaultLineThickness

    def _setLineThickness(self, theLineThickness):
        gm = ['GramTikzStyle._setLineThickness()']
        isOk = False
        if theLineThickness in Gram._goodLineThicknesses:
            isOk = True
        if not isOk:
            try:
                theLineThickness = float(theLineThickness)
            except:
                gm.append('The lineThickness should be one of %s' %
                          Gram._goodLineThicknesses)
                gm.append(
                    "or the lineThickness should be a positive float, the width in postscript points")
                raise GramError(gm)
            if theLineThickness > 100.:
                gm.append(
                    "property 'lineThickness' has an arbitrary upper limit of 100 pt.")
                gm.append("Got attempt to set to '%s'" % theLineThickness)
                raise GramError(gm)

        self._lineThickness = theLineThickness

    def _delLineThickness(self):
        self._lineThickness = None

    lineThickness = property(
        _getLineThickness, _setLineThickness, _delLineThickness)

    def _checkCapVal(self, newVal):
        # goodEnds = ['', '<', '>', '<<', '>>', '|', '|*',
        #            '[', ']', '(', ')', 'o', '*', 'oo', '**',
        #            'c', 'cc', 'C', '|<', '>|', '|<*', '>|*']
        goodCaps = ['rect', 'butt', 'round']
        if newVal not in goodCaps:
            gm = ['GramTikzStyle._checkCapVal()']
            gm.append("You can only set the line cap to one of ")
            gm.append("%s" % goodCaps)
            gm.append("   %12s  %s" %
                      ('empty string, or butt', 'Flush square ends'))
            gm.append("   %12s  %s" % ('round', 'Extended, rounded'))
            gm.append("   %12s  %s" % ('rect', 'Square extended'))
            gm.append("Got %s" % newVal)
            raise GramError(gm)
        return True

    def _getCap(self):
        return self._cap

    def _setCap(self, newVal):
        if self._checkCapVal(newVal):
            self._cap = newVal
    cap = property(_getCap, _setCap)

    def _checkLineStyleVal(self, newVal):
        # goodLineStyles = [None, 'solid', 'dotted', 'densely dotted',
        #'loosely dotted', 'dashed', 'densely dashed', 'loosely dashed' ]
        if newVal not in self.goodLineStyles:
            gm = ['GramTikzStyle._checkLineStyleVal()']
            gm.append("You can only set the line style to one of ")
            gm.append("%s" % goodLineStyles)
            gm.append("Got %s" % newVal)
            raise GramError(gm)
        return True

    def _getLineStyle(self):
        return self._lineStyle

    def _setLineStyle(self, newVal):
        if self._checkLineStyleVal(newVal):
            self._lineStyle = newVal

    def _delLineStyle(self):
        self._lineStyle = None
    lineStyle = property(_getLineStyle, _setLineStyle, _delLineStyle)

    def _getTextHeight(self):
        return self._textHeight

    def _setTextHeight(self, newVal):
        self._textHeight = newVal

    def _delTextHeight(self):
        self._textHeight = None
    textHeight = property(_getTextHeight, _setTextHeight, _delTextHeight)

    def _getTextDepth(self):
        return self._textDepth

    def _setTextDepth(self, newVal):
        self._textDepth = newVal

    def _delTextDepth(self):
        self._textDepth = None
    textDepth = property(_getTextDepth, _setTextDepth, _delTextDepth)

    def _getTextWrapWidth(self):
        return self._textWrapWidth

    def _setTextWrapWidth(self, newVal):
        try:
            nV = float(newVal)
        except:
            if newVal is None:
                nV = newVal
            else:
                raise GramError(
                    "_setTextWrapWidth, should set to a float or None.")
        self._textWrapWidth = nV

    def _delTextWrapWidth(self):
        self._textWrapWidth = None
    textWrapWidth = property(_getTextWrapWidth, _setTextWrapWidth, _delTextWrapWidth)

    def _getTextAlign(self):
        return self._textAlign

    def _setTextAlign(self, newVal):
        if newVal not in Gram._goodTextAligns:
            gm = ["Set textAlign."]
            gm.append("Should be one of %s" % Gram._goodTextAligns)
            gm.append(f"Got '{newVal}'")
            raise GramError(gm)
        else:
            self._textAlign = newVal

    def _delTextAlign(self):
        self._textAlign = None
    textAlign = property(
        _getTextAlign, _setTextAlign, _delTextAlign)

    def _getInnerSep(self):
        return self._innerSep

    def _setInnerSep(self, newVal):
        #assert newVal.endswith('pt')
        self._innerSep = newVal

    def _delInnerSep(self):
        self._innerSep = None
    innerSep = property(_getInnerSep, _setInnerSep, _delInnerSep)

    def _getRoundedCorners(self):
        return self._roundedCorners

    def _setRoundedCorners(self, newVal):
        #assert newVal.endswith('pt')
        self._roundedCorners = newVal

    def _delRoundedCorners(self):
        self._roundedCorners = None
    roundedCorners = property(
        _getRoundedCorners, _setRoundedCorners, _delRoundedCorners)

    def getTikzOptions(self):  # GramTikzStyle
        gm = ["GramTikzStyle.getTikzOptions()  self=%s" % self]
        #print(gm[0])
        #print(f"    xx-- color:{self.color}, draw:{self.draw}, fill:{self.fill}")

        options = []
        # or self.font=='helvetica':
        # extraSffamilyHasBeenWritten = False
        if self.textSize or self.textFamily or self.textSeries or self.textShape:
            fStr = 'font='
            if self.textSize:
                #print(f"getTikzOptions() Got textSize {self.textSize}")
                # if self.textFamily == "sffamily":
                #     fStr += '\\sffamily\\%s' % self.textSize
                #     extraSffamilyHasBeenWritten = True
                # elif self.defaultTextFamily == "sffamily":
                #     fStr += '\\sffamily\\%s' % self.textSize
                #     extraSffamilyHasBeenWritten = True
                # else:
                fStr += '\\%s' % self.textSize

            if self.textFamily:
                # print(f"getTikzOptions() Got textFamily {self.textFamily}")
                #if self.textFamily != self.defaultTextFamily:
                fStr += '\\%s' % self.textFamily

            # if self.name == "tikzPictureDefaults":
            #     fStr += '\\%s' % self.defaultTextFamily
            if self.textSeries:
                # If default sffamily and bfseries, then we need to repeat sffamily
                # if self.textFamily == "sffamily" and not extraSffamilyHasBeenWritten:
                #     fStr += '\\sffamily\\%s' % self.textSeries
                # elif self.defaultTextFamily == "sffamily" and not extraSffamilyHasBeenWritten:
                #     fStr += '\\sffamily\\%s' % self.textSeries
                # else:
                fStr += '\\%s' % self.textSeries
            if self.textShape:
                fStr += '\\%s' % self.textShape
            # print(f"style getTikzOptions() fStr is {fStr}")
            options.append(fStr)
        if self.color:
            if isinstance(self, GramRect):
                gm.append('This week, "color" is not for GramRect objects')
                raise GramError(gm)

            if self.color is True:
                # options.append("color")
                pass
            else:
                assert isinstance(self.color, GramColor)
                if self.color.value:
                    if self.color.transparent:
                        options.append("color=%s" % CSS4_COLORS[self.color.color][2])
                        if isinstance(self, GramText):
                            options.append("text opacity=%s" % self.color.value)
                        else:
                            options.append("opacity=%s" % self.color.value)
                    else:
                        options.append("color=%s!%s" % (CSS4_COLORS[self.color.color][2], self.color.value[2:]))
                else:
                    options.append("color=%s" % CSS4_COLORS[self.color.color][2])


        if self.draw:
            if isinstance(self, GramText) or isinstance(self, GramRect):
                pass
            else:
                gm.append('This week, "draw" is only for GramText or GramRect objects')
                raise GramError(gm)

            if self.draw is True:
                options.append("draw")  # black
            else:
                assert isinstance(self.draw, GramColor)
                if self.draw.value:
                    if self.draw.transparent:
                        options.append("draw=%s" % CSS4_COLORS[self.draw.color][2])
                        options.append("draw opacity=%s" % self.draw.value)
                    else:
                        options.append("draw=%s!%s" % (CSS4_COLORS[self.draw.color][2], self.draw.value[2:]))
                else:
                    options.append("draw=%s" % CSS4_COLORS[self.draw.color][2])


        if self.fill:
            # options.append("fill=%s" % self.fill.color)
            # if self.fill.transparent and self.fill.value:
            #     options.append("fill opacity=%s" % self.fill.value)

            # Note that GramRect is a subclass of GramLine
            if isinstance(self, GramRect):
                pass
            elif isinstance(self, GramLine):
                gm.append('This week, "fill" does not make sense for GramLine objects')
                raise GramError(gm)

            if self.fill is True:
                options.append("fill")
            else:
                assert isinstance(self.fill, GramColor)
                if self.fill.value:
                    if self.fill.transparent:
                        options.append("fill=%s" % CSS4_COLORS[self.fill.color][2])
                        options.append("fill opacity=%s" % self.fill.value)
                    else:
                        options.append("fill=%s!%s" % (CSS4_COLORS[self.fill.color][2], self.fill.value[2:]))
                else:
                    options.append("fill=%s" % CSS4_COLORS[self.fill.color][2])

            # Hack to overcome bug that makes text have the same opacity as fill opacity.
            # if self.fill.value and self.fill.transparent:
            #    options.append("text opacity=1.0")


        if self.anch:
            options.append("anchor=%s" % self.anch)
        elif self.anchor:
            options.append("anchor=%s" % self.anchor)
        if self.xShift:
            options.append("xshift=%.3fcm" % self.xShift)
        if self.yShift:
            options.append('yshift=%.3fcm' % self.yShift)
        if self.rotate:
            options.append("rotate=%.1f" % self.rotate)
        if self.shape:
            options.append("shape=%s" % self.shape)
        if self.lineThickness is not None:
            if isinstance(self.lineThickness, str):
                options.append("%s" % self.lineThickness)
            else:
                options.append("line width=%spt" % self.lineThickness)
        if self.cap:
            options.append("line cap=%s" % self.cap)
        if self.lineStyle:
            options.append("%s" % self.lineStyle)
        if self.textHeight:
            options.append("text height=%.3fcm" % self.textHeight)
        if self.textDepth or self.textDepth == 0.0:
            options.append("text depth=%.3fcm" % self.textDepth)
        if self.textWrapWidth:
            options.append("text width=%.3fcm" % self.textWrapWidth)
        if self.textAlign:
            options.append("align=%s" % self.textAlign)
        if self.innerSep is not None:
            options.append("inner sep=%scm" % self.innerSep)
        if self.roundedCorners is not None:
            options.append("rounded corners=%s" % self.roundedCorners)
        # print "GramTikzStyle.getTikzOptions() returning %s" % options
        return options

    def getSvgOptions(self):   # GramTikzStyle
        gm = ["GramTikzStyle.getSvgOptions()"]

        options = []
        # or self.font=='helvetica':
        if self.textSize or self.textFamily or self.textSeries or self.textShape:
            fStr = 'font='
            if self.textSize:
                fStr += '\\%s' % self.textSize
            if self.textFamily:  # or self.font=='helvetica':
                # if self.font == 'helvetica':
                #    fStr += '\\%s' % 'sffamily'
                # elif self.textFamily:
                fStr += '\\%s' % self.textFamily
            if self.textSeries:
                fStr += '\\%s' % self.textSeries
            if self.textShape:
                fStr += '\\%s' % self.textShape
            options.append(fStr)

        #print("GramTikzStyle.getSvgOptions() self is %s" % self)
        #print("    self.color is %s, self.draw is %s, self.fill= %s" % (self.color, self.draw, self.fill))
        if self.color:
            # print("    GramTikzStyle.getSvgOptions() self is %s,  self.color is %s" % (self, self.color))

            if isinstance(self, GramRect):
                gm.append("This week, 'color' is not for GramRect objects")
                gm.append("Got self: %s, color: %s" % (self, self.color))
                raise GramError(gm)

            if self.color == True:
                options.append('stroke="black"')
            else:
                assert isinstance(self.color, GramColor)
                options += self.color.getSvgOptions()
        elif self.color in [False, None]:
            if isinstance(self, GramRect):
                pass                           # <----- ??????  Should be error?
            else:
                options.append('stroke="black"')


        if self.draw:
            # "draw" is used for GramText objects, but we should not end up here,
            # because it is handled by GramText.getSvg()
            if isinstance(self, GramText):
                gm.append("Setting draw for a GramText")
                gm.append("Programming error -- this should not happen.")
                raise GramError(gm)
            elif isinstance(self, GramRect):
                pass
            else:
                gm.append("This week, 'draw' is only for GramText and GramRect objects")
                gm.append("Got self: %s, draw: %s" % (self, self.draw))
                raise GramError(gm)

            if self.draw == True:
                options.append('stroke="black"')
            else:
                assert isinstance(self.draw, GramColor)
                dOptions = self.draw.getSvgOptions()
                # print(f"GramTikzStyle() draw options {dOptions}")
                options += dOptions

        if self.fill:    # GramTikzStyle.getSvgOptions
            # fill for GramText is handled by GramText.getSvg()
            if isinstance(self, GramText):
                gm.append("Setting fill for a GramText")
                gm.append("Programming error -- this should not happen.")
                raise GramError(gm)
            elif isinstance(self, GramRect):
                pass
            elif isinstance(self, GramSvgMarker):
                pass
            elif isinstance(self, GramLine):
                gm.append('This week, "fill" does not make sense for GramLine objects')
                gm.append(f"self is {self}")
                raise GramError(gm)


            # if not isinstance(self, GramRect):
            #     gm.append(f'Setting the "fill" does not work for {self} objects')
            #     raise GramError(gm)

            # print(f"GramTikzStyle.getSvgOptions() self is {self}, color: {self.color} fill is {self.fill}")
            if self.fill == True:
                options.append('fill="black"')
            else:
                assert isinstance(self.fill, GramColor)
                options += self.fill.getSvgOptions(stroke="fill")
        elif self.fill in [False, None]:
            options.append('fill="none"')   # needed, else fill is black

        #if self.anch:
        #    options.append('anchor=%s' % self.anch)
        #elif self.anchor:
        #    options.append('anchor=%s' % self.anchor)

        if self.xShift:
            options.append('xshift=%.3fcm' % self.xShift)
        if self.yShift:
            options.append('yshift=%.3fcm' % self.yShift)

        if self.rotate:
            negRot = -self.rotate
            options.append('transform="rotate(%.1f)"' % negRot)
        # if self.shape:
        #     options.append('shape=%s' % self.shape)

        if self.lineThickness is not None:
            #if isinstance(self.lineThickness, str):
            myLineThickness = cmForLineThickness(self.lineThickness)
            myLineThickness = self.svgPxForCmF(myLineThickness)
            options.append('stroke-width="%.2f"' % myLineThickness)
        else:
            if self.tikzPictureDefaults.lineThickness:
                myLineThickness = cmForLineThickness(self.tikzPictureDefaults.lineThickness)
            else:
                # TikZ default is thin, which is 0.4 pts
                myLineThickness = cmForLineThickness('thin')
            myLineThickness = self.svgPxForCmF(myLineThickness)
            options.append('stroke-width="%.2f"' % myLineThickness)

        if self.cap:
            # tikz caps ['rect', 'butt', 'round']
            # svg caps butt square round
            if self.cap:
                if self.cap == 'rect':
                    options.append('stroke-linecap="square"')
                else:
                    options.append('stroke-linecap="%s"' % self.cap)
        if self.lineStyle:
            myDashArray = svgDasharrayForLinestyle(self.lineStyle)
            options.append('stroke-dasharray="%s"' % myDashArray)
        # if self.textHeight:
        #     options.append('text height=%.3fcm' % self.textHeight)
        # if self.textDepth:
        #     options.append('text depth=%.3fcm' % self.textDepth)
        # if self.textWrapWidth:
        #     options.append('text width=%.3fcm' % self.textWrapWidth)
        # if self.innerSep is not None:
        #     options.append('inner sep=%scm' % self.innerSep)
        # if self.roundedCorners is not None:
        #     options.append('rounded corners=%s' % self.roundedCorners)
        # print 'GramTikzStyle.getSvgOptions() returning %s' % options
        return options

    def getDefString(self):
        assert self.name
        # print(f"getDefString() self.name is {self.name}")
        options = self.getTikzOptions()
        return "{%s}" % ','.join(options)

    def dump(self):
        print("GramTikzStyle.dump() here")
        import inspect
        myMembers = inspect.getmembers(self)
        # print myMembers    #2-tuples
        for it in myMembers:
            if it[0].startswith("_"):
                if it[0] == '__class__':
                    print("  CLASS: %s" % it[1])
            else:
                if inspect.ismethod(it[1]):
                    # print "method: %s" % it[0]
                    pass
                else:

                    it1 = getattr(self, it[0])
                    print("  %-20s   %s" % (it[0], it1))


class GramGraphic(GramTikzStyle):

    """Base class for Gram graphic objects."""

    def __init__(self):  # GramGraphic
        GramTikzStyle.__init__(self)
        # cA is the GramCoord where the Graphic is put.
        self.cA = None
        self.comment = None
        self.style = None
        self.myStyle = None
        self.bb = [0.0] * 4
        self.gId = None
        self.titleAttribute = None

    def pdf(self):
        gm = ["pdf() method called on a GramGraphic instance"]
        gm.append("That won't work.")
        gm.append("Call it on a Gram instance")
        raise GramError(gm)

    def setGIdAndAddToDict(self, typeString):
        if self.gId:
            assert self.gForGIdDict[self.gId] == self
        else:
            self.gId = "%s-%i" % (typeString, self.gIdCounter)
            self.gIdCounter += 1
            self.gForGIdDict[self.gId] = self

    def setPositions(self):
        for g in self.graphics:
            g.setPositions()

    def setBB(self):
        raise GramError("setBB() called.  self is %s" % self)

    def getTikzOptions(self):
        dbug = False
        if dbug:
            if hasattr(self, "rawText"):
                print("------- GramGraphic.getTikzOptions()  rawText=%s" % self.rawText)
            else:
                print(f"------- GramGraphic.getTikzOptions() {self}")
            print("    self.draw is %s" % self.draw)
        options = []

        # First get the style string.
        # style and myStyle are just strings.  They are keys to
        # self.styleDict, but often we do not need that.

        theStyleString = ''
        theStyleObject = None
        if self.style or self.myStyle:
            if self.myStyle:
                theStyleString = self.myStyle
            else:
                theStyleString = self.style

            # This next bit is the first part of a hack to avoid repetition of
            # sffamily.
            try:
                theStyleObject = self.styleDict[theStyleString]
            except KeyError:
                print(self.styleDict)
                print(self.styleDict.keys())
                print("styleDict can't find style '%s'" % theStyleString)
                raise
            # print " *** theStyleObject.textFamily is %s" % theStyleObject.textFamily
            # print("getTikzOptions()  A  theStyleObject.anchor is %s" % theStyleObject.anchor)
            options.append(theStyleString)
        if dbug:
            print("    getTikzOptions()  B  options from style = %s" % options)

        # Then get options not associated with the style from the style string.
        nonStyleOptions = GramTikzStyle.getTikzOptions(self)
        if dbug:
            print("    getTikzOptions()  C  nonStyleOptions = %s" % nonStyleOptions)

        # Avoid repetition of font=\sffamily and anchor
        booger = r'font=\sffamily'
        if theStyleObject and theStyleObject.textFamily == 'sffamily':
            if booger in nonStyleOptions:
                nonStyleOptions.remove(booger)

        # Here is a bit of a hack, to overcome what looks a lot like a bug.  If
        # the style says fill=white and the options include a color, then the
        # fill becomes that color, when I just wanted the text to be that color,
        # not the background.  So I have to add fill to the options.
        if theStyleObject:
            if theStyleObject.fill:
                if isinstance(theStyleObject.fill, GramColor):
                    nonStyleOptions.append("fill=%s" % theStyleObject.fill.color)

        # if theStyleObject and theStyleObject.anchor:
        #    booger = "anchor=%s" % theStyleObject.anchor
        #    if booger in nonStyleOptions:
        #        nonStyleOptions.remove(booger)

        options += nonStyleOptions
        if dbug:
            print("    getTikzOptions()  D  (final) options = %s" % options)
        return options

    def getSvgOptions(self):  # GramGraphic
        #print("------- GramGraphic.getSvgOptions()  self=%s" % self)
        options = []

        # First get the style string.
        # style and myStyle are just strings.  They are keys to
        # self.styleDict, but often we do not need that.

        theStyleString = ''
        theStyleObject = None
        if self.style or self.myStyle:
            if self.myStyle:
                theStyleString = self.myStyle
            else:
                theStyleString = self.style

            # This next bit is the first part of a hack to avoid repetition of
            # sffamily.  Is it still needed?
            try:
                theStyleObject = self.styleDict[theStyleString]
            except KeyError:
                print(self.styleDict)
                print(self.styleDict.keys())
                print("styleDict can't find style '%s'" % theStyleString)
                raise
            # print " *** theStyleObject.textFamily is %s" % theStyleObject.textFamily
            # print("GramGraphic.getSvgOptions()  A  theStyleObject.anchor is %s" %
            # theStyleObject.anchor)
            options.append(theStyleString)
        # print("GramGraphic.getSvgOptions()  B  style (ie class) options = %s" % options)

        # Then get options not associated with the style from the style string.
        # if isinstance(self, GramSvgMarker):
        #     print("FIXME: by-passing getSvgOptions for GramSvgMarker")
        #     nonStyleOptions = []
        # else:
        nonStyleOptions = GramTikzStyle.getSvgOptions(self)
        # print("GramGraphic.getSvgOptions()  C  nonStyleOptions = %s" % nonStyleOptions)

        # Avoid repetition of font=\sffamily and anchor
        # booger = 'font=\\sffamily'
        # if theStyleObject and theStyleObject.textFamily == 'sffamily':
        #     if booger in nonStyleOptions:
        #         nonStyleOptions.remove(booger)

        # if theStyleObject and theStyleObject.anchor:
        #    booger = "anchor=%s" % theStyleObject.anchor
        #    if booger in nonStyleOptions:
        #        nonStyleOptions.remove(booger)

        options += nonStyleOptions
        # print("GramGraphic.getSvgOptions()  D  (final) options = %s" % options)
        return options

    def getTikz(self):
        ss = []
        ss.append('%% This is from GramGraphic.getTikz()')
        if self.comment:
            ss.append("%% %s" % self.comment)
        for gr in self.graphics:
            ss.append(gr.getTikz())
        return '\n'.join(ss)

    def getSvg(self):
        ss = []
        #ss.append('%% This is from GramGraphic.getSvg()')
        if self.comment:
            ss.append("<!--  %s -->" % self.comment)
        for gr in self.graphics:
            ss.append(gr.getSvg())
        return '\n'.join(ss)

    def getDraw(self):
        ret = self.draw
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.draw
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.draw
        return ret

    def getTextSize(self):
        ret = self.textSize
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.textSize
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.textSize
        return ret

    def getTextFamily(self):
        ret = self.textFamily
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.textFamily
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.textFamily
        if ret is None and self.tikzPictureDefaults:
            ret = self.tikzPictureDefaults.textFamily
        # if ret is None and self.defaultTextFamily:
        #     ret = self.defaultTextFamily
        return ret

    def getTextSeries(self):
        ret = self.textSeries
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.textSeries
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.textSeries
        return ret

    def getTextShape(self):
        ret = self.textShape
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.textShape
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.textShape
        return ret

    def getTextAlign(self):
        ret = self.textAlign
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.textAlign
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.textAlign
        return ret

    def getColor(self):
        ret = self.color
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.color
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.color
        return ret

    # def getDraw(self):
    #    pass

    def getFill(self):
        ret = self.fill
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.fill
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.fill
        return ret

    def getAnch(self):
        ret = self.anch
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.anch
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.anch
        return ret

    def getXShift(self):
        ret = self.xShift
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.xShift
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.xShift
        return ret

    def getYShift(self):
        ret = self.yShift
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.yShift
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.yShift
        return ret

    # def getShape(self):
    #    pass

    def getRotate(self):
        ret = self.rotate
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.rotate
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.rotate
        return ret

    def getLineThickness(self):
        ret = self.lineThickness
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.lineThickness
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.lineThickness
        if ret is None and self.tikzPictureDefaults:
            ret = self.tikzPictureDefaults.lineThickness
        if ret is None:
            ret = 'thin'
        return ret

    def getCap(self):
        ret = self.cap
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.cap
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.cap
        return ret

    def getLineStyle(self):
        ret = self.lineStyle
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.lineStyle
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.lineStyle
        return ret

    # def getTextHeight(self):
    #    pass
    # def getTextDepth(self):
    #    pass

    def getTextWrapWidth(self):
        ret = self.textWrapWidth
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.textWrapWidth
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.textWrapWidth
        return ret


    def getInnerSep(self):
        ret = self.innerSep
        if ret is None and self.myStyle:
            st = self.styleDict[self.myStyle]
            ret = st.innerSep
        if ret is None and self.style:
            st = self.styleDict[self.style]
            ret = st.innerSep
        if ret is None:
            ret = self.defaultInnerSep
        if ret is None:
            # We should never be here.
            gm = ["GramGraphic GramText.getInnerSep()"]
            gm.append("rawText %s" % self.rawText)
            gm.append("getInnerSep() is None")
            raise GramError(gm)
        return ret

    def pdf(self):
        gm = ["GramGraphic.pdf() is turned off"]
        gm.append("pdf() should be called by Gram or a subclass, not called by GramGraphic")
        gm.append(f"self is {self}")
        raise GramError(gm)

    def svg(self, extraMarginHack=1.0, writeWidthHeight=False, fixTextOverlaps=False):
        gm = ["GramGraphic.svg() is turned off"]
        gm.append("svg() should be called by Gram or a subclass, not called by GramGraphic")
        gm.append(f"self is {self}")
        raise GramError(gm)

class GramSvgMarker(GramGraphic):

    _counter = 0

    def __init__(self, markerShape, markerRelativeSize=None):
        GramGraphic.__init__(self)
        #assert markerShape in ['+', 'x', '*', '-', '|', 'o', 'asterisk',  ## 'star', 'oplus', 'oplus*',
        #                       ##'otimes', 'otimes*',
        #                        'square', 'square*', 'triangle',
        #                       'triangle*', 'diamond', 'diamond*' ##, 'pentagon', 'pentagon*']
        #assert markerShape in ['+', 'x', '*', 'asterisk']
        self.markerShape = markerShape
        self.markerRelativeSize = markerRelativeSize
        markerIdBaseDict = {
            '+': 'gmCross',
            'x': 'gmX',
            '*': 'gmCircF',
            '-': 'gmDash',
            '|': 'gmBar',
            'o': 'gmCirc',
            'asterisk': 'gmAsterisk',
            'square': 'gmSquare',
            'square*': 'gmSquareF',
            'triangle': 'gmTriangle',
            'triangle*': 'gmTriangleF',
            'diamond': 'gmDiamond',
            'diamond*': 'gmDiamondF',
        }
        self.markerId = markerIdBaseDict[self.markerShape]
        self.markerId += "_%i" % GramSvgMarker._counter
        GramSvgMarker._counter += 1
        #self.haveDoneResetMarkerId = False

    def getTikz(self):
        pass

    def getSvg(self):    # GramSvgMarker
        gm = ["GramSvgMarker.getSvg() markerShape %s, markerId %s, color %s, fill %s" % (
            self.markerShape, self.markerId, self.color, self.fill)]
        #print gm[0]
        if not self.color and not self.fill:
            self.fill = 'black'
            gm.append("... setting fill to black")
        elif self.color and not self.fill:
            self.fill = self.color
            gm.append("... setting fill to the color")
        elif self.fill and not self.color:
            self.color = 'black'
            gm.append("... setting the color to the fill")

        # if len(gm) == 2:
        #     print gm[1]

        #mySc = 0.035 * self.svgPxForCm
        mySc = 0.038 * self.svgPxForCm

        if self.markerRelativeSize:
            mySc *= self.markerRelativeSize

        mySc2 = mySc * 2
        mySc4 = mySc * 4
        myScR = mySc * 1.7
        ss = []
        ss.append('  <marker id="%s" markerWidth="%.2f" markerHeight="%.2f" refX="%.2f" refY="%.2f">' % (
            self.markerId, mySc4, mySc4, mySc2, mySc2))


        if self.markerShape == '*':   # filled circle
            ss2 = []
            ss2.append('    <circle cx="%.2f" cy="%.2f" r="%.2f"' % (
                mySc2, mySc2, myScR))
            # if self.color:
            #     ss2.append('stroke="%s"' % self.color.svgColor)
            #     if self.color.svgColorOpacity:
            #         ss2.append('stroke-opacity="%s"' % self.color.svgColorOpacity)
            # else:
            #     if not self.fill:
            #         #gm.append("No color (OK), but also no fill --- invisible?")
            #         #raise GramError(gm)
            #         #self.fill = 'black'
            #         pass
            #     #ss2.append('stroke="black"')
            # if self.fill:
            #     ss2.append('fill="%s"' % self.fill.svgColor)
            #     if self.fill.svgColorOpacity:
            #         ss2.append('fill-opacity="%s"' % self.fill.svgColorOpacity)
            # else:
            #     ss2.append('fill="black"')
            ss2 += self.getSvgOptions()
            ss2.append('/>')
            ss.append(' '.join(ss2))

        elif self.markerShape == '+':
            ss2 = []
            ss2.append('    <path d="M%.2f,0 L%.2f,%.2f M0,%.2f L%.2f,%.2f"' % (
                mySc2, mySc2, mySc4, mySc2, mySc4, mySc2))
            # if self.color:
            #     ss2.append('stroke="%s"' % self.color.svgColor)
            #     if self.color.svgColorOpacity:
            #         ss2.append('stroke-opacity="%s"' % self.color.svgColorOpacity)
            # else:
            #     ss2.append('stroke="black"')
            ss2 += self.getSvgOptions()
            ss2.append('/>')
            ss.append(' '.join(ss2))

        elif self.markerShape == 'x':
            mySc01 = mySc * 0.1
            mySc39 = mySc * 3.9
            ss2 = []
            ss2.append('    <path d="M %.2f,%.2f L %.2f,%.2f M %.2f,%.2f L %.2f,%.2f"' % (
                mySc01, mySc01, mySc39, mySc39, mySc39, mySc01, mySc01, mySc39))
            # if self.color:
            #     ss2.append('stroke="%s"' % self.color.svgColor)
            #     if self.color.svgColorOpacity:
            #         ss2.append('stroke-opacity="%s"' % self.color.svgColorOpacity)
            # else:
            #     ss2.append('stroke="black"')
            ss2 += self.getSvgOptions()
            ss2.append('/>')
            ss.append(' '.join(ss2))

        elif self.markerShape == '-':
            ss2 = []
            ss2.append('    <path d="M 0,%.2f L%.2f,%.2f"' % (
                mySc2, mySc4, mySc2))
            # if self.color:
            #     ss2.append('stroke="%s"' % self.color.svgColor)
            #     if self.color.svgColorOpacity:
            #         ss2.append('stroke-opacity="%s"' % self.color.svgColorOpacity)
            # else:
            #     ss2.append('stroke="black"')
            ss2 += self.getSvgOptions()
            ss2.append('/>')
            ss.append(' '.join(ss2))

        elif self.markerShape == '|':
            ss2 = []
            ss2.append('    <path d="M%.2f,0 L%.2f,%.2f"' % (
                mySc2, mySc2, mySc4))
            # if self.color:
            #     ss2.append('stroke="%s"' % self.color.svgColor)
            #     if self.color.svgColorOpacity:
            #         ss2.append('stroke-opacity="%s"' % self.color.svgColorOpacity)
            # else:
            #     ss2.append('stroke="black"')
            ss2 += self.getSvgOptions()
            ss2.append('/>')
            ss.append(' '.join(ss2))

        elif self.markerShape == 'o':   # empty circle
            ss2 = []
            ss2.append('    <circle cx="%.2f" cy="%.2f" r="%.2f"' % (
                mySc2, mySc2, myScR))
            if self.color:
                ss2.append('stroke="%s"' % self.color.color)
                if self.color.value and self.color.transparent:
                    ss2.append('stroke-opacity="%s"' % self.color.value)
            else:
                ss2.append('stroke="black"')
            ss2.append('fill="none"')
            # ss2 += self.getSvgOptions()
            ss2.append('/>')
            ss.append(' '.join(ss2))

        elif self.markerShape == 'asterisk':
            ss2 = []
            ss2.append('    <path d="M %.2f,%.2f L %.2f,%.2f M %.2f,%.2f L %.2f,%.2f M %.2f,%.2f L %.2f,%.2f"' % (
                mySc * 3.732, mySc,
                mySc * 0.268, mySc * 3.,
                mySc2, 0,
                mySc2, mySc4,
                mySc * 0.268, mySc,
                mySc * 3.732, mySc * 3.))
            # if self.color:
            #     ss2.append('stroke="%s"' % self.color.svgColor)
            #     if self.color.svgColorOpacity:
            #         ss2.append('stroke-opacity="%s"' % self.color.svgColorOpacity)
            # else:
            #     ss2.append('stroke="black"')
            ss2 += self.getSvgOptions()
            ss2.append('/>')
            ss.append(' '.join(ss2))

        elif self.markerShape.startswith('square'):
            mySc03 = mySc * 0.3
            mySc37 = mySc * 3.7
            ss2 = []
            ss2.append('    <path d="M%.2f,%.2f L%.2f,%.2f %.2f,%.2f %.2f,%.2f z"' % (
                mySc03, mySc03, mySc37, mySc03, mySc37, mySc37, mySc03, mySc37))
            if self.color:
                ss2.append('stroke="%s"' % self.color.color)
                if self.color.value and self.color.transparent:
                    ss2.append('stroke-opacity="%s"' % self.color.value)
            #else:
            #    ss2.append('stroke="black"')
            isFilled = False
            if self.markerShape.endswith('*'):
                isFilled = True
            if not self.color and not isFilled:
                ss2.append('stroke="black"')
            if isFilled:
                if self.fill:
                    ss2.append('fill="%s"' % self.fill.color)
                    if self.fill.value and self.fill.transparent:
                        ss2.append('fill-opacity="%s"' % self.fill.value)
                else:
                    ss2.append('fill="black"')
            else:
                ss2.append('fill="none"')
            ss2.append('/>')
            ss.append(' '.join(ss2))

        elif self.markerShape.startswith('triangle'):
            mySc37 = mySc * 3.7
            ss2 = []
            ss2.append('    <path d="M%.2f,0 L%.2f,%.2f 0,%.2f z"' % (
                mySc2, mySc4, mySc37, mySc37))
            if self.color:
                ss2.append('stroke="%s"' % self.color.color)
                if self.color.value and self.color.transparent:
                    ss2.append('stroke-opacity="%s"' % self.color.value)
            #else:
            #    ss2.append('stroke="black"')
            isFilled = False
            if self.markerShape.endswith('*'):
                isFilled = True
            if not self.color and not isFilled:
                ss2.append('stroke="black"')
            if isFilled:
                if self.fill:
                    ss2.append('fill="%s"' % self.fill.color)
                    if self.fill.value and self.fill.transparent:
                        ss2.append('fill-opacity="%s"' % self.fill.value)
                else:
                    ss2.append('fill="black"')
            else:
                ss2.append('fill="none"')
            ss2.append('/>')
            ss.append(' '.join(ss2))

        elif self.markerShape.startswith('diamond'):
            ss2 = []
            ss2.append('    <path d="M%.2f,0 L%.2f,%.2f %.2f,%.2f 0,%.2f z"' % (
                mySc2, mySc4, mySc2, mySc2, mySc4, mySc2))
            if self.color:
                ss2.append('stroke="%s"' % self.color.color)
                if self.color.value and self.color.transparent:
                    ss2.append('stroke-opacity="%s"' % self.color.value)
            #else:
            #    ss2.append('stroke="black"')
            isFilled = False
            if self.markerShape.endswith('*'):
                isFilled = True
            if not self.color and not isFilled:
                ss2.append('stroke="black"')
            if isFilled:
                if self.fill:
                    ss2.append('fill="%s"' % self.fill.color)
                    if self.fill.value and self.fill.transparent:
                        ss2.append('fill-opacity="%s"' % self.fill.value)
                else:
                    ss2.append('fill="black"')
            else:
                ss2.append('fill="none"')
            ss2.append('/>')
            ss.append(' '.join(ss2))



        ss.append('  </marker>\n')
        return '\n'.join(ss)

class GramGrid(GramGraphic):

    def __init__(self, llx, lly, urx, ury, color='gray'):
        GramGraphic.__init__(self)
        assert isinstance(llx, int)
        assert isinstance(lly, int)
        assert isinstance(urx, int)
        assert isinstance(ury, int)

        assert urx > llx
        assert ury > lly

        self.llx = llx
        self.lly = lly
        self.urx = urx
        self.ury = ury
        self.color = color

    def getTikz(self):
        ss = []
        # if self.comment:
        #    ss.append("%% %s" % self.comment)
        ss.append("\\draw[%s,very thin] (%i,%i) grid (%i,%i);" %
                  (self.color.color, self.llx, self.lly, self.urx, self.ury))
        for gr in self.graphics:
            ss.append(gr.getTikz())
        return '\n'.join(ss)

    def getSvg(self):
        ss = []
        ss.append("\n<!-- grid -->\n")
        if self.color.transparent:
            ss.append('<path stroke="%s" stroke-opacity="%s" stroke-width="0.5" d="' % (
                      self.color.color, self.color.value))
        else:
            ss.append('<path stroke="%s" stroke-width="0.5" d="' % self.color.color)
        for colNum in range(self.llx, self.urx + 1):
            ss.append('M %.1f %.1f L %.1f %.1f ' % (
                self.svgPxForCmF(colNum), -self.svgPxForCmF(self.lly),
                self.svgPxForCmF(colNum), -self.svgPxForCmF(self.ury)))
        for rowNum in range(self.lly, self.ury + 1):
            ss.append('M %.1f %.1f L %.1f %.1f ' % (
                self.svgPxForCmF(self.llx), -self.svgPxForCmF(rowNum),
                self.svgPxForCmF(self.urx), -self.svgPxForCmF(rowNum)))
        ss.append('"/>\n')
        for gr in self.graphics:
            ss.append(gr.getSvg())
        return ''.join(ss)

    def setBB(self):
        extra = 0.1
        self.bb = [self.llx - extra, self.lly - extra,
                   self.urx + extra, self.ury + extra]



###############################################################
###############################################################
#
# TEXT
#
###############################################################
###############################################################


class GramText(GramGraphic):

    def __init__(self, text, addToGIdDict=True):
        GramGraphic.__init__(self)

        # GramGraphic provides ---
        # self.cA = None
        # self.comment = None
        # self.style = None
        # self.myStyle = None
        # self.bb = [0.0] * 4
        # self.gId = None
        # Plus all the stuff inherited from GramTikzStyle
        # That includes _textHeight and _textDepth, and
        # GramTikzStyle properties textHeight and TextDepth, and
        # textWrapWidth

        gm = ["GramText.__init__(%s)" % text]
        self.rawText = text
        self.cookedText = None   # with added modifiers like sffamily, bfseries, itshape, Large, etc
        if r"\begin{minipage}" in text:
            self.mpText = text
        elif r"\begin{varwidth}" in text:
            self.mpText = text
        else:
            self.mpText = None                     # wrapped in a minipage
        if addToGIdDict:
            self.setGIdAndAddToDict('text')

        self.width = 0.1

        self.corners = None
        self.fullHeight = 0.0    # Note we also have self.textHeight, inherited, which is different
        self.tbb = [0.0] * 4

        # more text measurements for tikz
        # inner sep is initially 0.3333em
        # em is the point size; it is not the width of an M (although maybe in history it was ...)
        # default inner sep is 0.3333em for normalsize text, regardless of text size
        # So for 10pt documents, inner sep is 3.333pt
        # self.ex = 0.0         # vertical size of an x
        # self.exWid = 0.0      # width of an x
        # self.bigX = 0.0       # vertical size of a big X, cap height
        # self.yuh = 0.0        # vertical underhang of a y
        self.half_normal_x = 0.0   # half vertical size of a normalsize x
        self.svg_half_normal_x = 0.0   # half vertical size of a normalsize x
        self.underhang = 0.0
        self.rise = 0.0
        self.svgBaseline_cm = 0.0   # Used to calculate underhang from inkscape bb
        # Gram._svgNormalsize_x = None  # vertical size, for mid anchor, measured by inkscape

        # parts, to make make multi-texts easier,
        # eg normal red-BOLD blue-italic backToNormal in the same text object
        # with different outputs for tikz and svg, but a shared interface.
        # Parts are GramText objects, and are added, once, to rawText in setPositions()
        self.parts = []
        self.partsHaveBeenAdded = False

        self.fontSizeMultiplierDict = {
            'tiny': 0.5,
            'scriptsize': 0.7,
            'footnotesize': 0.8,
            'small': 0.9,
            'normalsize': 1.,
            'large': 1.2,
            'Large': 1.44,
            'LARGE': 1.728,
            'huge': 2.074,
            'Huge': 2.488,
        }

        self.gX = 0.0
        self.gY = 0.0

    # def dupe(self, gIdMod):
    #     assert gIdMod
    #     assert isinstance(gIdMod, str)

    #     c = copy.deepcopy(self)
    #     c.gId += gIdMod
    #     return c


    def append(self, aText):
        tp = GramText(aText, addToGIdDict=False)
        self.parts.append(tp)
        return tp

    def dump(self):
        print("GramText.dump()")
        spacer = " " * 8
        print(f"{spacer} rawText: {self.rawText}")
        print(f"{spacer} cookedText: {self.cookedText}")
        print(f"{spacer} gId: {self.gId}")
        # print(f"{spacer} name: {self.name}")
        if self.cA:
            print(f"{spacer} cA: {self.cA.xPosn:.3f},{self.cA.yPosn:.3f}")
        else:
            print(f"{spacer} cA: None")
        print(f"{spacer} anchor: {self.getAnch()}")
        print(f"{spacer} bb: {self.bb}")
        print(f"{spacer} width: {self.width:.5f}")
        print(f"{spacer} fullHeight: {self.fullHeight:.5f}")
        print(f"{spacer} innerSep: {self.getInnerSep()}")
        print(f"{spacer} lineThickness (cm): {cmForLineThickness(self.getLineThickness())}")
        print(f"{spacer} underhang (cm): {self.underhang}")
        print(f"{spacer} rise (cm): {self.rise}")
        print(f"{spacer} half_normal_x (cm): {self.half_normal_x}")
        #print(f"{spacer} svgNormalsize_x (cm): {Gram._svgNormalsize_x}")
        #print(f"{spacer} svgBaseline_cm (cm): {self.svgBaseline_cm}")
        print(f"{spacer} textShape: {self.getTextShape()}")
        # print(f"{spacer} ")


    def setCookedText(self):
        if self.mpText:
            self.cookedText = self.mpText
        else:
            self.cookedText = self.cookText(self.rawText)
        # print(f"Cooked Text: {self.cookedText}")

    def cookText(self, rawText):
        """Add adjectives like sffamily, bfseries, itshape, Large, etc to rawText.
        """
        #_goodTextFamilies = ['rmfamily', 'sffamily', 'ttfamily']
        #_goodTextSeries = ['bfseries']
        #_goodTextShapes = ['itshape', 'scshape', "upshape"]         # and "slshape"?

        if not rawText:
            return ''

        if r"\begin{minipage}" in self.rawText:
            raise GramError("programming error: cookText with minipage.")

        if 0:
            theText = func.fixCharsForLatex(rawText)
        else:
            theText = rawText
        # print("cookText() the raw text is %s" % rawText)
        # print("cookText() theText (a) is %s" % theText)
        # try:
        #     theTextFamily = self.getTextFamily()
        # except:
        #     print(self.styleDict)
        #     print("cookText()  style is:", self.style)
        #     sys.exit()
        theTextSeries = self.getTextSeries()
        theTextShape = self.getTextShape()
        theSize = self.getTextSize()
        # print("cookText() the raw text is %s, theTextFamily %s, theTextSeries %s, theTextShape %s, theSize %s" % (
        #     rawText, theTextFamily, theTextSeries, theTextShape, theSize))

        if theTextShape:
            theText = r"\%s %s" % (theTextShape, theText)
        if theTextSeries:
            theText = r"\%s %s" % (theTextSeries, theText)
        # if theTextFamily:
        #     if theTextFamily == self.defaultTextFamily:
        #         print("cookText()  textFamily %s is default, so not using it" % theTextFamily)
        #     else:
        #         theText = r"\%s %s" % (theTextFamily, theText)
        if theSize and theSize != 'normalsize':
            theText = r"\%s %s" % (theSize, theText)

        return theText




    def setBogusBB(self):

        if self.style:
            print("====== Turning off style for textbox '%s'" % self.rawText)
            self.style = None
        theAnch = self.getAnch()
        if theAnch == 'south west':
            self.bb[0] = self.cA.xPosn
            self.bb[1] = self.cA.yPosn
            self.bb[2] = self.cA.xPosn + 1.
            self.bb[3] = self.cA.yPosn + 1.

        elif theAnch == 'south':
            self.bb[0] = self.cA.xPosn - 0.5
            self.bb[1] = self.cA.yPosn
            self.bb[2] = self.cA.xPosn + 0.5
            self.bb[3] = self.cA.yPosn + 1.0

        elif theAnch == 'south east':
            self.bb[0] = self.cA.xPosn - 1.0
            self.bb[1] = self.cA.yPosn
            self.bb[2] = self.cA.xPosn
            self.bb[3] = self.cA.yPosn + 1.0

        elif theAnch == 'base east':
            self.bb[0] = self.cA.xPosn - 1.
            self.bb[1] = self.cA.yPosn - 0.35
            self.bb[2] = self.cA.xPosn
            self.bb[3] = self.cA.yPosn + 0.65

        elif theAnch == 'east':
            self.bb[0] = self.cA.xPosn - 1.0
            self.bb[1] = self.cA.yPosn - 0.5
            self.bb[2] = self.cA.xPosn
            self.bb[3] = self.cA.yPosn + 0.5

        elif theAnch == 'north east':
            self.bb[0] = self.cA.xPosn - 1.0
            self.bb[1] = self.cA.yPosn - 1.0
            self.bb[2] = self.cA.xPosn
            self.bb[3] = self.cA.yPosn

        elif theAnch == 'north':
            self.bb[0] = self.cA.xPosn - 0.5
            self.bb[1] = self.cA.yPosn - 1.0
            self.bb[2] = self.cA.xPosn + 0.5
            self.bb[3] = self.cA.yPosn

        elif theAnch == 'north west':
            self.bb[0] = self.cA.xPosn
            self.bb[1] = self.cA.yPosn - 1.0
            self.bb[2] = self.cA.xPosn + 1.0
            self.bb[3] = self.cA.yPosn

        elif theAnch == 'west':
            self.bb[0] = self.cA.xPosn
            self.bb[1] = self.cA.yPosn - 0.5
            self.bb[2] = self.cA.xPosn + 1.0
            self.bb[3] = self.cA.yPosn + 0.5

        elif theAnch == 'base west':
            self.bb[0] = self.cA.xPosn
            self.bb[1] = self.cA.yPosn - 0.35
            self.bb[2] = self.cA.xPosn + 1.0
            self.bb[3] = self.cA.yPosn + 0.65

        elif theAnch == 'base':
            self.bb[0] = self.cA.xPosn - 0.5
            self.bb[1] = self.cA.yPosn - 0.35
            self.bb[2] = self.cA.xPosn + 0.5
            self.bb[3] = self.cA.yPosn + 0.65

        elif theAnch == 'mid west':
            self.bb[0] = self.cA.xPosn
            self.bb[1] = self.cA.yPosn - 0.5
            self.bb[2] = self.cA.xPosn + 1.0
            self.bb[3] = self.cA.yPosn + 0.5

        elif theAnch == 'mid':
            self.bb[0] = self.cA.xPosn - 0.5
            self.bb[1] = self.cA.yPosn - 0.5
            self.bb[2] = self.cA.xPosn + 0.5
            self.bb[3] = self.cA.yPosn + 0.5

        elif theAnch == 'mid east':
            self.bb[0] = self.cA.xPosn - 1.0
            self.bb[1] = self.cA.yPosn - 0.5
            self.bb[2] = self.cA.xPosn
            self.bb[3] = self.cA.yPosn + 0.5

        elif theAnch == 'center' or theAnch is None:
            self.bb[0] = self.cA.xPosn - 0.5
            self.bb[1] = self.cA.yPosn - 0.5
            self.bb[2] = self.cA.xPosn + 0.5
            self.bb[3] = self.cA.yPosn + 0.5


        # ====================================

        else:
            raise GramError("GramText.setBogusBB().  anch '%s' not implemented." % theAnch)


    def setBB(self):    # GramText
        gm = ["GramText.setBB() %s" % self.rawText[:30]]
        # print(gm[0])

        if not self.cA:
            self.cA = GramCoord()

        assert self.engine == 'tikz'

        # if 1:
        #     if self.rawText == "20":
        #         print("a GramText.setBB() for '%s';" % self.rawText)
        #         print("    self.width is %s, self.fullHeight is %s" % (self.width, self.fullHeight))
        #         print("    bb is %s" % self.bb)

        halfHeight = self.fullHeight / 2.0
        halfWidth = self.width / 2.0
        # oneSep = (self.normal_em * 0.3333) + 0.009 # The 0.009 is a total
        # fudge, but it appears to be right.

        theAnch = self.getAnch()
        #print("xxy GramText.setBB() theAnch is %s" % theAnch)
        oneInnerSep = self.getInnerSep()
        #if oneInnerSep < 0.11:
        #    print(f"GramText.setBB() {theAnch}, innerSep {oneInnerSep}")
        if oneInnerSep is None:
            raise GramError("GramText.setBB(). %s getInnerSep() returned None." % self.rawText)

        theLineThickness = self.getLineThickness()
        # if oneInnerSep is None:
        #    oneInnerSep = self.defaultInnerSep
        twoInnerSep = 2 * oneInnerSep
        twoOuterSep = cmForLineThickness(theLineThickness)
        oneOuterSep = 0.5 * twoOuterSep
        # print "    oneInnerSep is %.3f" % oneInnerSep
        # print "    oneOuterSep is %.3f" % oneOuterSep
        # print "  %s theAnch is %s, width=%.5f, height=%s, halfHeight=%s" % (
        #    self.rawText, theAnch, self.width, self.fullHeight, halfHeight)
        # sys.exit()

        if theAnch == 'south west':
            self.tbb[0] = self.cA.xPosn + oneOuterSep + oneInnerSep
            self.tbb[1] = self.cA.yPosn + oneOuterSep + oneInnerSep
            self.tbb[2] = self.tbb[0] + self.width
            self.tbb[3] = self.tbb[1] + self.fullHeight

            self.bb[0] = self.cA.xPosn
            self.bb[1] = self.cA.yPosn
            self.bb[2] = self.cA.xPosn + self.width + twoInnerSep + twoOuterSep
            self.bb[3] = self.cA.yPosn + self.fullHeight + twoInnerSep + twoOuterSep



        elif theAnch == 'south':
            self.bb[0] = self.cA.xPosn - \
                (halfWidth + oneInnerSep + oneOuterSep)
            self.bb[1] = self.cA.yPosn
            self.bb[2] = self.cA.xPosn + \
                (halfWidth + oneInnerSep + oneOuterSep)
            self.bb[3] = self.cA.yPosn + \
                self.fullHeight + twoInnerSep + twoOuterSep

        elif theAnch == 'south east':
            self.bb[0] = self.cA.xPosn - \
                (self.width + twoInnerSep + twoOuterSep)
            self.bb[1] = self.cA.yPosn
            self.bb[2] = self.cA.xPosn
            self.bb[3] = self.cA.yPosn + \
                (self.fullHeight + twoInnerSep + twoOuterSep)

        elif theAnch == 'base east':
            # if self.textWrapWidth:
            if 0:
                self.bb[0] = self.cA.xPosn - \
                    (self.width + twoInnerSep + twoOuterSep)
                self.bb[1] = self.cA.yPosn - \
                    (self.fullHeight + oneInnerSep + oneOuterSep)
                self.bb[2] = self.cA.xPosn
                self.bb[3] = self.cA.yPosn + (oneInnerSep + oneOuterSep)
            else:
                self.bb[0] = self.cA.xPosn - (self.width + twoInnerSep + twoOuterSep)
                self.bb[1] = self.cA.yPosn - (self.underhang + oneInnerSep + oneOuterSep)
                self.bb[2] = self.cA.xPosn
                self.bb[3] = self.cA.yPosn + (self.rise + oneInnerSep + oneOuterSep)

        elif theAnch == 'east':
            self.bb[0] = self.cA.xPosn - (self.width + twoInnerSep + twoOuterSep)
            self.bb[1] = self.cA.yPosn - (halfHeight + oneInnerSep + oneOuterSep)
            self.bb[2] = self.cA.xPosn
            self.bb[3] = self.cA.yPosn + (halfHeight + oneInnerSep + oneOuterSep)

        elif theAnch == 'north east':
            self.bb[0] = self.cA.xPosn - \
                (self.width + twoInnerSep + twoOuterSep)
            self.bb[1] = self.cA.yPosn - \
                (self.fullHeight + twoInnerSep + twoOuterSep)
            self.bb[2] = self.cA.xPosn
            self.bb[3] = self.cA.yPosn

        elif theAnch == 'north':
            self.bb[0] = self.cA.xPosn - \
                (halfWidth + oneInnerSep + oneOuterSep)
            self.bb[1] = self.cA.yPosn - \
                (self.fullHeight + twoInnerSep + twoOuterSep)
            self.bb[2] = self.cA.xPosn + \
                (halfWidth + oneInnerSep + oneOuterSep)
            self.bb[3] = self.cA.yPosn

        elif theAnch == 'north west':
            self.bb[0] = self.cA.xPosn
            self.bb[1] = self.cA.yPosn - \
                (self.fullHeight + twoInnerSep + twoOuterSep)
            self.bb[2] = self.cA.xPosn + \
                (self.width + twoInnerSep + twoOuterSep)
            self.bb[3] = self.cA.yPosn

        elif theAnch == 'west':
            self.bb[0] = self.cA.xPosn
            self.bb[1] = self.cA.yPosn - \
                (halfHeight + oneInnerSep + oneOuterSep)
            self.bb[2] = self.cA.xPosn + \
                (self.width + twoInnerSep + twoOuterSep)
            self.bb[3] = self.cA.yPosn + \
                (halfHeight + oneInnerSep + oneOuterSep)

        elif theAnch == 'base west':
            # if self.textWrapWidth:
            if 0:
                self.bb[0] = self.cA.xPosn
                self.bb[1] = self.cA.yPosn - \
                    (self.fullHeight + oneInnerSep + oneOuterSep)
                self.bb[2] = self.cA.xPosn + \
                    (self.width + twoInnerSep + twoOuterSep)
                self.bb[3] = self.cA.yPosn + (oneInnerSep + oneOuterSep)
            else:
                self.bb[0] = self.cA.xPosn
                self.bb[1] = self.cA.yPosn - (self.underhang + oneInnerSep + oneOuterSep)
                self.bb[2] = self.cA.xPosn + (self.width + twoInnerSep + twoOuterSep)
                self.bb[3] = self.cA.yPosn + (self.rise + oneInnerSep + oneOuterSep)

        elif theAnch == 'base':
            # if self.textWrapWidth:
            if 0:
                self.bb[0] = self.cA.xPosn - \
                    (halfWidth + oneInnerSep + oneOuterSep)
                self.bb[1] = self.cA.yPosn - \
                    (self.fullHeight + oneInnerSep + oneOuterSep)
                self.bb[2] = self.cA.xPosn + \
                    (halfWidth + oneInnerSep + oneOuterSep)
                self.bb[3] = self.cA.yPosn + (oneInnerSep + oneOuterSep)
            else:
                self.bb[0] = self.cA.xPosn - (halfWidth + oneInnerSep + oneOuterSep)
                self.bb[1] = self.cA.yPosn - (self.underhang + oneInnerSep + oneOuterSep)
                self.bb[2] = self.cA.xPosn + (halfWidth + oneInnerSep + oneOuterSep)
                self.bb[3] = self.cA.yPosn + (self.rise + oneInnerSep + oneOuterSep)

        elif theAnch == 'center' or theAnch is None:
            self.bb[0] = self.cA.xPosn - (halfWidth + oneInnerSep + oneOuterSep)
            self.bb[1] = self.cA.yPosn - (halfHeight + oneInnerSep + oneOuterSep)
            self.bb[2] = self.cA.xPosn + (halfWidth + oneInnerSep + oneOuterSep)
            self.bb[3] = self.cA.yPosn + (halfHeight + oneInnerSep + oneOuterSep)

        # ====================================
        elif theAnch == 'mid west':
            if self.textWrapWidth:
                # self.bb[0] = self.cA.xPosn
                # self.bb[1] = self.cA.yPosn - (self.fullHeight + twoInnerSep + oneOuterSep)
                # self.bb[2] = self.cA.xPosn + (self.width + twoInnerSep + twoOuterSep)
                # # + (self.fullHeight + oneInnerSep + oneOuterSep)
                # self.bb[3] = self.cA.yPosn

                # Behaves like "west"
                self.bb[0] = self.cA.xPosn
                self.bb[1] = self.cA.yPosn - \
                    (halfHeight + oneInnerSep + oneOuterSep)
                self.bb[2] = self.cA.xPosn + \
                    (self.width + twoInnerSep + twoOuterSep)
                self.bb[3] = self.cA.yPosn + \
                    (halfHeight + oneInnerSep + oneOuterSep)

            else:
                self.bb[0] = self.cA.xPosn
                self.bb[1] = self.cA.yPosn - (self.underhang + self.half_normal_x + oneInnerSep + oneOuterSep)
                self.bb[2] = self.cA.xPosn + (self.width + twoInnerSep + twoOuterSep)
                self.bb[3] = self.cA.yPosn + ((self.rise - self.half_normal_x) + oneInnerSep + oneOuterSep)

        elif theAnch == 'mid east':
            if self.textWrapWidth:
                # self.bb[0] = self.cA.xPosn - (self.width + twoInnerSep + twoOuterSep)
                # self.bb[1] = self.cA.yPosn - (self.fullHeight + twoInnerSep + oneOuterSep)
                # self.bb[2] = self.cA.xPosn
                # # + (self.fullHeight + oneInnerSep + oneOuterSep)
                # self.bb[3] = self.cA.yPosn

                # This week it behaves like "east"
                self.bb[0] = self.cA.xPosn - (self.width + twoInnerSep + twoOuterSep)
                self.bb[1] = self.cA.yPosn - (halfHeight + oneInnerSep + oneOuterSep)
                self.bb[2] = self.cA.xPosn
                self.bb[3] = self.cA.yPosn + (halfHeight + oneInnerSep + oneOuterSep)

            else:
                self.bb[0] = self.cA.xPosn - (self.width + twoInnerSep + twoOuterSep)
                self.bb[1] = self.cA.yPosn - (self.underhang + self.half_normal_x + oneInnerSep + oneOuterSep)
                self.bb[2] = self.cA.xPosn
                self.bb[3] = self.cA.yPosn + ((self.rise - self.half_normal_x) + oneInnerSep + oneOuterSep)

        elif theAnch == 'mid':     # setBB
            if self.textWrapWidth:
                # self.bb[0] = self.cA.xPosn - (halfWidth + oneInnerSep + oneOuterSep)
                # self.bb[1] = self.cA.yPosn - (self.fullHeight + twoInnerSep + oneOuterSep)
                # self.bb[2] = self.cA.xPosn + (halfWidth + oneInnerSep + oneOuterSep)
                # self.bb[3] = self.cA.yPosn  # + (oneInnerSep + oneOuterSep)

                # This week it behaves like "center"
                self.bb[0] = self.cA.xPosn - (halfWidth + oneInnerSep + oneOuterSep)
                self.bb[1] = self.cA.yPosn - (halfHeight + oneInnerSep + oneOuterSep)
                self.bb[2] = self.cA.xPosn + (halfWidth + oneInnerSep + oneOuterSep)
                self.bb[3] = self.cA.yPosn + (halfHeight + oneInnerSep + oneOuterSep)
            else:
                self.bb[0] = self.cA.xPosn - (halfWidth + oneInnerSep + oneOuterSep)
                self.bb[1] = self.cA.yPosn - (self.underhang + self.half_normal_x + oneInnerSep + oneOuterSep)
                self.bb[2] = self.cA.xPosn + (halfWidth + oneInnerSep + oneOuterSep)
                self.bb[3] = self.cA.yPosn + ((self.rise - self.half_normal_x) + oneInnerSep + oneOuterSep)

        else:
            raise GramError("anch '%s' not implemented." % theAnch)

        if 1:
            if self.rawText == "20":
                print("b GramText.setBB() for '%s';  self.width is %s, bb is %s" % (
                    self.rawText, self.width, self.bb))


        # Get bb for rotated text  GramText.setBB
        theRotate = self.getRotate()
        if theRotate:
            # The textbox rotates around its anchor.
            # print "   *tb.bb %25s  %.2f %.2f %.2f %.2f " % (
            # self.rawText, self.bb[0], self.bb[1], self.bb[2], self.bb[3])
            corners = []
            corners.append([self.bb[0], self.bb[1]])
            corners.append([self.bb[2], self.bb[1]])
            corners.append([self.bb[2], self.bb[3]])
            corners.append([self.bb[0], self.bb[3]])
            # print "xPosn=%.1f, yPosn=%.1f" % (self.cA.xPosn,
            # self.cA.yPosn)
            for cNum in range(4):
                corner = corners[cNum]
                corner[0] -= self.cA.xPosn
                corner[1] -= self.cA.yPosn
            polarCorners = []
            for cNum in range(4):
                polarCorners.append(func.square2polar(corners[cNum]))
            # print "a polarCorners = ", polarCorners
            rads = (theRotate * math.pi) / 180.
            # print "theRotate %f is %f radians" % (theRotate, rads)
            for cNum in range(4):
                pCorner = polarCorners[cNum]
                pCorner[0] += rads
            # print "b polarCorners = ", polarCorners

            corners = []
            for cNum in range(4):
                corners.append(func.polar2square(polarCorners[cNum]))
            # print 'corners', corners
            for cNum in range(4):
                corner = corners[cNum]
                corner[0] += self.cA.xPosn
                corner[1] += self.cA.yPosn
            # print corners

            llx = 1000000.
            lly = 1000000.
            urx = -1000000.
            ury = -1000000.

            for cNum in range(4):
                corner = corners[cNum]
                if corner[0] < llx:
                    llx = corner[0]
                if corner[1] < lly:
                    lly = corner[1]
                if corner[0] > urx:
                    urx = corner[0]
                if corner[1] > ury:
                    ury = corner[1]
            self.bb = [llx, lly, urx, ury]
            # print "   @tb.bb %25s  %.2f %.2f %.2f %.2f " % (
            # self.rawText, self.bb[0], self.bb[1], self.bb[2], self.bb[3])
            self.corners = corners

        # Blank text should have a zero-dimension bb
        if not self.rawText:
            self.bb[0] = self.cA.xPosn
            self.bb[1] = self.cA.yPosn
            self.bb[2] = self.cA.xPosn
            self.bb[3] = self.cA.yPosn



        theXShift = self.getXShift()
        if theXShift:
            self.bb[0] += theXShift
            self.bb[2] += theXShift
            if self.corners:
                for cNum in range(4):
                    self.corners[cNum][0] += theXShift
        theYShift = self.getYShift()
        if theYShift:
            self.bb[1] += theYShift
            self.bb[3] += theYShift
            if self.corners:
                for cNum in range(4):
                    self.corners[cNum][1] += theYShift

    def setMpTextTikz(self):
        "maybe wrap self in a minipage or varwidth, setting self.mpText"

        if self.mpText:    # a minipage, set during GramText.init
            pass
        else:
            # decide
            if self.textWrapWidth or r"\\" in self.rawText or r"\newline" in self.rawText:
                # print("GramText.setMpTextTikz().  Wrapping in minipage or varwidth.   %s" % self.rawText[:30])
                self.wrapRawInMinipageOrVarwidth()


    def wrapRawInMinipageOrVarwidth(self):
        gm = ["GramText.wrapRawInMinipageOrVarwidth()"]

        if self.textWrapWidth:
            widStr = "%.3fcm" % self.textWrapWidth
        else:
            widStr = None  # use varwidth

        alig = self.getTextAlign()

        # Gram._goodTextAligns = [None, 'left', 'flush left', 'right', 'flush right',
        #                    'center', 'flush center', 'justify', 'none']
        mpAlig = None
        if alig in [None, 'left', 'flush left', 'none']:
            mpAlig = "raggedright"
        elif alig in ["right", "flush right"]:
            mpAlig = "raggedleft"
        elif alig in ["center", "flush center"]:
            mpAlig = "centering"
        elif alig in ["justify"]:
            mpAlig = "justify"
        assert mpAlig


        # print(f"wrapRawInMinipageOrVarwidth() widStr = {widStr}, mpAlig={mpAlig}")

        # cookedText = self.cookText(self.rawText)
        self.setCookedText()        # cooked text needs to be inside the minipage

        myCmds = ""
        for it in [mpAlig]:
            if it:
                myCmds += r"\%s" % it
        # print(myCmds)

        if self.textWrapWidth:
            self.mpText = r"\begin{minipage}{%s}%s %s \end{minipage}" % (widStr, myCmds, self.cookedText)
        else:
            self.mpText = r"\begin{varwidth}{%s}%s %s \end{varwidth}" % ("10cm", myCmds, self.cookedText)

    def setPositionsBeforeTextMetrics(self):
        # print("GramText.setPositionsBeforeTextMetrics()")
        if self.engine == "svg":
            if not self.partsHaveBeenAdded:
                self.setTextPartsSvg()


    def setPositions(self):    # GramText
        # print("GramText.setPositions() %s" % self.rawText[:30])
        if self.engine == "tikz":
            self.setBB()
            # self.dump()

        elif self.engine == "svg":
            pass

    def setTextPartsTikz(self):
        gm = ['GramText.setTextPartsTikz() rawText=%s' % self.rawText]

        assert self.engine == "tikz", f"GramText.setTextPartsTikz(), self.engine is {self.engine}"


        if not self.partsHaveBeenAdded:
            for tp in self.parts:
                tp.rawText = fixUnderscores(tp.rawText)
                if tp.color:
                    cs = tp.color.color  # cs is colourString
                    if tp.color.value:
                        cs = f"{cs}!{100 * float(tp.color.value):.0f}"
                    theText = r"\textcolor{%s}{%s}" % (cs, tp.rawText)
                else:
                    theText = tp.rawText

                theTextFamily = tp.getTextFamily()
                theTextSeries = tp.getTextSeries()   # 'bfseries' or 'mdseries'
                theTextShape = tp.getTextShape()
                theSize = tp.getTextSize()

                if theTextShape:
                    theText = r"\%s %s" % (theTextShape, theText)
                else: 
                    if theText:
                        theText = r"\%s %s" % ("upshape", theText)
                if theTextSeries:
                    theText = r"\%s %s" % (theTextSeries, theText)
                if theTextFamily:
                    theText = r"\%s %s" % (theTextFamily, theText)
                if theSize and theSize != 'normalsize':
                    theText = r"\%s %s" % (theSize, theText)
                theText = "{" + theText + "}"
                self.rawText += theText
            self.partsHaveBeenAdded = True


    def setTextPartsSvg(self):
        gm = ['GramText.setTextPartsSvg() rawText=%s' % self.rawText]

        assert self.engine == "svg", f"GramText.setTextPartsSvg(), self.engine is {self.engine}"

        if self.partsHaveBeenAdded:
            pass
        else:
            ss = []
            for tp in self.parts:
                sss = []
                myClass = None
                myTextFamilyString = tp.getTextFamily()
                if myTextFamilyString == 'ttfamily':
                    myClass = 'ttfamily'
                elif myTextFamilyString == "sffamily":
                    myClass = "sffamily"

                myTextSizeStr = tp.getTextSize()
                if myTextSizeStr is None or myTextSizeStr == 'normalsize':
                    myTextSizeCm = self.svgTextNormalsize
                else:
                    myTextSizeCm = self.fontSizeMultiplierDict[
                        myTextSizeStr] * self.svgTextNormalsize
                myTextSizeStr = "%.2f" % (myTextSizeCm * self.svgPxForCm)

                sss.append('<tspan ')
                if myClass:
                    sss.append('class="%s"' % myClass)
                sss.append('font-size="%s"' % myTextSizeStr)

                myTextShape = tp.getTextShape()  #  ['itshape', 'scshape', "upshape"]     # and slshape?
                #print(f"setTextPartsSvg, {tp.rawText} got myTextShape {myTextShape}, font {tp.font}")
                if myTextShape == 'scshape':
                    sss.append('font-variant="small-caps"')
                #     gm.append("Small caps is currently off for SVG.") # because inkscape cannot measure it
                #     raise GramError(gm)
                if myTextShape == "upshape":
                    sss.append('font-style="normal"')
                if myTextShape == None:
                    sss.append('font-style="normal"')
                if myTextShape == 'itshape':
                    if tp.font in ['helvetica', 'lms']:
                        sss.append('font-style="oblique"')
                    elif tp.font in ['lmr', 'palatino', "times"]:
                        sss.append('font-style="italic"')
                    else:
                        gm.append("itshape specified, but not for %s.  Fixme!" % tp.font)
                        raise GramError(gm)

                # Since font-weight is part of the style, I need to use "style=..."
                myTextSeries = tp.getTextSeries()   # 'bfseries' or 'mdseries'
                # print("myTextSeries: %s" % myTextSeries)
                if myTextSeries == "bfseries":
                    sss.append('style="font-weight:bold"')   # or a number?
                elif myTextSeries == "mdseries":
                    sss.append('style="font-weight:normal"')

                myColor = tp.getColor()
                if myColor:
                    sss.append('fill="%s"' % myColor.color)
                    if myColor.transparent:
                        sss.append('fill-opacity="%s"' % myColor.value)

                sss.append(">%s</tspan>" % tp.rawText)
                theText = " ".join(sss)
                ss.append(theText)
            theText = "".join(ss)
            self.rawText += theText
            self.partsHaveBeenAdded = True


    def getTikz(self):   # GramText
        gm = ['GramText.getTikz() rawText=%s' % self.rawText]
        # print(gm[0])

        if self.mpText:
            theText = self.mpText
        else:
            # We don't want to use self.cookedText here, because we get tikz options, below.
            # However, we want to escape underscores and such.
            # But not in includegraphics filenames

            # Changed my mind.  It is now up to the user to escape underscores and set math mode
            # if self.rawText.startswith(r"\includegraphics"):
            #     theText = self.rawText
            # else:
            #     theText = func.fixCharsForLatex(self.rawText)
            theText = self.rawText

        # print(f"GramText.getTikz()  self.rawText= {self.rawText}")
        # print(f"theText (after fixCharsForLatex(self.rawText))= {theText}")

        # Hack
        # if 1:
        #     if 'fcolorbox' in theText:
        #         print("------fixing ------", theText)
        #         splText = theText.split()
        #         for tNum in range(len(splText)):
        #             if splText[tNum].startswith("\\fcolorbox"):
        #                 splText[tNum] = "\\raisebox{1.5bp}{\\scalebox{0.5}{%s}}" % splText[
        #                     tNum]
        #         theText = ' '.join(splText)


        ss = []
        ss.append(r'\node')

        options = self.getTikzOptions()
        if 0:
            print("tikz options for GramText: %s" % self.rawText)
            for opti in options:
                print(f"    {opti}")

        #print("%s, options %s" % (self.rawText, options))
        # If fill.value and fill.transparent, then fill-opacity is set to
        # fill.value (good) but the text gets that same opacity (bad).
        # Here is a hack fix.
        # if self.fill and self.fill.value and self.fill.transparent:
        #     options.append("text opacity=1.0")

        if options:
            ss.append('[%s]' % ','.join(options))
        # if self.name:
        #    ss.append(f"({self.name})")
        if self.cA.name:
            ss.append('at (%s)' % self.cA.name)
        else:
            ss.append('at (%.3f,%.3f)' % (self.cA.xPosn, self.cA.yPosn))

        ss.append('{%s};' % theText)

        if 0:
            tbbLine = '\n'
            tbbLine += r"\draw [teal,ultra thin] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (
                self.tbb[0], self.tbb[1],
                self.tbb[2], self.tbb[3])
            # print tbbLine
            ss.append(tbbLine)


        if self.showTextBB:
            # bbLine = '\n'
            # bbLine += r"\draw [blue,ultra thin] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (
            #     self.tbb[0], self.tbb[1],
            #     self.tbb[2], self.tbb[3])
            # # print bbLine
            # ss.append(bbLine)

            bbLine = '\n'
            bbLine += r"\draw [red,ultra thin] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (
                self.bb[0], self.bb[1],
                self.bb[2], self.bb[3])
            # print bbLine
            ss.append(bbLine)

        if self.showTextAnchor:
            ss.append("\\draw [red] plot[only marks,mark=x] coordinates {(%.3f,%.3f)};" % (
                self.cA.xPosn, self.cA.yPosn))
        return ' '.join(ss)


    def svgDump(self):
        print("GramText.svgDump()")
        spacer = " " * 8
        print(f"{spacer} rawText: {self.rawText}")
        print(f"{spacer} cA: {self.cA.xPosn:.3f},{self.cA.yPosn:.3f}")
        print(f"{spacer} anchor: {self.getAnch()}")
        print(f"{spacer} width: {self.width:.5f}")
        print(f"{spacer} fullHeight: {self.fullHeight:.5f}")
        print(f"{spacer} underhang (cm): {self.underhang}")
        print(f"{spacer} rise (cm): {self.rise}")
        print(f"{spacer} Gram._svgNormalsize_x (cm): {Gram._svgNormalsize_x}")
        print(f"{spacer} svgBaseline_cm (cm): {self.svgBaseline_cm}")


    def getSvg(self):    # GramText
        gm = [f"GramText.getSvg() rawText={self.rawText}, gId={self.gId}"]
        # print(gm[0])
        if not self.cA:
            self.cA = GramCoord()
        # print gm[0], self.gId, self.gForGIdDict[self.gId].rawText

        myClass = None
        myTextFamilyString = self.getTextFamily()
        if myTextFamilyString == 'ttfamily':
            myClass = 'ttfamily'
        elif myTextFamilyString == "sffamily":
            myClass = "sffamily"
        elif myTextFamilyString == "rmfamily":
            myClass = "rmfamily"

        # Deal with small caps -- it becomes a class
        myTextShapeString = self.getTextShape()
        if myTextShapeString == "scshape":
            myClass = "scshape"
            # print(f"GramText.getSvg()  setting myClass to {myClass}")

        myTextSizeStr = self.getTextSize()
        #print(f"GramText.getSvg()  myTextSizeStr is {myTextSizeStr}")
        if myTextSizeStr is None or myTextSizeStr == 'normalsize':
            myTextSizeCm = self.svgTextNormalsize
        else:
            myTextSizeCm = self.fontSizeMultiplierDict[
                myTextSizeStr] * self.svgTextNormalsize

        #print(f"GramText.getSvg()  a myTextSizeStr is {myTextSizeStr}")
        #print(f"GramText.getSvg()  myTextSizeCm is {myTextSizeCm}")
        myTextSizeStr = "%.2f" % (myTextSizeCm * self.svgPxForCm)
        #print(f"GramText.getSvg()  b myTextSizeStr= {myTextSizeStr}")

        myAnch = self.getAnch()
        # print "GramText.getSvg()  myAnch=%s" % myAnch

        halfHeight = self.fullHeight / 2.
        #self.width = (self.bb[2] - self.bb[0])  no workee for rotated!
        halfWidth = self.width/2.
        # print(f"GramText.getSvg() '{self.rawText}' width {self.width:.2} cm, height is {self.fullHeight:.2} cm")

        oneInnerSep = self.getInnerSep()
        # print("GramText.getSvg() Got oneInnerSep %.2f for %s" % (oneInnerSep, self.rawText))
        twoInnerSep = 2 * oneInnerSep

        # Get outer sep
        theLineThickness = self.getLineThickness()
        # print("a Got theLineThickness %s" % theLineThickness)
        twoOuterSep = cmForLineThickness(theLineThickness)
        oneOuterSep = 0.5 * twoOuterSep

        # For mid anchors, need half_normal_x, but it does not exist at first
        if Gram._svgNormalsize_x:
            self.svg_half_normal_x = Gram._svgNormalsize_x / 2.
        # print(f"{gm[0]} svg_half_normal_x is {self.svg_half_normal_x}")


        # dx and dy are fine-tuning args for svg text, that modify the x and y positions.
        # Eg <text id="text-1"  x="300.00" y="-300.00" font-size="108.00" dx="-93.29" dy="28.62" >acly</text>
        # If they are zero, the text is placed at x,y as the start of the text, and the baseline
        # For a rect, the x,y is the top left corner, width goes right (as usual) and height goes down (unusual)
        # Eg <rect x="300.0" y="-300.0"  width="186.57" height="100.62" stroke="red" fill="none" stroke-width="0.5" />
        myDx = 0.0
        myDy = 0.0
        myDrDx = 0.0   # for the box, ie the "draw"
        myDrDy = 0.0

        if myAnch == 'west':
            myDx += oneInnerSep
            myDx += oneOuterSep
            myDy -= self.underhang
            myDy += halfHeight
            myDrDy += oneInnerSep
            myDrDy += oneOuterSep
            myDrDy += halfHeight
        elif myAnch == 'north west':
            myDx += oneInnerSep
            myDx += oneOuterSep
            myDy += oneInnerSep
            myDy += oneOuterSep
            myDy += self.rise
            myDrDy += self.fullHeight
            myDrDy += twoInnerSep
            myDrDy += twoOuterSep
        elif myAnch == 'north':
            myDx += -halfWidth
            myDy += self.rise
            myDy += oneInnerSep
            myDy += oneOuterSep
            myDrDx += -halfWidth
            myDrDx += -oneInnerSep
            myDrDx += -oneOuterSep
            myDrDy += self.fullHeight
            myDrDy += twoInnerSep
            myDrDy += twoOuterSep
        elif myAnch == 'north east':
            myDx += -self.width
            myDx += -oneInnerSep
            myDx += -oneOuterSep
            myDy += oneInnerSep
            myDy += oneOuterSep
            myDy += self.rise
            myDrDx += -self.width
            myDrDx += -twoInnerSep
            myDrDx += -twoOuterSep
            myDrDy += self.fullHeight
            myDrDy += twoInnerSep
            myDrDy += twoOuterSep
        elif myAnch == 'east':
            myDx += -self.width
            myDx += -oneInnerSep
            myDx += -oneOuterSep
            myDy -= self.underhang
            myDy += halfHeight
            myDrDx += -self.width
            myDrDx += -twoInnerSep
            myDrDx += -twoOuterSep
            myDrDy += oneInnerSep
            myDrDy += oneOuterSep
            myDrDy += halfHeight
        elif myAnch == 'base':
            myDx += -halfWidth
            myDrDx += -halfWidth
            myDrDx += -oneInnerSep
            myDrDx += -oneOuterSep
            myDrDy += oneInnerSep
            myDrDy += oneOuterSep
            myDrDy += self.underhang
        elif myAnch == 'base west':
            myDx += oneInnerSep
            myDx += oneOuterSep
            myDrDy += oneInnerSep
            myDrDy += oneOuterSep
            myDrDy += self.underhang
        elif myAnch == 'base east':
            myDx += -self.width
            myDx += -oneInnerSep
            myDx += -oneOuterSep
            myDrDx += -self.width
            myDrDx += -twoInnerSep
            myDrDx += -twoOuterSep
            myDrDy += oneInnerSep
            myDrDy += oneOuterSep
            myDrDy += self.underhang
        elif myAnch == 'mid':
            # print(f"mid: oneInnerSep: {oneInnerSep}, oneOuterSep {oneOuterSep}, underhang: {self.underhang}, svg_half_normal_x: {self.svg_half_normal_x}")
            myDx += -halfWidth
            myDy  += self.svg_half_normal_x
            myDrDx += -halfWidth
            myDrDx += -oneInnerSep
            myDrDx += -oneOuterSep
            myDrDy += oneInnerSep
            myDrDy += oneOuterSep
            # myDrDy += self.svg_half_normal_x
            myDrDy += self.underhang
        elif myAnch == 'mid west':
            myDx += oneInnerSep
            myDx += oneOuterSep
            myDy += self.svg_half_normal_x
            myDrDy += oneInnerSep
            myDrDy += oneOuterSep
            # myDrDy += self.svg_half_normal_x
            myDrDy += self.underhang
        elif myAnch == 'mid east':
            myDx += -self.width
            myDx += -oneInnerSep
            myDx += -oneOuterSep
            myDy += self.svg_half_normal_x
            myDrDx += -self.width
            myDrDx += -twoInnerSep
            myDrDx += -twoOuterSep
            myDrDy += oneInnerSep
            myDrDy += oneOuterSep
            # myDrDy += self.svg_half_normal_x
            myDrDy += self.underhang
        elif myAnch == 'south west':
            myDx += oneInnerSep
            myDx += oneOuterSep
            myDy += -oneInnerSep
            myDy += -oneOuterSep
            myDy += -self.underhang
            # myDx = 0.0
            # myDy = 0.0
        elif myAnch == 'south':
            myDx += -halfWidth
            myDy += -oneInnerSep
            myDy += -oneOuterSep
            myDy += -self.underhang
            myDrDx += -halfWidth
            myDrDx += -oneInnerSep
            myDrDx += -oneOuterSep
        elif myAnch == 'south east':
            myDx += -self.width
            myDx += -oneInnerSep
            myDx += -oneOuterSep
            myDy += -oneInnerSep
            myDy += -oneOuterSep
            myDy += -self.underhang
            myDrDx += -self.width
            myDrDx += -twoInnerSep
            myDrDx += -twoOuterSep
        elif myAnch == 'center' or myAnch is None:
            myDx += -halfWidth
            myDy += -self.underhang
            myDy += halfHeight
            myDrDx += -halfWidth
            myDrDx += -oneInnerSep
            myDrDx += -oneOuterSep
            myDrDy += oneInnerSep
            myDrDy += oneOuterSep
            myDrDy += halfHeight
        else:
            gm.append("Bad anchor %s" % myAnch)
            raise GramError(gm)

        # Calculate the tight bounding box self.tbb for svg for GramText
        # First for the un-rotated text box, and then rotate it if needed.
        # # rotatePointAroundPoint(pointToRotate, degrees, pivotPoint)

        # tbb is [llx, lly, urx, ury]

        if myAnch in ["mid", "mid east", "mid west"]:
            self.tbb[0] = self.cA.xPosn + myDx
            self.tbb[1] = self.cA.yPosn - self.underhang
            self.tbb[2] = self.tbb[0] + self.width
            self.tbb[3] = self.tbb[1] + self.fullHeight
        else:
            self.tbb[0] = self.cA.xPosn + myDx
            self.tbb[1] = self.cA.yPosn - self.underhang - myDy
            self.tbb[2] = self.tbb[0] + self.width
            self.tbb[3] = self.tbb[1] + self.fullHeight


        #     myRotate = self.getRotate()
        #     if myRotate:
        #         # ss.append('transform="rotate(%.2f, %.2f, %.2f)"' % (
        #         #    -myRotate, self.svgPxForCmF(self.cA.xPosn), -self.svgPxForCmF(self.cA.yPosn)))

        #         ll = (self.tbb[0], self.tbb[1])
        #         ur = (self.tbb[2], self.tbb[3])
        #         pivotPoint = (self.svgPxForCmF(self.cA.xPosn), -self.svgPxForCmF(self.cA.yPosn))
        #         (self.tbb[0], self.tbb[1]) = rotatePointAroundPoint(ll, -myRotate, pivotPoint)
        #         (self.tbb[2], self.tbb[3]) = rotatePointAroundPoint(ur, -myRotate, pivotPoint)

        # get self.bb

        self.bb[0] = self.tbb[0] - oneInnerSep - oneOuterSep
        self.bb[1] = self.tbb[1] - oneInnerSep - oneOuterSep
        self.bb[2] = self.tbb[2] + oneInnerSep + oneOuterSep
        self.bb[3] = self.tbb[3] + oneInnerSep + oneOuterSep

        if not self.rawText:   # Empty text
            self.tbb[0] = self.cA.xPosn
            self.tbb[1] = self.cA.yPosn
            self.tbb[2] = self.cA.xPosn
            self.tbb[3] = self.cA.yPosn

            self.bb[0] = self.cA.xPosn
            self.bb[1] = self.cA.yPosn
            self.bb[2] = self.cA.xPosn
            self.bb[3] = self.cA.yPosn



        theRotate = self.getRotate()
        if theRotate:
            # The textbox rotates around its anchor.
            corners = []
            corners.append([self.bb[0], self.bb[1]])
            corners.append([self.bb[2], self.bb[1]])
            corners.append([self.bb[2], self.bb[3]])
            corners.append([self.bb[0], self.bb[3]])
            # print("xPosn=%.1f, yPosn=%.1f" % (self.cA.xPosn,
            # self.cA.yPosn))
            for cNum in range(4):
                corner = corners[cNum]
                corner[0] -= self.cA.xPosn
                corner[1] -= self.cA.yPosn
            polarCorners = []
            for cNum in range(4):
                polarCorners.append(func.square2polar(corners[cNum]))
            # print("a polarCorners = ", polarCorners)
            rads = (theRotate * math.pi) / 180.
            # print "theRotate %f is %f radians" % (theRotate, rads)
            for cNum in range(4):
                pCorner = polarCorners[cNum]
                pCorner[0] += rads
            # print "b polarCorners = ", polarCorners

            corners = []
            for cNum in range(4):
                corners.append(func.polar2square(polarCorners[cNum]))
            # print 'corners', corners
            for cNum in range(4):
                corner = corners[cNum]
                corner[0] += self.cA.xPosn
                corner[1] += self.cA.yPosn
            # print corners

            llx = 1000000.
            lly = 1000000.
            urx = -1000000.
            ury = -1000000.

            for cNum in range(4):
                corner = corners[cNum]
                if corner[0] < llx:
                    llx = corner[0]
                if corner[1] < lly:
                    lly = corner[1]
                if corner[0] > urx:
                    urx = corner[0]
                if corner[1] > ury:
                    ury = corner[1]
            self.bb = [llx, lly, urx, ury]
            # print "   @tb.bb %25s  %.2f %.2f %.2f %.2f " % (
            # self.rawText, self.bb[0], self.bb[1], self.bb[2], self.bb[3])
            self.corners = corners

        theXShift = self.getXShift()
        if theXShift:
            self.bb[0] += theXShift
            self.bb[2] += theXShift
            if self.corners:
                for cNum in range(4):
                    self.corners[cNum][0] += theXShift
        theYShift = self.getYShift()
        if theYShift:
            self.bb[1] += theYShift
            self.bb[3] += theYShift
            if self.corners:
                for cNum in range(4):
                    self.corners[cNum][1] += theYShift


        myDx *= self.svgPxForCm
        myDy *= self.svgPxForCm

        myXShift = self.getXShift()
        if myXShift:
            myDx += myXShift * self.svgPxForCm
        myYShift = self.getYShift()
        if myYShift:
            myDy -= myYShift * self.svgPxForCm

        # print "%20s  %+.2f  %+6.2f" % (myAnch, myDx, myDy)

        #print("b GramText.getSvg() self.width is %s; svgHackDoRotate is %s" % (self.width, Gram._svgHackDoRotate))


        ss = []  # GramText.getSvg()

        myDraw = self.getDraw()
        myFill = self.getFill()
        #print("GramText.getSvg() for %s --- myDraw is %s, myFill is %s" % (self.rawText, myDraw, myFill))

        if myDraw or myFill:
            myDrDx *= self.svgPxForCm
            myDrDy *= self.svgPxForCm

            #myXShift = self.getXShift()
            if myXShift:
                myDrDx += myXShift * self.svgPxForCm
            #myYShift = self.getYShift()
            if myYShift:
                myDrDy -= myYShift * self.svgPxForCm


            myDrHeight = ((self.fullHeight + twoInnerSep) * self.svgPxForCm)
            myDrX = ((self.cA.xPosn + oneOuterSep) * self.svgPxForCm)  + myDrDx
            myDrY = ((-self.cA.yPosn - oneOuterSep) * self.svgPxForCm) - myDrHeight + myDrDy
            myDrWid = ((self.width + twoInnerSep) * self.svgPxForCm)
            ss.append('<rect x="%.2f" y="%.2f"  width="%.2f" height="%.2f"' % (
                myDrX, myDrY, myDrWid, myDrHeight))
            # ss.append('stroke="black" fill="none" stroke-width="1" />\n')

            if myDraw:
                if myDraw is True:
                    ss.append('stroke="black"')
                elif myDraw in [False, None]:
                    pass

                elif isinstance(myDraw, GramColor):
                    myColor = myDraw
                    colorOptions = myColor.getSvgOptions()
                    # print(f"GramText.getSvg() myDraw B colorOptions:{colorOptions}")
                    ss += colorOptions

                else:
                    gm.append(f"Programming error.  Bad myDraw value {myDraw}")
                    raise GramError(gm)

                # If myFill is None or False, it will be filled in black unless I do this
                if myFill in [None, False]:
                    ss.append('fill="none"')


            if myFill:
                if myFill == True:
                    ss.append('fill="black"')

                elif isinstance(myFill, GramColor):
                    colorOptions = myFill.getSvgOptions(stroke="fill")
                    # print(f"GramText.getSvg() myFill A colorOptions:{colorOptions}")
                    ss += colorOptions
                else:
                    gm.append(f"GramText.getSvg() Programming error.  Bad myFill value {myFill}")
                    raise GramError(gm)

            if theLineThickness:
                myLineThickness = cmForLineThickness(theLineThickness)
                #print "b Got myLineThickness %s cm" % myLineThickness
                myLineThickness = self.svgPxForCmF(myLineThickness)
                #print "c Got myLineThickness %s px" % myLineThickness
                ss.append('stroke-width="%s"' % myLineThickness)

            myRotate = self.getRotate()
            if myRotate:
                ss.append('transform="rotate(%.2f, %.2f, %.2f)"' % (
                    -myRotate, self.svgPxForCmF(self.cA.xPosn), -self.svgPxForCmF(self.cA.yPosn)))

            ss.append('/>\n')

        ss.append('<text id="%s"' % self.gId)  # GramText.getSvg()
        # print(f"GramText.getSvg()  myClass is {myClass}")
        if myClass:
            ss.append('class="%s"' % myClass)

        # preserve spaces.  The default mucks with spaces
        # This directive is deprecated, but it is still used by inkscape, so
        # leave it.   When svg v 2 is more fully supported by inkscape,
        # then use style="white-space: pre" instead
        # This has been put in Gram.svgWriteToOpenFile()
        #if self.svgTextPreserveWhitespace:
        #    ss.append('xml:space="preserve"')

        myX = (self.svgPxForCmF(self.cA.xPosn))


        ss.append('x="%.2f" y="%.2f"' %
                  (myX, -self.svgPxForCmF(self.cA.yPosn)))
        #ss.append('dy="0.35em" dx="1ex"')
        ss.append('font-size="%s"' % myTextSizeStr)
        if myDx:
            ss.append('dx="%.2f"' % myDx)
        if myDy:
            if self.rawText.startswith("in order"):
                print(f"{gm[0]} dy {myDy:.2f}")
            ss.append('dy="%.2f"' % myDy)


        myTextShape = self.getTextShape()  #  ['itshape', 'scshape', "upshape"]     # and slshape?
        # # print(f"{gm[0]}, got myTextShape {myTextShape}, font {self.font}")
        # # if myTextShape == 'scshape':
        # #     ss.append('font-variant="small-caps"')
        # #     #gm.append("Small caps is currently off for SVG.") # because inkscape cannot measure it
        # #     #raise GramError(gm)
        # if myTextShape == "upshape":
        #     pass
        # if myTextShape == None:
        #     pass
        # if myTextShape == 'itshape':
        #     if self.font in ['helvetica', 'lms']:
        #         ss.append('font-style="oblique"')
        #     elif self.font in ['lmr', 'palatino', "times"]:
        #         ss.append('font-style="italic"')
        #     else:
        #         gm.append("itshape specified, but not for %s.  Fixme!" % self.font)
        #         raise GramError(gm)

        # # Since font-weight is part of the style, I need to use "style=..."
        myTextSeries = self.getTextSeries()   # 'bfseries' or 'mdseries'
        # if myTextSeries == "bfseries":
        #     ss.append('style="font-weight:bold"')   # or a number?
        # elif myTextSeries == "mdseries":
        #     ss.append('style="font-weight:normal"')

        textStyles=[]

        if myTextShape == "itshape":
            textStyles.append("font-style:italic")
        else:
            if myTextShape != "scshape":
                textStyles.append("font-style:normal")

        if myTextShape == "scshape":
            # For lmr, it should have a class that defines font-variant: normal
            if self.font in ["lmr"]:
            #    textStyles.append("font-variant: small-caps")
                pass
        if myTextSeries == "bfseries":
            textStyles.append("font-weight:bold")
        else:
            textStyles.append("font-weight:normal")
        if textStyles:
            textStyles = ";".join(textStyles)
            textStyles = f'style="{textStyles}"'
            ss.append(textStyles)

        myColor = self.getColor()
        # print(f"GramText.getSvg() after getColor(); myColor is {myColor};  {self.rawText}")
        if myColor:
            if myColor == True:
                pass  # in svg text, absence of fill means fill="black"
            elif isinstance(myColor, GramColor):
                colourOptions = myColor.getSvgOptions(stroke="fill")
                # print(f"GramText.getSvg() got colourOptions {colourOptions}")
                ss += colourOptions
            else:
                gm.append(f"unknown myColor {myColor}; programming error")
                raise GramError(gm)

        # print(f"GramText.getSvg() Gram._svgHackDoRotate is  {Gram._svgHackDoRotate}")
        if Gram._svgHackDoRotate:
            myRotate = self.getRotate()
            # print(f"GramText.getSvg() myRotate is  {myRotate}")
            if myRotate:
                ss.append('transform="rotate(%.2f, %.2f, %.2f)"' % (
                    -myRotate, self.svgPxForCmF(self.cA.xPosn), -self.svgPxForCmF(self.cA.yPosn)))

        if Gram._svgHack_x_Only:
            ss.append('>x</text>')
        else:
            # both rawText and titleAttribute at once, so no space between text and <title>
            if self.titleAttribute:
                ss.append(">%s<title>\n%s</title></text>" % (self.rawText, self.titleAttribute))
            else:
                ss.append(">%s</text>" % self.rawText)

        if self.showTextBB:
            # Tight bb first
            if 1:
                if myAnch in ["mid", "mid east", "mid west"]:
                    ss.append('\n<rect x="%.2f" y="%.2f"  width="%.2f" height="%.2f"' % (
                        self.svgPxForCmF(self.cA.xPosn) + myDx,
                        -self.svgPxForCmF(self.cA.yPosn + self.fullHeight - self.underhang),
                        self.svgPxForCmF(self.width),
                        self.svgPxForCmF(self.fullHeight)))
                else:
                    ss.append('\n<rect x="%.2f" y="%.2f"  width="%.2f" height="%.2f"' % (
                        self.svgPxForCmF(self.cA.xPosn) + myDx,
                        -self.svgPxForCmF(self.cA.yPosn + self.fullHeight - self.underhang) + myDy,
                        self.svgPxForCmF(self.width),
                        self.svgPxForCmF(self.fullHeight)))
                myRotate = self.getRotate()
                if myRotate:
                    ss.append('transform="rotate(%.2f, %.2f, %.2f)"' % (
                        -myRotate, self.svgPxForCmF(self.cA.xPosn), -self.svgPxForCmF(self.cA.yPosn)))
                ss.append('stroke="blue" fill="none" stroke-width="0.1" stroke-opacity="0.5"/>')


            # baseline
            if 1:
                ss.append('\n<line x1="%.2f" y1="%.2f" x2="%.2f" y2="%.2f"' % (
                    self.svgPxForCmF(self.cA.xPosn) + myDx,
                    -self.svgPxForCmF(self.cA.yPosn) + myDy,
                    self.svgPxForCmF(self.cA.xPosn + self.width) + myDx,
                    -self.svgPxForCmF(self.cA.yPosn) + myDy))
                myRotate = self.getRotate()
                if myRotate:
                    ss.append('transform="rotate(%.2f, %.2f, %.2f)"' % (
                        -myRotate, self.svgPxForCmF(self.cA.xPosn), -self.svgPxForCmF(self.cA.yPosn)))
                ss.append('stroke="red" fill="none" stroke-width="0.1" stroke-opacity="0.5"/>')

            # ss.append('\n<rect x="%.2f" y="%.2f"  width="%.2f" height="%.2f"' % (
            #     self.bb[0] * self.svgPxForCm, -self.bb[3] * self.svgPxForCm,
            #     (self.bb[2] - self.bb[0]) * self.svgPxForCm, (self.bb[3] - self.bb[1]) * self.svgPxForCm))
            # ss.append('stroke="red" fill="none" stroke-width="0.5" />')

            # bb
            ss.append("\n\n<!-- bb -->\n")
            ss.append('\n<rect x="%.2f" y="%.2f"  width="%.2f" height="%.2f"' % (
                self.svgPxForCmF(self.bb[0]),
                -self.svgPxForCmF(self.bb[3]),
                self.svgPxForCmF(self.bb[2] - self.bb[0]),
                self.svgPxForCmF(self.bb[3] - self.bb[1])))
            ss.append('stroke="red" fill="none" fill-opacity="0.5" stroke-width="0.2" stroke-opacity="0.5"/>')

        if self.showTextAnchor:
            ss.append('\n<circle cx="%.2f" cy="%.2f" r="2" stroke="none" fill="red" opacity="0.5"/>' % (
                self.svgPxForCmF(self.cA.xPosn), -self.svgPxForCmF(self.cA.yPosn)))
        ret = ' '.join(ss)
        # print ret
        return ret


class GramLine(GramGraphic):

    def __init__(self, cA, cB):
        GramGraphic.__init__(self)
        self.cA = cA
        self.cB = cB
        self._color = True

    def getTikz(self):
        #gm = ['GramLine.getTikz()']
        ss = []
        ss.append('\\draw')

        options = self.getTikzOptions()
        if options:
            ss.append('[%s]' % ','.join(options))

        if self.cA.name:
            ss.append('(%s)' % self.cA.name)
        else:
            ss.append('(%.3f,%.3f)' % (self.cA.xPosn, self.cA.yPosn))
        ss.append('--')
        if self.cB.name:
            ss.append('(%s);' % self.cB.name)
        else:
            ss.append('(%.3f,%.3f);' % (self.cB.xPosn, self.cB.yPosn))

        # For debugging.  Obviously this is not text.
        # if self.showTextAnchor:
        #    ss.append("\\draw [blue] plot[only marks,mark=*] coordinates {(%.3f,%.3f)};" % (self.cA.xPosn, self.cA.yPosn))
        #    ss.append("\\draw [green] plot[only marks,mark=*] coordinates {(%.3f,%.3f)};" % (self.cB.xPosn, self.cB.yPosn))
        return ' '.join(ss)


    def getSvg(self):   # GramLine
        gm = ['GramLine.getSvg()']
        ss = []
        ss.append('<line')

        ss.append('x1="%.1f" y1="%.1f"' % (
            self.svgPxForCmF(self.cA.xPosn), -self.svgPxForCmF(self.cA.yPosn)))
        ss.append('x2="%.1f" y2="%.1f"' % (
            self.svgPxForCmF(self.cB.xPosn), -self.svgPxForCmF(self.cB.yPosn)))

        options = self.getSvgOptions()
        #print(f"GramLine.getSvg() getSvgOptions {options}")
        ss += options

        if self.titleAttribute:
            ss.append("><title>\n%s</title></line>" % self.titleAttribute)
        else:
            ss.append('/>')
        return ' '.join(ss)

    def setBB(self):
        theLineThickness = cmForLineThickness(self.getLineThickness())
        halfLT = theLineThickness / 2.
        if self.cA.xPosn < self.cB.xPosn:
            self.bb[0] = self.cA.xPosn - halfLT
            self.bb[2] = self.cB.xPosn + halfLT
        else:
            self.bb[0] = self.cB.xPosn + halfLT
            self.bb[2] = self.cA.xPosn - halfLT

        if self.cA.yPosn < self.cB.yPosn:
            self.bb[1] = self.cA.yPosn - halfLT
            self.bb[3] = self.cB.yPosn + halfLT
        else:
            self.bb[1] = self.cB.yPosn + halfLT
            self.bb[3] = self.cA.yPosn - halfLT



class GramRect(GramLine):

    def __init__(self, cA, cB):
        GramLine.__init__(self, cA, cB)
        self._color = None    # This week, color is not used by GramRect; just use draw and fill.
        self._draw = True
        self.setGIdAndAddToDict('rect')
        # print(f"GramRect.__init__()  self.color = {self.color} self.draw = {self.draw}  self.fill = {self.fill}")

    def getTikz(self):  # GramRect
        ss = []

        #ss.append(r"\draw[gray,very thin] (0,0) grid (4,4);")

        #ss.append('\\draw')
        ss.append('\\path')

        options = self.getTikzOptions()
        if options:
            ss.append('[%s]' % ','.join(options))

        if self.cA.name:
            ss.append('(%s)' % self.cA.name)
        else:
            ss.append('(%.3f,%.3f)' % (self.cA.xPosn, self.cA.yPosn))
        ss.append('rectangle')
        if self.cB.name:
            ss.append('(%s);' % self.cB.name)
        else:
            ss.append('(%.3f,%.3f);' % (self.cB.xPosn, self.cB.yPosn))

        if 0:
            self.setBB()
            bbLine = '\n'
            bbLine += "\\draw [red,ultra thin] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (
                self.bb[0], self.bb[1],
                self.bb[2], self.bb[3])
            ss.append(bbLine)
        if 0:
            ss.append(
                "\\draw plot[only marks,mark=+] coordinates {(%.3f,%.3f)};" % (self.cA.xPosn, self.cA.yPosn))
            ss.append(
                "\\draw plot[only marks,mark=+] coordinates {(%.3f,%.3f)};" % (self.cB.xPosn, self.cB.yPosn))

        return ' '.join(ss)

    def getSvg(self):  # GramRect
        gm = [f'GramRect.getSvg(), color {self.color}, draw {self.draw}, fill {self.fill}']
        # print(gm[0], self.gId, self.color)

        ss = []
        ss.append('<rect id="%s" ' % self.gId)
        ss.append('x="%.2f" y="%.2f"' % (
            self.svgPxForCmF(self.cA.xPosn), -self.svgPxForCmF(self.cB.yPosn)))
        ss.append('width="%.2f" height="%.2f"' % (
            self.svgPxForCmF(self.cB.xPosn - self.cA.xPosn),
            self.svgPxForCmF(self.cB.yPosn - self.cA.yPosn)))

        options = self.getSvgOptions()
        if 0:
            print("GramRect.getSvg()  SVG options")
            print(gm[0])
            for opti in options:
                print("            %s" % opti)
        ss += options

        if self.titleAttribute:
            ss.append("><title>\n%s</title></rect>" % self.titleAttribute)
        else:
            ss.append('/>')
        #print(' '.join(ss))
        return ' '.join(ss)


class GramPdf(GramGraphic):

    def __init__(self, pdf_fName):
        GramGraphic.__init__(self)
        gm = ['GramPdf.__init__()']

        self.jpegPxPerCm = 100

        if not os.path.isfile(pdf_fName):
            gm.append("Can't find pdf file '%s'" % pdf_fName)
            raise GramError(gm)
        self.pdf_fName = pdf_fName
        theBasename = os.path.basename(self.pdf_fName)
        gif_fName = '%s.gif' % theBasename
        # if os.path.exists(gif_fName):
        #    gm.append("The file %s exists.  It should not.  Get rid of it." % gif_fName)
        #    raise GramError(gm)
        self.gif_fName = gif_fName
        self.jpeg_fName = '%s.jpeg' % theBasename

        identifyLines = None
        if func.which('gm'):
            try:
                po = Popen(['gm', 'identify', '-verbose', '%s' %
                            self.pdf_fName], stdout=PIPE, stderr=PIPE)
            except OSError:
                gm.append(
                    "Could not find the gm (GraphicsMagick) 'identify' program.  Install it.")
                raise GramError(gm)
            ret_tup = po.communicate()
            # print "GramPdf init.  identify returns", ret_tup
            spl = None
            if ret_tup[0]:
                #spl = ret_tup[0].split()
                identifyLines = [l.strip() for l in ret_tup[0].split('\n')]
            else:
                if ret_tup[1]:
                    gm.append("Got stderr: %s" % ret_tup[1])
                gm.append("Could not 'identify' the pdf.")
                raise GramError(gm)
        elif func.which('identify'):
            try:
                po = Popen(
                    ['identify', '-verbose', '%s' % self.pdf_fName], stdout=PIPE, stderr=PIPE)
            except OSError:
                gm.append(
                    "Could not find the ImageMagick 'identify' program.  Install it.")
                raise GramError(gm)
            ret_tup = po.communicate()
            # print "GramPdf init.  (ImageMagick) identify returns", ret_tup
            if ret_tup[0]:
                identifyLines = [l.strip() for l in ret_tup[0].split('\n')]
            else:
                if ret_tup[1]:
                    gm.append("Got stderr: %s" % ret_tup[1])
                gm.append("Could not 'identify' the pdf.")
                raise GramError(gm)
        else:
            raise GramError(
                "Cant find GraphicsMagick identify or ImageMagick identify.")

        # print identifyLines
        # assert spl
        # if not spl or len(spl) < 2:
        #     gm.append('Idenfication of the pdf did not work.')
        #     raise GramError(gm)
        # if spl[1] != 'PDF':
        #     gm.append("This does not appear to be a pdf file.  Or maybe the file name has spaces in it?")
        #     raise GramError(gm)
        # theDim = spl[2]
        # splDim = spl[2].split('x')
        # self.pdfWid = int(splDim[0])
        # self.pdfHeight = int(splDim[1])

        self.pdfWid = None
        self.pdfHeight = None
        for iL in identifyLines:
            if iL.startswith("Geometry:"):
                spl_iL = iL.split()
                AxB = spl_iL[1].split('+')[0]
                spl_AxB = AxB.split('x')
                self.pdfWid = int(spl_AxB[0])
                self.pdfHeight = int(spl_AxB[1])

        # Hack!
        # print "GramPdf init.  Ugly hack.  Decreasing the pdfWid by 4"
        #self.pdfWid -= 4

        print("GramPdf init. Pdf width: %.2f pt, height %.2f pt" % (self.pdfWid, self.pdfHeight))
        # 1 PostScript point = 0.35277138 mm
        self.pdfWid_cm = self.pdfWid * 0.035277138
        self.pdfHeight_cm = self.pdfHeight * 0.035277138
        print("GramPdf init. The pdf is %.2f cm x %.2f cm." % (self.pdfWid_cm, self.pdfHeight_cm))

        self.gif_pi = None  # gif photoimage, used for tweakerDraw()

        # Make the jpeg
        if func.which('gm'):
            try:
                po = Popen(["gm", "convert", '-density', '%.2f' % (self.jpegPxPerCm * 2.54),
                            self.pdf_fName, self.jpeg_fName], stdout=PIPE, stderr=PIPE)
            except OSError:
                gm.append("Could not run the 'gm convert' program.")
                raise GramError(gm)
            ret_tup = po.communicate()
            if ret_tup[0] or ret_tup[1]:
                gm.append("Something wrong with gm convert.")
                gm.append("Here is what it said:")
                gm.append(ret_tup[0])
                gm.append(ret_tup[1])
                raise GramError(gm)
        elif func.which('convert'):
            try:
                po = Popen(["convert", '-density', '%.2f' % (self.jpegPxPerCm * 2.54),
                            self.pdf_fName, self.jpeg_fName], stdout=PIPE, stderr=PIPE)
            except OSError:
                gm.append("Could not run the 'convert' program.")
                raise GramError(gm)
            ret_tup = po.communicate()
            if ret_tup[0] or ret_tup[1]:
                gm.append("Something wrong with convert.")
                gm.append("Here is what it said:")
                gm.append(ret_tup)
                raise GramError(gm)
        else:
            raise GramError(
                "Cant find GraphicsMagick convert or ImageMagick convert.")

    def setBB(self):
        self.bb = [0.0, 0.0, self.pdfWid_cm, self.pdfHeight_cm]

    def getTikz(self):
        ss = []

        #ss.append(r"\draw[gray,very thin] (0,0) grid (4,4);")

        if 0:
            self.setBB()
            bbLine = '% GramPdf.getTikz() debug.  Adding a bounding box rectangle.\n'
            # bbLine += r"\draw [red,ultra thin] (%.3f,%.3f) rectangle
            # (%.3f,%.3f);" % (
            bbLine += r"\draw [red] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (
                self.bb[0], self.bb[1],
                self.bb[2], self.bb[3])
            ss.append(bbLine)
        if 0:
            ss.append(
                "\\draw plot[only marks,mark=+] coordinates {(%.3f,%.3f)};" % (self.bb[0], self.bb[1]))
            ss.append(
                "\\draw plot[only marks,mark=+] coordinates {(%.3f,%.3f)};" % (self.bb[2], self.bb[3]))

        return ' '.join(ss)



class GramJpeg(GramGraphic):

    def __init__(self, jpeg_fName, cA, scale):
        GramGraphic.__init__(self)
        gm = ['GramJpeg.__init__()']
        self.corners = None

        # x and y positions are put in self.cA, as usual
        self.cA = cA
        if not os.path.isfile(jpeg_fName):
            gm.append("Can't find jpeg file '%s'" % jpeg_fName)
            raise GramError(gm)
        self.jpeg_fName = jpeg_fName
        self.scale = scale

        identifyLines = None
        if func.which('gm'):
            try:
                po = Popen(['gm', 'identify', '-verbose', '%s' %
                            self.jpeg_fName], stdout=PIPE, stderr=PIPE)
            except OSError:
                gm.append(
                    "Could not find the gm (GraphicsMagick) 'identify' program.  Install it.")
                raise GramError(gm)
            ret_tup = po.communicate()
            # print "GramJpeg init.  gm (GraphicsMagick) identify returns",
            # ret_tup
            if ret_tup[0]:
                identifyLines = [l.strip() for l in ret_tup[0].split('\n')]
            else:
                if ret_tup[1]:
                    gm.append("Got stderr: %s" % ret_tup[1])
                gm.append("Could not identify the jpeg.")
                raise GramError(gm)
        elif func.which('identify'):
            try:
                po = Popen(
                    ['identify', '-verbose', '%s' % self.jpeg_fName], stdout=PIPE, stderr=PIPE)
            except OSError:
                gm.append(
                    "Could not find the ImageMagick 'identify' program.  Install it.")
                raise GramError(gm)
            ret_tup = po.communicate()
            print("GramJpeg init.  (ImageMagick) identify returns", ret_tup)
            if ret_tup[0]:
                identifyLines = [l.strip() for l in ret_tup[0].split('\n')]
            else:
                if ret_tup[1]:
                    gm.append("Got stderr: %s" % ret_tup[1])
                gm.append("Could not identify the jpeg.")
                raise GramError(gm)
        else:
            raise GramError(
                "Cant find GraphicsMagick identify or ImageMagick identify.")

        # print identifyLines

        # We want the geometry and the resolution.
        # GraphicsMagick:
        #   Geometry: 1518x1520
        #   Resolution: 254x254 pixels/inch
        # or
        #   Resolution: 118x118 pixels/centimeter
        # ImageMagick:
        #   Geometry: 1518x1520+0+0
        #   Resolution: 254x254

        self.jpegWid_px = None
        self.jpegHeight_px = None
        self.resolution_dpi = None

        for iL in identifyLines:
            if iL.startswith("Geometry:"):
                spl_iL = iL.split()
                AxB = spl_iL[1].split('+')[0]
                spl_AxB = AxB.split('x')
                self.jpegWid_px = int(spl_AxB[0])
                self.jpegHeight_px = int(spl_AxB[1])

            elif iL.startswith("Resolution:"):
                spl_iL = iL.split()

                # pixels/something
                theUnits = spl_iL[2]
                spl_units = theUnits.split('/')
                unitNumerator = spl_units[0]
                assert unitNumerator == 'pixels'
                unitDenominator = spl_units[1]

                AxB = spl_iL[1]
                spl_AxB = AxB.split('x')
                rA = int(round(float(spl_AxB[0])))
                rB = int(round(float(spl_AxB[1])))
                if rA != rB:
                    raise GramError(
                        "GramJpeg.  Odd -- the two resolutions of the jpg are not the same!")
                if unitDenominator == 'inch':
                    self.resolution_dpi = rA
                elif unitDenominator == 'centimeter':
                    self.resolution_dpi = int(round(float(spl_AxB[0]) * 2.54))
                else:
                    raise GramError(
                        "I don't know unitDenominator %s.  Fix me." % unitDenominator)

        if not self.resolution_dpi:
            # This in GraphicsMagick
            #    X Resolution: 4718592/65536
            #    Y Resolution: 4718592/65536
            #    Resolution Unit: 2
            for iL in identifyLines:
                if iL.startswith('X Resolution:'):
                    lastBit = iL.split()[2]
                    splLastBit = lastBit.split('/')
                    theFloat = float(splLastBit[0]) / float(splLastBit[1])
                    rA = int(theFloat)
                elif iL.startswith('Y Resolution:'):
                    lastBit = iL.split()[2]
                    splLastBit = lastBit.split('/')
                    theFloat = float(splLastBit[0]) / float(splLastBit[1])
                    rB = int(theFloat)
                elif iL.startswith('Resolution Unit:'):
                    lastBit = iL.split()[2]
                    resUnit = int(lastBit)
                    if resUnit != 2:
                        raise GramError(
                            "GramJpeg.  Not sure what is going on here.  Resolution Unit ?!?  Fix me")
            if not rA or not rB:
                raise GramError("GramJpeg.  Failed to get resolution")
            if rA != rB:
                raise GramError(
                    "GramJpeg.  Odd -- x res and y res are not the same.")
            self.resolution_dpi = rA

        if not self.jpegWid_px:
            raise GramError("GramJpeg.  Failed to get jpegWid_px")
        if not self.jpegHeight_px:
            raise GramError("GramJpeg.  Failed to get jpegHeight_px")
        if not self.resolution_dpi:
            raise GramError("GramJpeg.  Failed to get resolution_dpi")

        print("GramJpeg. Got wid_px %i, height_px %i, and resolution (dpi) %i" % (
            self.jpegWid_px, self.jpegHeight_px, self.resolution_dpi))

        self.jpegWid_cm = (
            (float(self.jpegWid_px) / self.resolution_dpi) * 2.54) * self.scale
        self.jpegHeight_cm = (
            (float(self.jpegHeight_px) / self.resolution_dpi) * 2.54) * self.scale
        print("GramJpeg.__init__()  Got jpegWid_cm %.2f, jpegHeight_cm %.2f" % (
            self.jpegWid_cm, self.jpegHeight_cm))


        self.gX = 0.0
        self.gY = 0.0

    def setBB(self):
        gm = ["GramJpeg() '%s'  setBB()" % self.jpeg_fName]
        if not self.cA:
            self.cA = GramCoord()

        theAnch = self.getAnch()
        if theAnch and theAnch not in ['west', 'north west', 'north', 'north east', 'east',
                                       'south west', 'south', 'south east',
                                       'center']:
            gm.append("anchor '%s' does not work for jpegs")
            raise GramError(gm)

        if 1:

            halfHeight = self.jpegHeight_cm / 2.0
            halfWidth = self.jpegWid_cm / 2.0

            theAnch = self.getAnch()

            if theAnch == 'south west':
                self.bb[0] = self.cA.xPosn
                self.bb[1] = self.cA.yPosn
                self.bb[2] = self.cA.xPosn + self.jpegWid_cm
                self.bb[3] = self.cA.yPosn + self.jpegHeight_cm

            elif theAnch == 'south':
                self.bb[0] = self.cA.xPosn - halfWidth
                self.bb[1] = self.cA.yPosn
                self.bb[2] = self.cA.xPosn + halfWidth
                self.bb[3] = self.cA.yPosn + self.jpegHeight_cm

            elif theAnch == 'south east':
                self.bb[0] = self.cA.xPosn - self.jpegWid_cm
                self.bb[1] = self.cA.yPosn
                self.bb[2] = self.cA.xPosn
                self.bb[3] = self.cA.yPosn + self.jpegHeight_cm

            elif theAnch == 'east':
                self.bb[0] = self.cA.xPosn - self.jpegWid_cm
                self.bb[1] = self.cA.yPosn - halfHeight
                self.bb[2] = self.cA.xPosn
                self.bb[3] = self.cA.yPosn + halfHeight

            elif theAnch == 'north east':
                self.bb[0] = self.cA.xPosn - self.jpegWid_cm
                self.bb[1] = self.cA.yPosn - self.jpegHeight_cm
                self.bb[2] = self.cA.xPosn
                self.bb[3] = self.cA.yPosn

            elif theAnch == 'north':
                self.bb[0] = self.cA.xPosn - halfWidth
                self.bb[1] = self.cA.yPosn - self.jpegHeight_cm
                self.bb[2] = self.cA.xPosn + halfWidth
                self.bb[3] = self.cA.yPosn

            elif theAnch == 'north west':
                self.bb[0] = self.cA.xPosn
                self.bb[1] = self.cA.yPosn - self.jpegHeight_cm
                self.bb[2] = self.cA.xPosn + self.jpegWid_cm
                self.bb[3] = self.cA.yPosn

            elif theAnch == 'west':
                self.bb[0] = self.cA.xPosn
                self.bb[1] = self.cA.yPosn - halfHeight
                self.bb[2] = self.cA.xPosn + self.jpegWid_cm
                self.bb[3] = self.cA.yPosn + halfHeight

            elif theAnch == 'center' or theAnch is None:
                self.bb[0] = self.cA.xPosn - halfWidth
                self.bb[1] = self.cA.yPosn - halfHeight
                self.bb[2] = self.cA.xPosn + halfWidth
                self.bb[3] = self.cA.yPosn + halfHeight

            else:
                raise GramError("anch '%s' not implemented." % theAnch)

            theRotate = self.getRotate()
            if theRotate:
                # The picture rotates around its anchor.
                # print "   *jpeg.bb %.2f %.2f %.2f %.2f " % (
                #        self.bb[0], self.bb[1], self.bb[2], self.bb[3])
                corners = []
                corners.append([self.bb[0], self.bb[1]])
                corners.append([self.bb[2], self.bb[1]])
                corners.append([self.bb[2], self.bb[3]])
                corners.append([self.bb[0], self.bb[3]])
                # print "xPosn=%.1f, yPosn=%.1f" % (self.cA.xPosn,
                # self.cA.yPosn)
                for cNum in range(4):
                    corner = corners[cNum]
                    corner[0] -= self.cA.xPosn
                    corner[1] -= self.cA.yPosn
                polarCorners = []
                for cNum in range(4):
                    polarCorners.append(func.square2polar(corners[cNum]))
                # print "a polarCorners = ", polarCorners
                rads = (theRotate * math.pi) / 180.
                # print "theRotate %f is %f radians" % (theRotate, rads)
                for cNum in range(4):
                    pCorner = polarCorners[cNum]
                    pCorner[0] += rads
                # print "b polarCorners = ", polarCorners

                corners = []
                for cNum in range(4):
                    corners.append(func.polar2square(polarCorners[cNum]))
                # print 'corners', corners
                for cNum in range(4):
                    corner = corners[cNum]
                    corner[0] += self.cA.xPosn
                    corner[1] += self.cA.yPosn
                # print corners

                llx = 1000000.
                lly = 1000000.
                urx = -1000000.
                ury = -1000000.

                for cNum in range(4):
                    corner = corners[cNum]
                    if corner[0] < llx:
                        llx = corner[0]
                    if corner[1] < lly:
                        lly = corner[1]
                    if corner[0] > urx:
                        urx = corner[0]
                    if corner[1] > ury:
                        ury = corner[1]
                self.bb = [llx, lly, urx, ury]
                # print "   @tb.bb %.2f %.2f %.2f %.2f " % (
                #         self.bb[0], self.bb[1], self.bb[2], self.bb[3])
                self.corners = corners

            theXShift = self.getXShift()
            if theXShift:
                self.bb[0] += theXShift
                self.bb[2] += theXShift
                if self.corners:
                    for cNum in range(4):
                        self.corners[cNum][0] += theXShift
            theYShift = self.getYShift()
            if theYShift:
                self.bb[1] += theYShift
                self.bb[3] += theYShift
                if self.corners:
                    for cNum in range(4):
                        self.corners[cNum][1] += theYShift

    def getTikz(self):
        # self.setBB()  Is this needed here?
        ss = []
        ss.append(r'\node')

        options = self.getTikzOptions()
        if options:
            ss.append('[%s]' % ','.join(options))
        if self.cA.name:
            ss.append('at (%s)' % self.cA.name)
        else:
            ss.append('at (%.3f,%.3f)' % (self.cA.xPosn, self.cA.yPosn))

        ss.append(
            '{\\includegraphics[scale=%.3f]{../%s}};' % (self.scale, self.jpeg_fName))

        if 0:
            self.setBB()
            bbLine = '% GramPdf.getTikz() debug.  Adding a bounding box rectangle.\n'
            # bbLine += r"\draw [red,ultra thin] (%.3f,%.3f) rectangle
            # (%.3f,%.3f);" % (
            bbLine += r"\draw [red] (%.3f,%.3f) rectangle (%.3f,%.3f);" % (
                self.bb[0], self.bb[1],
                self.bb[2], self.bb[3])
            ss.append(bbLine)
        if 0:
            ss.append(
                "\\draw plot[only marks,mark=+] coordinates {(%.3f,%.3f)};" % (self.bb[0], self.bb[1]))
            ss.append(
                "\\draw plot[only marks,mark=+] coordinates {(%.3f,%.3f)};" % (self.bb[2], self.bb[3]))

        return ' '.join(ss)



class GramError(Exception):

    """A class for exceptions in gram.

    You can raise this with a string, or a list of strings.  If its
    a single string, it gets wrapped.  If its a list of 2 strings, the
    first one is output flush and unwrapped, and the second is
    indented and wrapped."""

    def __init__(self, msg=''):
        myIndent = ' ' * 4
        if isinstance(msg, str):
            #self.msg = '\n\n' + textwrap.fill(msg, 70, initial_indent=myIndent, subsequent_indent=myIndent)
            try:
                if msg.startswith('\n\n'):
                    firstLine = '%s' % msg
                elif msg.startswith('\n'):
                    firstLine = '\n%s' % msg
                else:
                    firstLine = '\n\n%s' % msg
            except:
                firstLine = ''
            self.msg = firstLine

        elif isinstance(msg, list):
            try:
                if msg[0].startswith('\n\n'):
                    firstLine = '%s' % msg[0]
                elif msg[0].startswith('\n'):
                    firstLine = '\n%s' % msg[0]
                else:
                    firstLine = '\n\n%s' % msg[0]
            except:
                firstLine = ''
            niceMsgList = [firstLine]
            for i in range(len(msg))[1:]:
                if isinstance(msg[i], str):
                    #  If it is short, use it as is.  If it is long, wrap it.
                    if len(msg[i]) < 66:
                        niceMsgList.append(myIndent + msg[i])
                    else:
                        wLine = textwrap.fill(msg[i], 70, initial_indent=myIndent, subsequent_indent=myIndent)
                        niceMsgList.append(wLine)
                else:
                    pass

            self.msg = '\n'.join(niceMsgList)
        else:
            self.msg = ''
        Exception.__init__(self)

    def __str__(self):
        return self.msg


# makeStuff_1 =  """TEXFILEROOT = t
#EPS_TEXFILEROOT = t
#"""
# OUTFILEROOT goes here, between makeStuff_1 and makeStuff_2.
# No!, no more makeStuff_1

# The 'open' command on the mac opens the pdf with Preview.  If you
# are using linux you will want to change that to something more
# appropriate.  Evince? ggv?

makeStuff_2 = """

# For debugging, remove the '> /dev/null' bit, so you can see the error messages!
pdf: $(TEXFILEROOT).tex
\t$(LATEXPROGRAM) $(TEXFILEROOT).tex > /dev/null
\t$(PDFVIEWER) $(TEXFILEROOT).pdf

pdfPage: $(TEXFILEROOT).tex
\t$(LATEXPROGRM) $(TEXFILEROOT).tex > /dev/null
\t$(PDFVIEWER) $(TEXFILEROOT).pdf
"""

makeStuff_2b = """

pdf: $(TEXFILEROOT).tex
\t$(LATEXPROGRAM) $(TEXFILEROOT).tex
\t$(PDFVIEWER) $(TEXFILEROOT).pdf

pdfPage: $(TEXFILEROOT).tex
\t$(LATEXPROGRAM) $(TEXFILEROOT).tex
\t$(PDFVIEWER) $(TEXFILEROOT).pdf
"""

makeStuff_3 = """
composite:$(COMPOSITEROOT).tex
\trm -f $(COMPOSITEOUTFILEROOT).pdf
\t$(LATEXPROGRAM) $(COMPOSITEROOT).tex
\tmv $(COMPOSITEROOT).pdf $(COMPOSITEOUTFILEROOT).pdf
\t$(PDFVIEWER) $(COMPOSITEOUTFILEROOT).pdf
"""

# makeStuff_4 = """

# ps: $(TEXFILEROOT).tex
# \tlatex $(TEXFILEROOT).tex
# \tdvips -Ppdf -o $(OUTFILEROOT).ps $(TEXFILEROOT)

# # making an eps with dvips -E might work, or might not ...
# eps: $(EPS_TEXFILEROOT).tex
# \tlatex $(EPS_TEXFILEROOT).tex
# \tdvips -Ppdf -E -o $(OUTFILEROOT).eps $(EPS_TEXFILEROOT)

# clean:
# \trm -f $(TEXFILEROOT).aux  $(TEXFILEROOT).dvi  $(TEXFILEROOT).log
# \trm -f $(EPS_TEXFILEROOT).aux  $(EPS_TEXFILEROOT).dvi  $(EPS_TEXFILEROOT).log
# \trm -f $(JOBNAME).aux $(JOBNAME).log


# """

makeStuff_4 = """
clean:
\trm -f $(TEXFILEROOT).aux  $(TEXFILEROOT).log

"""


# tTexStuff_1 = r"""\documentclass[%ipt]{standalone}
#\usepackage{tikz}
#"""
# tTexStuff_1 = r"""\documentclass[%ipt,a4paper]{scrartcl}
#\usepackage{tikz}
#"""
# tTexStuff_1 = r"""\documentclass[%ipt,a4paper,extrafontsizes]{memoir}
#\usepackage{tikz}
#"""


# texStuffExtras goes here

tTexStuff_2 = r"""\renewcommand\floatpagefraction{1.0}
\renewcommand\topfraction{1.0}
\renewcommand\bottomfraction{1.0}
\renewcommand\textfraction{0.0}
"""

# tTexStuff_3 = r"""\begin{document}
# \thispagestyle{empty}
# """
# tTexStuff_3 = r"""\begin{document}
# """
# # inputGramLine goes here

# tTexStuff_4 = r"""\end{document}

# """


tTexStuff_5 = r"""\documentclass[%ipt,a4paper]{scrartcl}
\usepackage{graphicx}
\usepackage{pdfpages}
\usepackage[absolute,overlay]{textpos}
%%\textblockorigin{0mm}{-0.3mm}
%%\textblockorigin{0.27mm}{0.32mm}
\textblockorigin{0mm}{-1.1mm}
\setlength{\parindent}{0pt}
\begin{document}
\thispagestyle{empty}
"""


svgLMStyleFF = """

    @font-face {
        font-family: 'Latin Modern Roman';
        src: url('https://pgfoster.gitlab.io/css10/fonts/lmroman10-regular-webfont.woff') format('woff');
        font-weight: normal;
        font-style: normal;

    }

    @font-face {
        font-family: 'Latin Modern Roman';
        src: url('https://pgfoster.gitlab.io/css10/fonts/lmroman10-bold-webfont.woff') format('woff');
        font-weight: bold;
        font-style: normal;

    }

    @font-face {
        font-family: 'Latin Modern Roman';
        src: url('https://pgfoster.gitlab.io/css10/fonts/lmroman10-italic-webfont.woff') format('woff');
        font-weight: normal;
        font-style: italic;

    }

    @font-face {
        font-family: 'Latin Modern Roman';
        src: url('https://pgfoster.gitlab.io/css10/fonts/lmroman10-bolditalic-webfont.woff') format('woff');
        font-weight: bold;
        font-style: italic;

    }

    @font-face {
        font-family: 'Latin Modern Roman Caps';
        src: url('https://pgfoster.gitlab.io/css10/fonts/lmromancaps10-regular-webfont.woff') format('woff');
        font-weight: normal;
        font-style: normal;
    }

    @font-face {
        font-family: 'Latin Modern Roman Caps';
        src: url('https://pgfoster.gitlab.io/css10/fonts/lmromancaps10-oblique-webfont.woff') format('woff');
        font-weight: normal;
        font-style: italic;
    }

    @font-face {
        font-family: 'Latin Modern Sans';
        src: url('https://pgfoster.gitlab.io/css10/fonts/lmsans10-regular-webfont.woff') format('woff');
        font-weight: normal;
        font-style: normal;
    }

    @font-face {
        font-family: 'Latin Modern Sans';
        src: url('https://pgfoster.gitlab.io/css10/fonts/lmsans10-bold-webfont.woff') format('woff');
        font-weight: bold;
        font-style: normal;
    }

    @font-face {
        font-family: 'Latin Modern Sans';
        src: url('https://pgfoster.gitlab.io/css10/fonts/lmsans10-oblique-webfont.woff') format('woff');
        font-weight: normal;
        font-style: oblique;
    }

    @font-face {
        font-family: 'Latin Modern Sans';
        src: url('https://pgfoster.gitlab.io/css10/fonts/lmsans10-boldoblique-webfont.woff') format('woff');
        font-weight: bold;
        font-style: oblique;
    }

    @font-face {
        font-family: 'Latin Modern Mono';
        src: url('https://pgfoster.gitlab.io/css10/fonts/lmmono10-regular-webfont.woff') format('woff');
        font-weight: normal;
        font-style: normal;
    }

    @font-face {
        font-family: 'Latin Modern Mono';
        src: url('https://pgfoster.gitlab.io/css10/fonts/lmmono10-italic-webfont.woff') format('woff');
        font-weight: normal;
        font-style: italic;
    }

    text,tspan {
        font-family: %s;
    }
    .rmfamily {
        font-family: "Latin Modern Roman", serif;
    }
    .sffamily {
        font-family: "Latin Modern Sans", sans-serif;
    }
    .ttfamily {
        font-family: "Latin Modern Mono", monospace;
    }
    .scshape {
        font-family: "Latin Modern Roman Caps", serif;
    }
"""


svgHelveticaStyle = """
    text,tspan {
        font-family: Helvetica, sans-serif;
    }
    .rmfamily {
        font-family: Georgia, serif;
    }
    .sffamily {
        font-family: Helvetica, sans-serif;
    }
    .ttfamily {
        font-family: "Lucida Console", Courier, monospace;
    }
    .scshape {
        /* font-variant: small-caps;  BAD!  */
        /* font-variant-caps: small-caps;  nope! */
        font-family: "Helvetica", sans-serif;
    }
"""

svgPalatinoStyle = """
    text,tspan {
        font-family: Palatino, serif;
    }
    text.rmfamily,tspan.rmfamily {
        font-family: "Palatino", serif;
    }
    text.sffamily,tspan.sffamily {
        font-family: "Helvetica", sans-serif;
    }
    text.ttfamily,tspan.ttfamily {
        font-family: "Lucida Console", monospace;
    }
    text.scshape,tspan.scshape {
        font-variant: small-caps;        /* bad in inkscape */
        font-family: "Palatino", serif;
    }
"""

svgTimesStyle = """
    text,tspan {
        font-family: Times Roman, serif;
    }
    .rmfamily {
        font-family: "Times Roman", serif;
    }
    .sffamily {
        font-family: "Helvetica", sans-serif;
    }
    .ttfamily {
        font-family: "Lucida Console", monospace;
    }
    .scshape {
        font-variant: small-caps;           /* bad in inkscape */
        font-family: "Times Roman", serif;
    }
"""

svgFiraStyle = """

    @font-face {
        font-family: "Fira Sans";
        src: url("https://fonts.cdnfonts.com/s/15889/FiraSans-Regular.woff") format("woff");
        font-weight: normal;
        font-style: normal;
    
    }
    
    @font-face {
        font-family: "Fira Sans";
        src: url("https://fonts.cdnfonts.com/s/15889/FiraSans-Italic.woff") format("woff");
        font-weight: normal;
        font-style: italic;
    
    }
    

    @font-face {
        font-family: "Fira Sans";
        src: url("https://fonts.cdnfonts.com/s/15889/FiraSans-Bold.woff") format("woff");
        font-weight: bold;
        font-style: normal;
    
    }
    
    @font-face {
        font-family: "Fira Sans";
        src: url("https://fonts.cdnfonts.com/s/15889/FiraSans-BoldItalic.woff") format("woff");
        font-weight: bold;
        font-style: italic;
    
    }
    

    @font-face {
        font-family: "Fira Mono";
        font-style: normal;
        font-weight: normal;
        src: url("https://fonts.cdnfonts.com/s/15657/FiraMono-Regular.woff") format("woff");
    }
    @font-face {
        font-family: "Fira Mono";
        font-style: normal;
        font-weight: bold;
        src: url("https://fonts.cdnfonts.com/s/15657/FiraMono-Bold.woff") format("woff");
    }



    text,tspan {
        font-family: Fira Sans, sans-serif;
    }
    .rmfamily {
        font-family: "Georgia", serif;
    }
    .sffamily {
        font-family: "Fira Sans", sans-serif;
    }
    .ttfamily {
        font-family: "Fira Mono", monospace;
    }
    .scshape {
        font-variant: small-caps;
        font-family: "Fira Sans", sans-serif;
    }
"""

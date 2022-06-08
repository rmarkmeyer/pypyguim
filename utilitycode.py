import FileViewer
import sys

def indentEveryLine(s, indent=5):
	news = ""
	for line in s.split("\n"):
		newline = " "*indent + line
		news += ("" if news == "" else "\n") + newline
	return news

colors = [x.split(":") for x in ["black:000000", "white:ffffff", "red:ff0000", "pink:ffafaf", "green:00ff00", "blue:0000ff", "yellow:00ffff", "lightgray:e6e6e6"]]
colors = [(a[0], "#"+a[1]) for a in colors]

def translateColor(colorName):
	for color in colors:
		if color[0] == colorName:
			return color[1]
	return"#e6e6e6"   # light gray

def getColorName(colorCode):
	for color in colors:
		if color[1] == colorCode:
			return color[0]
	return "lightgray"

def showStringInEditor(s):
     fv = FileViewer.FileViewer()
     fv.showText(s)

def within(somepoint, startpoint, endpoint):
     return (startpoint.x <= somepoint.x <= endpoint.x) and (startpoint.y <= somepoint.y <= endpoint.y)

def justIdentifier(s):
     "  If the string is just a single identifier, return True.  If it is code or a call or anything else, return False. "
     for ch in s:
          if not ch.isalnum():
               return False
     return True

def encodeNewlines(s):
     news = ""
     for line in s.split("\n"):
          if len(news) == 0:
                news = line
          else:
                news += ";;;" + line
     return news

def decodeNewlines(s):
     return s.replace(";;;", "\n")

def nothing():
     pass

def kill():
     sys.exit()
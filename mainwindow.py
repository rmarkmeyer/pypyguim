#--------------------topcode, do not change!--------------------
from  tkinter import *
import tkinter.messagebox as box
import tkinter.simpledialog as simpledialog
import tkinter.filedialog as filedialog
import sys
import math
import functools


#--------------------common helper functions, do not change!--------------------
def settext(widget, newtext):
	'''
		This is how you change text in a widget.  What it does varies depending on the widget.
		Always give a string as the second parameter, even if you want to just put a number in it.
	'''
	if type(widget).__name__ == 'ScrolledList':               # have to do this because ScrolledList may not have been included
		widget.listbox.delete(0,END)
		if type(newtext) == list:
			for string in newtext:
				widget.listbox.insert(END,string)
		elif type(newtext) == str:
			for string in newtext.split('\n'):
 				widget.listbox.insert(END,string)

	elif type(widget).__name__ == 'ScrolledText':               # have to do this because ScrolledText may not have been included
		widget.text.delete('1.0', END)
		widget.text.insert('1.0', newtext)
		widget.text.mark_set(INSERT, '1.0')

	elif type(widget) == Text:
		widget.delete('1.0', END)
		widget.insert('1.0', newtext)

	elif type(widget) == Entry:
		widget.delete(0,END)
		widget.insert(0,newtext)

	elif type(widget) == Label:
		widget['text'] = newtext

	elif type(widget) == Button:
		widget.config(text=newtext)

	elif type(widget) == Checkbutton:
		widget.config(text=newtext)

	elif type(widget) == Scale:
		widget['label'] = newtext

	elif type(widget) == Listbox:
		widget.delete(0,END)
		if type(newtext) == list:
			for string in newtext:
				widget.insert(END,string)
		elif type(newtext) == str:
			for string in newtext.split('\n'):
				widget.insert(END,string)

	elif type(widget) == Menubutton:
		widget['text'] = newtext

def gettext(widget):
	'''
		This gets the contents of a widget and returns a string.  If it is a label, it just returns the label text.
		If it is a button, it returns the text on the face of the button.  If it is a list or checkbox, it returns the
		string that is currently selected.
	'''
	if type(widget).__name__ == 'ScrolledList':
		return list(widget.listbox.get(0,END))

	elif type(widget).__name__ == 'ScrolledText':
		return widget.text.get('1.0', END+'-1c')

	elif type(widget) == Text:
		return widget.get('1.0', END+'-1c')

	elif type(widget) == Entry:
		return widget.get()

	elif type(widget) == Label:
		return widget.cget('text')

	elif type(widget) == Button:
		return widget['text']

	elif type(widget) == Checkbutton:
		return widget.cget('text')

	elif type(widget) == Scale:
		return widget['label']

	elif type(widget) == Listbox:
		return list(widget.get(0,END))

	elif type(widget) == Menubutton:
		return widget['text']

def appendtext(widget, newtext):
	'''
		This sets the text by first getting the current text and appending to the end.
		It does not automatically insert a newline or any spaces.  You should do that yourself, if desired.
	'''
	current_text = gettext(widget)
	settext(widget, current_text + newtext)

def popup(msg):
	'''
		Use this to display a quick message to the user.  Just give it a string.
	'''
	box.showinfo('msg', msg)

def askforstring(prompt):
	'''
		Use this to get a string from the user.  The prompt is what is displayed on the dialog box.
	'''
	return simpledialog.askstring('request for input', prompt)

def askforyesno(prompt):
	'''
		Use this to get a String response from the user.  It is either yes or no.
		Notice, the type of the returned object is str, not boolean!
		The prompt is what is displayed on the dialog box.
	'''
	return box.askquestion('request for yes/no', prompt)

def getselected(somelistbox):
	'''
		Use this to get the currently selected text from a listbox.
	'''
	if type(somelistbox) == Listbox:
		try:
			return somelistbox.get(somelistbox.curselection()[0])
		except:
			return ''
	else:
		return somelistbox.getselected()

def readFile(filename):
	'''
		Read contents of file whose name is filename, and return it.
		Return empty string on error.
	'''
	try:
		f = open(filename,'r')
		text = f.read()
		f.close()
		return text
	except:
		print('Error in readfile:  filename='+filename)
		return ''

def writeFile(filename, text):
	'''
		Write contents into file whose name is filename.
		Return False on error, True on success
	'''
	try:
		f = open(filename,'w')
		f.write(text)
		f.close()
		return True
	except:
		print('Error in writefile:  filename='+filename)
		return False

def exists(filename):
	'''
		Return True if file named filename exists
	'''
	return os.path.isfile(filename)


#--------------------modulecode, do not change!--------------------

##%MODULECODE
from classes import *
import sys,os
from PropertyWindow import *
from CodeWindow import *
from DocWindow import *
from MenuWindow import *
from OptionsWindow import *
from tkinter.filedialog import askopenfilename,asksaveasfilename,askdirectory
import tkinter, tkinter.filedialog
import FileBrowser
import FileViewer
import NewHelpWindow
import samples
import threading
import utilitycode

lastFileSaved = ""    # the most recent python.py GUI file that was created with writePython()

state = 0
startPoint = Point(0,0)
endPoint = Point(0,0)
boxlines = []
topBox = None
multiselected = False

def dfa(eventType, event):
     global state, startPoint, endPoint, topBox
     #print("dfa, type="+eventType+"   state="+str(state))
     if event is not None:
          thepoint = Point(event.x, event.y)
     if state == 0:
          if eventType == "move":
               state = 0
          elif eventType == "mousedown":
               startPoint = Point(event.x, event.y)
               focusBox = globals.findBoxContainingPoint(startPoint)
               if focusBox is None:
                    deselect()
                    state = 2
               else:
                    #if not focusBox.multiselected:
                    #     demultiselect()
                    #print("focusbox = "+str(focusBox.id)) 
                    #print("within LR ? " + str(focusBox.withinLRcorner(startPoint)))
                    if focusBox.withinLRcorner(startPoint):
                         select(focusBox)
                         state = 9
                    else:
                         focusBox.calculateOffset(thepoint)
                         select(focusBox)
                         state = 3
     elif state == 2:
          if eventType == "move":
               state = 0
          elif eventType == "drag":
               startPoint = Point(event.x, event.y)
               endPoint = Point(event.x, event.y)
               state = 6
     elif state == 3:
          if eventType =="move":
               state = 3
          elif eventType == "drag":
               if topBox.withinLRcorner(thepoint):
                    state = 9
               else:
                    state = 4
          elif eventType == "mousedown":
               #print("thepoint="+str(thepoint))
               #print("event dict = "+str(event.__dict__))
               focusBox = globals.findBoxContainingPoint(thepoint)
               if event.widget == propertiesB:
                    openPropertyWindow()
                    state=10
                    return
               if focusBox == None:
                    state = 0
                    deselect()
               else:
                    if focusBox != topBox:
                         #print("focusBox != topBox")
                         state = 3
                         deselect()
                         select(focusBox)
                    if multiselected and not focusBox.multiselected:
                         demultiselect()
                    if focusBox.withinLRcorner(thepoint):
                         #select(focusBox)
                         state = 9
     elif state == 4:
          if eventType == "drag":
               endPoint = thepoint
               if multiselected:
                      moveSelectedBoxes()
               else:
                      moveTopBox()
               state = 4
          elif eventType == "mouseup":
               state = 5
     elif state == 5:
          if eventType == "drag":
               state = 4
          elif eventType == "mousedown":
               focusBox = globals.findBoxContainingPoint(thepoint)
               if focusBox == None:
                    state = 0
                    deselect()
               else:
                    if not focusBox.multiselected:
                         demultiselect()
                         select(focusBox)
                         state = 3
                         focusBox.calculateOffset(thepoint)
                    elif focusBox != topBox:
                         state = 3
                         select(focusBox)
                         focusBox.calculateOffset(thepoint)
                    if topBox.withinLRcorner(thepoint):
                         state = 9
                    else:
                         focusBox.calculateOffset(thepoint)
     elif state == 6:
          if eventType == "drag":
               endPoint = Point(event.x, event.y)
               draw_red_outline()
               state = 6
          elif eventType == "mouseup":
               state = 7
     elif state == 7:
          if eventType == "makenew":
               state = 8
               clear_red_outline()
          elif eventType == "mousedown":
               #print("state=7, mousedown")
               focusBox = globals.findBoxContainingPoint(thepoint)
               if multiselected:
                    topBox = focusBox
                    if topBox is not None and not topBox.multiselected:
                          demultiselect()
                    clear_red_outline()
                    globals.repaint_all()
                    state = 4
                    return
               if focusBox == None:
                    state = 0
               elif focusBox != topBox:
                    #print("selected "+str(focusBox.id))
                    state = 3
                    select(focusBox)
                    focusBox.calculateOffset(thepoint)
               clear_red_outline()
     elif state == 8:
          topBox.calculateOffset(thepoint)
          if eventType == "drag":
               state = 4
          elif eventType == "mousedown":
               if event.widget == propertiesB:
                    openPropertyWindow()
                    state=10
                    return
               focusBox = globals.findBoxContainingPoint(thepoint)
               if focusBox == None or focusBox != topBox:
                    state = 0
                    deselect()
               elif topBox.withinLRcorner(thepoint):
                    state = 9
               else:
                    state = 3
     elif state == 9:
          if eventType == "drag":
               topBox.resize(thepoint)
          else:
               state = 0
     elif state == 10:
          state = 0
     elif state == 11:                # aligning X (no change of width)
          if eventType == "move":
               state = 11
          elif eventType == "mousedown":
               focusBox = globals.findBoxContainingPoint(thepoint)
               if focusBox == None:
                    state = 0
                    settext(someLabel, "")
               elif focusBox == topBox:
                   state = 11   #do nothing
               else:
                   focusBox.alignX(topBox, False)
     elif state == 12:                # aligning Y (no change of height)
          if eventType == "move":
               state = 12
          elif eventType == "mousedown":
               focusBox = globals.findBoxContainingPoint(thepoint)
               if focusBox == None:
                    state = 0
                    settext(someLabel, "")
               elif focusBox == topBox:
                   state = 12   #do nothing
               else:
                   focusBox.alignY(topBox, False)
     elif state == 13:                # aligning X (change of width, too)
          if eventType == "move":
               state = 13
          elif eventType == "mousedown":
               focusBox = globals.findBoxContainingPoint(thepoint)
               if focusBox == None:
                    state = 0
                    settext(someLabel, "")
               elif focusBox == topBox:
                   state = 13   #do nothing
               else:
                   focusBox.alignX(topBox, True)
     elif state == 14:                # aligning Y (change of height, too)
          if eventType == "move":
               state = 14
          elif eventType == "mousedown":
               focusBox = globals.findBoxContainingPoint(thepoint)
               if focusBox == None:
                    state = 0
                    settext(someLabel, "")
               elif focusBox == topBox:
                   state = 14   #do nothing
               else:
                   focusBox.alignY(topBox, True)
     sys.stdout.flush()
     globals.repaint_all()

def deselect():
     global topBox
     if topBox is not None:
          topBox.selected = False
          topBox = None

def demultiselect():
     global multiselected, startPoint, endPoint
     multiselected = False
     for widget in globals.widgets:
           widget.multiselected = False
           widget.selected = False
           widget.clearbox()
           widget.paintme()
     globals.repaint_all()
     startPoint = Point(0,0)
     endPoint = Point(0,0)
     sys.stdout.flush()

def select(focusbox):
     global topBox
     if topBox is not None:
          topBox.selected = False
     focusbox.selected = True
     topBox = focusbox
     #print("Just selected "+str(focusbox.id))

def move(event):
     dfa("move", event)

def drag(event):
     dfa("drag", event)

def mousedown(event):
     dfa("mousedown", event)

def mouseup(event):
     dfa("mouseup", event)

def draw_red_outline():
    global boxlines
    clear_red_outline()
    someLabel['text'] = f"{startPoint} to {endPoint}"
    #print(f"draw_box, {startPoint} to {endPoint}")
    top = mycanvas.create_line(startPoint.x, startPoint.y, endPoint.x, startPoint.y, width=2, fill="red")
    bot = mycanvas.create_line(startPoint.x, endPoint.y, endPoint.x, endPoint.y, width=2, fill="red")
    left = mycanvas.create_line(startPoint.x, startPoint.y, startPoint.x, endPoint.y, width=2, fill="red")
    right = mycanvas.create_line(endPoint.x, startPoint.y, endPoint.x, endPoint.y, width=2, fill="red")
    boxlines = [top,bot,left,right]
    #for id in boxlines:
    #    print("id=",id,end=" ")
    #print()

def clear_red_outline():
    global boxlines
    for id in boxlines:
         mycanvas.delete(id)
    boxlines = []  

def moveTopBox():
    if topBox is None: return
    #print("moveTopBox, newPoint = "+str(newPoint)+"   topBox.id="+str(topBox.id))
    topBox.moveTo(endPoint)
    topBox.paintme()

def moveSelectedBoxes():
     #print(f"multiselected={multiselected}");sys.stdout.flush()
     #print(f"topbox is None?  {topBox is None}");sys.stdout.flush()
     if topBox is None or not multiselected: return
     oldStartPoint = topBox.startPoint

     topBox.moveTo(endPoint)
     distance_x = topBox.startPoint.x -oldStartPoint.x
     distance_y = topBox.startPoint.y - oldStartPoint.y

     #print(f"distance_x={distance_x}  {distance_y}")
     for widget in globals.widgets:
          if widget != topBox:
               if widget.multiselected:
                    #print(f"Moving box {widget.id}")
                    widget.adjustPosition(distance_x, distance_y)
     globals.repaint_all()
     sys.stdout.flush()

def selectBoxesInOutline():
     global multiselected
     for widget in globals.widgets:
          widget.multiselected = False
     numselected = 0
     for widget in globals.widgets:
          bottomLeftCorner = Point(widget.startPoint.x, widget.startPoint.y + widget.height)
          if utilitycode.within(widget.startPoint, startPoint, endPoint) or utilitycode.within(bottomLeftCorner, startPoint, endPoint):
               widget.multiselected = True
               numselected += 1
     if numselected == 0:
         multiselected = False
         popup("0 boxes selected, multiselected is turned off!")
         multiselectedCB.config(fg="black")
         multi_var.set(0)
     globals.repaint_all()

def makeNewWidget():
     global topBox,startPoint,endPoint
     if state != 7:
           #  There is no red outline so we'll just make a generic button in the middle of the window
           startPoint = Point(75, 75)
           endPoint = Point(75+200, 75+90)
           
     w = MyWidget()
     w.setbox(startPoint, endPoint, mycanvas)
     globals.add(w)
     topBox = w
     clear_red_outline()
     globals.repaint_all()
     topBox.calculateOffset(startPoint)
     topBox.selected = True
     dfa("makenew", None)

def startAlignmentX():
     global topBox, state
     state = 11
     settext(someLabel, "Aligning to box #'s x" + str(topBox.id))

def startAlignmentY():
     global topBox, state
     state = 12
     settext(someLabel, "Aligning to box #'s y" + str(topBox.id))

def startAlignmentXandWidth():
     global topBox, state
     state = 13
     settext(someLabel, "Aligning to box #'s x and width" + str(topBox.id))

def startAlignmentYandHeight():
     global topBox, state
     state = 14
     settext(someLabel, "Aligning to box #'s y and height" + str(topBox.id))


def copyMultiSelected():
     #print("in copyMultiSelected")
     global topBox
     newBoxes = []
     currentlyMulti = []
     for widget in globals.widgets:
          if widget.multiselected:
               currentlyMulti.append(widget)
               #print(f"Box {widget.id} ")
     #print(f"There are {len(currentlyMulti)} multiselected")
     for widget in currentlyMulti:
         newWidget = MyWidget.copy(widget)
         newWidget.startPoint = Point(widget.startPoint.x+20, widget.startPoint.y+20)
         newWidget.endPoint = Point(widget.endPoint.x+20, widget.endPoint.y+20)
         globals.add(newWidget)
         widget.multiselected = False
         newBoxes.append(newWidget)
         widget.selected = False
         topBox = None
     #print(f"There are {len(newBoxes)} widgets in newBoxes")
     for widget in newBoxes:
           widget.multiselected = True
     globals.repaint_all()
     sys.stdout.flush()

def deleteMultis():
     global multiselected
     saveBoxes = []
     globals.deleteds = []
     for widget in globals.widgets:
          if widget.multiselected:
               globals.deleteds.append(widget)
               widget.clearbox()
               #print(f"Box {widget.id} ")
          else:
               saveBoxes.append(widget)
     globals.widgets.clear()
     for widget in saveBoxes:
          globals.widgets.append(widget)
     multiselected = False
     globals.repaint_all()

def resizeMe(event):
      w, h = event.width, event.height
      mycanvas.place(x=0, y=0, width=w, height=h-24)
      propertiesB.place(x=9, y=h-25, width=84, height=21)
      someLabel.place(x=102, y=h-25, width=363, height=21)
      multiselectedCB.place(x=w-110, y=h-25, width=110, height=21)
      globals.window_width = root.winfo_width()
      globals.window_height = root.winfo_height()

def clearWindow():
     if len(globals.widgets) == 0: 
          popup("No widgets...")
          return
     number = len(globals.widgets)
     globals.deleteAll()
     popup(f"{number} widgets deleted.\nYou can use UNDO to get all these back.")

def openPropertyWindow():
     global propwin
     if topBox is None:
          popup("Click on a widget first")
          return
     propwin = PropertyWindow()
     propwin.setTarget(topBox)
     propwin.setGlobals(globals)

def openCodeWindow():
     global codewin
     codewin = CodeWindow()
     codewin.setGlobals(globals)

def openDocWindow():
     global docwin
     docwin = DocWindow()
     docwin.setGlobals(globals)

def openMenuWindow():
     global menuwin
     menuwin = MenuWindow()
     menuwin.setGlobals(globals)

def openOptionsWindow():
     global optionswin
     optionswin = OptionsWindow()
     optionswin.setFields(globals)

def showWidgets():
     popup(globals.listWidgets())

def showCode():
     popup(globals.code)

def loadData():
     global lastFileSaved
     filename = askopenfilename()
     if filename is None or filename == "":
          return
     if os.path.isfile(filename):
          f = open(filename)
          contents = f.read()  #  this is a single string
          f.close()
          loadImage(contents)
          lastFileSaved = filename
          root.title(filename)
     print("loadData, lastFileSaved="+lastFileSaved)
     sys.stdout.flush()

def loadImage(image):
     global lastLoadedImage
     lastLoadedImage = image
     globals.clear()
     #print("~-~-~-~-loadImage, image=")
     #print(image)
     #print("\n\n\n")
     rets = globals.parse(image)
     if rets == "okay":
          globals.applyCanvas(mycanvas)
          globals.repaint_all()
          root.geometry(str(globals.window_width) + "x" + str(globals.window_height))
     else:
          popup(rets)

def loadOldStyle():
     global lastFileSaved
     filename = askopenfilename()
     if filename is None or filename == "":
          return
     if os.path.isfile(filename):
          f = open(filename)
          contents = f.read()  #  this is a single string
          f.close()
          loadImageOldStyle(contents)
          lastFileSaved = filename
          root.title(filename)
     print("loadData, lastFileSaved="+lastFileSaved)
     sys.stdout.flush()

def loadImageOldStyle(image):
     global lastLoadedImage
     lastLoadedImage = image
     globals.clear()
     globals.oldStyle = True
     rets = globals.parse(image)
     if rets == "okay":
          globals.applyCanvas(mycanvas)
          globals.repaint_all()
          root.geometry(str(globals.window_width) + "x" + str(globals.window_height))
     else:
          popup(rets)

def save():
     global lastFileSaved
     if lastFileSaved == "":
          popup("You must have a filename to save")
          return
     writeFile(lastFileSaved, globals.makePythonFile())

def saveas():
     global lastFileSaved
     filename = tkinter.filedialog.asksaveasfilename()
     fp = open(filename, "w")
     fp.write(globals.makePythonFile())
     fp.close()
     lastFileSaved = filename
     root.title(filename)

def saveDirectives():
     filename = tkinter.filedialog.asksaveasfilename()
     fp = open(filename, "w")
     fp.write(globals.makeDirectives())
     fp.close()

def runThisGui():
     global lastFileSaved
     if lastFileSaved == "":
          filename = asksaveasfilename()
          if filename is None or filename == "":
               #popup("No file, nothing done")
               #return
               filename = os.environ["USERPROFILE"]+"/Desktop/sample_python_gui.py"
          lastFileSaved = filename
     else:
          filename = lastFileSaved
     fp = open(filename,"w")
     fp.write(globals.makePythonFile())
     fp.close()
     os.system("python \"" + filename + "\"")

def showThisImage():
     showFile(globals.makePythonFile())

def keypress(event):
    global copiedBox, topBox, multiselected
    if event.char == "n":
        if state == 7:
            makeNewWidget()
    elif event.char == "m":
        if multiselected:
             multi_var.set(0)
             demultiselect()
             multiselected = False
        else:
             multi_var.set(1)
             multiselected = True
             selectBoxesInOutline()
    elif event.char == "s":
        save()
        popup("Saved!")
    elif event.char == "r":
        runThisGui()
    elif event.char == "p":
        openPropertyWindow()
    elif event.char == "c":
        if topBox == None:
            popup("You must click on a widget to select it before you try to copy it")
        else:
            copiedBox = topBox
    elif event.char == "x" or event.char == "d":
        if multiselected:
            deleteMultis()
            topBox = None
            multiselected = False
        elif topBox != None:
            globals.delWidget(topBox)
            copiedBox = topBox
            globals.deleteds = [topBox]
            topBox = None
    elif event.char == "v":
        if multiselected:
             copyMultiSelected()
        else:
             if copiedBox == None:
                 popup("You need to copy or cut a box first")
             else:
                 newWidget = MyWidget.copy(copiedBox)
                 newWidget.startPoint = Point(copiedBox.startPoint.x+20, copiedBox.startPoint.y+20)
                 newWidget.endPoint = Point(copiedBox.endPoint.x+20, copiedBox.endPoint.y+20)
                 globals.add(newWidget)
                 copiedBox.selected = False
                 topBox = newWidget
                 newWidget.selected = True
                 globals.repaint_all()
    elif event.char == "u":
        undoDelete()

    elif event.char == "C":
        openCodeWindow()
    elif event.char == "i":
        mainInfo()
    elif event.char == "f":
        openFileViewer()

    elif event.char == "h":
         if topBox is None: return
         topBox.moveLeft(1)
         globals.repaint_all()
    elif event.char == "l":
         if topBox is None: return
         topBox.moveLeft(-1)
         globals.repaint_all()
    elif event.char == "j":
         if topBox is None: return
         topBox.moveUp(-1)
         globals.repaint_all()
    elif event.char == "k":
         if topBox is None: return
         topBox.moveUp(1)
         globals.repaint_all()

    elif event.char == "H":
         if topBox is None: return
         topBox.makeWider(-1)
         globals.repaint_all()
    elif event.char == "L":
         if topBox is None: return
         topBox.makeWider(1)
         globals.repaint_all()
    elif event.char == "J":
         if topBox is None: return
         topBox.makeTaller(1)
         globals.repaint_all()
    elif event.char == "K":
         if topBox is None: return
         topBox.makeTaller(-1)
         globals.repaint_all()
    #text.insert('end', 'You pressed %s\n' % (event.char, ))

def doMultiselect():
     global multiselected
     print("in doMultiselect, multiselected="+str(multiselected))

     if multiselected:
             print("HERE!!!!")
             sys.stdout.flush()
             demultiselect()
             multiselected = False
             multiselectedCB.config(fg="black")
             #settext(multiselectedCB, "")
             print("multi="+str(multiselected))
     else:
             print("RUSSIA....")
             multiselected = True
             multiselectedCB.config(fg="red")
             selectBoxesInOutline()

             #settext(multiselectedCB, "Multiselected")
     sys.stdout.flush()

def deleteSelectedWidget():
     global topBox
     if topBox != None:
            globals.delWidget(topBox)
            copiedBox = topBox
            globals.deleteds = [topBox]
            topBox = None
            globals.repaint_all()
     else:
            popup("You need to click on a box first.")

def undoDelete():
     if len(globals.deleteds) == 0:
           popup("Nothing in the deleteds list")
           return
     for widget in globals.deleteds:
          globals.widgets.append(widget)
     globals.deleteds = []
     globals.repaint_all()

def mainInfo():
     s = "Last file saved: " + lastFileSaved + "\n"
     s += globals.info()
     popup(s)

def showVersion():
     popup("This version: " + str(current_version) + "\n" +\
           "Acceptable difference: " + str(acceptable_difference))

def globalsInfo():
    showFile(globals.longInfo())

def showLastLoaded():
     showFile(lastLoadedImage)

def openFileViewer():
     fv = FileViewer.FileViewer()

def openFileBrowser():
     fb = FileBrowser.FileBrowser()

def showFile(s):
     fv = FileViewer.FileViewer()
     fv.showText(s)

def sample1():
     loadImage(samples.sample1)
     root.title("Sample1 -- simple program")
     global lastFileSaved
     lastFileSaved = ""

def sample2():
     loadImage(samples.sample2)
     root.title("Sample2 -- button code is a function")
     global lastFileSaved
     lastFileSaved = ""

def sample3():
     loadImage(samples.sample3)
     root.title("Sample3 -- textfields and textareas")
     global lastFileSaved
     lastFileSaved = ""

def sample4():
     loadImage(samples.sample4)
     root.title("Sample4 -- prompt for a string")
     global lastFileSaved
     lastFileSaved = ""

def sample5():
     loadImage(samples.sample5)
     root.title("Sample5 -- radio buttons")
     global lastFileSaved
     lastFileSaved = ""

def sample6():
     loadImage(samples.sample6)
     root.title("Sample6 -- list widget")
     global lastFileSaved
     lastFileSaved = ""

def sample7():
     loadImage(samples.sample7)
     root.title("Sample7 -- menu events")
     global lastFileSaved
     lastFileSaved = ""

def sample8():
     loadImage(samples.sample8)
     root.title("Sample8 -- pressing enter in a textfield")
     global lastFileSaved
     lastFileSaved = ""

def sample9():
     loadImage(samples.sample9)
     root.title("Sample9 -- all widgets")
     global lastFileSaved
     lastFileSaved = ""

def openHelpWindow():
     NewHelpWindow.main()

def quitme():
	sys.exit()

def post_initialization():
    global globals
    root.bind('<Motion>', move)
    root.bind('<B1-Motion>', drag)
    root.bind("<ButtonPress-1>", mousedown)
    root.bind("<ButtonRelease-1>", mouseup)
    root.bind("<KeyPress>", keypress)
    mycanvas.config(bg="white")
    globals = Globals()
##%ENDCODE

def window_init():
     global root
     root=Tk()
     root.geometry("694x447")
     root.configure(background='#ebebeb')
     root.title("PyGuimaker")
     canvas = Canvas(bd=0, highlightthickness=0)
     canvas.pack(fill=BOTH, expand=1)
     canvas.bind("<Configure>", resizeMe)

#--------------------internally defined widget classes, do not change!--------------------


#--------------------functions for widget event handlers, do not change!--------------------
def onCheckbuttonPress_multiselectedCB(labelname):
    doMultiselect()



#--------------------Menu defs, do not change!--------------------


#--------------------extra class code, you can change this!--------------------
##%EXTRACLASSCODE

##%ENDCODE

def main():
     window_init()
     global someLabel
     global mycanvas
     global clearFirstCB_var
     global clearFirstCB
     global multi_var
     global multiselectedCB
     global propertiesB
#--------------------widget making code, do not change anything from here to the end of the file!--------------------
     someLabel = Label(root, text="",width=363,height=21)
     someLabel.place(x=102,y=418, width=363, height=21)
     someLabel.config(font=("SansSerif", 11, 'normal'))
     someLabel.config(bg=("#ffffff"))
     someLabel.config(fg=("#000000"))
     mycanvas = Canvas(root, width=682, height=413)
     mycanvas.place(x=12,y=2, width=682, height=413)
     clearFirstCB_var=IntVar()
     clearFirstCB = Checkbutton(root, text="Clear each repaint", variable=clearFirstCB_var)
     clearFirstCB.config(bg=root['bg'])
     clearFirstCB.place(x=818,y=729, width=172, height=19)
     multi_var=IntVar()
     multiselectedCB = Checkbutton(root, text="Multiselected", variable=multi_var, command=(lambda what="Multiselected":onCheckbuttonPress_multiselectedCB(what)))
     multiselectedCB.config(bg=root['bg'])
     multiselectedCB.place(x=585,y=420, width=108, height=21)
     propertiesB = Button(root, text="Properties",width=84,height=21)
     propertiesB.place(x=11,y=417, width=84, height=21)
     propertiesB.config(font=("SansSerif", 9, 'normal'))
     propertiesB.config(bg=("#ffffff"))
     propertiesB.config(fg=("#000000"))

     topmenu = Menu(root)
     root.config(menu=topmenu)
     menu1 = Menu(topmenu)
     topmenu.add_cascade(label="File", menu=menu1, underline=0)
     menu1.add_command(label="Load", command=loadData, underline=0)
     menu1.add_command(label="Save", command=save, underline=0)
     menu1.add_command(label="Save As...", command=saveas, underline=0)
     menu1.add_command(label="Save only directives", command=saveDirectives, underline=0)
     menu1.add_command(label="Quit", command=quitme, underline=0)
     menu2 = Menu(topmenu)
     topmenu.add_cascade(label="Widgets", menu=menu2, underline=0)
     menu2.add_command(label="Clear window", command=clearWindow, underline=0)
     menu2.add_command(label="New", command=makeNewWidget, underline=0)
     menu2.add_command(label="Properties", command=openPropertyWindow, underline=0)
     menu2.add_command(label="List of all widgets", command=showWidgets, underline=0)
     menu2.add_command(label="Delete selected widget", command=deleteSelectedWidget, underline=0)
     menu2.add_command(label="Undo last delete", command=undoDelete, underline=0)
     menu3 = Menu(topmenu)
     topmenu.add_cascade(label="Code", menu=menu3, underline=0)
     menu3.add_command(label="Code Window", command=openCodeWindow, underline=0)
     menu3.add_command(label="Internal documentation", command=openDocWindow, underline=0)
     menu3.add_command(label="Menus", command=openMenuWindow, underline=0)
     menu4 = Menu(topmenu)
     topmenu.add_cascade(label="Alignment", menu=menu4, underline=0)
     menu4.add_command(label="Align x", command=startAlignmentX, underline=0)
     menu4.add_command(label="Align y", command=startAlignmentY, underline=0)
     menu4.add_command(label="Align x and same width", command=startAlignmentXandWidth, underline=0)
     menu4.add_command(label="Align y and same height", command=startAlignmentYandHeight, underline=0)
     menu5 = Menu(topmenu)
     topmenu.add_cascade(label="Run", menu=menu5, underline=0)
     menu5.add_command(label="Run this gui", command=runThisGui, underline=0)
     menu6 = Menu(topmenu)
     topmenu.add_cascade(label="Info", menu=menu6, underline=0)
     menu6.add_command(label="Main info", command=mainInfo, underline=0)
     menu6.add_command(label="Globals", command=globalsInfo, underline=0)
     menu6.add_command(label="Last loaded file image", command=showLastLoaded, underline=0)
     menu6.add_command(label="What this image would be", command=showThisImage, underline=0)
     menu7 = Menu(topmenu)
     topmenu.add_cascade(label="Tools", menu=menu7, underline=0)
     menu7.add_command(label="File Viewer", command=openFileViewer, underline=0)
     menu7.add_command(label="File Browser", command=openFileBrowser, underline=0)
     menu8 = Menu(topmenu)
     topmenu.add_cascade(label="Options", menu=menu8, underline=0)
     menu8.add_command(label="Options", command=openOptionsWindow, underline=0)
     menu9 = Menu(topmenu)
     topmenu.add_cascade(label="Samples", menu=menu9, underline=0)
     menu9.add_command(label="Simple button press", command=sample1, underline=0)
     menu9.add_command(label="Button press 2", command=sample2, underline=0)
     menu9.add_command(label="Textareas and textfields", command=sample3, underline=0)
     menu9.add_command(label="Prompt for name", command=sample4, underline=0)
     menu9.add_command(label="Radio button", command=sample5, underline=0)
     menu9.add_command(label="List example", command=sample6, underline=0)
     menu9.add_command(label="Menu example", command=sample7, underline=0)
     menu9.add_command(label="Pressing enter in textfield", command=sample8, underline=0)
     menu9.add_command(label="All widgets", command=sample9, underline=0)
     menu10 = Menu(topmenu)
     topmenu.add_cascade(label="Help", menu=menu10, underline=0)
     menu10.add_command(label="Help", command=openHelpWindow, underline=0)
     menu10.add_command(label="Version", command=showVersion, underline=0)

     post_initialization()
     root.mainloop()

if __name__ == '__main__':
     main()

####DIRECTIVES
##%START
##%PROGRAM DATE=Sat, Jun 12, 2021 11:06:26 AM
##%VERSION=PY2
##%CLASS_STYLE=no class
##%WHENWRITTEN=Wed Jun 08 09:46:05 EDT 2022
##%CLASSNAME=xmainwindow
##%PACKAGENAME=
##%DIRECTORY=
##%GUITYPE=Python
##%EXTRAMETHODS=0
##%PROGTYPE=Application
##%TITLEBAR=PyGuimaker
##%SAVEMYTEXTAREA=true
##%SNAPSHOTVARLIST=
##%RUNTIMECLASSPATH=
##%BGIMAGENAME=
##%BGIMAGERESIZE=true
##%USEBGIMAGE=true
##%CANRESIZEMAINWINDOW=true
##%MENUS
##%File
##%   Load&loadData
##%   Save&save
##%   Save As...&saveas
##%   Save only directives&saveDirectives
##%   #   Load old style&loadOldStyle
##%   Quit&quitme
##%Widgets
##%   Clear window&clearWindow
##%   New&makeNewWidget
##%   Properties&openPropertyWindow
##%   List of all widgets&showWidgets
##%   Delete selected widget&deleteSelectedWidget
##%   Undo last delete&undoDelete
##%Code
##%   Code Window&openCodeWindow
##%   Internal documentation&openDocWindow
##%   Menus&openMenuWindow
##%Alignment
##%   Align x&startAlignmentX
##%   Align y&startAlignmentY
##%   Align x and same width&startAlignmentXandWidth
##%   Align y and same height&startAlignmentYandHeight
##%Run
##%   Run this gui&runThisGui
##%Info
##%   Main info&mainInfo
##%   Globals&globalsInfo
##%   Last loaded file image&showLastLoaded
##%   What this image would be&showThisImage
##%Tools
##%   File Viewer&openFileViewer
##%   File Browser&openFileBrowser
##%Options
##%  Options&openOptionsWindow
##%Samples
##%   Simple button press&sample1
##%   Button press 2&sample2
##%   Textareas and textfields&sample3
##%   Prompt for name&sample4
##%   Radio button&sample5
##%   List example&sample6
##%   Menu example&sample7
##%   Pressing enter in textfield&sample8
##%   All widgets&sample9
##%Help
##%   Help&openHelpWindow
##%   Version&showVersion
##%   #this is commented out&anything
##%ENDMENU
##%BGCOLOR=235,235,235
##%WIDTH=709
##%HEIGHT=502
##%COMPONENTS
##%COMPONENT 
##%  id=1
##%  type=Label
##%  label=
##%  varname=someLabel
##%  startpoint=102,468
##%  endpoint=465,489
##%  fgcolor=0,0,0
##%  bgcolor=255,255,255
##%  fontname=SansSerif
##%  fontsize=11
##%  fontstyle=plain
##%  samebgcolor=0
##%  fixedx=0
##%  fixedy=0
##%  resizable=1
##%  filename=
##%  scrollbar_isHorizontal=true
##%  list_rowsMultiselect=false
##%  minval=1
##%  maxval=100
##%  startingval=50
##%  rescaleImage=1
##%  moreoptions=
##%  assocvarname=someLabel_var
##%  other=
##%  codeAction=
##%  codeItem=
##%END
##%COMPONENT 
##%  id=2
##%  type=Canvas
##%  label=
##%  varname=mycanvas
##%  startpoint=12,52
##%  endpoint=694,465
##%  fgcolor=0,0,0
##%  bgcolor=119,229,175
##%  fontname=SansSerif
##%  fontsize=12
##%  fontstyle=plain
##%  samebgcolor=1
##%  fixedx=0
##%  fixedy=0
##%  resizable=1
##%  filename=
##%  scrollbar_isHorizontal=true
##%  list_rowsMultiselect=false
##%  minval=1
##%  maxval=100
##%  startingval=50
##%  rescaleImage=1
##%  moreoptions=
##%  assocvarname=canvas_var
##%  other=
##%  codeAction=
##%  codeItem=
##%END
##%COMPONENT 
##%  id=3
##%  type=Checkbox
##%  label=Clear each repaint
##%  varname=clearFirstCB
##%  startpoint=818,779
##%  endpoint=990,798
##%  fgcolor=0,0,0
##%  bgcolor=235,235,235
##%  fontname=SansSerif
##%  fontsize=12
##%  fontstyle=plain
##%  samebgcolor=1
##%  fixedx=0
##%  fixedy=0
##%  resizable=1
##%  filename=
##%  scrollbar_isHorizontal=true
##%  list_rowsMultiselect=false
##%  minval=1
##%  maxval=100
##%  startingval=50
##%  rescaleImage=1
##%  moreoptions=
##%  assocvarname=clearFirstCB_var
##%  other=
##%  codeAction=
##%  codeItem=
##%END
##%COMPONENT 
##%  id=5
##%  type=Checkbox
##%  label=Multiselected
##%  varname=multiselectedCB
##%  startpoint=585,470
##%  endpoint=693,491
##%  fgcolor=0,0,0
##%  bgcolor=235,235,235
##%  fontname=SansSerif
##%  fontsize=10
##%  fontstyle=plain
##%  samebgcolor=1
##%  fixedx=0
##%  fixedy=0
##%  resizable=1
##%  filename=
##%  scrollbar_isHorizontal=true
##%  list_rowsMultiselect=false
##%  minval=1
##%  maxval=100
##%  startingval=50
##%  rescaleImage=1
##%  moreoptions=
##%  assocvarname=multi_var
##%  other=
##%  codeAction=
##%  codeItem=doMultiselect()
##%END
##%COMPONENT 
##%  id=6
##%  type=Button
##%  label=Properties
##%  varname=propertiesB
##%  startpoint=11,467
##%  endpoint=95,488
##%  fgcolor=0,0,0
##%  bgcolor=255,255,255
##%  fontname=SansSerif
##%  fontsize=9
##%  fontstyle=plain
##%  samebgcolor=1
##%  fixedx=0
##%  fixedy=0
##%  resizable=1
##%  filename=
##%  scrollbar_isHorizontal=true
##%  list_rowsMultiselect=false
##%  minval=1
##%  maxval=100
##%  startingval=50
##%  rescaleImage=1
##%  moreoptions=
##%  assocvarname=Button1_var
##%  other=
##%  codeAction=
##%  codeItem=
##%END
##%ENDCOMPONENTS


####END
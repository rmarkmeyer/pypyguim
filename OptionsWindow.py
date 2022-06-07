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
import sys
import time

import utilitycode
import NewHelpWindow
##%ENDCODE

class OptionsWindow():
#--------------------internally defined widget classes, do not change!--------------------
     

#--------------------functions for widget event handlers, do not change!--------------------
     def colorHelpB_action_code(self):
         NewHelpWindow.main2("Colors")
     
     def applyB_action_code(self):
         self.saveBack()
         self.root.destroy()
         self.globals.repaint_all()
     
     def cancelB_action_code(self):
         self.root.destroy()
     
     def helpResizeB_action_code(self):
         NewHelpWindow.main2("Resizing")
     
     def toggleB_action_code(self):
         self.checked = not self.checked
         if self.checked:
              settext(self.allowResizeTF, "Yes")
         else:
              settext(self.allowResizeTF, "No")

#--------------------Menu defs, do not change!--------------------


#--------------------extra class code, you can change this!--------------------
##%EXTRACLASSCODE
     import sys
     
     def setFields(self, globals):
          self.globals = globals
     
          settext(self.windowTitleTF, globals.title)
          settext(self.bgcolorTF, globals.bgcolor)
          if globals.allowResize:
                 self.checked = True
                 print("allowResize=True")
                 settext(self.allowResizeTF, "Yes")
          else:
                 print("allowResize=False")
                 self.checked = False
                 settext(self.allowResizeTF, "No")
          sys.stdout.flush()
      
     def saveBack(self):
          self.globals.title = gettext(self.windowTitleTF)
          self.globals.bgcolor = gettext(self.bgcolorTF)
          self.globals.allowResize = gettext(self.allowResizeTF) == "Yes"
     
     
     def post_initialization(self):
          self.checked = False
##%ENDCODE

     def __init__(self):
          self.root=Tk()
          self.root.geometry("508x142")
          self.root.configure(background='#ebebeb')
          self.root.title("Options Window")
#--------------------widget making code, do not change anything from here to the end of the file!--------------------
          self.colorHelpB = Button(self.root, text="?",width=24,height=27,command=self.colorHelpB_action_code)
          self.colorHelpB.place(x=216,y=34, width=24, height=27)
          self.colorHelpB.config(font=("SansSerif", 10, 'normal'))
          self.colorHelpB.config(bg=("#ffffff"))
          self.colorHelpB.config(fg=("#000000"))
          self.Button1_var=StringVar()
          self.Button1_var.set("")
          self.bgcolorTF = Entry(self.root,width=92, textvariable=self.Button1_var)
          self.bgcolorTF.place(x=121,y=35, width=92, height=26)
          self.bgcolorTF.config(font=("SansSerif", 10, 'normal'))
          self.bgcolorTF.config(fg=("#000000"))
          self.bgcolorTF.config(bg=("#ffffff"))
          self.Button1_var=StringVar()
          self.Button1_var.set("")
          self.windowTitleTF = Entry(self.root,width=385, textvariable=self.Button1_var)
          self.windowTitleTF.place(x=121,y=9, width=385, height=22)
          self.windowTitleTF.config(font=("SansSerif", 10, 'normal'))
          self.windowTitleTF.config(fg=("#000000"))
          self.windowTitleTF.config(bg=("#ffffff"))
          self.component0BL = Label(self.root, text="Title of window:",width=91,height=22)
          self.component0BL.place(x=27,y=9, width=91, height=22)
          self.component0BL.config(font=("SansSerif", 10, 'normal'))
          self.component0BL.config(bg=self.root['bg'])
          self.component0BL.config(fg=("#000000"))
          self.applyB = Button(self.root, text="Apply",width=67,height=26,command=self.applyB_action_code)
          self.applyB.place(x=133,y=103, width=67, height=26)
          self.applyB.config(font=("SansSerif", 10, 'normal'))
          self.applyB.config(bg=("#ffffff"))
          self.applyB.config(fg=("#000000"))
          self.cancelB = Button(self.root, text="Cancel",width=67,height=26,command=self.cancelB_action_code)
          self.cancelB.place(x=202,y=103, width=67, height=26)
          self.cancelB.config(font=("SansSerif", 10, 'normal'))
          self.cancelB.config(bg=("#ffffff"))
          self.cancelB.config(fg=("#000000"))
          self.label3L = Label(self.root, text="Background color:",width=103,height=25)
          self.label3L.place(x=15,y=36, width=103, height=25)
          self.label3L.config(font=("SansSerif", 10, 'normal'))
          self.label3L.config(bg=self.root['bg'])
          self.label3L.config(fg=("#000000"))
          self.helpResizeB = Button(self.root, text="?",width=23,height=23,command=self.helpResizeB_action_code)
          self.helpResizeB.place(x=254,y=69, width=23, height=23)
          self.helpResizeB.config(font=("SansSerif", 10, 'normal'))
          self.helpResizeB.config(bg=("#ffffff"))
          self.helpResizeB.config(fg=("#000000"))
          self.Button1_var=StringVar()
          self.Button1_var.set("")
          self.allowResizeTF = Entry(self.root,width=63, textvariable=self.Button1_var)
          self.allowResizeTF.place(x=123,y=69, width=63, height=23)
          self.allowResizeTF.config(font=("SansSerif", 10, 'normal'))
          self.allowResizeTF.config(fg=("#000000"))
          self.allowResizeTF.config(bg=("#ffffff"))
          self.toggleB = Button(self.root, text="Toggle",width=62,height=23,command=self.toggleB_action_code)
          self.toggleB.place(x=188,y=69, width=62, height=23)
          self.toggleB.config(font=("SansSerif", 10, 'normal'))
          self.toggleB.config(bg=("#ffffff"))
          self.toggleB.config(fg=("#000000"))
          self.component1BL = Label(self.root, text="Allow resize:",width=105,height=24)
          self.component1BL.place(x=15,y=68, width=105, height=24)
          self.component1BL.config(font=("SansSerif", 10, 'normal'))
          self.component1BL.config(bg=self.root['bg'])
          self.component1BL.config(fg=("#000000"))

          self.post_initialization()
if __name__ == '__main__':
     tempwin=OptionsWindow()
     tempwin.root.mainloop()

####DIRECTIVES
##%START
##%PROGRAM DATE=Fri, Jun 11, 2021 9:25:02 PM
##%VERSION=PY2
##%CLASS_STYLE=class
##%WHENWRITTEN=Mon Jun 06 21:43:16 EDT 2022
##%CLASSNAME=OptionsWindow
##%PACKAGENAME=
##%DIRECTORY=
##%GUITYPE=Python
##%EXTRAMETHODS=0
##%PROGTYPE=Application
##%TITLEBAR=Options Window
##%SAVEMYTEXTAREA=true
##%SNAPSHOTVARLIST=
##%RUNTIMECLASSPATH=
##%BGIMAGENAME=
##%BGIMAGERESIZE=true
##%USEBGIMAGE=true
##%CANRESIZEMAINWINDOW=true
##%MENUS
##%ENDMENU
##%BGCOLOR=235,235,235
##%WIDTH=523
##%HEIGHT=197
##%COMPONENTS
##%COMPONENT 
##%  id=1
##%  type=Label
##%  label=Title of window:
##%  varname=component0BL
##%  startpoint=27,59
##%  endpoint=118,81
##%  fgcolor=0,0,0
##%  bgcolor=255,255,255
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
##%  assocvarname=Button1_var
##%  other=
##%  codeAction=
##%  codeItem=
##%END
##%COMPONENT 
##%  id=2
##%  type=TextField
##%  label=
##%  varname=windowTitleTF
##%  startpoint=121,59
##%  endpoint=506,81
##%  fgcolor=0,0,0
##%  bgcolor=255,255,255
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
##%  assocvarname=Button1_var
##%  other=
##%  codeAction=
##%  codeItem=
##%END
##%COMPONENT 
##%  id=5
##%  type=Button
##%  label=Apply
##%  varname=applyB
##%  startpoint=133,153
##%  endpoint=200,179
##%  fgcolor=0,0,0
##%  bgcolor=255,255,255
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
##%  assocvarname=Button1_var
##%  other=
##%  codeAction=self.saveBack()\nself.root.destroy()\nself.globals.repaint_all()
##%  codeItem=
##%END
##%COMPONENT 
##%  id=6
##%  type=Button
##%  label=Cancel
##%  varname=cancelB
##%  startpoint=202,153
##%  endpoint=269,179
##%  fgcolor=0,0,0
##%  bgcolor=255,255,255
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
##%  assocvarname=Button1_var
##%  other=
##%  codeAction=self.root.destroy()
##%  codeItem=
##%END
##%COMPONENT 
##%  id=15
##%  type=Label
##%  label=Background color:
##%  varname=label3L
##%  startpoint=15,86
##%  endpoint=118,111
##%  fgcolor=0,0,0
##%  bgcolor=255,255,255
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
##%  assocvarname=Button1_var
##%  other=
##%  codeAction=
##%  codeItem=
##%END
##%COMPONENT 
##%  id=16
##%  type=TextField
##%  label=
##%  varname=bgcolorTF
##%  startpoint=121,85
##%  endpoint=213,111
##%  fgcolor=0,0,0
##%  bgcolor=255,255,255
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
##%  assocvarname=Button1_var
##%  other=
##%  codeAction=
##%  codeItem=
##%END
##%COMPONENT 
##%  id=54
##%  type=Button
##%  label=?
##%  varname=helpResizeB
##%  startpoint=254,119
##%  endpoint=277,142
##%  fgcolor=0,0,0
##%  bgcolor=255,255,255
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
##%  assocvarname=Button1_var
##%  other=
##%  codeAction=NewHelpWindow.main2("Resizing")
##%  codeItem=
##%END
##%COMPONENT 
##%  id=56
##%  type=TextField
##%  label=
##%  varname=allowResizeTF
##%  startpoint=123,119
##%  endpoint=186,142
##%  fgcolor=0,0,0
##%  bgcolor=255,255,255
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
##%  assocvarname=Button1_var
##%  other=
##%  codeAction=
##%  codeItem=
##%END
##%COMPONENT 
##%  id=57
##%  type=Button
##%  label=Toggle
##%  varname=toggleB
##%  startpoint=188,119
##%  endpoint=250,142
##%  fgcolor=0,0,0
##%  bgcolor=255,255,255
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
##%  assocvarname=Button1_var
##%  other=
##%  codeAction=self.checked = not self.checked\nif self.checked:\n     settext(self.allowResizeTF, "Yes")\nelse:\n     settext(self.allowResizeTF, "No")
##%  codeItem=
##%END
##%COMPONENT 
##%  id=58
##%  type=Label
##%  label=Allow resize:
##%  varname=component1BL
##%  startpoint=15,118
##%  endpoint=120,142
##%  fgcolor=0,0,0
##%  bgcolor=255,255,255
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
##%  assocvarname=Button1_var
##%  other=
##%  codeAction=
##%  codeItem=
##%END
##%COMPONENT 
##%  id=59
##%  type=Button
##%  label=?
##%  varname=colorHelpB
##%  startpoint=216,84
##%  endpoint=240,111
##%  fgcolor=0,0,0
##%  bgcolor=255,255,255
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
##%  assocvarname=Button1_var
##%  other=
##%  codeAction=NewHelpWindow.main2("Colors")
##%  codeItem=
##%END
##%ENDCOMPONENTS


####END
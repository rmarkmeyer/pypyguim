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
from utilitycode import *
##%ENDCODE

class MenuWindow():
#--------------------internally defined widget classes, do not change!--------------------
     class ScrolledText(Frame):
     	def __init__(self, parent=None):
     		Frame.__init__(self, parent)
     		self._makewidgets()
     
     	def _makewidgets(self):
     		sbar = Scrollbar(self)
     		text = Text(self, relief=SUNKEN)
     		sbar.config(command=text.yview)
     		text.config(yscrollcommand=sbar.set)
     		sbar.pack(side=RIGHT,fill=Y)
     		text.pack(side=LEFT,expand=YES,fill=BOTH)
     		self.text = text
     	
     	def settext(self, text=''):
     		#print('We are setting text here')
     		#sys.stdout.flush()
     		self.text.delete('1.0', END)
     		self.text.insert('1.0', text)
     		self.text.mark_set(INSERT, '1.0')
     
     	def gettext(self):
     		return self.text.get('1.0', END+'-1c');
     
     	def append(self, text=''):
     		self.text.insert(END,text)

#--------------------functions for widget event handlers, do not change!--------------------
     def applyB_action_code(self):
         self.saveBack()
         self.root.destroy()
         self.globals.repaint_all()
     
     def cancelB_action_code(self):
         destroy()
     
     def sampleB_action_code(self):
         self.makeSample()

#--------------------Menu defs, do not change!--------------------


#--------------------extra class code, you can change this!--------------------
##%EXTRACLASSCODE
     def saveBack(self):
          self.globals.menus = gettext(self.bigTA)
     
     def setGlobals(self, globals):
          self.globals = globals
          settext(self.bigTA, globals.menus)
     
     def makeSample(self):
          s = \
     '''
     File
          Load&nothing
          Save&nothing
          Exit&kill
     Edit
          Cut
          Paste
     Options
          Global options&nothing
     Help
          #this is a comment
     '''
          xs = ""
          lines = s.split("\n")
          for i in range(1,len(lines)):
               xs += lines[i][5:] + "\n"
          settext(self.bigTA, xs)
     
     def post_initialization(self):
          pass
##%ENDCODE

     def __init__(self):
          self.root=Tk()
          self.root.geometry("364x608")
          self.root.configure(background='#ebebeb')
          self.root.title("Property Window")
#--------------------widget making code, do not change anything from here to the end of the file!--------------------
          self.applyB = Button(self.root, text="Apply",width=67,height=26,command=self.applyB_action_code)
          self.applyB.place(x=77,y=572, width=67, height=26)
          self.applyB.config(font=("SansSerif", 10, 'normal'))
          self.applyB.config(bg=("#ffffff"))
          self.applyB.config(fg=("#000000"))
          self.cancelB = Button(self.root, text="Cancel",width=67,height=26,command=self.cancelB_action_code)
          self.cancelB.place(x=156,y=571, width=67, height=26)
          self.cancelB.config(font=("SansSerif", 10, 'normal'))
          self.cancelB.config(bg=("#ffffff"))
          self.cancelB.config(fg=("#000000"))
          self.bigTA = self.ScrolledText(self.root)
          self.bigTA.place(x=14,y=4, width=347, height=565)
          self.bigTA.settext("")
          self.bigTA.text.config(font=("Courier", 10, 'normal'))
          self.bigTA.text.config(bg=("#ffffff"))
          self.bigTA.text.config(fg=("#000000"))
          self.sampleB = Button(self.root, text="Sample",width=67,height=26,command=self.sampleB_action_code)
          self.sampleB.place(x=230,y=571, width=67, height=26)
          self.sampleB.config(font=("SansSerif", 10, 'normal'))
          self.sampleB.config(bg=("#ffffff"))
          self.sampleB.config(fg=("#000000"))

          self.post_initialization()
if __name__ == '__main__':
     tempwin=MenuWindow()
     tempwin.root.mainloop()

####DIRECTIVES
##%START
##%PROGRAM DATE=Sat, Jun 12, 2021 11:06:26 AM
##%VERSION=PY2
##%CLASS_STYLE=class
##%WHENWRITTEN=Sat Jun 04 09:59:47 EDT 2022
##%CLASSNAME=MenuWindow
##%PACKAGENAME=
##%DIRECTORY=
##%GUITYPE=Python
##%EXTRAMETHODS=0
##%PROGTYPE=Application
##%TITLEBAR=Property Window
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
##%WIDTH=379
##%HEIGHT=663
##%COMPONENTS
##%COMPONENT 
##%  id=5
##%  type=Button
##%  label=Apply
##%  varname=applyB
##%  startpoint=77,622
##%  endpoint=144,648
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
##%  startpoint=156,621
##%  endpoint=223,647
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
##%  codeAction=destroy()
##%  codeItem=
##%END
##%COMPONENT 
##%  id=15
##%  type=TextArea
##%  label=
##%  varname=bigTA
##%  startpoint=14,54
##%  endpoint=361,619
##%  fgcolor=0,0,0
##%  bgcolor=255,255,255
##%  fontname=Monospaced
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
##%  type=Button
##%  label=Sample
##%  varname=sampleB
##%  startpoint=230,621
##%  endpoint=297,647
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
##%  codeAction=self.makeSample()
##%  codeItem=
##%END
##%ENDCOMPONENTS


####END
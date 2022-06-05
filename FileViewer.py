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
from tkinter.filedialog import askopenfilename,asksaveasfilename,askdirectory

import threading
import os

def makeChecksum(text):
	sum = 0
	for ch in text:
		sum += ord(ch)
		sum = sum % 367847537
	return sum

def fileContains(fullpath, target):
     if os.path.isfile(fullpath):
          f = open(fullpath)
          contents = f.read()  #  this is a single string
          contents = contents.lower()
          f.close()
          return contents.find(target) > -1
     else:
          return False


##%ENDCODE

class FileViewer():
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
     		self.text.delete('1.0', END)
     		self.text.insert('1.0', text)
     		self.text.mark_set(INSERT, '1.0')
     
     	def gettext(self):
     		return self.text.get('1.0', END+'-1c');
     
     	def append(self, text=''):
     		self.text.insert(END,text)

#--------------------functions for widget event handlers, do not change!--------------------
     def browseForFileB_action_code(self):
         self.browseAndLoadFile()
     
     def saveB_action_code(self):
         self.save()
     
     def fileSearchTF_action_code(self):
         self.fileSearch()
     
     def clearFileSearchB_action_code(self):
         settext(self.fileSearchTF, "")
         self.fileSearch()
     
     def saveAsB_action_code(self):
         self.saveas()

#--------------------Menu defs, do not change!--------------------


#--------------------extra class code, you can change this!--------------------
##%EXTRACLASSCODE
     def showText(self, text):
          settext(self.bigTA, text)
     
     def clear(self):
          settext(self.bigTA, "")
     
     def clearFileInfo(self):
          settext(self.bigTA, "")
          settext(self.checksumTF, "")
          settext(self.bottomMsg1L, "")
     
     def browseAndLoadFile(self):
          filename = askopenfilename()
          if filename is None or filename == "":
               return
          settext(self.filenameTF, filename)
          if os.path.isfile(filename):
               f = open(filename)
               contents = f.read()  #  this is a single string
               f.close()
               settext(self.bigTA,contents)
               numlines = len(contents.split("\n"))
               settext(self.bottomMsg1L,str(numlines) + " lines")
               settext(self.checksumTF, str(makeChecksum(contents)))
     
     def save(self):
          filename = gettext(self.filenameTF)
          if filename == "":
               popup("You must have a filename to save")
          writeFile(filename, gettext(self.bigTA))
          popup("Saved!")
     
     def saveas(self):
          filename = tkinter.filedialog.asksaveasfilename()
          fp = open(filename, "w")
          fp.write(gettext(self.bigTA))
          fp.close()
          settext(self.filenameTF, filename)
     
     
     lastSearchStart = ""
     lastSearchEnd = ""
     
     
     def fileSearch(self):
          self.findAll()
          return
          global lastSearchStart, lastSearchEnd
          target = gettext(self.fileSearchTF)
          if target.strip() == "":
               self.clearTags()
               return
          target = target.lower()
          contents = gettext(self.bigTA)
          contents = contents.lower()
          lines = contents.split("\n")
          i=1
          for line in lines:
               x = line.find(target)
               if x > -1:
                    break
               i += 1
          
          if x > -1:
               print("found at " + str(x))
               sys.stdout.flush()
               lastSearchStart = str(i) + "." + str(x)
               lastSearchEnd = str(i) + "." + str(len(target)+x)
               print("lastSearchStart=",lastSearchStart)
               print("lastSearchEnd=",lastSearchEnd)
               sys.stdout.flush()
               self.bigTA.text.tag_add("found", lastSearchStart, lastSearchEnd)
               self.bigTA.text.tag_config("found", background="black", foreground="white")
          else:
               self.clearTags()
     
     def findAll(self):
          target = gettext(self.fileSearchTF)
          if target.strip() == "":
               self.clearAllTags()
               return
          target = target.lower()
          contents = gettext(self.bigTA)
          contents = contents.lower()
          lines = contents.split("\n")
          i=1
          found = False
          for line in lines:
               m = 0
               while m <len(line):
                    x = line.find(target, m)
                    if x > -1:
                         self.setFound(line, i, x, len(target))
                         found = True
                         m = x + len(target)
                    else:
                         m += 1
               i += 1
          if not found:
               self.clearAllTags()
               self.foundDescriptions = None
          
     def setFound(self, line, linenum, position, length):
          if self.foundDescriptions is None:
               self.foundDescriptions = []
          searchStart = str(linenum) + "." + str(position)
          searchEnd = str(linenum) + "." + str(length+position)
          tagNum = len(self.foundDescriptions)
          tagName = "found" + str(tagNum)
          self.bigTA.text.tag_add(tagName, searchStart, searchEnd)
          self.bigTA.text.tag_config(tagName, background="black", foreground="white")
     
          self.foundDescriptions.append((tagName, searchStart, searchEnd))
     
     def reconfigure(self, event):
          if event.widget == self.root:
               if event.width != self.lastwidth or event.height != self.lastheight:
                    #print("width="+str(event.width))
                    #sys.stdout.flush()
                    self.lastwidth = event.width
                    self.lastheight = event.height
                    self.bigTA.place(width=self.lastwidth-12, height=self.lastheight-60)
                    y = self.bigTA.winfo_height() + self.bigTA.winfo_y()
                    #print("y="+str(y))
                    #sys.stdout.flush()
                    for component in [self.searchL, self.fileSearchTF, self.clearFileSearchB, 
                                      self.bottomMsg1L, self.checksumL, self.checksumTF, self.saveB, self.saveAsB]:
                          component.place(y=y)
                         
     def setTitle(self, new_title):
          self.root.title(new_title)
     
     def post_initialization(self):
          self.foundDescriptions = None
          self.lastwidth = 672
          self.lastheight = 490
          #popup("self.wiinfo =" + str(self.root.winfo_width()))
          self.root.bind("<Configure>", self.reconfigure)
          self.root.title("File viewer")
##%ENDCODE

     def __init__(self):
          self.root=Tk()
          self.root.geometry("672x490")
          self.root.configure(background='#ebebeb')
          self.root.title("File explorer")
#--------------------widget making code, do not change anything from here to the end of the file!--------------------
          self.bigTA = self.ScrolledText(self.root)
          self.bigTA.place(x=9,y=30, width=666, height=427)
          self.bigTA.settext("")
          self.bigTA.text.config(font=("Courier", 10, 'normal'))
          self.bigTA.text.config(bg=("#ffffff"))
          self.bigTA.text.config(fg=("#000000"))
          self.Button1_var=StringVar()
          self.Button1_var.set("")
          self.filenameTF = Entry(self.root,width=542, textvariable=self.Button1_var)
          self.filenameTF.place(x=74,y=4, width=542, height=24)
          self.filenameTF.config(font=("SansSerif", 8, 'normal'))
          self.filenameTF.config(fg=("#000000"))
          self.filenameTF.config(bg=("#ffffff"))
          self.browseForFileB = Button(self.root, text="Browse",width=58,height=24,command=self.browseForFileB_action_code)
          self.browseForFileB.place(x=617,y=4, width=58, height=24)
          self.browseForFileB.config(font=("SansSerif", 11, 'normal'))
          self.browseForFileB.config(bg=("#ffffff"))
          self.browseForFileB.config(fg=("#000000"))
          self.bottomMsg1L = Label(self.root, text="",width=156,height=22,anchor=W)
          self.bottomMsg1L.place(x=230,y=460, width=156, height=22)
          self.bottomMsg1L.config(font=("SansSerif", 12, 'normal'))
          self.bottomMsg1L.config(bg=self.root['bg'])
          self.bottomMsg1L.config(fg=("#000000"))
          self.saveB = Button(self.root, text="Save",width=42,height=22,command=self.saveB_action_code)
          self.saveB.place(x=573,y=459, width=42, height=22)
          self.saveB.config(font=("SansSerif", 10, 'normal'))
          self.saveB.config(bg=("#ffffff"))
          self.saveB.config(fg=("#000000"))
          self.checksumL = Label(self.root, text="Checksum:",width=75,height=21)
          self.checksumL.place(x=423,y=459, width=75, height=21)
          self.checksumL.config(font=("SansSerif", 10, 'normal'))
          self.checksumL.config(bg=self.root['bg'])
          self.checksumL.config(fg=("#000000"))
          self.Button1_var=StringVar()
          self.Button1_var.set("")
          self.checksumTF = Entry(self.root,width=72, textvariable=self.Button1_var)
          self.checksumTF.place(x=499,y=459, width=72, height=21)
          self.checksumTF.config(font=("SansSerif", 10, 'normal'))
          self.checksumTF.config(fg=("#000000"))
          self.checksumTF.config(bg=("#ffffff"))
          self.Button1_var=StringVar()
          self.Button1_var.set("")
          self.fileSearchTF = Entry(self.root,width=110, textvariable=self.Button1_var)
          self.fileSearchTF.place(x=68,y=461, width=110, height=20)
          self.fileSearchTF.config(font=("SansSerif", 12, 'normal'))
          self.fileSearchTF.config(fg=("#000000"))
          self.fileSearchTF.config(bg=("#ffffff"))
          self.fileSearchTF.bind('<Return>', lambda x: self.fileSearchTF_action_code())
          self.searchL = Label(self.root, text="Search:",width=56,height=20)
          self.searchL.place(x=10,y=461, width=56, height=20)
          self.searchL.config(font=("SansSerif", 10, 'normal'))
          self.searchL.config(bg=self.root['bg'])
          self.searchL.config(fg=("#000000"))
          self.component6BL = Label(self.root, text="File path:",width=64,height=24)
          self.component6BL.place(x=9,y=4, width=64, height=24)
          self.component6BL.config(font=("SansSerif", 10, 'normal'))
          self.component6BL.config(bg=self.root['bg'])
          self.component6BL.config(fg=("#000000"))
          self.clearFileSearchB = Button(self.root, text="Clear",width=35,height=22,command=self.clearFileSearchB_action_code)
          self.clearFileSearchB.place(x=180,y=461, width=35, height=22)
          self.clearFileSearchB.config(font=("SansSerif", 9, 'normal'))
          self.clearFileSearchB.config(bg=("#ffffff"))
          self.clearFileSearchB.config(fg=("#000000"))
          self.saveAsB = Button(self.root, text="Save As",width=56,height=22,command=self.saveAsB_action_code)
          self.saveAsB.place(x=618,y=459, width=56, height=22)
          self.saveAsB.config(font=("SansSerif", 10, 'normal'))
          self.saveAsB.config(bg=("#ffffff"))
          self.saveAsB.config(fg=("#000000"))

          self.post_initialization()
if __name__ == '__main__':
     tempwin=FileViewer()
     tempwin.root.mainloop()

####DIRECTIVES
##%START
##%PROGRAM DATE=Sun, Feb 04, 2018 3:28:54 PM
##%VERSION=PY2
##%CLASS_STYLE=class
##%WHENWRITTEN=Fri Jun 08 16:04:56 EDT 2018
##%CLASSNAME=FileViewer
##%PACKAGENAME=
##%DIRECTORY=
##%GUITYPE=Python
##%EXTRAMETHODS=1
##%PROGTYPE=Application
##%TITLEBAR=File explorer
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
##%WIDTH=687
##%HEIGHT=545
##%COMPONENTS
##%COMPONENT 
##%  id=29
##%  type=TextArea
##%  label=
##%  varname=bigTA
##%  startpoint=9,80
##%  endpoint=675,507
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
##%  id=32
##%  type=TextField
##%  label=
##%  varname=filenameTF
##%  startpoint=74,54
##%  endpoint=616,78
##%  fgcolor=0,0,0
##%  bgcolor=255,255,255
##%  fontname=SansSerif
##%  fontsize=8
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
##%  id=33
##%  type=Button
##%  label=Browse
##%  varname=browseForFileB
##%  startpoint=617,54
##%  endpoint=675,78
##%  fgcolor=0,0,0
##%  bgcolor=255,255,255
##%  fontname=SansSerif
##%  fontsize=11
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
##%  codeAction=self.browseAndLoadFile()
##%  codeItem=
##%END
##%COMPONENT 
##%  id=34
##%  type=Label
##%  label=
##%  varname=bottomMsg1L
##%  startpoint=230,510
##%  endpoint=386,532
##%  fgcolor=0,0,0
##%  bgcolor=255,255,255
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
##%  moreoptions=left
##%  assocvarname=Button1_var
##%  other=
##%  codeAction=
##%  codeItem=
##%END
##%COMPONENT 
##%  id=35
##%  type=Button
##%  label=Save
##%  varname=saveB
##%  startpoint=573,509
##%  endpoint=615,531
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
##%  codeAction=self.save()
##%  codeItem=
##%END
##%COMPONENT 
##%  id=37
##%  type=Label
##%  label=Checksum:
##%  varname=checksumL
##%  startpoint=423,509
##%  endpoint=498,530
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
##%  id=38
##%  type=TextField
##%  label=
##%  varname=checksumTF
##%  startpoint=499,509
##%  endpoint=571,530
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
##%  id=42
##%  type=TextField
##%  label=
##%  varname=fileSearchTF
##%  startpoint=68,511
##%  endpoint=178,531
##%  fgcolor=0,0,0
##%  bgcolor=255,255,255
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
##%  assocvarname=Button1_var
##%  other=
##%  codeAction=self.fileSearch()
##%  codeItem=
##%END
##%COMPONENT 
##%  id=43
##%  type=Label
##%  label=Search:
##%  varname=searchL
##%  startpoint=10,511
##%  endpoint=66,531
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
##%  id=44
##%  type=Label
##%  label=File path:
##%  varname=component6BL
##%  startpoint=9,54
##%  endpoint=73,78
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
##%  id=45
##%  type=Button
##%  label=Clear
##%  varname=clearFileSearchB
##%  startpoint=180,511
##%  endpoint=215,533
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
##%  codeAction=settext(self.fileSearchTF, "")\nself.fileSearch()
##%  codeItem=
##%END
##%COMPONENT 
##%  id=46
##%  type=Button
##%  label=Save As
##%  varname=saveAsB
##%  startpoint=618,509
##%  endpoint=674,531
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
##%  codeAction=self.saveas()
##%  codeItem=
##%END
##%ENDCOMPONENTS


####END
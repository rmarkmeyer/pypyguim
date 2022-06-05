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

import tkinter, tkinter.filedialog

import threading
import os
import socket

parent = None

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

def splitPath(path):
	x = path.replace("\\", "/")
	n = x.rfind("/")
	return [path[0:n], path[n+1:]]

def getDirectory(path):
	return splitPath(path)[0]
##%ENDCODE

class FileBrowser():
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
     
     class ScrolledList(Frame):
          def __init__(self, options, parent=None):
               Frame.__init__(self, parent)
               self.pack(expand=YES, fill=BOTH)
               self.makeWidgets(options)
     
          def handleList(self, event):
               index = self.listbox.curselection()     # on list double-click
               label = self.listbox.get(index)     # fetch selection text
               self.runCommand(label)     # or get(ACTIVE)
     
          def makeWidgets(self, options):
               sbar = Scrollbar(self)
               list = Listbox(self, relief=SUNKEN)
               sbar.config(command=list.yview)
               list.config(bg=('#000000'))
               list.config(yscrollcommand=sbar.set)
               sbar.pack(side=RIGHT, fill=Y)
               list.pack(side=LEFT, expand=YES, fill=BOTH)
               pos = 0
               for label in options:
                    list.insert(pos, label)
                    pos += 1
               self.listbox = list
     
          def getselected(self):
               temp = self.listbox.curselection()
               if len(temp) == 0: return ''
               n = temp[0]
               if n == -1: return None
               return self.listbox.get(n)
     
          def get_n(self, n):
               return self.listbox.get(n)
     
          def select(self, n):
               if type(n) is int:
                    self.listbox.selection_set(n)
               elif type(n) is str:
                    for k in range(0,self.listbox.size()):
                         if n == self.listbox.get(k):
                              self.listbox.selection_set(k)
     
          def insert(self, item):
               self.listbox.insert(END,item)
     
          def insert_n(self, item, before_n):
               self.listbox.insert(before_n, item)
     
          def append(self, item):
               self.listbox.insert(END,item)
     
          def deleteSelected(self):
               index = self.listbox.curselection()[0]
               self.listbox.delete(index,index)
     
          def delete(self, target):
               n = self.find(target)
               if n > -1:
                    self.listbox.delete(n,n)
     
          def delete_n(self, n):
               self.listbox.delete(n,n)
     
          def find(self, target):
               i = 0
               for item in self.listbox.get(0,END):
                    if item == target:
                         return i
                    i+=1
               return -1
     
          def size(self):
               return self.listbox.size()
     
          def clear(self):
               self.listbox.delete(0,END)

#--------------------functions for widget event handlers, do not change!--------------------
     def filenameList_item_code(self):
         self.showFile(getselected(self.filenameList))
     
     def filenameList_action_code(self):
         self.showDir(getselected(self.filenameList))
     
     def dirTF_action_code(self):
         self.loadFilenames()
     
     def browseForDirB_action_code(self):
         self.browseForDir()
     
     def saveB_action_code(self):
         self.save()
     
     def goUpB_action_code(self):
         self.goUp()
         self.clearFileInfo()
     
     def dirSearchTF_action_code(self):
         self.dirSearch()
     
     def clearDirFilterB_action_code(self):
         settext(self.dirSearchTF, "")
         self.dirSearch()
     
     def fileSearchTF_action_code(self):
         self.fileSearch()
     
     def clearFileSearchB_action_code(self):
         settext(self.fileSearchTF, "")
         self.fileSearch()
     
     def putInParentB_action_code(self):
         settext(self.parent_codeTA,gettext(self.bigTA))
         #popup(gettext(self.parent_codeTA))
     
     def putB_action_code(self):
         #popup(gettext(self.whereCH))
         
         where = gettext(self.whereCH)
         if where == "code":
         	settext(self.parent_codeTA,gettext(self.bigTA))
         elif where == "testing area":
         	self.ltf(gettext(self.bigTA))
     
     def whereCH_respond(self , keycode):
          if keycode == 1:
               self.whereCH.config(text='--select--')
               for thing in self.whereCH_varlist:
                    thing.set(0)
               self.whereCH_xvar1.set(1)
          if keycode == 2:
               self.whereCH.config(text='code')
               for thing in self.whereCH_varlist:
                    thing.set(0)
               self.whereCH_xvar2.set(1)
          if keycode == 3:
               self.whereCH.config(text='testing area')
               for thing in self.whereCH_varlist:
                    thing.set(0)
               self.whereCH_xvar3.set(1)
     def saveAsB_action_code(self):
         self.saveAs()

#--------------------Menu defs, do not change!--------------------


#--------------------extra class code, you can change this!--------------------
##%EXTRACLASSCODE
     def setDirectory(self, dirname):
          settext(dirTF, dirname)
     
     def showText(self, text):
          settext(self.bigTA, text)
     
     def setDirectory(self, path):
          settext(self.dirTF, path)
          #popup("in FIleBrowser.setDirectory")
          if len(path) > 0:
               self.loadFilenames()
     
     def showFile(self, filename):
          directory = gettext(self.dirTF)
          path = directory + "/" + filename 
          if os.path.isfile(path):
               f = open(path)
               contents = f.read()  #  this is a single string
               f.close()
               settext(self.bigTA,contents)
               numlines = len(contents.split("\n"))
               settext(self.bottomMsg1L,str(numlines) + " lines")
               settext(self.checksumTF, str(makeChecksum(contents)))
               settext(self.filenameTF, filename)
     
     def clear(self):
          settext(self.bigTA, "")
     
     def clearFileInfo(self):
          settext(self.bigTA, "")
          settext(self.checksumTF, "")
          settext(self.bottomMsg1L, "")
     
     def showDir(self, filename):
          directory = gettext(self.dirTF)
          self.clearFileInfo()
          if filename[0] == "*":
               print("filename starts with *")
               path = directory + "/" + filename[1:]    # chop off the leading "*" 
               print("path="+path)
               settext(self.dirTF, path)
               self.loadFilenames()
     
     def goUp(self):
          directory = gettext(self.dirTF)
          n = directory.rfind("/")
          if n == -1:
               popup("Can't go up")
               return
          directory = directory[0:n]
          settext(self.dirTF, directory)
          self.loadFilenames()
     
     def browseForDir(self):
          options = {}
          options['initialdir'] = gettext(self.dirTF)
          options['title'] = "Which directory to load?"
          dirname = tkinter.filedialog.askdirectory(**options)
     
     
          #dirname = askdirectory()
          if dirname is None or dirname == "":
               return
          settext(self.dirTF, dirname)
          self.loadFilenames()
          self.root.lift()
     
     def save(self):
          filename = getselected(self.filenameList)
          if filename == "":
               popup("You must have a filename to save")
               return
          if gettext(self.dirTF) == "":
               popup("You must have a directory to save")
               return 
          pathname = gettext(self.dirTF) + "/" + filename
          writeFile(pathname, gettext(self.bigTA))
          popup("Saved!")
     
     def saveAs(self):
          filename = asksaveasfilename()
          if filename is None or filename == "":
               popup("You must have a filename to save")
               return
          writeFile(filename, gettext(self.bigTA))
          popup("Saved to "+filename)
     
     def setDirectory(self, path):
          settext(self.dirTF, path)
          self.loadFilenames()
     
     def loadFilenames(self):
          directory = gettext(self.dirTF)
          if len(directory) == 0:    # this may have been because the main's directory is not yet filled
               return
          #if len(directory) == 0:
          #     popup("The directory name cannot be blank")
          #     return
          self.filenameList.delete(0,END)
          thelist = []
          for f in os.listdir(directory):
               toshow = f
               if os.path.isdir(directory + "/" + f):
                    toshow = "*" + toshow
               thelist.append(toshow)
     
          thelist.sort()
          for f in thelist:
               self.filenameList.insert(END,f)
     
     def dirSearch(self):
          target = gettext(self.dirSearchTF)
          if target.strip() == "":
               self.loadFilenames()
               return
          target = target.lower()
          directory = gettext(self.dirTF)
          if len(directory) == 0:
               popup("The directory name cannot be blank")
               return
          self.filenameList.delete(0,END)
          for f in os.listdir(directory):
               toshow = f
               fullpath = directory + "/" + f
               #if os.path.isdir(fullpath):
               #    toshow = "*" + toshow
               if fileContains(fullpath, target):
                    self.filenameList.insert(END,toshow)
     
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
     
     def clearTags(self):
          if lastSearchStart != "":
               self.bigTA.text.tag_remove("found", lastSearchStart, lastSearchEnd)
     
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
     
     def clearAllTags(self):
          if self.foundDescriptions is not None:
               for descrip in self.foundDescriptions:
                    tagName = descrip[0]
                    start = descrip[1]
                    length = descrip[2]
                    self.bigTA.text.tag_remove(tagName, start, length)
          self.foundDescriptions = None
     
     def selectMe(self, what):
     	for i in range(self.filenameList.size()):
     		if self.filenameList.get(i) == what:
     			self.filenameList.select_set(i)
     			break
     
     def post_initialization(self):
          self.foundDescriptions = None
##%ENDCODE

     def __init__(self):
          self.root=Tk()
          self.root.geometry("968x490")
          self.root.configure(background='#ebebeb')
          self.root.title("File explorer")
#--------------------widget making code, do not change anything from here to the end of the file!--------------------
          self.filenameList = Listbox(self.root)
          self.filenameList.place(x=5,y=33, width=268, height=426)
          self.filenameList.config(font=("SansSerif", 11, 'normal'))
          self.filenameList.config(bg=("#ffffff"))
          self.filenameList.config(fg=("#000000"))
          self.filenameList.insert(END,"")
          self.filenameList.bind("<<ListboxSelect>>", (lambda event: self.filenameList_item_code()))
          self.filenameList.bind("<Double-1>", (lambda event: self.filenameList_action_code()))
          self.bigTA = self.ScrolledText(self.root)
          self.bigTA.place(x=274,y=33, width=689, height=427)
          self.bigTA.settext("")
          self.bigTA.text.config(font=("Courier", 10, 'normal'))
          self.bigTA.text.config(bg=("#ffffff"))
          self.bigTA.text.config(fg=("#000000"))
          self.Button1_var=StringVar()
          self.Button1_var.set("")
          self.dirTF = Entry(self.root,width=386, textvariable=self.Button1_var)
          self.dirTF.place(x=74,y=4, width=386, height=24)
          self.dirTF.config(font=("SansSerif", 8, 'normal'))
          self.dirTF.config(fg=("#000000"))
          self.dirTF.config(bg=("#ffffff"))
          self.dirTF.bind('<Return>', lambda x: self.dirTF_action_code())
          self.browseForDirB = Button(self.root, text="Browse",width=58,height=24,command=self.browseForDirB_action_code)
          self.browseForDirB.place(x=461,y=4, width=58, height=24)
          self.browseForDirB.config(font=("SansSerif", 11, 'normal'))
          self.browseForDirB.config(bg=("#ffffff"))
          self.browseForDirB.config(fg=("#000000"))
          self.bottomMsg1L = Label(self.root, text="",width=156,height=22,anchor=W)
          self.bottomMsg1L.place(x=539,y=462, width=156, height=22)
          self.bottomMsg1L.config(font=("SansSerif", 12, 'normal'))
          self.bottomMsg1L.config(bg=self.root['bg'])
          self.bottomMsg1L.config(fg=("#000000"))
          self.saveB = Button(self.root, text="Save",width=42,height=22,command=self.saveB_action_code)
          self.saveB.place(x=852,y=462, width=42, height=22)
          self.saveB.config(font=("SansSerif", 10, 'normal'))
          self.saveB.config(bg=("#ffffff"))
          self.saveB.config(fg=("#000000"))
          self.goUpB = Button(self.root, text="Go up",width=46,height=22,command=self.goUpB_action_code)
          self.goUpB.place(x=7,y=460, width=46, height=22)
          self.goUpB.config(font=("SansSerif", 11, 'normal'))
          self.goUpB.config(bg=("#ffffff"))
          self.goUpB.config(fg=("#000000"))
          self.component2BL = Label(self.root, text="Checksum:",width=75,height=21)
          self.component2BL.place(x=702,y=462, width=75, height=21)
          self.component2BL.config(font=("SansSerif", 10, 'normal'))
          self.component2BL.config(bg=self.root['bg'])
          self.component2BL.config(fg=("#000000"))
          self.Button1_var=StringVar()
          self.Button1_var.set("")
          self.checksumTF = Entry(self.root,width=72, textvariable=self.Button1_var)
          self.checksumTF.place(x=778,y=462, width=72, height=21)
          self.checksumTF.config(font=("SansSerif", 10, 'normal'))
          self.checksumTF.config(fg=("#000000"))
          self.checksumTF.config(bg=("#ffffff"))
          self.component4BL = Label(self.root, text="Search:",width=62,height=20)
          self.component4BL.place(x=63,y=462, width=62, height=20)
          self.component4BL.config(font=("SansSerif", 11, 'normal'))
          self.component4BL.config(bg=self.root['bg'])
          self.component4BL.config(fg=("#000000"))
          self.Button1_var=StringVar()
          self.Button1_var.set("")
          self.dirSearchTF = Entry(self.root,width=143, textvariable=self.Button1_var)
          self.dirSearchTF.place(x=128,y=462, width=143, height=20)
          self.dirSearchTF.config(font=("SansSerif", 12, 'normal'))
          self.dirSearchTF.config(fg=("#000000"))
          self.dirSearchTF.config(bg=("#ffffff"))
          self.dirSearchTF.bind('<Return>', lambda x: self.dirSearchTF_action_code())
          self.clearDirFilterB = Button(self.root, text="Clear",width=35,height=22,command=self.clearDirFilterB_action_code)
          self.clearDirFilterB.place(x=274,y=462, width=35, height=22)
          self.clearDirFilterB.config(font=("SansSerif", 9, 'normal'))
          self.clearDirFilterB.config(bg=("#ffffff"))
          self.clearDirFilterB.config(fg=("#000000"))
          self.Button1_var=StringVar()
          self.Button1_var.set("")
          self.fileSearchTF = Entry(self.root,width=110, textvariable=self.Button1_var)
          self.fileSearchTF.place(x=385,y=463, width=110, height=20)
          self.fileSearchTF.config(font=("SansSerif", 12, 'normal'))
          self.fileSearchTF.config(fg=("#000000"))
          self.fileSearchTF.config(bg=("#ffffff"))
          self.fileSearchTF.bind('<Return>', lambda x: self.fileSearchTF_action_code())
          self.component5BL = Label(self.root, text="Search:",width=56,height=20)
          self.component5BL.place(x=327,y=463, width=56, height=20)
          self.component5BL.config(font=("SansSerif", 10, 'normal'))
          self.component5BL.config(bg=self.root['bg'])
          self.component5BL.config(fg=("#000000"))
          self.component6BL = Label(self.root, text="Directory:",width=64,height=24)
          self.component6BL.place(x=9,y=4, width=64, height=24)
          self.component6BL.config(font=("SansSerif", 10, 'normal'))
          self.component6BL.config(bg=self.root['bg'])
          self.component6BL.config(fg=("#000000"))
          self.clearFileSearchB = Button(self.root, text="Clear",width=35,height=20,command=self.clearFileSearchB_action_code)
          self.clearFileSearchB.place(x=497,y=463, width=35, height=20)
          self.clearFileSearchB.config(font=("SansSerif", 9, 'normal'))
          self.clearFileSearchB.config(bg=("#ffffff"))
          self.clearFileSearchB.config(fg=("#000000"))
          self.putInParentB = Button(self.root, text="Put this file into parent's code",width=197,height=24,command=self.putInParentB_action_code)
          self.putInParentB.place(x=1081,y=91, width=197, height=24)
          self.putInParentB.config(font=("SansSerif", 11, 'normal'))
          self.putInParentB.config(bg=("#ffffff"))
          self.putInParentB.config(fg=("#000000"))
          self.putB = Button(self.root, text="Save",width=46,height=25,command=self.putB_action_code)
          self.putB.place(x=916,y=4, width=46, height=25)
          self.putB.config(font=("SansSerif", 11, 'normal'))
          self.putB.config(bg=("#ffffff"))
          self.putB.config(fg=("#000000"))
          self.whereCH = Menubutton(self.root, text='Where to put this text?')
          self.whereCH.place(x=987,y=53, width=144, height=25)
          self.whereCH.config(font=("SansSerif", 10, 'normal'))
          self.whereCH.config(bg=("#ffffff"))
          self.whereCH.config(fg=("#000000"))
          self.whereCH.menu = Menu(self.whereCH, tearoff=0)
          self.whereCH['menu'] = self.whereCH.menu
          self.whereCH_varlist=[]
          self.whereCH_xvar1=IntVar()
          self.whereCH_varlist.append(self.whereCH_xvar1)
          self.whereCH.menu.add_checkbutton(label='--select--',variable=self.whereCH_xvar1, command=functools.partial(self.whereCH_respond, 1))
          self.whereCH_xvar2=IntVar()
          self.whereCH_varlist.append(self.whereCH_xvar2)
          self.whereCH.menu.add_checkbutton(label='code',variable=self.whereCH_xvar2, command=functools.partial(self.whereCH_respond, 2))
          self.whereCH_xvar3=IntVar()
          self.whereCH_varlist.append(self.whereCH_xvar3)
          self.whereCH.menu.add_checkbutton(label='testing area',variable=self.whereCH_xvar3, command=functools.partial(self.whereCH_respond, 3))
          self.component10BL = Label(self.root, text="Filename:",width=57,height=25)
          self.component10BL.place(x=522,y=4, width=57, height=25)
          self.component10BL.config(font=("SansSerif", 10, 'normal'))
          self.component10BL.config(bg=self.root['bg'])
          self.component10BL.config(fg=("#000000"))
          self.Button1_var=StringVar()
          self.Button1_var.set("")
          self.filenameTF = Entry(self.root,width=334, textvariable=self.Button1_var)
          self.filenameTF.place(x=580,y=4, width=334, height=25)
          self.filenameTF.config(font=("SansSerif", 10, 'normal'))
          self.filenameTF.config(fg=("#000000"))
          self.filenameTF.config(bg=("#ffffff"))
          self.saveAsB = Button(self.root, text="Save As",width=63,height=22,command=self.saveAsB_action_code)
          self.saveAsB.place(x=900,y=462, width=63, height=22)
          self.saveAsB.config(font=("SansSerif", 10, 'normal'))
          self.saveAsB.config(bg=("#ffffff"))
          self.saveAsB.config(fg=("#000000"))

          self.post_initialization()
if __name__ == '__main__':
     tempwin=FileBrowser()
     tempwin.root.mainloop()

####DIRECTIVES
##%START
##%PROGRAM DATE=Sat, Jun 12, 2021 11:06:26 AM
##%VERSION=PY2
##%CLASS_STYLE=class
##%WHENWRITTEN=Tue May 24 14:15:26 EDT 2022
##%CLASSNAME=FileBrowser
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
##%WIDTH=983
##%HEIGHT=545
##%COMPONENTS
##%COMPONENT 
##%  id=28
##%  type=List
##%  label=
##%  varname=filenameList
##%  startpoint=5,83
##%  endpoint=273,509
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
##%  moreoptions=non-scrolling
##%  assocvarname=countriesList_var
##%  other=
##%  codeAction=self.showDir(getselected(self.filenameList))
##%  codeItem=self.showFile(getselected(self.filenameList))\n
##%END
##%COMPONENT 
##%  id=29
##%  type=TextArea
##%  label=
##%  varname=bigTA
##%  startpoint=274,83
##%  endpoint=963,510
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
##%  varname=dirTF
##%  startpoint=74,54
##%  endpoint=460,78
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
##%  codeAction=self.loadFilenames()
##%  codeItem=
##%END
##%COMPONENT 
##%  id=33
##%  type=Button
##%  label=Browse
##%  varname=browseForDirB
##%  startpoint=461,54
##%  endpoint=519,78
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
##%  codeAction=self.browseForDir()
##%  codeItem=
##%END
##%COMPONENT 
##%  id=34
##%  type=Label
##%  label=
##%  varname=bottomMsg1L
##%  startpoint=539,512
##%  endpoint=695,534
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
##%  startpoint=852,512
##%  endpoint=894,534
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
##%  id=36
##%  type=Button
##%  label=Go up
##%  varname=goUpB
##%  startpoint=7,510
##%  endpoint=53,532
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
##%  codeAction=self.goUp()\nself.clearFileInfo()
##%  codeItem=
##%END
##%COMPONENT 
##%  id=37
##%  type=Label
##%  label=Checksum:
##%  varname=component2BL
##%  startpoint=702,512
##%  endpoint=777,533
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
##%  startpoint=778,512
##%  endpoint=850,533
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
##%  id=39
##%  type=Label
##%  label=Search:
##%  varname=component4BL
##%  startpoint=63,512
##%  endpoint=125,532
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
##%  codeAction=
##%  codeItem=
##%END
##%COMPONENT 
##%  id=40
##%  type=TextField
##%  label=
##%  varname=dirSearchTF
##%  startpoint=128,512
##%  endpoint=271,532
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
##%  codeAction=self.dirSearch()
##%  codeItem=
##%END
##%COMPONENT 
##%  id=41
##%  type=Button
##%  label=Clear
##%  varname=clearDirFilterB
##%  startpoint=274,512
##%  endpoint=309,534
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
##%  codeAction=settext(self.dirSearchTF, "")\nself.dirSearch()
##%  codeItem=
##%END
##%COMPONENT 
##%  id=42
##%  type=TextField
##%  label=
##%  varname=fileSearchTF
##%  startpoint=385,513
##%  endpoint=495,533
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
##%  varname=component5BL
##%  startpoint=327,513
##%  endpoint=383,533
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
##%  label=Directory:
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
##%  startpoint=497,513
##%  endpoint=532,533
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
##%  label=Put this file into parent's code
##%  varname=putInParentB
##%  startpoint=1081,141
##%  endpoint=1278,165
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
##%  codeAction=settext(self.parent_codeTA,gettext(self.bigTA))\n#popup(gettext(self.parent_codeTA))
##%  codeItem=
##%END
##%COMPONENT 
##%  id=47
##%  type=Button
##%  label=Save
##%  varname=putB
##%  startpoint=916,54
##%  endpoint=962,79
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
##%  codeAction=#popup(gettext(self.whereCH))\n\nwhere = gettext(self.whereCH)\nif where == "code":\n	settext(self.parent_codeTA,gettext(self.bigTA))\nelif where == "testing area":\n	self.ltf(gettext(self.bigTA))\n
##%  codeItem=
##%END
##%COMPONENT 
##%  id=48
##%  type=Choice
##%  label=Where to put this text?
##%  varname=whereCH
##%  startpoint=987,103
##%  endpoint=1131,128
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
##%  assocvarname=where_var
##%  other=--select--\ncode\ntesting area\n
##%  codeAction=
##%  codeItem=
##%END
##%COMPONENT 
##%  id=63
##%  type=Label
##%  label=Filename:
##%  varname=component10BL
##%  startpoint=522,54
##%  endpoint=579,79
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
##%  id=64
##%  type=TextField
##%  label=
##%  varname=filenameTF
##%  startpoint=580,54
##%  endpoint=914,79
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
##%  id=65
##%  type=Button
##%  label=Save As
##%  varname=saveAsB
##%  startpoint=900,512
##%  endpoint=963,534
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
##%  codeAction=self.saveAs()
##%  codeItem=
##%END
##%ENDCOMPONENTS


####END
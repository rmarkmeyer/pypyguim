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

import os
import FileViewer

def loadFile(filename):
     global topics
     topics = {}  #new dictionary
     if os.path.isfile(filename):
          f = open(filename)
          contents = f.read()  #  this is a single string
          f.close()
          currentText = ""; currentTopic = ""
          for line in contents.split("\n"):
                if line.startswith("$$$"):
                      if len(currentText) > 0:
                            topicsList.listbox.insert(END, currentTopic)
                            topics[currentTopic] = currentText
                            print(currentTopic + "    " + str(len(currentText.split("\n"))) + " lines.")
                      currentTopic = line[3:]
                      currentText = ""
                else:
                      currentText += line + "\n"
          topicsList.listbox.insert(END, currentTopic)
          topics[currentTopic] = currentText

def getTopics(filename):
     global topics
     topics = {}  #new dictionary
     if os.path.isfile(filename):
          f = open(filename)
          contents = f.read()  #  this is a single string
          f.close()
          currentText = ""; currentTopic = ""
          for line in contents.split("\n"):
                if line.startswith("$$$"):
                      if len(currentText) > 0:
                            topics[currentTopic] = currentText
                            print(currentTopic + "    " + str(len(currentText.split("\n"))) + " lines.")
                      currentTopic = line[3:]
                      currentText = ""
                else:
                      currentText += line + "\n"

def clear():
     settext(bigTA, "")

lastSearchStart = ""
lastSearchEnd = ""
helptextfilename = "helpwindowtext.txt"

def fileSearch():
     #findAll()
     #return
     global lastSearchStart, lastSearchEnd
     target = gettext(fileSearchTF)
     if target.strip() == "":
          clearTags()
          return
     target = target.lower()
     contents = gettext(bigTA)
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
          print(">>>>>>>>>lastSearchStart=",lastSearchStart)
          print("lastSearchEnd=",lastSearchEnd)
          sys.stdout.flush()
          bigTA.text.tag_add("found", lastSearchStart, lastSearchEnd)
          bigTA.text.tag_config("found", background="black", foreground="white")
     else:
          clearTags()

def clearTags():
     if lastSearchStart != "":
          bigTA.text.tag_remove("found", lastSearchStart, lastSearchEnd)

def findAll():
     target = gettext(fileSearchTF)
     if target.strip() == "":
          clearAllTags()
          return
     target = target.lower()
     contents = gettext(bigTA)
     contents = contents.lower()
     lines = contents.split("\n")
     i=1
     found = False
     for line in lines:
          m = 0
          while m <len(line):
               x = line.find(target, m)
               if x > -1:
                    #setFound(line, i, x, len(target))
                    setFound(i, x, len(line))
                    found = True
                    m = x + len(target)
               else:
                    m += 1
          i += 1
     if not found:
          clearAllTags()
          foundDescriptions = None

def setFound(linenum, starting_pos, len_line):
     #bigTA.text.selection_range(starting_pos, starting_pos + len_target)
     #bigTA.text.tag_add(SEL, "1.0", END)
     pass 

def findInTopics():
     target = gettext(findTF).lower()
     if len(target.strip()) == 0:
          settext(topicsList, "")
          for topic in topics.keys():
               if len(topic.strip()) > 0:
                    topicsList.listbox.insert(END, topic)  
     else:
          settext(topicsList, "")
          for topic in topics.keys():
               if target in topics[topic].lower():
                    topicsList.listbox.insert(END, topic)

def showTopic(what):
     print("what="+what)
     #print("topics="+str(topics))
     sys.stdout.flush()
     settext(bigTA, topics[what])

startupMessage = "This help system contains much useful information about the IDE\n" + \
        "as well as the three underlying assembler languages and their interpreters.\n" + \
        "\nJust click on a topic at the left to view it."

def post_initialization():
     loadFile(helptextfilename)
     settext(bigTA, startupMessage)

def main2(what):
     #main()
     getTopics(helptextfilename)
     fv = FileViewer.FileViewer()
     fv.showText(topics[what])
     #popup("HI there")   #bigTA.settext("Hi there!")   #settext(bottomMsg1L, "Hi there!")
	#showTopic("Fonts")
	#showTopic(what)
##%ENDCODE

def window_init():
     global root
     root=Tk()
     root.geometry("994x601")
     root.configure(background='#ebebeb')
     root.title("PyPyGUIM help")

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
def fileSearchTF_action_code():
    fileSearch()

def searchB_action_code():
    fileSearch()

def clearFileSearchB_action_code():
    #settext(self.fileSearchTF, "")
    fileSearchClear()

def topicsList_item_code():
    value = getselected(topicsList)
    settext(bigTA, topics[value])

def findTF_action_code():
    findInTopics()

def searchNextB_action_code():
    fileSearchNext()

def searchAllB_action_code():
    fileSearchAll()



#--------------------Menu defs, do not change!--------------------


#--------------------extra class code, you can change this!--------------------
##%EXTRACLASSCODE

##%ENDCODE

def main():
     window_init()
     global bigTA
     global bottomMsg1L
     global Button1_var
     global fileSearchTF
     global searchB
     global clearFileSearchB
     global topicsList
     global component7BL
     global component8BL
     global Button1_var
     global findTF
     global searchNextB
     global searchAllB
#--------------------widget making code, do not change anything from here to the end of the file!--------------------
     bigTA = ScrolledText(root)
     bigTA.place(x=241,y=2, width=747, height=570)
     bigTA.settext("")
     bigTA.text.config(font=("Courier", 11, 'normal'))
     bigTA.text.config(bg=("#ffffff"))
     bigTA.text.config(fg=("#000000"))
     bottomMsg1L = Label(root, text="",width=156,height=20,anchor=W)
     bottomMsg1L.place(x=545,y=574, width=156, height=20)
     bottomMsg1L.config(font=("SansSerif", 11, 'normal'))
     bottomMsg1L.config(bg=root['bg'])
     bottomMsg1L.config(fg=("#000000"))
     Button1_var=StringVar()
     Button1_var.set("")
     fileSearchTF = Entry(root,width=110, textvariable=Button1_var)
     fileSearchTF.place(x=300,y=574, width=110, height=20)
     fileSearchTF.config(font=("SansSerif", 12, 'normal'))
     fileSearchTF.config(fg=("#000000"))
     fileSearchTF.config(bg=("#ffffff"))
     fileSearchTF.bind('<Return>', lambda x: fileSearchTF_action_code())
     searchB = Button(root, text="Search:",width=56,height=20,command=searchB_action_code)
     searchB.place(x=243,y=574, width=56, height=20)
     searchB.config(font=("SansSerif", 10, 'normal'))
     searchB.config(bg=("#fafafa"))
     searchB.config(fg=("#000000"))
     clearFileSearchB = Button(root, text="Clear",width=43,height=20,command=clearFileSearchB_action_code)
     clearFileSearchB.place(x=500,y=574, width=43, height=20)
     clearFileSearchB.config(font=("SansSerif", 9, 'normal'))
     clearFileSearchB.config(bg=("#ffffff"))
     clearFileSearchB.config(fg=("#000000"))
     topicsList = ScrolledList([], parent=root)
     topicsList.place(x=10,y=25, width=227, height=545)
     topicsList.listbox.config(font=("SansSerif", 10, 'normal'))
     topicsList.listbox.config(bg=("#ffffff"))
     topicsList.listbox.config(fg=("#000000"))
     topicsList.listbox.bind("<<ListboxSelect>>", (lambda event: topicsList_item_code()))
     component7BL = Label(root, text="Topics:",width=85,height=21)
     component7BL.place(x=10,y=2, width=85, height=21)
     component7BL.config(font=("SansSerif", 12, 'bold'))
     component7BL.config(bg=root['bg'])
     component7BL.config(fg=("#000000"))
     component8BL = Label(root, text="Find:",width=38,height=21)
     component8BL.place(x=11,y=572, width=38, height=21)
     component8BL.config(font=("SansSerif", 10, 'bold'))
     component8BL.config(bg=root['bg'])
     component8BL.config(fg=("#000000"))
     Button1_var=StringVar()
     Button1_var.set("")
     findTF = Entry(root,width=168, textvariable=Button1_var)
     findTF.place(x=51,y=572, width=168, height=21)
     findTF.config(font=("SansSerif", 12, 'normal'))
     findTF.config(fg=("#000000"))
     findTF.config(bg=("#ffffff"))
     findTF.bind('<Return>', lambda x: findTF_action_code())
     searchNextB = Button(root, text="Next",width=43,height=20,command=searchNextB_action_code)
     searchNextB.place(x=411,y=574, width=43, height=20)
     searchNextB.config(font=("SansSerif", 9, 'normal'))
     searchNextB.config(bg=("#ffffff"))
     searchNextB.config(fg=("#000000"))
     searchAllB = Button(root, text="All",width=43,height=20,command=searchAllB_action_code)
     searchAllB.place(x=455,y=574, width=43, height=20)
     searchAllB.config(font=("SansSerif", 9, 'normal'))
     searchAllB.config(bg=("#ffffff"))
     searchAllB.config(fg=("#000000"))


     post_initialization()
     root.mainloop()

if __name__ == '__main__':
     main()

####DIRECTIVES
##%START
##%PROGRAM DATE=Sat, Jun 12, 2021 11:06:26 AM
##%VERSION=PY2
##%CLASS_STYLE=no class
##%WHENWRITTEN=Sat Jun 04 13:26:33 EDT 2022
##%CLASSNAME=NewHelpWindow
##%PACKAGENAME=
##%DIRECTORY=
##%GUITYPE=Python
##%EXTRAMETHODS=1
##%PROGTYPE=Application
##%TITLEBAR=PyPyGUIM help
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
##%WIDTH=1009
##%HEIGHT=656
##%COMPONENTS
##%COMPONENT 
##%  id=29
##%  type=TextArea
##%  label=
##%  varname=bigTA
##%  startpoint=241,52
##%  endpoint=988,622
##%  fgcolor=0,0,0
##%  bgcolor=255,255,255
##%  fontname=Monospaced
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
##%  id=34
##%  type=Label
##%  label=
##%  varname=bottomMsg1L
##%  startpoint=545,624
##%  endpoint=701,644
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
##%  moreoptions=left
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
##%  startpoint=300,624
##%  endpoint=410,644
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
##%  codeAction=fileSearch()
##%  codeItem=
##%END
##%COMPONENT 
##%  id=43
##%  type=Button
##%  label=Search:
##%  varname=searchB
##%  startpoint=243,624
##%  endpoint=299,644
##%  fgcolor=0,0,0
##%  bgcolor=250,250,250
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
##%  codeAction=fileSearch()
##%  codeItem=
##%END
##%COMPONENT 
##%  id=45
##%  type=Button
##%  label=Clear
##%  varname=clearFileSearchB
##%  startpoint=500,624
##%  endpoint=543,644
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
##%  codeAction=#settext(self.fileSearchTF, "")\nfileSearchClear()
##%  codeItem=
##%END
##%COMPONENT 
##%  id=46
##%  type=List
##%  label=
##%  varname=topicsList
##%  startpoint=10,75
##%  endpoint=237,620
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
##%  codeItem=value = getselected(topicsList)\nsettext(bigTA, topics[value])
##%END
##%COMPONENT 
##%  id=47
##%  type=Label
##%  label=Topics:
##%  varname=component7BL
##%  startpoint=10,52
##%  endpoint=95,73
##%  fgcolor=0,0,0
##%  bgcolor=255,255,255
##%  fontname=SansSerif
##%  fontsize=12
##%  fontstyle=bold
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
##%  id=48
##%  type=Label
##%  label=Find:
##%  varname=component8BL
##%  startpoint=11,622
##%  endpoint=49,643
##%  fgcolor=0,0,0
##%  bgcolor=255,255,255
##%  fontname=SansSerif
##%  fontsize=10
##%  fontstyle=bold
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
##%  id=49
##%  type=TextField
##%  label=
##%  varname=findTF
##%  startpoint=51,622
##%  endpoint=219,643
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
##%  codeAction=findInTopics()
##%  codeItem=
##%END
##%COMPONENT 
##%  id=50
##%  type=Button
##%  label=Next
##%  varname=searchNextB
##%  startpoint=411,624
##%  endpoint=454,644
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
##%  codeAction=fileSearchNext()
##%  codeItem=
##%END
##%COMPONENT 
##%  id=51
##%  type=Button
##%  label=All
##%  varname=searchAllB
##%  startpoint=455,624
##%  endpoint=498,644
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
##%  codeAction=fileSearchAll()
##%  codeItem=
##%END
##%ENDCOMPONENTS


####END
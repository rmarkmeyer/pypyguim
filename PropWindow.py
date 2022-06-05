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

class PropWindow():
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
     def widgetTypeCH_item_code(self):
         self.myreconfig()
     
     def widgetTypeCH_respond(self , keycode):
          if keycode == 1:
               self.widgetTypeCH.config(text='button')
               for thing in self.widgetTypeCH_varlist:
                    thing.set(0)
               self.widgetTypeCH_xvar1.set(1)
          if keycode == 2:
               self.widgetTypeCH.config(text='textfield')
               for thing in self.widgetTypeCH_varlist:
                    thing.set(0)
               self.widgetTypeCH_xvar2.set(1)
          if keycode == 3:
               self.widgetTypeCH.config(text='textarea')
               for thing in self.widgetTypeCH_varlist:
                    thing.set(0)
               self.widgetTypeCH_xvar3.set(1)
          if keycode == 4:
               self.widgetTypeCH.config(text='label')
               for thing in self.widgetTypeCH_varlist:
                    thing.set(0)
               self.widgetTypeCH_xvar4.set(1)
          if keycode == 5:
               self.widgetTypeCH.config(text='checkbox')
               for thing in self.widgetTypeCH_varlist:
                    thing.set(0)
               self.widgetTypeCH_xvar5.set(1)
          if keycode == 6:
               self.widgetTypeCH.config(text='radiobutton')
               for thing in self.widgetTypeCH_varlist:
                    thing.set(0)
               self.widgetTypeCH_xvar6.set(1)
          if keycode == 7:
               self.widgetTypeCH.config(text='choice')
               for thing in self.widgetTypeCH_varlist:
                    thing.set(0)
               self.widgetTypeCH_xvar7.set(1)
          if keycode == 8:
               self.widgetTypeCH.config(text='list')
               for thing in self.widgetTypeCH_varlist:
                    thing.set(0)
               self.widgetTypeCH_xvar8.set(1)
          if keycode == 9:
               self.widgetTypeCH.config(text='scrollbar')
               for thing in self.widgetTypeCH_varlist:
                    thing.set(0)
               self.widgetTypeCH_xvar9.set(1)
          if keycode == 10:
               self.widgetTypeCH.config(text='canvas')
               for thing in self.widgetTypeCH_varlist:
                    thing.set(0)
               self.widgetTypeCH_xvar10.set(1)
          self.myreconfig()
     def applyB_action_code(self):
         self.saveBack()
         self.root.destroy()
         self.globals.repaint_all()
     
     def cancelB_action_code(self):
         self.root.destroy()
     
     def bgColorCH_item_code(self):
         settext(self.customBgColorTF, utilitycode.translateColor(gettext(self.bgColorCH)))
     
     def bgColorCH_respond(self , keycode):
          if keycode == 1:
               self.bgColorCH.config(text='white')
               for thing in self.bgColorCH_varlist:
                    thing.set(0)
               self.bgColorCH_xvar1.set(1)
          if keycode == 2:
               self.bgColorCH.config(text='pink')
               for thing in self.bgColorCH_varlist:
                    thing.set(0)
               self.bgColorCH_xvar2.set(1)
          if keycode == 3:
               self.bgColorCH.config(text='green')
               for thing in self.bgColorCH_varlist:
                    thing.set(0)
               self.bgColorCH_xvar3.set(1)
          if keycode == 4:
               self.bgColorCH.config(text='blue')
               for thing in self.bgColorCH_varlist:
                    thing.set(0)
               self.bgColorCH_xvar4.set(1)
          if keycode == 5:
               self.bgColorCH.config(text='red')
               for thing in self.bgColorCH_varlist:
                    thing.set(0)
               self.bgColorCH_xvar5.set(1)
          if keycode == 6:
               self.bgColorCH.config(text='black')
               for thing in self.bgColorCH_varlist:
                    thing.set(0)
               self.bgColorCH_xvar6.set(1)
          if keycode == 7:
               self.bgColorCH.config(text='--custom--')
               for thing in self.bgColorCH_varlist:
                    thing.set(0)
               self.bgColorCH_xvar7.set(1)
          settext(self.customBgColorTF, utilitycode.translateColor(gettext(self.bgColorCH)))
     def fgColorCH_item_code(self):
         settext(self.customFgColorTF, utilitycode.translateColor(gettext(self.fgColorCH)))
     
     def fgColorCH_respond(self , keycode):
          if keycode == 1:
               self.fgColorCH.config(text='white')
               for thing in self.fgColorCH_varlist:
                    thing.set(0)
               self.fgColorCH_xvar1.set(1)
          if keycode == 2:
               self.fgColorCH.config(text='pink')
               for thing in self.fgColorCH_varlist:
                    thing.set(0)
               self.fgColorCH_xvar2.set(1)
          if keycode == 3:
               self.fgColorCH.config(text='green')
               for thing in self.fgColorCH_varlist:
                    thing.set(0)
               self.fgColorCH_xvar3.set(1)
          if keycode == 4:
               self.fgColorCH.config(text='blue')
               for thing in self.fgColorCH_varlist:
                    thing.set(0)
               self.fgColorCH_xvar4.set(1)
          if keycode == 5:
               self.fgColorCH.config(text='red')
               for thing in self.fgColorCH_varlist:
                    thing.set(0)
               self.fgColorCH_xvar5.set(1)
          if keycode == 6:
               self.fgColorCH.config(text='black')
               for thing in self.fgColorCH_varlist:
                    thing.set(0)
               self.fgColorCH_xvar6.set(1)
          if keycode == 7:
               self.fgColorCH.config(text='--custom--')
               for thing in self.fgColorCH_varlist:
                    thing.set(0)
               self.fgColorCH_xvar7.set(1)
          settext(self.customFgColorTF, utilitycode.translateColor(gettext(self.fgColorCH)))
     def standardFontB_action_code(self):
         settext(self.fontTF, "Helvetica 9")
     
     def fontHelpB_action_code(self):
         #hw = NewHelpWindow()
         #hw.showTopic("Fonts")
         NewHelpWindow.main2("Fonts")
     
     def scrollbarOptionsB_action_code(self):
         settext(self.scrollbarOptionsTF, "from_=0, to=100, length=200, tickinterval=5, showvalue=YES, orient='horizontal'")

#--------------------Menu defs, do not change!--------------------


#--------------------extra class code, you can change this!--------------------
##%EXTRACLASSCODE
     import sys
     
     
     def setTarget(self, newtopBox):
          self.topBox = newtopBox
          settext(self.idTF, str(newtopBox.id))
          settext(self.nameTF, newtopBox.name)
          settext(self.widgetTypeCH, newtopBox.mytype)
          settext(self.widthTF, str(newtopBox.width))
          settext(self.heightTF, str(newtopBox.height))
          settext(self.labelTF, newtopBox.label)
          settext(self.codeTF, newtopBox.code)
          #print("newtopBox.bgcolor = "+newtopBox.bgcolor)
          settext(self.customBgColorTF, newtopBox.bgcolor)
          if (newtopBox.bgcolor.startswith("#")):
               settext(self.bgColorCH, utilitycode.getColorName(newtopBox.bgcolor))
          print("bgcolorCH set to "+utilitycode.getColorName(newtopBox.bgcolor))
          settext(self.customFgColorTF, newtopBox.fgcolor)
          if (newtopBox.fgcolor.startswith("#")):
               settext(self.fgColorCH, utilitycode.getColorName(newtopBox.fgcolor))
          settext(self.fontTF, newtopBox.font)
     
          if newtopBox.choices == []:
               settext(self.choicesTA, "")
          else:
               settext(self.choicesTA, "\n".join(newtopBox.choices))
     
          settext(self.radiogroupTF, newtopBox.radiogroup)
          if newtopBox.mytype == "scrollbar":
               settext(self.scrollbarOptionsTF, newtopBox.scrollbaroptions)
          sys.stdout.flush()
          self.myreconfig()
     
     def myreconfig(self):
          print("reconfigurating")
     
          if self.topBox.mytype != "choice" and self.topBox.mytype != "list":
               self.choicesTA.text.config(state=DISABLED)
               self.choicesTA.text.config(bg="gray")
          else:
               self.choicesTA.text.config(state=NORMAL)
               self.choicesTA.text.config(bg="white")
     
          if self.topBox.mytype != "scrollbar":
               self.scrollbarOptionsTF.config(state=DISABLED)
          else:
               self.scrollbarOptionsTF.config(state=NORMAL)
     
          if self.topBox.mytype != "radiobutton":
               self.radiogroupTF.config(state=DISABLED)
          else:
               self.radiogroupTF.config(state=NORMAL)
     
          print("done!")
          sys.stdout.flush()
          #self.root.update()
          #time.sleep(0.5)
     
     '''
     def refresh(self):
         self.destroy()
         self.__init__()
     '''
     
     def setGlobals(self, globals):
          self.globals = globals
          print("SetGlobals, parent="+str(self.globals))
          sys.stdout.flush()
     
     def saveBack(self):
          self.topBox.name = gettext(self.nameTF)
          self.topBox.updateWidth(int(gettext(self.widthTF)))
          self.topBox.updateHeight(int(gettext(self.heightTF)))
          self.topBox.mytype = gettext(self.widgetTypeCH)
          self.topBox.label = gettext(self.labelTF)
          self.topBox.code = gettext(self.codeTF)
          self.topBox.bgcolor = gettext(self.customBgColorTF)
          self.topBox.fgcolor = gettext(self.customFgColorTF)
          self.topBox.font = gettext(self.fontTF)
          self.topBox.choices = gettext(self.choicesTA).split("\n")
          if self.topBox.mytype == "radiobutton":
               if gettext(self.radiogroupTF).strip() == "":
                    popup("No group variable name given, so \"group1\" was given, which might not work.")
                    self.topBox.radiogroup = "group1"
               else:
                    self.topBox.radiogroup = gettext(self.radiogroupTF)
          self.topBox.scrollbaroptions = gettext(self.scrollbarOptionsTF)
     
     def post_initialization(self):
          pass
##%ENDCODE

     def __init__(self):
          self.root=Tk()
          self.root.geometry("480x448")
          self.root.configure(background='#ebebeb')
          self.root.title("Property Window")
#--------------------widget making code, do not change anything from here to the end of the file!--------------------
          self.component0BL = Label(self.root, text="Name:",width=56,height=22)
          self.component0BL.place(x=107,y=4, width=56, height=22)
          self.component0BL.config(font=("SansSerif", 10, 'normal'))
          self.component0BL.config(bg=self.root['bg'])
          self.component0BL.config(fg=("#000000"))
          self.Button1_var=StringVar()
          self.Button1_var.set("")
          self.nameTF = Entry(self.root,width=241, textvariable=self.Button1_var)
          self.nameTF.place(x=166,y=4, width=241, height=22)
          self.nameTF.config(font=("SansSerif", 10, 'normal'))
          self.nameTF.config(fg=("#000000"))
          self.nameTF.config(bg=("#ffffff"))
          self.label1L = Label(self.root, text="Type:",width=58,height=22)
          self.label1L.place(x=16,y=34, width=58, height=22)
          self.label1L.config(font=("SansSerif", 10, 'normal'))
          self.label1L.config(bg=self.root['bg'])
          self.label1L.config(fg=("#000000"))
          self.widgetTypeCH = Menubutton(self.root, text='')
          self.widgetTypeCH.place(x=75,y=34, width=101, height=22)
          self.widgetTypeCH.config(font=("SansSerif", 10, 'normal'))
          self.widgetTypeCH.config(bg=("#ffffff"))
          self.widgetTypeCH.config(fg=("#000000"))
          self.widgetTypeCH.menu = Menu(self.widgetTypeCH, tearoff=0)
          self.widgetTypeCH['menu'] = self.widgetTypeCH.menu
          self.widgetTypeCH_varlist=[]
          self.widgetTypeCH_xvar1=IntVar()
          self.widgetTypeCH_varlist.append(self.widgetTypeCH_xvar1)
          self.widgetTypeCH.menu.add_checkbutton(label='button',variable=self.widgetTypeCH_xvar1, command=functools.partial(self.widgetTypeCH_respond, 1))
          self.widgetTypeCH_xvar2=IntVar()
          self.widgetTypeCH_varlist.append(self.widgetTypeCH_xvar2)
          self.widgetTypeCH.menu.add_checkbutton(label='textfield',variable=self.widgetTypeCH_xvar2, command=functools.partial(self.widgetTypeCH_respond, 2))
          self.widgetTypeCH_xvar3=IntVar()
          self.widgetTypeCH_varlist.append(self.widgetTypeCH_xvar3)
          self.widgetTypeCH.menu.add_checkbutton(label='textarea',variable=self.widgetTypeCH_xvar3, command=functools.partial(self.widgetTypeCH_respond, 3))
          self.widgetTypeCH_xvar4=IntVar()
          self.widgetTypeCH_varlist.append(self.widgetTypeCH_xvar4)
          self.widgetTypeCH.menu.add_checkbutton(label='label',variable=self.widgetTypeCH_xvar4, command=functools.partial(self.widgetTypeCH_respond, 4))
          self.widgetTypeCH_xvar5=IntVar()
          self.widgetTypeCH_varlist.append(self.widgetTypeCH_xvar5)
          self.widgetTypeCH.menu.add_checkbutton(label='checkbox',variable=self.widgetTypeCH_xvar5, command=functools.partial(self.widgetTypeCH_respond, 5))
          self.widgetTypeCH_xvar6=IntVar()
          self.widgetTypeCH_varlist.append(self.widgetTypeCH_xvar6)
          self.widgetTypeCH.menu.add_checkbutton(label='radiobutton',variable=self.widgetTypeCH_xvar6, command=functools.partial(self.widgetTypeCH_respond, 6))
          self.widgetTypeCH_xvar7=IntVar()
          self.widgetTypeCH_varlist.append(self.widgetTypeCH_xvar7)
          self.widgetTypeCH.menu.add_checkbutton(label='choice',variable=self.widgetTypeCH_xvar7, command=functools.partial(self.widgetTypeCH_respond, 7))
          self.widgetTypeCH_xvar8=IntVar()
          self.widgetTypeCH_varlist.append(self.widgetTypeCH_xvar8)
          self.widgetTypeCH.menu.add_checkbutton(label='list',variable=self.widgetTypeCH_xvar8, command=functools.partial(self.widgetTypeCH_respond, 8))
          self.widgetTypeCH_xvar9=IntVar()
          self.widgetTypeCH_varlist.append(self.widgetTypeCH_xvar9)
          self.widgetTypeCH.menu.add_checkbutton(label='scrollbar',variable=self.widgetTypeCH_xvar9, command=functools.partial(self.widgetTypeCH_respond, 9))
          self.widgetTypeCH_xvar10=IntVar()
          self.widgetTypeCH_varlist.append(self.widgetTypeCH_xvar10)
          self.widgetTypeCH.menu.add_checkbutton(label='canvas',variable=self.widgetTypeCH_xvar10, command=functools.partial(self.widgetTypeCH_respond, 10))
          self.widgetTypeCH.bind("<<ListboxSelect>>", (lambda event: self.widgetTypeCH_item_code()))
          self.applyB = Button(self.root, text="Apply",width=67,height=26,command=self.applyB_action_code)
          self.applyB.place(x=179,y=415, width=67, height=26)
          self.applyB.config(font=("SansSerif", 10, 'normal'))
          self.applyB.config(bg=("#ffffff"))
          self.applyB.config(fg=("#000000"))
          self.cancelB = Button(self.root, text="Cancel",width=67,height=26,command=self.cancelB_action_code)
          self.cancelB.place(x=248,y=415, width=67, height=26)
          self.cancelB.config(font=("SansSerif", 10, 'normal'))
          self.cancelB.config(bg=("#ffffff"))
          self.cancelB.config(fg=("#000000"))
          self.component4BL = Label(self.root, text="Width:",width=60,height=20)
          self.component4BL.place(x=180,y=35, width=60, height=20)
          self.component4BL.config(font=("SansSerif", 10, 'normal'))
          self.component4BL.config(bg=self.root['bg'])
          self.component4BL.config(fg=("#000000"))
          self.Button1_var=StringVar()
          self.Button1_var.set("")
          self.widthTF = Entry(self.root,width=63, textvariable=self.Button1_var)
          self.widthTF.place(x=245,y=34, width=63, height=22)
          self.widthTF.config(font=("SansSerif", 10, 'normal'))
          self.widthTF.config(fg=("#000000"))
          self.widthTF.config(bg=("#ffffff"))
          self.Button1_var=StringVar()
          self.Button1_var.set("")
          self.heightTF = Entry(self.root,width=63, textvariable=self.Button1_var)
          self.heightTF.place(x=379,y=34, width=63, height=22)
          self.heightTF.config(font=("SansSerif", 10, 'normal'))
          self.heightTF.config(fg=("#000000"))
          self.heightTF.config(bg=("#ffffff"))
          self.label2L = Label(self.root, text="Height:",width=60,height=20)
          self.label2L.place(x=314,y=35, width=60, height=20)
          self.label2L.config(font=("SansSerif", 10, 'normal'))
          self.label2L.config(bg=self.root['bg'])
          self.label2L.config(fg=("#000000"))
          self.component6BL = Label(self.root, text="Id:",width=38,height=21)
          self.component6BL.place(x=15,y=5, width=38, height=21)
          self.component6BL.config(font=("SansSerif", 10, 'normal'))
          self.component6BL.config(bg=self.root['bg'])
          self.component6BL.config(fg=("#000000"))
          self.Button1_var=StringVar()
          self.Button1_var.set("")
          self.idTF = Entry(self.root,width=48, textvariable=self.Button1_var)
          self.idTF.place(x=56,y=4, width=48, height=22)
          self.idTF.config(font=("SansSerif", 10, 'normal'))
          self.idTF.config(fg=("#000000"))
          self.idTF.config(bg=("#ffffff"))
          self.label3L = Label(self.root, text="Function to call:",width=103,height=25)
          self.label3L.place(x=15,y=87, width=103, height=25)
          self.label3L.config(font=("SansSerif", 10, 'normal'))
          self.label3L.config(bg=self.root['bg'])
          self.label3L.config(fg=("#000000"))
          self.Button1_var=StringVar()
          self.Button1_var.set("")
          self.codeTF = Entry(self.root,width=244, textvariable=self.Button1_var)
          self.codeTF.place(x=121,y=87, width=244, height=24)
          self.codeTF.config(font=("SansSerif", 10, 'normal'))
          self.codeTF.config(fg=("#000000"))
          self.codeTF.config(bg=("#ffffff"))
          self.label4L = Label(self.root, text="Label:",width=49,height=25)
          self.label4L.place(x=69,y=59, width=49, height=25)
          self.label4L.config(font=("SansSerif", 10, 'normal'))
          self.label4L.config(bg=self.root['bg'])
          self.label4L.config(fg=("#000000"))
          self.Button1_var=StringVar()
          self.Button1_var.set("")
          self.labelTF = Entry(self.root,width=244, textvariable=self.Button1_var)
          self.labelTF.place(x=121,y=59, width=244, height=24)
          self.labelTF.config(font=("SansSerif", 10, 'normal'))
          self.labelTF.config(fg=("#000000"))
          self.labelTF.config(bg=("#ffffff"))
          self.component7BL = Label(self.root, text="Background color:",width=110,height=25)
          self.component7BL.place(x=10,y=174, width=110, height=25)
          self.component7BL.config(font=("SansSerif", 10, 'normal'))
          self.component7BL.config(bg=self.root['bg'])
          self.component7BL.config(fg=("#000000"))
          self.bgColorCH = Menubutton(self.root, text='')
          self.bgColorCH.place(x=122,y=173, width=127, height=27)
          self.bgColorCH.config(font=("SansSerif", 10, 'normal'))
          self.bgColorCH.config(bg=("#ffffff"))
          self.bgColorCH.config(fg=("#000000"))
          self.bgColorCH.menu = Menu(self.bgColorCH, tearoff=0)
          self.bgColorCH['menu'] = self.bgColorCH.menu
          self.bgColorCH_varlist=[]
          self.bgColorCH_xvar1=IntVar()
          self.bgColorCH_varlist.append(self.bgColorCH_xvar1)
          self.bgColorCH.menu.add_checkbutton(label='white',variable=self.bgColorCH_xvar1, command=functools.partial(self.bgColorCH_respond, 1))
          self.bgColorCH_xvar2=IntVar()
          self.bgColorCH_varlist.append(self.bgColorCH_xvar2)
          self.bgColorCH.menu.add_checkbutton(label='pink',variable=self.bgColorCH_xvar2, command=functools.partial(self.bgColorCH_respond, 2))
          self.bgColorCH_xvar3=IntVar()
          self.bgColorCH_varlist.append(self.bgColorCH_xvar3)
          self.bgColorCH.menu.add_checkbutton(label='green',variable=self.bgColorCH_xvar3, command=functools.partial(self.bgColorCH_respond, 3))
          self.bgColorCH_xvar4=IntVar()
          self.bgColorCH_varlist.append(self.bgColorCH_xvar4)
          self.bgColorCH.menu.add_checkbutton(label='blue',variable=self.bgColorCH_xvar4, command=functools.partial(self.bgColorCH_respond, 4))
          self.bgColorCH_xvar5=IntVar()
          self.bgColorCH_varlist.append(self.bgColorCH_xvar5)
          self.bgColorCH.menu.add_checkbutton(label='red',variable=self.bgColorCH_xvar5, command=functools.partial(self.bgColorCH_respond, 5))
          self.bgColorCH_xvar6=IntVar()
          self.bgColorCH_varlist.append(self.bgColorCH_xvar6)
          self.bgColorCH.menu.add_checkbutton(label='black',variable=self.bgColorCH_xvar6, command=functools.partial(self.bgColorCH_respond, 6))
          self.bgColorCH_xvar7=IntVar()
          self.bgColorCH_varlist.append(self.bgColorCH_xvar7)
          self.bgColorCH.menu.add_checkbutton(label='--custom--',variable=self.bgColorCH_xvar7, command=functools.partial(self.bgColorCH_respond, 7))
          self.bgColorCH.bind("<<ListboxSelect>>", (lambda event: self.bgColorCH_item_code()))
          self.Button1_var=StringVar()
          self.Button1_var.set("")
          self.customBgColorTF = Entry(self.root,width=106, textvariable=self.Button1_var)
          self.customBgColorTF.place(x=252,y=172, width=106, height=28)
          self.customBgColorTF.config(font=("SansSerif", 10, 'normal'))
          self.customBgColorTF.config(fg=("#000000"))
          self.customBgColorTF.config(bg=("#ffffff"))
          self.Button1_var=StringVar()
          self.Button1_var.set("")
          self.customFgColorTF = Entry(self.root,width=106, textvariable=self.Button1_var)
          self.customFgColorTF.place(x=252,y=204, width=106, height=28)
          self.customFgColorTF.config(font=("SansSerif", 10, 'normal'))
          self.customFgColorTF.config(fg=("#000000"))
          self.customFgColorTF.config(bg=("#ffffff"))
          self.label5L = Label(self.root, text="Foreground color:",width=110,height=25)
          self.label5L.place(x=10,y=206, width=110, height=25)
          self.label5L.config(font=("SansSerif", 10, 'normal'))
          self.label5L.config(bg=self.root['bg'])
          self.label5L.config(fg=("#000000"))
          self.fgColorCH = Menubutton(self.root, text='')
          self.fgColorCH.place(x=122,y=205, width=127, height=27)
          self.fgColorCH.config(font=("SansSerif", 10, 'normal'))
          self.fgColorCH.config(bg=("#ffffff"))
          self.fgColorCH.config(fg=("#000000"))
          self.fgColorCH.menu = Menu(self.fgColorCH, tearoff=0)
          self.fgColorCH['menu'] = self.fgColorCH.menu
          self.fgColorCH_varlist=[]
          self.fgColorCH_xvar1=IntVar()
          self.fgColorCH_varlist.append(self.fgColorCH_xvar1)
          self.fgColorCH.menu.add_checkbutton(label='white',variable=self.fgColorCH_xvar1, command=functools.partial(self.fgColorCH_respond, 1))
          self.fgColorCH_xvar2=IntVar()
          self.fgColorCH_varlist.append(self.fgColorCH_xvar2)
          self.fgColorCH.menu.add_checkbutton(label='pink',variable=self.fgColorCH_xvar2, command=functools.partial(self.fgColorCH_respond, 2))
          self.fgColorCH_xvar3=IntVar()
          self.fgColorCH_varlist.append(self.fgColorCH_xvar3)
          self.fgColorCH.menu.add_checkbutton(label='green',variable=self.fgColorCH_xvar3, command=functools.partial(self.fgColorCH_respond, 3))
          self.fgColorCH_xvar4=IntVar()
          self.fgColorCH_varlist.append(self.fgColorCH_xvar4)
          self.fgColorCH.menu.add_checkbutton(label='blue',variable=self.fgColorCH_xvar4, command=functools.partial(self.fgColorCH_respond, 4))
          self.fgColorCH_xvar5=IntVar()
          self.fgColorCH_varlist.append(self.fgColorCH_xvar5)
          self.fgColorCH.menu.add_checkbutton(label='red',variable=self.fgColorCH_xvar5, command=functools.partial(self.fgColorCH_respond, 5))
          self.fgColorCH_xvar6=IntVar()
          self.fgColorCH_varlist.append(self.fgColorCH_xvar6)
          self.fgColorCH.menu.add_checkbutton(label='black',variable=self.fgColorCH_xvar6, command=functools.partial(self.fgColorCH_respond, 6))
          self.fgColorCH_xvar7=IntVar()
          self.fgColorCH_varlist.append(self.fgColorCH_xvar7)
          self.fgColorCH.menu.add_checkbutton(label='--custom--',variable=self.fgColorCH_xvar7, command=functools.partial(self.fgColorCH_respond, 7))
          self.fgColorCH.bind("<<ListboxSelect>>", (lambda event: self.fgColorCH_item_code()))
          self.fontL = Label(self.root, text="Font:",width=41,height=24)
          self.fontL.place(x=78,y=143, width=41, height=24)
          self.fontL.config(font=("SansSerif", 10, 'normal'))
          self.fontL.config(bg=self.root['bg'])
          self.fontL.config(fg=("#000000"))
          self.Button1_var=StringVar()
          self.Button1_var.set("")
          self.fontTF = Entry(self.root,width=244, textvariable=self.Button1_var)
          self.fontTF.place(x=121,y=143, width=244, height=24)
          self.fontTF.config(font=("SansSerif", 10, 'normal'))
          self.fontTF.config(fg=("#000000"))
          self.fontTF.config(bg=("#ffffff"))
          self.standardFontB = Button(self.root, text="Standard",width=68,height=24,command=self.standardFontB_action_code)
          self.standardFontB.place(x=369,y=143, width=68, height=24)
          self.standardFontB.config(font=("SansSerif", 10, 'normal'))
          self.standardFontB.config(bg=("#ffffff"))
          self.standardFontB.config(fg=("#000000"))
          self.fontHelpB = Button(self.root, text="?",width=28,height=24,command=self.fontHelpB_action_code)
          self.fontHelpB.place(x=440,y=143, width=28, height=24)
          self.fontHelpB.config(font=("SansSerif", 10, 'normal'))
          self.fontHelpB.config(bg=("#ffffff"))
          self.fontHelpB.config(fg=("#000000"))
          self.label6L = Label(self.root, text="Choices:",width=68,height=25)
          self.label6L.place(x=52,y=238, width=68, height=25)
          self.label6L.config(font=("SansSerif", 10, 'normal'))
          self.label6L.config(bg=self.root['bg'])
          self.label6L.config(fg=("#000000"))
          self.choicesTA = self.ScrolledText(self.root)
          self.choicesTA.place(x=123,y=238, width=354, height=110)
          self.choicesTA.settext("")
          self.choicesTA.text.config(font=("SansSerif", 10, 'normal'))
          self.choicesTA.text.config(bg=("#ffffff"))
          self.choicesTA.text.config(fg=("#000000"))
          self.label7L = Label(self.root, text="(for checkboxes",width=93,height=21)
          self.label7L.place(x=28,y=266, width=93, height=21)
          self.label7L.config(font=("SansSerif", 10, 'normal'))
          self.label7L.config(bg=self.root['bg'])
          self.label7L.config(fg=("#000000"))
          self.label8L = Label(self.root, text="and lists)",width=93,height=21)
          self.label8L.place(x=28,y=289, width=93, height=21)
          self.label8L.config(font=("SansSerif", 9, 'normal'))
          self.label8L.config(bg=self.root['bg'])
          self.label8L.config(fg=("#000000"))
          self.scrollbarOptionsB = Button(self.root, text="Sample",width=71,height=21,command=self.scrollbarOptionsB_action_code)
          self.scrollbarOptionsB.place(x=405,y=378, width=71, height=21)
          self.scrollbarOptionsB.config(font=("SansSerif", 9, 'normal'))
          self.scrollbarOptionsB.config(bg=("#ffffff"))
          self.scrollbarOptionsB.config(fg=("#000000"))
          self.label9L = Label(self.root, text="Radiobutton group:",width=111,height=25)
          self.label9L.place(x=8,y=115, width=111, height=25)
          self.label9L.config(font=("SansSerif", 10, 'normal'))
          self.label9L.config(bg=self.root['bg'])
          self.label9L.config(fg=("#000000"))
          self.Button1_var=StringVar()
          self.Button1_var.set("")
          self.radiogroupTF = Entry(self.root,width=244, textvariable=self.Button1_var)
          self.radiogroupTF.place(x=121,y=115, width=244, height=24)
          self.radiogroupTF.config(font=("SansSerif", 10, 'normal'))
          self.radiogroupTF.config(fg=("#000000"))
          self.radiogroupTF.config(bg=("#ffffff"))
          self.component8BL = Label(self.root, text="Scrollbar options:",width=110,height=19)
          self.component8BL.place(x=12,y=355, width=110, height=19)
          self.component8BL.config(font=("SansSerif", 10, 'normal'))
          self.component8BL.config(bg=self.root['bg'])
          self.component8BL.config(fg=("#000000"))
          self.Button1_var=StringVar()
          self.Button1_var.set("")
          self.scrollbarOptionsTF = Entry(self.root,width=350, textvariable=self.Button1_var)
          self.scrollbarOptionsTF.place(x=125,y=354, width=350, height=22)
          self.scrollbarOptionsTF.config(font=("SansSerif", 9, 'normal'))
          self.scrollbarOptionsTF.config(fg=("#000000"))
          self.scrollbarOptionsTF.config(bg=("#ffffff"))

          self.post_initialization()
if __name__ == '__main__':
     tempwin=PropWindow()
     tempwin.root.mainloop()

####DIRECTIVES
##%START
##%PROGRAM DATE=Sat, Jun 12, 2021 11:06:26 AM
##%VERSION=PY2
##%CLASS_STYLE=class
##%WHENWRITTEN=Sat Jun 04 08:33:59 EDT 2022
##%CLASSNAME=PropWindow
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
##%WIDTH=495
##%HEIGHT=503
##%COMPONENTS
##%COMPONENT 
##%  id=1
##%  type=Label
##%  label=Name:
##%  varname=component0BL
##%  startpoint=107,54
##%  endpoint=163,76
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
##%  varname=nameTF
##%  startpoint=166,54
##%  endpoint=407,76
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
##%  id=3
##%  type=Label
##%  label=Type:
##%  varname=label1L
##%  startpoint=16,84
##%  endpoint=74,106
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
##%  id=4
##%  type=Choice
##%  label=
##%  varname=widgetTypeCH
##%  startpoint=75,84
##%  endpoint=176,106
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
##%  other=button\ntextfield\ntextarea\nlabel\ncheckbox\nradiobutton\nchoice\nlist\nscrollbar\ncanvas
##%  codeAction=
##%  codeItem=self.myreconfig()
##%END
##%COMPONENT 
##%  id=5
##%  type=Button
##%  label=Apply
##%  varname=applyB
##%  startpoint=179,465
##%  endpoint=246,491
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
##%  startpoint=248,465
##%  endpoint=315,491
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
##%  id=7
##%  type=Label
##%  label=Width:
##%  varname=component4BL
##%  startpoint=180,85
##%  endpoint=240,105
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
##%  id=8
##%  type=TextField
##%  label=
##%  varname=widthTF
##%  startpoint=245,84
##%  endpoint=308,106
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
##%  id=11
##%  type=TextField
##%  label=
##%  varname=heightTF
##%  startpoint=379,84
##%  endpoint=442,106
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
##%  id=12
##%  type=Label
##%  label=Height:
##%  varname=label2L
##%  startpoint=314,85
##%  endpoint=374,105
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
##%  id=13
##%  type=Label
##%  label=Id:
##%  varname=component6BL
##%  startpoint=15,55
##%  endpoint=53,76
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
##%  id=14
##%  type=TextField
##%  label=
##%  varname=idTF
##%  startpoint=56,54
##%  endpoint=104,76
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
##%  id=15
##%  type=Label
##%  label=Function to call:
##%  varname=label3L
##%  startpoint=15,137
##%  endpoint=118,162
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
##%  varname=codeTF
##%  startpoint=121,137
##%  endpoint=365,161
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
##%  id=19
##%  type=Label
##%  label=Label:
##%  varname=label4L
##%  startpoint=69,109
##%  endpoint=118,134
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
##%  id=20
##%  type=TextField
##%  label=
##%  varname=labelTF
##%  startpoint=121,109
##%  endpoint=365,133
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
##%  id=21
##%  type=Label
##%  label=Background color:
##%  varname=component7BL
##%  startpoint=10,224
##%  endpoint=120,249
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
##%  id=22
##%  type=Choice
##%  label=
##%  varname=bgColorCH
##%  startpoint=122,223
##%  endpoint=249,250
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
##%  other=white\npink\ngreen\nblue\nred\nblack\n--custom--
##%  codeAction=
##%  codeItem=settext(self.customBgColorTF, utilitycode.translateColor(gettext(self.bgColorCH)))
##%END
##%COMPONENT 
##%  id=23
##%  type=TextField
##%  label=
##%  varname=customBgColorTF
##%  startpoint=252,222
##%  endpoint=358,250
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
##%  id=27
##%  type=TextField
##%  label=
##%  varname=customFgColorTF
##%  startpoint=252,254
##%  endpoint=358,282
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
##%  id=28
##%  type=Label
##%  label=Foreground color:
##%  varname=label5L
##%  startpoint=10,256
##%  endpoint=120,281
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
##%  id=29
##%  type=Choice
##%  label=
##%  varname=fgColorCH
##%  startpoint=122,255
##%  endpoint=249,282
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
##%  other=white\npink\ngreen\nblue\nred\nblack\n--custom--
##%  codeAction=
##%  codeItem=settext(self.customFgColorTF, utilitycode.translateColor(gettext(self.fgColorCH)))
##%END
##%COMPONENT 
##%  id=32
##%  type=Label
##%  label=Font:
##%  varname=fontL
##%  startpoint=78,193
##%  endpoint=119,217
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
##%  id=33
##%  type=TextField
##%  label=
##%  varname=fontTF
##%  startpoint=121,193
##%  endpoint=365,217
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
##%  id=34
##%  type=Button
##%  label=Standard
##%  varname=standardFontB
##%  startpoint=369,193
##%  endpoint=437,217
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
##%  codeAction=settext(self.fontTF, "Helvetica 9")
##%  codeItem=
##%END
##%COMPONENT 
##%  id=35
##%  type=Button
##%  label=?
##%  varname=fontHelpB
##%  startpoint=440,193
##%  endpoint=468,217
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
##%  codeAction=#hw = NewHelpWindow()\n#hw.showTopic("Fonts")\nNewHelpWindow.main()
##%  codeItem=
##%END
##%COMPONENT 
##%  id=36
##%  type=Label
##%  label=Choices:
##%  varname=label6L
##%  startpoint=52,288
##%  endpoint=120,313
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
##%  id=37
##%  type=TextArea
##%  label=
##%  varname=choicesTA
##%  startpoint=123,288
##%  endpoint=477,398
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
##%  type=Label
##%  label=(for checkboxes
##%  varname=label7L
##%  startpoint=28,316
##%  endpoint=121,337
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
##%  id=40
##%  type=Label
##%  label=and lists)
##%  varname=label8L
##%  startpoint=28,339
##%  endpoint=121,360
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
##%COMPONENT 
##%  id=41
##%  type=Button
##%  label=Sample
##%  varname=scrollbarOptionsB
##%  startpoint=405,428
##%  endpoint=476,449
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
##%  codeAction=settext(self.scrollbarOptionsTF, "from_=0, to=100, length=200, tickinterval=5, showvalue=YES, orient='horizontal'")
##%  codeItem=
##%END
##%COMPONENT 
##%  id=44
##%  type=Label
##%  label=Radiobutton group:
##%  varname=label9L
##%  startpoint=8,165
##%  endpoint=119,190
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
##%  type=TextField
##%  label=
##%  varname=radiogroupTF
##%  startpoint=121,165
##%  endpoint=365,189
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
##%  id=50
##%  type=Label
##%  label=Scrollbar options:
##%  varname=component8BL
##%  startpoint=12,405
##%  endpoint=122,424
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
##%  id=51
##%  type=TextField
##%  label=
##%  varname=scrollbarOptionsTF
##%  startpoint=125,404
##%  endpoint=475,426
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
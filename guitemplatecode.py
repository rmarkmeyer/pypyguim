preamble = """
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
			for string in newtext.split('\\n'):
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
			for string in newtext.split('\\n'):
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

def promptForFilename(prompt):
     return filedialog.askopenfilename(title=prompt)

def promptForFileSavename(prompt):
     return filedialog.asksaveasfilename(title=prompt)

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

def nothing():
	pass

def kill():
	sys.exit()

def resizeMe(event):
	#  This can be overridden below by the user's own version if they want
	pass

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

"""

#---------------------------------------------------------------------------------------------------------------------------------------------------------

window_init_code1 = """
def window_init():
     global root
     root=Tk()
"""
#     root.geometry("685x445")

#     root.configure(background='#ebebeb')
#     root.title("Python application")

window_init_code2 = """
     global canvas
     canvas = Canvas(bd=0, highlightthickness=0)
     canvas.pack(fill=BOTH, expand=1)
     canvas.bind("<Configure>", resizeMe)
     canvas.place(x=0,y=0,width=685,height=445)
"""

#---------------------------------------------------------------------------------------------------------------------------------------------------------

make_main = """
def main():
     window_init()
"""

#----------------------------------------------------------------------------------------------------------------------------------------------------------

postlude = """
     root.mainloop()

if __name__ == '__main__':
     main()
"""
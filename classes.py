from datetime import datetime,date
import os,os.path,sys
import utilitycode
import guitemplatecode

current_version = 10
acceptable_difference = 2

class Globals:
	def __init__(self):
		self.clear()

	def clear(self):
		if "widgets" in self.__dict__:
			for widget in self.widgets:
				widget.clearbox()
		self.widgets = []
		self.code = ""
		self.menus = ""
		self.lastLoadedImage = ""
		self.window_width = 685
		self.window_height = 450
		self.title = "Python GUI app"
		self.bgcolor = "white"
		self.documentation = ""       # internal documentation
		self.deleteds = []                 # not saved, just temporary

	def repaint_all(self):
		#print("----------repaint all----------------")
		for widget in self.widgets:
			widget.clearbox()
			widget.paintme()
		#print("--------------------------------------")
		sys.stdout.flush()

	def add(self, widget):
		self.widgets.append(widget)

	def findBoxContainingPoint(self, somePoint):
		'''  We need to go backwards because the most recently added box is likely the top one. '''
		for i in range(len(self.widgets)-1,-1,-1):
			widget = self.widgets[i]
			if widget.contains(somePoint):
				#print("widget " + str(widget.id)+"  contains the point " + str(somePoint))
				return widget
		#print("No widget found containing point " + str(somePoint))
		return None

	def listWidgets(self):
		if len(self.widgets) == 0:
			return "NO WIDGETS YET!"
		s = ""
		for widget in self.widgets:
			s += widget.shortSummary() + "\n"
		return s

	def delWidget(self, somebox):
		somebox.clearbox()
		newlist = []
		for widget in self.widgets:
			if widget != somebox:
				newlist.append(widget)
		self.widgets = newlist

	def parse(self, image):
		lines = image.split("\n")
		if lines[0].startswith("#."):
			newlines = []
			for line in lines:
				if line.startswith("#."):
					if line.startswith("#.END"): break
					line = line[2:]
				newlines.append(line)
			lines = newlines
		else:
			pass    # this is the old, naked format which we maintain for backwards compatibility

		headerline = lines[0]
		if headerline.startswith("PYPYGUIM "):
			saved_version = int(headerline.split(";")[0].split(" ")[1])  
			if current_version - saved_version > acceptable_difference:
				print(">>>>>>> This PYPYGUIM file is version " + saved_version + " and does not match the current program version " + current_version)
				return
		else:
			print(">>>>>>> ERROR!  This is not a PYPYGUIM file! <<<<<<<<<<<")
			sys.stdout.flush()
			return
		self.lastSavedTime = headerline.split(";")[1]

		i = 0
		found = False
		while i < len(lines):
			if lines[i].startswith("$$$options"):
				print("found $$$options at i="+str(i))
				found = True
				break
			i += 1
		if found:
			self.code = ""
			i += 1
			while i < len(lines):
				if lines[i].startswith("$$$end-options"):
					break
				if lines[i].startswith("title:"):
					print("title is "+ self.title)
					self.title = lines[i][6:]
				if lines[i].startswith("bgcolor:"):
					self.bgcolor = lines[i][8:]
					print("bgcolor = " + self.bgcolor)
				if lines[i].startswith("geom:"):
					temp = lines[i][5:].split("x")
					self.window_width = int(temp[0])
					self.window_height = int(temp[1])
				i += 1
		sys.stdout.flush()

		i = 0
		found = False
		while i < len(lines):
			if lines[i].startswith("$$$documentation"):
				found = True
				break
			i += 1
		if found:
			self.documentation = ""
			i += 1
			while i < len(lines):
				if lines[i].startswith("$$$end-documentation"):
					break
				self.documentation += lines[i] + "\n"
				i += 1

		i = 0
		found = False
		while i < len(lines):
			if lines[i].startswith("$$$code"):
				found = True
				break
			i += 1
		if found:
			self.code = ""
			i += 1
			while i < len(lines):
				if lines[i].startswith("$$$end-code"):
					break
				self.code += lines[i] + "\n"
				i += 1
		i = 0
		found = False
		while i < len(lines):
			if lines[i].startswith("$$$menus"):
				found = True
				break
			i += 1
		if found:
			self.menus = ""
			i += 1
			while i < len(lines):
				if lines[i].startswith("$$$end-menus"):
					break
				self.menus += lines[i] + "\n"
				i += 1
		i = 0
		found = False
		while i < len(lines):
			if lines[i].startswith("$$$widgets"):
				found = True
				break
			i += 1
		if not found: return
		while i < len(lines):
			if lines[i].startswith("$$$$"):
				widget_image = []
				widget_image.append(lines[i])
				i += 1
				while i < len(lines):
					if lines[i].startswith("//end:"):
						i += 1
						break
					widget_image.append(lines[i])
					i += 1

				#print("widget lines = "+str(widget_image))
				w = MyWidget()
				w.parse(widget_image)
				self.widgets.append(w)

			elif lines[i].startswith("$%end"):
				break
			else:
				i += 1   # shouldn't be here...

	def applyCanvas(self, somecanvas):
		if somecanvas is None:
			print("somecanvas is None")
		else:
			print("somecanvas is ok")
		for widget in self.widgets:
			widget.canvas = somecanvas
			#print("applied canvas to "+str(widget.id))
		sys.stdout.flush()

	def makeImage(self):
		'''   this saves the directives in Python comments, starting with #.
		'''
		now = datetime.now()
		image = "PYPYGUIM " + str(current_version) + ";" + now.__format__("%a %b %d, %Y") + "  system:" + os.environ['COMPUTERNAME'] + "\n"
		image += "$$$documentation\n"
		image += self.documentation
		if not self.documentation.endswith("\n"):
			image += "\n"
		image += "$$$end-documentation\n"
		image += "$$$options\n"
		image += "title:" + self.title + "\n"
		image += "geom:" + 	str(self.window_width) +"x" + str(self.window_height) + "\n"
		image += "bgcolor:" + self.bgcolor + "\n"
		image += "$$$end-options\n"
		image += "$$$code\n"
		image += self.code
		if not self.code.endswith("\n"):
			image += "\n"
		image += "$$$end-code\n"
		image += "$$$menus\n"
		image += self.menus
		if not self.menus.endswith("\n"):
			image += "\n"
		image += "$$$end-menus\n"

		image += "$$$widgets\n"
		for widget in self.widgets:
			image += widget.makeImage() + "\n"
		image += "$$$end-widgets\n"
		image += "$%end\n"
		image += "END\n"

		newimage = ""
		for line in image.split("\n"):
			newimage += ("" if newimage == "" else "\n") + "#." + line
		return newimage

	def makePythonFile(self):
		'''  This builds the Python tkinter file that will implement the GUI for the user.
		    This is the desired endpoint of this whole thing! 
		    The directives are stored at the beginning with Python comments, starting with #.
		'''
		image = guitemplatecode.preamble
		image += "#------------------------------ module code -------------------------------------------\n"
		image += self.code + "\n"
		image += "#------------------------------ end of module code -------------------------------------------\n"
		image += "#------------------------------ choice and list code -------------------------------------------\n"

		for widget in self.widgets:
			if widget.mytype == "choice":
				image += widget.makeChoiceHandler()
			if widget.mytype == "list":
				image += widget.makeListHandler()
			if widget.mytype == "radiobutton":
				image += widget.makeRadiobuttonHandler()

		image += "#------------------------------ end of choice and list code -------------------------------------------\n"
		image += guitemplatecode.window_init_code1
		image += "     root.geometry(\"" + str(self.window_width) + "x" + str(self.window_height) + "\")\n"
		image += "     root.configure(background=\"" + self.bgcolor + "\")\n"
		image += "     root.title(\"" + self.title + "\")\n"
		image += "     canvas = Canvas(bd=0, highlightthickness=0)\n"
		for line in self.code.split("\n"):
			if line.startswith("def resizeMe("):
				image += "     canvas.bind(\"<Configure>\", resizeMe)\n"
		image += "     canvas.configure(background=\"" + self.bgcolor + "\")\n"
		#image += guitemplatecode.window_init_code2
		image += guitemplatecode.make_main

		if len(self.widgets) == 0:
			return ("No widgets!  This program will crash...")

		globals_line = "     global "
		for widget in self.widgets:
			globals_line += widget.name + ","
		globals_line = globals_line[0:-1]    # trim off final comma
		image += globals_line + "\n"

		for widget in self.widgets:
			if widget.mytype == "choice":
				image += "     global " + widget.name + "_varlist\n"

		radiobuttonGroupVars = set()
		for widget in self.widgets:
			if widget.radiogroup != "":
				radiobuttonGroupVars.add(widget.radiogroup)
		for varname in list(radiobuttonGroupVars):
			image += f"     global {varname}\n"
			image += f"     {varname} = StringVar()\n"


		widgetscode = ""
		for widget in self.widgets:
			widgetscode += utilitycode.indentEveryLine(widget.writePython()) + "\n"
		image += widgetscode + "\n"

		if self.menus.strip() != "":
			image += "     topmenu = Menu(root)\n"
			image += "     root.config(menu=topmenu)\n"
			menunumber = 0
			for line in self.menus.split("\n"):
				if line.strip() == "": continue
				if line.strip().startswith("#"): continue
				if not line.startswith(" "):
					menunumber += 1
					menuname = "menu" + str(menunumber)
					image += f"     {menuname} = Menu(topmenu)\n"
					image += f"     topmenu.add_cascade(label=\"{line}\", menu={menuname}, underline=0)\n"
				else:
					#print("...line="+line)
					parts = line.strip().split("&")
					#print("...parts="+str(parts))
					sys.stdout.flush()
					menuitem = parts[0]
					command="nothing"
					if len(parts) == 2:
						command = parts[1]
					image += f"     {menuname}.add_command(label=\"{menuitem}\", command={command}, underline=0)\n"


		for line in self.code.split("\n"):
			if line.startswith("def post_initialization("):
				image += "     post_initialization()\n"
				break
			
		image += guitemplatecode.postlude
		newimage = self.makeImage() + "\n"
		newimage += image
		return newimage

	def info(self):
		s = ""
		s += str(len(self.widgets)) + " widgets.\n"
		return s

	def longInfo(self):
		s = ""
		#s += "Filename: " + self.filename + "\n"
		s += "Window width: " + str(self.window_width) + "\n"
		s += "Window height: " + str(self.window_height) + "\n"

		s += "Widgets:\n-------------------\n"
		for widget in self.widgets:
			s += widget.shortSummary() + "\n\n"
		if self.code.strip() == "":
			s += "NO CODE YET...\n\n"
		else:
			s += "Code:\n------------\n"
			s += self.code + "\n"
		if self.documentation.strip() == "":
			s += "NO DOCUMENTATION YET...\n\n"
		else:
			s += "Documentation:\n------------\n"
			s += self.documentation + "\n"
		return s

#==============================================================================================================================
#==============================================================================================================================
#==============================================================================================================================

standardFont = ('Helvetica 9')
boldfont = ('Helvetica 12 bold')
lightgray = "#E6E6E6"

class MyWidget:
	nextid = 1

	def __init__(self):
		self.id = MyWidget.nextid
		MyWidget.nextid += 1
		self.name = "Button" + str(self.id)
		self.mytype = "button"
		self.code = ""                       # function name
		self.label = "Example"          # this is useful for buttons and others
		self.startPoint = Point(0,0)
		self.endPoint = Point(0,0)
		self.width = 0
		self.height = 0
		self.myvar = ""             # for some widgets you need to have an additional variable
		self.bgcolor = "white"
		self.fgcolor = "black"
		self.font = standardFont
		self.choices = []          # list of strings, which are choices only for lists and checkboxes
		self.canvas = None
		self.radiogroup = ""    # only works for radiobuttons
		self.scrollbaroptions = ""

		self.multiselected = False
		self.selected = False            # temporary
		self.lines = []                         # temporary
		self.offsetX = 0
		self.offsetY = 0

	def shortSummary(self):
		s ="Id: " + str(self.id) + "  Name:" + self.name + "   Type:" + self.mytype + "  Label:" + self.label + "\n"
		s += "  width:" + str(self.width) + " height:"+ str(self.height)
		return s

	def setbox(self, startPoint, endPoint, canvas):
		self.startPoint = startPoint          # this may change as we move it around
		self.endPoint = endPoint
		self.width = endPoint.x - startPoint.x
		self.height = endPoint.y - startPoint.y
		self.canvas = canvas

	def parse(self, lines):
		print("parsing: " + str(lines) + "\n")
		parts = lines[0][4:].strip().split(" ")        # this is the $$$$id: line
		for part in parts:
			part = part.strip()
			if part.startswith("id:"):
				self.id = int(part[3:])
			elif part.startswith("name:"):
				self.name = part[5:]
			elif part.startswith("type:"):
				self.mytype = part[5:]
			elif part.startswith("start:"):
				xparts = part[6:].split(",")
				self.startPoint = Point(int(xparts[0]), int(xparts[1]))
			elif part.startswith("end:"):
				xparts = part[4:].split(",")
				self.endPoint = Point(int(xparts[0]), int(xparts[1]))
				print("just parsed endpoint = "+str(self.endPoint))
		n = lines[0].find("label:")
		if n != -1:
			self.label = lines[0][n+6:]        # avoids any breaking space in the label
		self.width = self.endPoint.x - self.startPoint.x
		self.height = self.endPoint.y - self.startPoint.y
		print("just parsed self.height = "+str(self.height))
		for line in lines:
			if line.startswith("code:"):
				self.code = line[5:]
			elif line.startswith("myvar:"):
				self.myvar = line[6:]
			elif line.startswith("colors:"):
				print("line="+line)
				pieces = line[7:].strip().split(" ")
				print("pieces="+str(pieces))
				self.bgcolor = pieces[0].split(":")[1]
				self.fgcolor = pieces[1].split(":")[1]
				print("self.bgcolor = "+self.bgcolor)
				sys.stdout.flush()
			elif line.startswith("choices:"):
				line = line[8:]
				self.choices = line.split(";")
			elif line.startswith("radiogroup:"):
				self.radiogroup = line[11:].strip()
			elif line.startswith("scrollbaroptions:"):
				self.scrollbaroptions = line[17:].strip()
			elif line.startswith("font:"):
				self.font = line[5:].strip()

	def paintme(self):
		if self.selected:
			outlinecolor = "red"
			fillcolor = "yellow"
		else:	
			outlinecolor = "black"
			if self.mytype == "button":
				fillcolor = "pink"
			elif self.mytype == "textfield":
				fillcolor = "magenta"
			elif self.mytype == "textarea":
				fillcolor = "cyan"
			elif self.mytype == "label":
				fillcolor = "#00FF00"
			elif self.mytype == "scrollbar":
				fillcolor = "#FF0000"
			elif self.mytype == "list":
				fillcolor = "#00FF00"
			elif self.mytype == "checkbox":
				fillcolor = "#FFC800"
			elif self.mytype == "choice":
				fillcolor = "#05CBE2"
			elif self.mytype == "radiobutton":
				fillcolor = "#A3C384"
			else:
				fillcolor = "#E6E6E6"  # light gray
		if self.multiselected:
			outlinecolor = "red"

		#print(f"painting {self.id}   self.multiselected={self.multiselected}")
		top = self.canvas.create_line(self.startPoint.x, self.startPoint.y, self.endPoint.x, self.startPoint.y, width=2, fill=outlinecolor)
		bot = self.canvas.create_line(self.startPoint.x, self.endPoint.y, self.endPoint.x, self.endPoint.y, width=2, fill=outlinecolor)
		left = self.canvas.create_line(self.startPoint.x, self.startPoint.y, self.startPoint.x, self.endPoint.y, width=2, fill=outlinecolor)
		right = self.canvas.create_line(self.endPoint.x, self.startPoint.y, self.endPoint.x, self.endPoint.y, width=2, fill=outlinecolor)
		rectangle = self.canvas.create_rectangle(self.startPoint.x,self.startPoint.y, self.endPoint.x-1, self.endPoint.y-1, fill=fillcolor)
		if self.multiselected:
			rectangle2 = self.canvas.create_rectangle(self.startPoint.x-2, self.startPoint.y-2, self.endPoint.x+2, self.endPoint.y+2,fill="red")
		xname = self.canvas.create_text(self.startPoint.x+25, self.startPoint.y+9,text=self.name,fill="black",font=standardFont)
		xlabel = self.canvas.create_text(self.startPoint.x+50, self.startPoint.y + 30,text=self.label,fill="black",font=boldfont)
		if self.selected:
			resizetop = self.canvas.create_line(self.endPoint.x - 10, self.endPoint.y - 10, self.endPoint.x, self.endPoint.y-10, width=2,fill="black")
			resizeleft = self.canvas.create_line(self.endPoint.x-10, self.endPoint.y - 10, self.endPoint.x-10, self.endPoint.y, width=2, fill="black")
			self.lines = [top,bot,left,right,rectangle,xname,xlabel,resizetop,resizeleft]
		else:
			self.lines = [top,bot,left,right,rectangle,xname,xlabel]
		if self.multiselected:
			self.lines.append(rectangle2)

	def moveTo(self, newPoint):
		self.clearbox()
		self.startPoint = Point(newPoint.x - self.offsetX, newPoint.y - self.offsetY)
		self.endPoint = Point(self.startPoint.x + self.width, self.startPoint.y + self.height)

	def adjustPosition(self, distance_x, distance_y):
		self.clearbox()
		self.startPoint = Point(self.startPoint.x + distance_x, self.startPoint.y + distance_y)
		self.endPoint = Point(self.startPoint.x + self.width, self.startPoint.y + self.height)

	def updateWidth(self, newWidth):
		self.width = newWidth
		self.endPoint.x = self.startPoint .x+ newWidth

	def updateHeight(self, newHeight):
		self.height = newHeight
		self.endPoint.y = self.startPoint.y + newHeight

	def clearbox(self):
		for id in self.lines:
			self.canvas.delete(id)
		self.lines = []

	def contains(self, somePoint):
		return (self.startPoint.x <= somePoint.x <= self.endPoint.x) and (self.startPoint.y <= somePoint.y <= self.endPoint.y)

	def withinLRcorner(self, somePoint):
		#print("withinLRCorner, somePoint = "+str(somePoint) +"   end:" + str(self.endPoint))
		return somePoint.x >= self.endPoint.x  - 10 and somePoint.x <= self.endPoint.x and \
		           somePoint.y >= self.endPoint.y - 10 and somePoint.y <= self.endPoint.y

	def calculateOffset(self, somePoint):
		self.offsetX = somePoint.x - self.startPoint.x
		self.offsetY = somePoint.y - self.startPoint.y

	def resize(self, somePoint):
		self.endPoint = somePoint
		self.width = self.endPoint.x - self.startPoint.x
		self.height = self.endPoint.y - self.startPoint.y
		#print("Resizing " + str(self.id) + "   self.width="+str(self.width))

	def makeImage(self):
		s = "$$$$" + "id:" + str(self.id) + " name:" + self.name + " type:" + self.mytype + " "
		s += "start:" + str(self.startPoint.x) + "," + str(self.startPoint.y) + " " + "end:" + str(self.endPoint.x) + "," + str(self.endPoint.y) +  \
		        " label:" + self.label + "\n"
		s += "font:" + self.font + "\n"
		s += "colors: bgcolor:" + self.bgcolor + " fgcolor:" + self.fgcolor + "\n"
		if self.code != "":
			s += "code:" + self.code + "\n"
		if self.myvar != "":
			s += "myvar:" + self.myvar + "\n"
		if self.choices != []:
			s += "choices:" + ";".join(self.choices) + "\n"
		if self.radiogroup != "":
			s += "radiogroup:" + self.radiogroup + "\n"
		if self.scrollbaroptions != "":
			s += "scrollbaroptions:" + self.scrollbaroptions + "\n"
		s += "//end:\n"
		return s

	def writePython(self):
		s = ""
		if self.mytype == "button":
			print("button, self.code = "+self.code)
			s = self.name + " = Button(root, text = \"" + self.label + "\",width=" + str(self.width) +",height=" + str(self.height) 
			s += ",command=" + ("nothing" if self.code == "" else self.code) + ")\n"
		elif self.mytype == "textfield":
			if self.myvar == "":
				self.myvar = self.name + "_var"
			s = self.myvar + "=StringVar()\n"
			s += self.myvar + ".set(\"" + self.label + "\")\n"
			s += self.name + "=Entry(root,width=" + str(self.width) + ",textvariable=" + self.myvar + ")\n"
			if self.code.strip() != "":
				s += self.name + ".bind('<Return>', lambda x: " + self.code + "())\n"
		elif self.mytype == "label":
			s = self.name + " = Label(root,text=\"" + self.label + "\",width=" +  str(self.width) +",height=" + str(self.height)  + ")\n"
		elif self.mytype == "textarea":
			s = self.name + "=ScrolledText(root)\n"
			s += self.name + ".settext(\"\")\n"
		elif self.mytype == "list":
			s += self.makeList()
		elif self.mytype == "choice":
			s += self.makeChoice()
		elif self.mytype == "checkbox":
			s += self.makeCheckbox()
		elif self.mytype == "radiobutton":
			s += self.makeRadiobutton()
		elif self.mytype == "scrollbar":
			s += self.makeScrollbar()
		elif self.mytype == "canvas":
			s += f"{self.name} = Canvas(root, width={self.width}, height={self.height}, bg='{self.bgcolor}')\n"
		s += self.name + ".place(x=" + str(self.startPoint.x) + ",y=" + str(self.startPoint.y) + ",width=" + str(self.width) + ",height=" + str(self.height) + ")\n"
		interposed = ""
		if self.mytype == "textarea": interposed = ".text"
		if self.font == "":
			usefont = ('SansSerif', 10, 'normal')
		else:
			usefont = tuple(self.font.split(" "))
		stringfont = str(usefont)
		if self.mytype != "list" and self.mytype != "canvas":
			s += self.name + interposed + ".config(font=(" + str(usefont) + "))\n"
			s += self.name + interposed + ".config(bg=(\"" + self.bgcolor + "\"))\n"
			s += self.name + interposed + ".config(fg=(\"" + self.fgcolor + "\"))\n"
		return s

	def makeChoice(self):
		s = self.name + " = Menubutton(root,text=\"" + self.label + "\")\n"
		s += self.name + ".menu = Menu(" + self.name + ", tearoff=0)\n"
		s += self.name + "['menu'] = " + self.name + ".menu\n"
		s += self.name + "_varlist=[]\n"
		number = 1
		for thing in self.choices:
			s += f"{self.name}_xvar{number} = IntVar()\n"
			s += f"{self.name}_varlist.append({self.name}_xvar{number})\n"
			s += f"{self.name}.menu.add_checkbutton(label=\"{thing}\", variable={self.name}_xvar{number}, command=functools.partial({self.name}_respond,{number}))\n"
			number += 1
		return s

	def makeChoiceHandler(self):
		s = f"def {self.name}_respond(keycode):\n"
		number = 1
		for thing in self.choices:
			s += f"     if keycode == {number}:\n"
			s += f"          {self.name}.config(text='{thing}')\n"
			s += f"          for thing in {self.name}_varlist:\n"
			s += f"               thing.set(0)\n"
			s += f"          {self.name}_xvar{number}.set({number})\n"
			number += 1
		return s

	def makeCheckbox(self):
		s = f"Button1_var=IntVar()\n"
		s += f"{self.name} = Checkbutton(root,text=\"{self.label}\",variable=Button1_var)\n"
		return s

	def makeList(self):
		s = self.name + " = ScrolledList([], parent=root)\n"
		if self.font == "":
			usefont = ('SansSerif', 10, 'normal')
		else:
			usefont = tuple(self.font.split(" "))
		s += self.name + ".listbox.config(font=(" + str(usefont) + "))\n"
		s += self.name + ".listbox.config(bg=(\"" + self.bgcolor + "\"))\n"
		s += self.name + ".listbox.config(fg=(\"" + self.fgcolor + "\"))\n"
		for item in self.choices:
			s += f"{self.name}.listbox.insert(END,\"{item}\")\n"
		s += self.name + ".listbox.bind(\"<Double-1>\",(lambda event: " + self.name + "_action_code()))\n"
		return s

	def makeListHandler(self):
		s = f"def {self.name}_action_code():\n"
		s += f"     value=getselected({self.name})\n"
		s += "     box.showinfo('title', 'You selected: ' + value)\n"
		return s

	def makeScrollbar(self):
		s = f"{self.name}_var = IntVar()\n"
		s += f"{self.name} = Scale(root,label=\"{self.label}\", variable={self.name}_var, {self.scrollbaroptions})\n"
		s += f"{self.name}.config(bg=root['bg'])\n"
		return s

	def makeRadiobutton(self):
		s = f"{self.name} = Radiobutton(root, text=\"{self.label}\", value=\"{self.label}\", variable={self.radiogroup}, command={self.name}_item_code)\n"
		s += f"{self.radiogroup}.set(\"{self.label}\")\n"
		return s

	def makeRadiobuttonHandler(self):
		s = f"def {self.name}_item_code():\n"
		if self.code.strip() == "": self.code = "nothing"
		s += f"     {self.code}()\n"
		return s

	def alignX(self, someBox, changeWidth):
		self.startPoint = Point(someBox.startPoint.x, self.startPoint.y)
		if changeWidth:
			self.endPoint = Point(self.startPoint.x + someBox.width, self.endPoint.y)
			self.width = someBox.width
		else:
			self.endPoint = Point(self.startPoint.x + self.width, self.endPoint.y)

	def alignY(self, someBox, changeHeight):
		self.startPoint = Point(self.startPoint.x, someBox.startPoint.y)
		if changeHeight:
			self.endPoint = Point(self.endPoint.x, self.startPoint.y + someBox.height)
			self.height = someBox.height
		else:
			self.endPoint = Point(self.endPoint.x, self.startPoint.y + self.height)

	def moveLeft(self, amount):
		self.startPoint = Point(self.startPoint.x - amount, self.startPoint.y)
		self.endPoint = Point(self.endPoint.x - amount, self.endPoint.y)

	def moveUp(self, amount):
		self.startPoint = Point(self.startPoint.x, self.startPoint.y - amount)
		self.endPoint = Point(self.endPoint.x, self.endPoint.y - amount)

	def makeWider(self, amount):
		self.width += amount
		self.endPoint = Point(self.endPoint.x + amount, self.endPoint.y)

	def makeTaller(self, amount):
		self.height += amount
		self.endPoint = Point(self.endPoint.x, self.endPoint.y + amount)

	def copy(oldbox):
		w = MyWidget()
		w.name = "copy_of_" + oldbox.name
		w.mytype = oldbox.mytype
		w.code = oldbox.code
		w.label = oldbox.label
		w.startPoint = oldbox.startPoint
		w.endPoint = oldbox.endPoint
		w.width = oldbox.width
		w.height = oldbox.height
		w.myvar = w.name + "_var"
		w.bgcolor = oldbox.bgcolor
		w.fgcolor = oldbox.fgcolor
		w.font = oldbox.font
		w.canvas = oldbox.canvas
		w.choices = list(oldbox.choices)
		w.radiogroup = oldbox.radiogroup
		w.scrollbaroptions = oldbox.scrollbaroptions
		w.offsetX = oldbox.offsetX
		w.offsetY = oldbox.offsetY
		return w

class Point:
	def __init__(self, x, y):
		self.x = x
		self.y = y
	def __str__(self):
		return f"x={self.x} y={self.y}"

def nothing():
	pass

def kill():
	sys.exit()
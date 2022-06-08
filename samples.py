sample1 = '''#.PYPYGUIM 13;Wed Jun 08, 2022  system:IC-27069
#.$$$documentation
#.This is a very simple first application, showing how buttons
#.cause events.
#.$$$end-documentation
#.$$$options
#.title:Sample1 -- click on a button
#.geom:685x450
#.bgcolor:#c3c3c3
#.$$$end-options
#.$$$code
#.
#.$$$end-code
#.$$$menus
#.
#.$$$end-menus
#.$$$widgets
#.$$$$id::1;;;name::doitB;;;type::button;;;start::212,33;;;end::450,89;;;label::Age next year
#.font::Helvetica 9
#.colors:: bgcolor:#ffffff fgcolor:#000000
#.code::age = int(gettext(ageTF));;;age += 1;;;settext(ageTF,str(age))
#.choices::
#.//end:
#.
#.$$$$id::2;;;name::ageTF;;;type::textfield;;;start::132,38;;;end::186,66;;;label::42
#.font::Helvetica 9
#.colors:: bgcolor:#ffffff fgcolor:#000000
#.myvar::ageTF_var
#.//end:
#.
#.$$$$id::4;;;name::ageL;;;type::label;;;start::61,37;;;end::129,75;;;label::Age:
#.font::Helvetica 12 bold
#.colors:: bgcolor:#c3c3c3 fgcolor:#000000
#.choices::
#.//end:
#.
#.$$$end-widgets
#.$%end
#.END
'''

sample2 = '''#.PYPYGUIM 13;Wed Jun 08, 2022  system:IC-27069
#.$$$documentation
#.This is the same as the first sample, except the code is
#.in a separate method.
#.$$$end-documentation
#.$$$options
#.title:Sample2 -- click on a button
#.geom:685x450
#.bgcolor:#c3c3c3
#.$$$end-options
#.$$$code
#.def ageNextYear():
#.     stringAge = gettext(ageTF)
#.     if stringAge == "":
#.          stringAge = 0
#.     age = int(stringAge)
#.     age += 1
#.     settext(ageTF,str(age))
#.$$$end-code
#.$$$menus
#.
#.$$$end-menus
#.$$$widgets
#.$$$$id::1;;;name::doitB;;;type::button;;;start::188,29;;;end::426,85;;;label::Age next year
#.font::Helvetica 12 bold
#.colors:: bgcolor:#ffffff fgcolor:#000000
#.code::ageNextYear
#.choices::
#.//end:
#.
#.$$$$id::4;;;name::ageL;;;type::label;;;start::50,28;;;end::118,66;;;label::Age:
#.font::Helvetica 12 bold
#.colors:: bgcolor:#c3c3c3 fgcolor:#000000
#.choices::
#.//end:
#.
#.$$$$id::4;;;name::ageTF;;;type::textfield;;;start::122,27;;;end::183,65;;;label::
#.font::Helvetica 12 bold
#.colors:: bgcolor:white fgcolor:black
#.myvar::ageTF_var
#.choices::
#.//end:
#.
#.$$$end-widgets
#.$%end
#.END
'''

sample3 = '''#.PYPYGUIM 13;Wed Jun 08, 2022  system:IC-25965
#.$$$documentation
#.This shows textfields and textareas.
#.$$$end-documentation
#.$$$options
#.title:Sample3 -- textareas and textfields
#.geom:685x450
#.bgcolor:#c3c3c3
#.$$$end-options
#.$$$code
#.def add2List():
#.     newname = gettext(friendNameTF)
#.     oldtext = gettext(friendListTA)
#.     if oldtext == "":
#.           newtext = newname
#.     else:
#.           newtext = oldtext + "\\n" + newname
#.     settext(friendListTA, newtext)
#.     settext(friendNameTF, "")   # clear out for next time
#.
#.def write2File():
#.     text = gettext(friendListTA)
#.     filename = promptForFileSavename("In which file to store this?")
#.     writeFile(filename, text)
#.     
#.$$$end-code
#.$$$menus
#.
#.$$$end-menus
#.$$$widgets
#.$$$$id::1;;;name::addToListb;;;type::button;;;start::519,19;;;end::606,57;;;label::Add
#.font::Helvetica 12 bold
#.colors:: bgcolor:#ffffff fgcolor:#000000
#.code::add2List
#.choices::
#.//end:
#.
#.$$$$id::3;;;name::friendListTA;;;type::textarea;;;start::30,100;;;end::432,330;;;label::
#.font::Helvetica 11
#.colors:: bgcolor:#ffafaf fgcolor:#000000
#.choices::
#.//end:
#.
#.$$$$id::12;;;name::myLabel;;;type::label;;;start::30,22;;;end::202,51;;;label::Your friend's name:
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.choices::
#.//end:
#.
#.$$$$id::13;;;name::friendNameTF;;;type::textfield;;;start::207,20;;;end::512,49;;;label::
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.code::add2List
#.myvar::friendNameTF_var
#.choices::
#.//end:
#.
#.$$$$id::5;;;name::write2FileB;;;type::button;;;start::32,340;;;end::179,366;;;label::Write to file
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.code::write2File
#.choices::
#.//end:
#.
#.$$$end-widgets
#.$%end
#.END
#.
'''

sample4 = '''#.PYPYGUIM 13;Wed Jun 08, 2022  system:IC-25965
#.$$$documentation
#.This illustrates how to use a popup to get a string and then put
#.that into a textfield.
#.$$$end-documentation
#.$$$options
#.title:Sample4 -- using a popup to get a string
#.geom:574x191
#.bgcolor:skyblue
#.$$$end-options
#.$$$code
#.def doit():
#.     name = askforstring("What is your name?")
#.     settext(nameTF, name)
#.$$$end-code
#.$$$menus
#.
#.$$$end-menus
#.$$$widgets
#.$$$$id::1;;;name::askForNameB;;;type::button;;;start::67,48;;;end::181,100;;;label::Ask for name
#.font::Helvetica 12 bold
#.colors:: bgcolor:white fgcolor:black
#.code::doit
#.choices::
#.//end:
#.
#.$$$$id::2;;;name::nameTF;;;type::textfield;;;start::187,49;;;end::457,81;;;label::Example
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.myvar::nameTF_var
#.choices::
#.//end:
#.
#.$$$end-widgets
#.$%end
#.END
'''

sample5 = '''#.PYPYGUIM 13;Wed Jun 08, 2022  system:IC-25965
#.$$$documentation
#.This illustrates how to get a radio button's current value.
#.$$$end-documentation
#.$$$options
#.title:Sample5 -- get radio button's current value
#.geom:685x288
#.bgcolor:white
#.$$$end-options
#.$$$code
#.def doit():
#.     getRBlabel()
#.
#.def getRBlabel():
#.     s = str(mygroup.get())
#.     popup("s="+s)
#.$$$end-code
#.$$$menus
#.
#.$$$end-menus
#.$$$widgets
#.$$$$id::1;;;name::catRB;;;type::radiobutton;;;start::57,63;;;end::247,96;;;label::Cat
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.code::doit
#.choices::
#.radiogroup::mygroup
#.//end:
#.
#.$$$$id::2;;;name::dogRB;;;type::radiobutton;;;start::251,63;;;end::441,96;;;label::Dog
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.code::doit
#.myvar::copy_of_catRB_var
#.choices::
#.radiogroup::mygroup
#.//end:
#.
#.$$$$id::3;;;name::birdRB;;;type::radiobutton;;;start::444,63;;;end::634,96;;;label::Bird
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.code::doit
#.myvar::copy_of_dogRB_var
#.choices::
#.radiogroup::mygroup
#.//end:
#.
#.$$$$id::4;;;name::Button4;;;type::button;;;start::259,143;;;end::434,203;;;label::Which is selected?
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.code::getRBlabel
#.choices::
#.//end:
#.
#.$$$end-widgets
#.$%end
#.END
'''

sample6 = '''#.PYPYGUIM 13;Wed Jun 08, 2022  system:IC-25965
#.$$$documentation
#.This illustrates how to get a selected line from a list widget.
#.$$$end-documentation
#.$$$options
#.title:Sample6 -- Get the selected line from a list widget
#.geom:692x292
#.bgcolor:white
#.$$$end-options
#.$$$code
#.def getSelectedAnimal():
#.     popup(getselected(animalList))
#.$$$end-code
#.$$$menus
#.
#.$$$end-menus
#.$$$widgets
#.$$$$id::1;;;name::animalList;;;type::list;;;start::54,51;;;end::257,218;;;label::Example
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.choices::cat;dog;bird;snake
#.//end:
#.
#.$$$$id::2;;;name::Button2;;;type::button;;;start::287,51;;;end::487,87;;;label::Get selected animal
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.code::getSelectedAnimal
#.choices::
#.//end:
#.
#.$$$end-widgets
#.$%end
#.END
'''

sample7 = '''#.PYPYGUIM 13;Wed Jun 08, 2022  system:IC-25965
#.$$$documentation
#.This illustrates how to respond to menu events.
#.$$$end-documentation
#.$$$options
#.title:Sample7 -- Respond to menu events
#.geom:504x161
#.bgcolor:white
#.$$$end-options
#.$$$code
#.def getAgeNext():
#.     if len(gettext(ageTF)) == 0:
#.          popup("You need to put a number into the age field")
#.          return
#.     age = int(gettext(ageTF))
#.     age += 1
#.     settext(ageTF, str(age))
#.
#.def writeAge():
#.     if len(gettext(ageTF)) == 0:
#.          popup("You need to put a number into the age field")
#.          return
#.     age = int(gettext(ageTF))
#.     settext(writeoutL, numberIntoWords(age))
#.
#.def numberIntoWords(n):
#.     words = "zero,one,two,three,four,five,six,seven,eight,nine,ten,eleven,twelve," 
#.     words += "thirteen,fourteen,fifteen,sixteen,seventeen,eighteen,nineteen"
#.     words = words.split(",")
#.     
#.     if n < 20:
#.         return words[n]
#.
#.     tens = n // 10
#.     digits = n % 10
#.
#.     tensWords = "null,null,twenty,thirty,forty,fifty,sixty,seventy,eighty,ninety".split(",")
#.     digitsWords = "null,one,two,three,four,five,six,seven,eight,nine".split(",")
#.
#.     if digits == 0:
#.          return tensWords[tens]
#.     else:
#.          return tensWords[tens] + "-" + digitsWords[digits]
#.
#.def sayHello():
#.     popup("Hello!")
#.$$$end-code
#.$$$menus
#.Action
#.     Get my age next year&getAgeNext
#.     Write my age out&writeAge
#.     Say hello&sayHello
#.     Exit&kill
#.
#.
#.$$$end-menus
#.$$$widgets
#.$$$$id::1;;;name::Button1;;;type::label;;;start::61,64;;;end::144,93;;;label::Your age:
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.choices::
#.//end:
#.
#.$$$$id::2;;;name::ageTF;;;type::textfield;;;start::147,64;;;end::210,95;;;label::
#.font::Helvetica 9
#.colors:: bgcolor:#ffafaf fgcolor:black
#.myvar::ageTF_var
#.choices::
#.//end:
#.
#.$$$$id::3;;;name::writeoutL;;;type::label;;;start::213,63;;;end::374,96;;;label::
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.choices::
#.//end:
#.
#.$$$end-widgets
#.$%end
#.END
'''

sample8 = '''#.PYPYGUIM 13;Wed Jun 08, 2022  system:IC-25965
#.$$$documentation
#.This illustrates how to respond to the event of pressing ENTER
#.inside a textfield.
#.$$$end-documentation
#.$$$options
#.title:Sample8 -- pressing ENTER in a textfield to trigger an action
#.geom:558x145
#.bgcolor:black
#.$$$end-options
#.$$$code
#.def doit():
#.	popup("hi, " + gettext(nameTF) + "!")
#.$$$end-code
#.$$$menus
#.
#.$$$end-menus
#.$$$widgets
#.$$$$id::1;;;name::nameTF;;;type::textfield;;;start::330,57;;;end::533,95;;;label::
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.code::doit
#.myvar::nameTF_var
#.choices::
#.//end:
#.
#.$$$$id::2;;;name::Button2;;;type::label;;;start::23,10;;;end::523,48;;;label::A very simple example of pressing enter in a textfield
#.font::Helvetica 12 bold
#.colors:: bgcolor:#000000 fgcolor:#ffffff
#.choices::
#.//end:
#.
#.$$$$id::5;;;name::Button5;;;type::label;;;start::133,58;;;end::326,91;;;label::Type your name and press enter:
#.font::Helvetica 10
#.colors:: bgcolor:#000000 fgcolor:#ffffff
#.choices::
#.//end:
#.
#.$$$end-widgets
#.$%end
#.END
'''

sample9 = '''#.PYPYGUIM 13;Wed Jun 08, 2022  system:IC-25965
#.$$$documentation
#.This illustrates all widgets, though it is not a useful application.
#.$$$end-documentation
#.$$$options
#.title:Sample9 -- all widgets example
#.geom:648x474
#.bgcolor:white
#.$$$end-options
#.$$$code
#.def ageNextYear():
#.     age = int(gettext(ageTF))
#.     age += 1
#.     settext(ageTF,str(age))
#.
#.def drawlineonit():
#.    mycanvas.create_line(0,0,200,200)
#.    mycanvas.create_line(200,0,0,200)
#.
#.def post_initialization():
#.     settext(bigTA, "Type something into this big area!")
#.$$$end-code
#.$$$menus
#.
#.$$$end-menus
#.$$$widgets
#.$$$$id::1;;;name::doitB;;;type::button;;;start::159,15;;;end::397,71;;;label::Age next year
#.font::Helvetica 20 bold
#.colors:: bgcolor:#00ff00 fgcolor:#000000
#.code::ageNextYear
#.choices::
#.//end:
#.
#.$$$$id::2;;;name::ageTF;;;type::textfield;;;start::79,20;;;end::133,48;;;label::42
#.font::Helvetica 12 bold
#.colors:: bgcolor:#ffafaf fgcolor:#000000
#.myvar::ageTF_var
#.choices::
#.//end:
#.
#.$$$$id::3;;;name::bigTA;;;type::textarea;;;start::15,88;;;end::338,212;;;label::Example
#.font::Helvetica 9
#.colors:: bgcolor:#000000 fgcolor:#ffffff
#.//end:
#.
#.$$$$id::4;;;name::ageL;;;type::label;;;start::23,20;;;end::72,44;;;label::Age:
#.font::Helvetica 12 bold
#.colors:: bgcolor:#ffffff fgcolor:#000000
#.choices::
#.//end:
#.
#.$$$$id::5;;;name::myScrollbar;;;type::scrollbar;;;start::13,354;;;end::623,436;;;label::Example
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.choices::
#.scrollbaroptions::from_=0, to=100, length=200, tickinterval=5, showvalue=YES, orient='horizontal'
#.//end:
#.
#.$$$$id::6;;;name::mylist;;;type::list;;;start::12,225;;;end::168,347;;;label::Example
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.choices::cat;dog;bird;snake;owl;elephant;hyena;lion;octopus
#.//end:
#.
#.$$$$id::7;;;name::Button7;;;type::label;;;start::173,225;;;end::270,246;;;label::Checkboxes
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.choices::
#.//end:
#.
#.$$$$id::8;;;name::cb1;;;type::checkbox;;;start::173,252;;;end::245,275;;;label::cat
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.choices::
#.//end:
#.
#.$$$$id::9;;;name::cb2;;;type::checkbox;;;start::172,282;;;end::245,304;;;label::dog
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.myvar::copy_of_cb1_var
#.choices::
#.//end:
#.
#.$$$$id::10;;;name::cb3;;;type::checkbox;;;start::173,311;;;end::245,335;;;label::bird
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.myvar::copy_of_cb1_var
#.choices::
#.//end:
#.
#.$$$$id::12;;;name::animalChoiceCH;;;type::choice;;;start::499,228;;;end::643,257;;;label::Animal choices
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.choices::cat;dog;bird;snake
#.//end:
#.
#.$$$$id::13;;;name::copy_of_copy_of_Button7;;;type::label;;;start::315,225;;;end::412,246;;;label::Radio boxes:
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.myvar::copy_of_copy_of_Button7_var
#.choices::
#.//end:
#.
#.$$$$id::14;;;name::catRB;;;type::radiobutton;;;start::314,257;;;end::379,282;;;label::Cat
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.code::nothing
#.choices::
#.radiogroup::group1
#.//end:
#.
#.$$$$id::15;;;name::dogRB;;;type::radiobutton;;;start::313,285;;;end::380,309;;;label::Dog
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.code::nothing
#.myvar::copy_of_catRB_var
#.choices::
#.radiogroup::group1
#.//end:
#.
#.$$$$id::16;;;name::birdRB;;;type::radiobutton;;;start::312,314;;;end::380,337;;;label::Bird
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.code::nothing
#.myvar::copy_of_dogRB_var
#.choices::
#.radiogroup::group1
#.//end:
#.
#.$$$$id::16;;;name::Button16;;;type::label;;;start::409,13;;;end::527,41;;;label::A canvas below:
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.choices::
#.//end:
#.
#.$$$$id::17;;;name::mycanvas;;;type::canvas;;;start::410,48;;;end::643,210;;;label::Example
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.choices::
#.//end:
#.
#.$$$$id::18;;;name::Button18;;;type::button;;;start::532,11;;;end::641,38;;;label::Draw line on it
#.font::Helvetica 9
#.colors:: bgcolor:white fgcolor:black
#.code::drawlineonit
#.choices::
#.//end:
#.
#.$$$end-widgets
#.$%end
#.END
'''


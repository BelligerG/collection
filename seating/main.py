from kivy.app import App
from kivy.uix.behaviors import DragBehavior
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.factory import Factory
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.uix.scatter import Scatter
from random import randrange


#Current issues:
#	check out https://www.youtube.com/watch?v=JA_qTwpXdcE seems to have a lot of useable code for dragging and selecting...
#	Dragging - no bounding box currently
#	Add scroll bar?  - zoom function required
#	Remove desks by clicking on them
#	Rework - make it prettier

#Possible idea for seating plan image: http://stackoverflow.com/questions/36600993/how-to-save-a-kivy-canvas-object-as-an-image-file

#Completed 1/5/17
#Fixed Update students - show students in text box
#	- allow creation and deletion of students
#	- check the go back button too

#Completed 1/6/17
#Allowed for random student positions - both initially and on request

#Completed 1/8/17
#Allowed information to be added for each student

#Next time
#Full screen permanently?
#Make students always on top
#Make it more user friendly

#Known BUGS/Things to correct:
# Check Desk numbering system
# Labels for information
# Hint text disappears when setting Information (could be sorted by using labels as hint text becomes irrelevant)
# When loading a new factory version of the class, it doesnt remove the old one from memory?


#Custom class based on DragBehaviour and Label kivy classes, so needs both
class Desk(DragBehavior, Label):
	pass

class SaveBox(BoxLayout):

	fileName = ObjectProperty()

	def saveFile(self, fileName):
		fileName = fileName+".SSplan"
		fout = open(fileName, 'w')
		for desk in currentDeskPositions:
			fout.write("%s, %s, %s\n" % (desk[0], desk[1][0], desk[1][1]))
		#Updated! Now writes the students full names at the end of the line - looks nicer when adding student details etc..
		posCounter=0
		for student in currentStudentPositions:
			PP = ""
			SEN = ""
			MED = ""
			ATT = ""
			try:
				for information in Info:
					if currentStudents.split("\n")[posCounter] in information:
						Name, PP, MED, SEN, ATT = information
			except NameError:
				pass
			fout.write("%s, %s, %s, \"%s\" %s %s %s %s\n" % (student[0], student[1][0], student[1][1], currentStudents.split("\n")[posCounter], PP, MED, SEN, ATT))
			posCounter+=1
		fout.close()
		self.goBack()

	def goBack(self):
		self.clear_widgets()
		seatingPlanInstance = Factory.SeatingPlanRoot()
		self.add_widget(seatingPlanInstance)
		SeatingPlanRoot.putDesksBack(seatingPlanInstance)
		SeatingPlanRoot.replaceStudents(seatingPlanInstance)


class SaveClassroomLayoutScreen(BoxLayout):

	fileName = ObjectProperty()

	def saveFile(self, fileName):
		fileName = fileName+".SSlayout"
		fout = open(fileName, 'w')
		for desk in currentDeskPositions:
			fout.write("%s, %s, %s\n" % (desk[0], desk[1][0], desk[1][1]))
		fout.close()
		self.goBack()

	def goBack(self):
		self.clear_widgets()
		seatingPlanInstance = Factory.SeatingPlanRoot()
		self.add_widget(seatingPlanInstance)
		SeatingPlanRoot.putDesksBack(seatingPlanInstance)
		SeatingPlanRoot.replaceStudents(seatingPlanInstance)

class LoadBox(BoxLayout):

	fileName = ObjectProperty()

	def loadFile(self, fileName):
		global currentDeskPositions
		currentDeskPositions = []
		global currentStudentPositions
		currentStudentPositions = []
		global currentStudents
		global Info
		Info = []

		students=""

		
		fileName = fileName+".SSplan"
		try:
			fin = open(fileName, 'r').readlines()

			for line in fin:
				line = line.strip()
				if "Desk" in line.split()[0]:
					position = []
					x = line.split()[1].strip(",")
					y = line.split()[2]
					position.append(x)
					position.append(y)

					deskInfo = []
					deskInfo.append(line.split()[0].strip(","))
					deskInfo.append(position)

					currentDeskPositions.append(deskInfo)

				if "Student" in line.split()[0]:
					position = []
					x = line.split()[1].strip(",")
					try:
						y = line.split()[2].strip(",")
					except:
						y = line.split()[2]
					position.append(x)
					position.append(y)

					studentInfo = []
					studentInfo.append(line.split()[0].strip(","))
					studentInfo.append(position)

					currentStudentPositions.append(studentInfo)

					line = line[8:]
					try:
						int(line[0])
						line = line[1:]
					except ValueError:
						pass

				#New file format has the student's whole name at the end of the file - this loads the name and saves it
					if "\"" in line:
						lineStudent = line.split()[3].strip("\"")+" "+line.split()[4].strip("\"")
						students = students+str(lineStudent)+"\n"

						try:
							PP=line.split()[5]
							SEN=line.split()[6]
							MED=line.split()[7]
							ATT=line.split()[8]
							EAL=line.split()[9]
						except IndexError:
							PP=""
							SEN=""
							MED=""
							ATT=""
							EAL=""

						studentInformation = [line.split()[3].strip("\"")+" "+line.split()[4].strip("\""), PP, SEN, MED, ATT, EAL]
				#This is for the original format, with no full names etc...
					else:
						line = line.split()[0].strip(",")
						students = students+str(line[-1])+", "+str(line[:-1]+"\n")
				try:
					Info.append(studentInformation)
				except UnboundLocalError:
					pass


			currentStudents=students

			self.goBack()
		except FileNotFoundError:
			pass


	def goBack(self):
		self.clear_widgets()
		seatingPlanInstance = Factory.SeatingPlanRoot()
		self.add_widget(seatingPlanInstance)
		SeatingPlanRoot.putDesksBack(seatingPlanInstance)
		SeatingPlanRoot.replaceStudents(seatingPlanInstance)


class LoadClassroomLayoutScreen(BoxLayout):

	fileName = ObjectProperty()

	def loadFile(self, fileName):
		global currentDeskPositions
		currentDeskPositions = []

		students=""

		fileName = fileName+".SSLayout"
		try:
			fin = open(fileName, 'r').readlines()

			for line in fin:
				line = line.strip()
				if "Desk" in line.split()[0]:
					position = []
					x = line.split()[1].strip(",")
					y = line.split()[2]
					position.append(x)
					position.append(y)

					deskInfo = []
					deskInfo.append(line.split()[0].strip(","))
					deskInfo.append(position)

					currentDeskPositions.append(deskInfo)

			self.goBack()

		except FileNotFoundError:
			pass

	


	def goBack(self):
		self.clear_widgets()
		seatingPlanInstance = Factory.SeatingPlanRoot()
		self.add_widget(seatingPlanInstance)
		SeatingPlanRoot.putDesksBack(seatingPlanInstance)
		SeatingPlanRoot.replaceStudents(seatingPlanInstance)


class Student(DragBehavior, Label):
	pass

class StudentTeacher(DragBehavior, Label):
	pass

class ManageStudentsScreen(BoxLayout):

	studentList = ObjectProperty()
	students = StringProperty()
	studentsHintText = StringProperty()

	#Adds in the text list of the students
	def __init__(self, **kwargs):
		super(ManageStudentsScreen, self).__init__(**kwargs)
		try:
			self.students = currentStudents
			self.studentsHintText = ""
		except NameError:
			self.students = ""
			self.studentsHintText = "Enter student's names here"

	def updateStudents(self, studentList):
		global currentStudents
		currentStudents = studentList

		#Puts the previous student list into "Chris S" format, for comparison with new student list
		previousStudentList = []
		for student in currentStudentPositions:
			student = student[0][8:]
			try:
				int(student[0])
				student = student[1:]

			except ValueError:
				pass
			previousStudentList.append(student)

		currentStudentsList = []

		#Gets rid of empty strings at the end
		if len(currentStudents)!=0:
			while currentStudents.split("\n")[-1] == "":
				currentStudents = currentStudents[:-1]

		#Only updates if not the first time adding students in
		if len(currentStudentPositions)!=0:
			for student in currentStudents.split("\n"):
				student = student.split(" ")
				try:
					student = student[1]+student[0][0]
				except IndexError:
					pass
				currentStudentsList.append(student)

			for student in currentStudentsList:
				if student in previousStudentList:
					pass

				else:
					#Adds in new students
					previousStudentList.append(student)
					studentDetail=[]
					student="Student"+str(len(previousStudentList)+1)+student
					studentDetail.append(student)
					studentDetail.append([0, 0])
					currentStudentPositions.append(studentDetail)

			#Allows for the deletion of students, just by deleting their name
			for student in previousStudentList:
				if student in currentStudentsList:
					pass
				else:
					for i in currentStudentPositions:
						if str(student) in str(i[0]):
							currentStudentPositions.remove(i)

		self.clear_widgets()
		seatingPlanInstance = Factory.SeatingPlanRoot()
		self.add_widget(seatingPlanInstance)
		SeatingPlanRoot.putDesksBack(seatingPlanInstance)
		if len(currentStudentPositions) == 0:
			SeatingPlanRoot.addStudents(seatingPlanInstance)
		elif len(currentStudentPositions) > 0:
			SeatingPlanRoot.replaceStudents(seatingPlanInstance)


	def goBack(self):
		self.clear_widgets()
		seatingPlanInstance = Factory.SeatingPlanRoot()
		self.add_widget(seatingPlanInstance)
		SeatingPlanRoot.putDesksBack(seatingPlanInstance)
		SeatingPlanRoot.replaceStudents(seatingPlanInstance)



class AddStudentDetails(BoxLayout):

	PPText = StringProperty()
	SENText = StringProperty()
	MEDText = StringProperty()
	ATTText = StringProperty()
	EALText = StringProperty()
	students = StringProperty()
	PPList = ObjectProperty()
	SENList = ObjectProperty()
	MEDList = ObjectProperty()
	ATTList = ObjectProperty()
	EALList = ObjectProperty()

	def __init__(self, **kwargs):
		super(AddStudentDetails, self).__init__(**kwargs)
		self.PPText = ""
		self.SENText = ""
		self.MEDText = ""
		self.ATTText = ""
		self.EALText = ""
		self.students = currentStudents
		try:
			#Loop within a loop, so trial number shows if we've been all through the students and not found their name
			trialNumber = 0
			for student in self.students.split("\n"):
				for information in Info:
					if student in information:
						self.PPText=self.PPText + str(information[1]) + "\n"
						self.SENText=self.SENText + str(information[2]) + "\n"
						self.MEDText=self.MEDText + str(information[3]) + "\n"
						self.ATTText=self.ATTText + str(information[4]) + "\n"
						self.EALText=self.EALText + str(information[4]) + "\n"
						trialNumber=1
				if trialNumber==0:
					self.PPText=self.PPText + "\n"
					self.SENText=self.SENText + "\n"
					self.MEDText=self.MEDText + "\n"
					self.ATTText=self.ATTText + "\n"
					self.EALText=self.EALText + "\n"
				trialNumber=0
		except:
			pass


	def studentInfo(self, PPList, SENList, MEDList, ATTList, EALList):

		global Info

		#gets rid of blank space at the end of the list
		if len(self.students)!=0:
			while self.students.split("\n")[-1] == "":
				self.students = self.students[:-1]

		#Creates a list the same length as the number of students
		Info = [[] for i in range(len(self.students.split("\n")))]

		PPList=PPList.split("\n")
		SENList=SENList.split("\n")
		MEDList=MEDList.split("\n")
		ATTList=ATTList.split("\n")
		EALList=EALList.split("\n")
		for i in range(len(self.students.split("\n"))):
			#If no PP value exists, assume they're not PP
			try:
				PPValue = PPList[i]
				if PPList[i] != "Y":
					PPValue = "N"
			except IndexError:
				PPValue = "N"
			try:
				SENValue = SENList[i]
				if SENList[i] == "":
					SENValue = "N"
			except IndexError:
				SENValue = "N"
			try:
				MEDValue = MEDList[i]
				if MEDList[i] == "":
					MEDValue = "N"
			except IndexError:
				MEDValue = "N"
			try:
				ATTValue = ATTList[i]
				if ATTList[i] == "":
					ATTValue = "N"
			except IndexError:
				ATTValue = "N"
			try:
				EALValue = EALList[i]
				if EALList[i] == "":
					EALValue = "N"
			except IndexError:
				EALValue = "N"
			#Creates a list of the format [Name, PP]
			Info[i].append(self.students.split("\n")[i])
			Info[i].append(PPValue)
			Info[i].append(SENValue)
			Info[i].append(MEDValue)
			Info[i].append(ATTValue)
			Info[i].append(EALValue)

		#print(Info)


		self.clear_widgets()
		seatingPlanInstance = Factory.SeatingPlanRoot()
		self.add_widget(seatingPlanInstance)
		SeatingPlanRoot.putDesksBack(seatingPlanInstance)
		SeatingPlanRoot.replaceStudents(seatingPlanInstance)

	def goBack(self):
		self.clear_widgets()
		seatingPlanInstance = Factory.SeatingPlanRoot()
		self.add_widget(seatingPlanInstance)
		SeatingPlanRoot.putDesksBack(seatingPlanInstance)
		SeatingPlanRoot.replaceStudents(seatingPlanInstance)

		
#Custom class root, should allow me to change the screens as and when required
class SeatingPlanRoot(FloatLayout):




	def __init__(self, **kwargs):
		super(SeatingPlanRoot, self).__init__(**kwargs)

		try:
			#Changes the colour of the student/teacher buttons depending on what was clicked last.
			if view == "student":
				self.StudentButtonColourR = 0.0
				self.StudentButtonColourG = 0.7
				self.StudentButtonColourB = 1.0
				self.TeacherButtonColourR = 0.8
				self.TeacherButtonColourG = 0.8
				self.TeacherButtonColourB = 0.8
			elif view == "teacher":
				self.StudentButtonColourR = 0.8
				self.StudentButtonColourG = 0.8
				self.StudentButtonColourB = 0.8
				self.TeacherButtonColourR = 0.0
				self.TeacherButtonColourG = 0.7
				self.TeacherButtonColourB = 1.0
			#Default is students view
		except NameError:
			self.StudentButtonColourR = 0.0
			self.StudentButtonColourG = 0.7
			self.StudentButtonColourB = 1.0
			self.TeacherButtonColourR = 0.8
			self.TeacherButtonColourG = 0.8
			self.TeacherButtonColourB = 0.8


	DeskCounter=0
	desk_positions=[]
	StudentCounter=0

	StudentButtonColourR = NumericProperty()
	StudentButtonColourG = NumericProperty()
	StudentButtonColourB = NumericProperty()
	
	TeacherButtonColourR = NumericProperty()
	TeacherButtonColourG = NumericProperty()
	TeacherButtonColourB = NumericProperty()



	def putDesksBack(self):
		for desk in currentDeskPositions:
				self.add_widget(Desk(id=desk[0], pos=(desk[1][0], desk[1][1])))

	def addStudents(self):
		#Very clunky positioning... have given it the absolute values, this could be an issue when using different screen sizes
		xPosition = 350
		yPosition = 0

		positions = (self.randomPositions())

		#Updates the students initially, need to fix positions
		for student in currentStudents.split("\n"):
		#Assumes format "Surname firstname" to have the format eg Chris S
			try:
			#Takes into account spaces at the end of the file - would otherwise cause an error
				studentName = student.split(" ")[1]+student.split(" ")[0][0]
				student = student.split(" ")[1]+" "+student.split(" ")[0][0]
				#print(self, self.width)
				if len(positions)>0:
					value = positions.pop()
					x=value[0]+38
					y=value[1]+38
					self.add_widget(Student(text="[color=000000]%s[/color]" % (student), markup=True, id="Student"+str(self.StudentCounter)+studentName, pos=[x, y]))
				else:
					self.add_widget(Student(text="[color=000000]%s[/color]" % (student), markup=True, id="Student"+str(self.StudentCounter)+studentName, pos=[xPosition, yPosition]))
				self.StudentCounter+=1

				yPosition += 15

				if self.StudentCounter % 10==0:
					xPosition += 100
					yPosition = 0
			except IndexError:
				pass

	def randomPositions(self):
		deskPos = currentDeskPositions
		#get list of current Desk positions
		randomPos=[]
		
		while len(deskPos) > 0:
			randomPos.append(deskPos.pop(randrange(len(deskPos))))
		
		for desk in randomPos:
			deskPos.append(desk[1])

		return deskPos

	def detailsToPrint(self, studentName):
		for information in Info:
			if str(information[0].split()[-1]+information[0].split()[0][0]) in studentName:
				PP, SEN, MED, ATT, EAL = information[1:6]

				if PP == "N":
					PP = ""
				elif PP == "Y":
					PP = "PP"
				if SEN == "N":
					SEN = ""
				if MED != "N":
					MED="MED"
				else:
					MED = ""
				if ATT == "N":
					ATT = ""
				if EAL == "N":
					EAL = ""
				elif EAL == "Y":
					EAL = "EAL"



		return (PP, SEN, MED, ATT, EAL)

	def replaceStudents(self):
		for student in currentStudentPositions:
			try:
				if view == "student":
			#Finds if the desk is single or double digits
					Digit=False
					try:
						int(student[0][8])
						Digit=True
					except ValueError:
						Digit=False
					if Digit==True:
						self.add_widget(Student(text="[color=000000]%s %s[/color]" % (student[0][9:-1], student[0][-1]), markup=True, id=student[0], pos=(student[1][0], student[1][1])))
					else:
						self.add_widget(Student(text="[color=000000]%s %s[/color]" % (student[0][8:-1], student[0][-1]), markup=True, id=student[0], pos=(student[1][0], student[1][1])))
				elif view == "teacher":
					(PP, SEN, MED, ATT, EAL) = self.detailsToPrint(student[0])

					Digit=False
					try:
						int(student[0][8])
						Digit=True
					except ValueError:
						Digit=False
					if Digit==True:
						self.add_widget(Student(text="[color=000000]%s %s[/color]\n[color=ffa500][i]%s[/color][color=000000] %s [/color][color=ff0000] %s[/color][color=00ff00] %s[/color][color=ee82ee] %s[/i][/color]" % (student[0][9:-1], student[0][-1], PP, SEN, MED, ATT, EAL), markup=True, id=student[0], pos=(student[1][0], student[1][1])))
					else:
						self.add_widget(Student(text="[color=000000]%s %s[/color]\n[i][color=ffa500][i]%s[/color][color=000000] %s [/color][color=ff0000]%s[/color][color=00ff00] %s[/color][color=ee82ee] %s[/i][/color]" % (student[0][8:-1], student[0][-1], PP, SEN, MED, ATT, EAL), markup=True, id=student[0], pos=(student[1][0], student[1][1])))
			except NameError:
				Digit=False
				try:
					int(student[0][8])
					Digit=True
				except ValueError:
					Digit=False
				if Digit==True:
					self.add_widget(Student(text="[color=000000]%s %s[/color]" % (student[0][9:-1], student[0][-1]), markup=True, id=student[0], pos=(student[1][0], student[1][1])))
				else:
					self.add_widget(Student(text="[color=000000]%s %s[/color]" % (student[0][8:-1], student[0][-1]), markup=True, id=student[0], pos=(student[1][0], student[1][1])))

	def addTable(self):
		deskID = "Desk"+str(self.DeskCounter)
		self.add_widget(Desk(id=deskID))
		self.DeskCounter+=1

	def removeTable(self):
		children = self.children[:]

		while children:
			child = children.pop()

			#Possible bug needs testing - what happens if desk is in double digits?
			if str(child.id)[:-1]=="Desk":
				lastDesk=child
		try:
			self.remove_widget(lastDesk)
		except: 
			pass

	def manageStudents(self):
		#has a list of desks and positions, needs to save it somewhere though
		global currentDeskPositions
		currentDeskPositions = self.findDeskPositions()
		global currentStudentPositions
		currentStudentPositions = self.findStudentPositions()
		self.clear_widgets()
		self.add_widget(ManageStudentsScreen())		

	def saveClassroomLayout(self):
		global currentDeskPositions
		currentDeskPositions = self.findDeskPositions()
		global currentStudentPositions
		currentStudentPositions = self.findStudentPositions()
		self.clear_widgets()
		self.add_widget(SaveClassroomLayoutScreen())

	def loadClassroomLayout(self):
		global currentDeskPositions
		currentDeskPositions = self.findDeskPositions()
		global currentStudentPositions
		currentStudentPositions = self.findStudentPositions()
		self.clear_widgets()
		self.add_widget(LoadClassroomLayoutScreen())

	def findDeskPositions(self):
		"""Finds all the children's ids"""
		#print(self.children)
		childrenList=[]
		children = self.children[:]
		while children:
			childList=[]
			child = children.pop()
			#print(child.id)
			#children.extend(child.children)

			if str(child.id)[:-1]=="Desk":
				childList.append(child.id)
				childList.append(child.pos)
				childrenList.append(childList)
			elif str(child.id)[:-2]=="Desk":
				childList.append(child.id)
				childList.append(child.pos)
				childrenList.append(childList)

		return childrenList

	def findStudentPositions(self):
		"""Finds all the children's ids"""
		#print(self.children)
		childrenList=[]
		children = self.children[:]
		while children:
			childList=[]
			child = children.pop()
			#print(child.id)
			#children.extend(child.children)

			if str(child.id)[:7]=="Student":
				childList.append(child.id)
				childList.append(child.pos)
				childrenList.append(childList)

		return childrenList

	def randomAssignPositions(self):
		global currentDeskPositions
		currentDeskPositions = self.findDeskPositions()


		xPosition = 350
		yPosition = 0

		positions = self.randomPositions()
		students = []
		children = self.children[:]

		while children:
			child = children.pop()

			if str(child.id)[:7]=="Student":
				students.append(child)
				self.remove_widget(child)

		for student in students:
			try:
			#Takes into account spaces at the end of the file - would otherwise cause an error
				studentName = student.id
				student = str(student.id[8:-1]+" "+student.id[-1])
				#Gets rid of additional digit (if 2 digits, e.g. student11)
				try:
					int(student[0])
					student = student[1:]

				except ValueError:
					pass

				try:
					if view == "student":
						if len(positions)>0:
							value = positions.pop()
							x=value[0]+38
							y=value[1]+38
							self.add_widget(Student(text="[color=000000]%s[/color]" % (student), markup=True, id=studentName, pos=[x, y]))
						else:
							self.add_widget(Student(text="[color=000000]%s[/color]" % (student), markup=True, id=studentName, pos=[xPosition, yPosition]))
						self.StudentCounter+=1

						yPosition += 15

						if self.StudentCounter % 10==0:
							xPosition += 100
							yPosition = 0
					elif view == "teacher":

						(PP, SEN, MED, ATT, EAL) = self.detailsToPrint(student.split()[0]+student.split()[1])

						if len(positions)>0:
							value = positions.pop()
							x=value[0]+38
							y=value[1]+38
							self.add_widget(Student(text="[color=000000]%s[/color]\n[color=ffa500][i]%s[/color][color=000000] %s[/color][color=ff0000] %s[/color][color=00ff00] %s[/color][color=ee82ee] %s[/i][/color]" % (student, PP, SEN, MED, ATT, EAL), markup=True, id=studentName, pos=[x, y]))
						else:
							self.add_widget(Student(text="[color=000000]%s[/color]\n[color=ffa500][i]%s[/color][color=000000] %s[/color][color=ff0000] %s[/color][color=00ff00] %s[/color][color=ee82ee] %s[/i][/color]" % (student, PP, SEN, MED, ATT, EAL), markup=True, id=studentName, pos=[xPosition, yPosition]))
						self.StudentCounter+=1

						yPosition += 15

						if self.StudentCounter % 10==0:
							xPosition += 100
							yPosition = 0
				except NameError:
					if len(positions)>0:
						value = positions.pop()
						x=value[0]+38
						y=value[1]+38
						self.add_widget(Student(text="[color=000000]%s[/color]" % (student), markup=True, id=studentName, pos=[x, y]))
					else:
						self.add_widget(Student(text="[color=000000]%s[/color]" % (student), markup=True, id=studentName, pos=[xPosition, yPosition]))
					self.StudentCounter+=1

					yPosition += 15

					if self.StudentCounter % 10==0:
						xPosition += 100
						yPosition = 0
			except IndexError:
				pass

	def saveFullSeatingPlan(self):
		#make a custom widget
		#save file

		global currentDeskPositions
		currentDeskPositions = self.findDeskPositions()
		global currentStudentPositions
		currentStudentPositions = self.findStudentPositions()
		self.clear_widgets()
		self.add_widget(SaveBox(id="saveBox"))

	def loadFullSeatingPlan(self):
		global currentDeskPositions
		currentDeskPositions = self.findDeskPositions()
		global currentStudentPositions
		currentStudentPositions = self.findStudentPositions()
		self.clear_widgets()
		self.add_widget(LoadBox(id="loadBox"))

	def addDetails(self):
		try:
			#Only completes if there are current students, otherwise clicking the button does nothing
			currentStudents
			global currentDeskPositions
			currentDeskPositions = self.findDeskPositions()
			global currentStudentPositions
			currentStudentPositions = self.findStudentPositions()
			self.clear_widgets()
			self.add_widget(AddStudentDetails())
		except NameError:
			pass

	def teacherView(self):
		global view

		view = "teacher"

		global currentDeskPositions
		currentDeskPositions = self.findDeskPositions()
		global currentStudentPositions
		currentStudentPositions = self.findStudentPositions()
		self.clear_widgets()
		seatingPlanInstance = Factory.SeatingPlanRoot()
		self.add_widget(seatingPlanInstance)
		SeatingPlanRoot.putDesksBack(seatingPlanInstance)
		SeatingPlanRoot.replaceStudents(seatingPlanInstance)

	def studentView(self):
		global view

		view = "student"

		global currentDeskPositions
		currentDeskPositions = self.findDeskPositions()
		global currentStudentPositions
		currentStudentPositions = self.findStudentPositions()
		self.clear_widgets()
		seatingPlanInstance = Factory.SeatingPlanRoot()
		self.add_widget(seatingPlanInstance)
		SeatingPlanRoot.putDesksBack(seatingPlanInstance)
		SeatingPlanRoot.replaceStudents(seatingPlanInstance)
		

#Custom Button class, put all functions for buttons here?
class CustomButton(Button):
	pass

#Passing the App class from kivy to actually show a gui
class SampsonSeatingApp(App):
	pass


if __name__=="__main__":
	SampsonSeatingApp().run()
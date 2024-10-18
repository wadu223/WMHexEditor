

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import tkinter.scrolledtext as st 
from math import log2

class betterText (Text):
	def __init__(self, parent, **kwargs):
		self.cursor = "1.0"
		super().__init__(parent, **kwargs)
		self.sibling = None
		self.tag_add("bold", "1.0")
		
	def gotoStart(self):
		self.cursor = "1.0"
		self.moveCursor("+0c")

	def moveCursor(self, next:str, idk=False):
		if(idk):
			self.cursor = self.index(next)
		else:
			self.cursor = self.index(self.cursor + next)
		if self.get(self.cursor) == " ":
			self.cursor = self.index(self.cursor + "+1c")
		if self.get(self.cursor) == "\n":
			self.cursor = self.index(self.cursor + "+1 lines linestart")
		self.tag_delete("bold")
		self.tag_add("bold", index1=self.cursor)
		self.tag_config("bold", foreground="red")

	def typeDaLetter(self, letter):
		self.config(state=NORMAL)
		self.delete(self.cursor)
		self.insert(self.cursor, KLUT[letter])

		self.sibling.delete(self.getLineNumber()+".0", self.getLineNumber()+".end +1c")
		self.sibling.insert(self.getLineNumber()+".0", toASCII(self.getLine()))

		self.config(state=DISABLED)
		self.moveCursor("+1c")
	
	def setSibling(self, sibling:Text):
		self.sibling = sibling

	def getLine(self):
		return(self.get(self.cursor + " linestart", self.cursor + " lineend"))

	
	def getLineNumber(self):
		return((self.cursor.split('.'))[0])
	
		

ALUT = {40:"+1 lines", 37:"-1c", 39:"+1c", 38:"-1 lines"}

KLUT= {
    48: "0",
    49: "1",
    50: "2",
    51: "3",
    52: "4",
    53: "5",
    54: "6",
    55: "7",
    56: "8",
    57: "9",
    65: "A",
    66: "B",
    67: "C",
    68: "D",
    69: "E",
    70: "F",
	96: "0",
    97: "1",
    98: "2",
    99: "3",
    100: "4",
    101: "5",
    102: "6",
    103: "7",
    104: "8",
    105: "9",
}

BLUT = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'A':10,'B':11,'C':12,'D':13,'E':14,'F':15}

def ceil(n:int):
	return (n >> 4) + ((n&15)!=0)

def lb1_control(start, end):
	'''
	user uses listbox1 to scroll, so
	- set the scrollbar position
	- set the listbox2 position
	'''
	scrollbar.set(start, end)
	BTB.yview('moveto', start)
	lineNumbers.yview('moveto', start)

def lb2_control(start, end):
	'''user scrolled via listbox 2'''
	scrollbar.set(start, end)
	TTB.yview('moveto', start)
	lineNumbers.yview('moveto', start)

def lb3_control(start, end):
	scrollbar.set(start,end)
	TTB.yview('moveto', start)
	BTB.yview('moveto', start)

def splitString(numbers):
	j = 0
	hugestringtoholdanswer = ""
	for i in numbers:
		if i < 32:
			i = 0x2e
		i = chr(i)
		hugestringtoholdanswer+=i
		j = j+1&15
		if j == 0:
			hugestringtoholdanswer+="\n"
	return(hugestringtoholdanswer)

def toHex(text):
	convet = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
	bigstringtoholdanswer = ""
	i = 0
	for n in text:
		bigstringtoholdanswer+=convet[(n&0b11110000) >> 4]
		bigstringtoholdanswer+=convet[n&0b00001111]
		bigstringtoholdanswer+=" "
		i = i+1&15
		if i == 0:
			bigstringtoholdanswer+="\n"
	return(bigstringtoholdanswer)

def toBytes(text):
	i = 0
	veryGiantArraytostoreanswer = []
	while i < len(text):
		byte = (BLUT[text[i]] << 4) | (BLUT[text[i+1]])
		veryGiantArraytostoreanswer.append(byte)
		i+=2
	
	return(veryGiantArraytostoreanswer)

def getLineNumbers(size):
	lineNum = ''
	ln = 0x0
	size2 = size
	size = ceil(size)
	size3 = int(log2(size2-1)/4)+1
	lineNumbers.config(width=size3)
	for i in range(size):	
		ln = hex(i)[2:]
		lineNum += str(ln).rjust(int(log2(size2-1)/4),'0').upper()
		lineNum += "\n"
	lineNum = lineNum[0:-1]
	return(lineNum)

def browseFiles():
	filename = filedialog.askopenfilename(title = "Select a File")
	if(not filename):
		return
	binary = open(file=filename, mode="r+b")
	text = binary.read(-1)
	lineNumbers.config(state='normal')
	TTB.config(state='normal')
	
	TTB.delete('1.0', END)
	BTB.delete('1.0', END)
	lineNumbers.delete('1.0', END)
	TTB.insert('end', toHex(text))
	BTB.insert('end', splitString(text))
	lineNumbers.insert('end', getLineNumbers(len(text)))

	lineNumbers.config(state=DISABLED)
	TTB.config(state=DISABLED)
	TTB.gotoStart()
	binary.close()

def multiple_yview(*args):
	TTB.yview(*args)
	BTB.yview(*args)
	lineNumbers.yview(*args)

def saveFile():
	path = filedialog.asksaveasfilename(title= "Save as")
	if(not path):
		return
	file = open(path, mode='wb')
	text = TTB.get('1.0', END)
	text = ''.join(text.split('\n'))
	text = ''.join(text.split(' '))
	file.write(bytearray(toBytes(text)))
	
def toASCII(text:str):
#	breakpoint()
	return(splitString(toBytes(text=text.replace(" ", ""))))


def keyHandle(event:Event):
	letter = event.keycode
	print(letter)
	if letter in KLUT:
		TTB.typeDaLetter(letter=letter)
	if letter in ALUT:
		TTB.moveCursor(ALUT[letter])
	

def mouseHandle(event:Event):
	TTB.moveCursor("current", True)

	


root = Tk()
TextBoxFrame = Frame(root)
ribbon = Frame(root)

ribbon.pack(expand=True,fill=X)
TextBoxFrame.pack(expand=True, fill=BOTH)

scrollbar = Scrollbar(TextBoxFrame)

TTB = betterText(TextBoxFrame, font='Courier 10', yscrollcommand=lb1_control, state=DISABLED)
BTB = betterText(TextBoxFrame, font='Courier 10', yscrollcommand=lb2_control)
lineNumbers = Text(TextBoxFrame, font='Courier 10', yscrollcommand=lb3_control, bg = 'gray', width=1, state=DISABLED)
TTB.setSibling(BTB)

scrollbar.grid(row=0,column=3, sticky=NS)
lineNumbers.grid(row=0,column=0, sticky=NS)
TTB.grid(row=0,column=1, sticky=NS)
BTB.grid(row=0,column=2, sticky=NS)
scrollbar.config(command=multiple_yview)

file = Menubutton(ribbon, text="File")
options = Menubutton(ribbon, text="Options")
file.grid(row=0, column=0, sticky=W)
options.grid(row=0, column=1, sticky=W)

fMenu = Menu(file, tearoff=False)
fMenu.add_command(command=browseFiles, label="Open")
fMenu.add_command(command=saveFile, label="Save As")

file.config(menu=fMenu)

TTB.bind("<KeyPress>", keyHandle)
TTB.bind("<Button>", mouseHandle)

root.mainloop()
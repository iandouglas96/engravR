#!/usr/bin/env python

#	Remote GUI Interface for Rapsberry Pi Laser Engraver
#	Ian D. Miller
#	Jan 7, 2014
#	http://www.pxlweavr.com
#	info [at] pxlweavr.com

#pexpect required
import pexpect
import Tkinter, tkFileDialog, tkMessageBox
from os import path

file_opt = options = {}
options['defaultextension'] = '.txt'
options['filetypes'] = [('all files', '.*'), ('gcode files', '.ngc')]
options['initialdir'] = '~'
options['title'] = 'Choose file to engrave'

ssh_newkey = "Are you sure you want to continue connecting"

#User set variables
remdir = "/home/pi/engravingfiles/"
address = "raspberrypi.local" #This will be an IP address if avahi-daemon is not installed (which I strongly reccommend
user = "pi"
password = "your-password-here"

#Also, laserengraver must be in the $PATH variable on the pi

filepath = "/"
filename = "."

def getpath():
    global filepath
    global filename
    filepath = tkFileDialog.askopenfilename(**file_opt)
    filename = path.basename(filepath)
    pathtext.set(filepath)

def sshcmd(cmd): #Automates sending of ssh commands to pi.
	print cmd
	p=pexpect.spawn(cmd)

	i=p.expect([ssh_newkey,'password:',pexpect.EOF])
	if i==0:
		print "I say yes"
		p.sendline('yes')
		i=p.expect([ssh_newkey,'password:',pexpect.EOF])
	if i==1:
		print "I give password",
		p.sendline(password)
		p.expect(pexpect.EOF)
	elif i==2:
		print "I either got key or connection timeout"
		pathtext.set("Connection Failed")
		pass
	print p.before # print out the result

def engrave():
	global filepath
	global filename
	
	proceed = True
	speed = 0.5
	
	try:
		speed = float(speedfield.get())
	except ValueError:
		proceed = False
		tkMessageBox.showerror(title="Error", message="'Engrave Speed' field must be filled with a number.")
	
	if (proceed == True):
		if filepath.endswith(".ngc"):#File of correct type?
			proceed = tkMessageBox.askokcancel(title="Are You Sure?", message="Make sure that the engraver is positioned correctly, power is applied, and the laser safety is off before continuing")
		else:
			proceed = False
			tkMessageBox.showerror(title="Error", message="Selected file not of correct type.  Must have extension '.ngc'.")
	
	if proceed:
		#Copy file to pi
		sshcmd("scp "+filepath+" "+user+"@"+address+":"+remdir)
		
		#Initiate Engraving
		#nohup required, or will fail when this program closed
		sshcmd("ssh "+user+"@"+address+" 'sudo -i nohup laserengraver -f "+remdir+filename+" -s "+str(speed)+" > foo.txt &'")

def cancel():
	proceed = tkMessageBox.askokcancel(title="Are You Sure?", message="Engraving cannot be resumed after cancellation.")
	
	if proceed:
		sshcmd("ssh "+user+"@"+address+" 'sudo killall python'")
		
def shutdown():
	proceed = tkMessageBox.askokcancel(title="Are You Sure?", message="Engraving will stop, and cannot be resumed.")
	
	if proceed:
		sshcmd("ssh "+user+"@"+address+" 'sudo shutdown -h now'")

root = Tkinter.Tk()
root.wm_title("RemotEngravR")
root.geometry("500x200")
pathtext = Tkinter.StringVar()
filepathlabel=Tkinter.Label(root,textvariable=pathtext)
pathtext.set("No File Selected")
filepathlabel.pack()
#Add all buttons, each calling a specified function
browsebutton=Tkinter.Button(root,text='Browse', command=getpath)
browsebutton.pack()
engravebutton=Tkinter.Button(root,text='Engrave', command=engrave)
engravebutton.pack()

speedframe=Tkinter.Frame(root)
speedframe.pack()
speedlabel=Tkinter.Label(speedframe, text='Engrave Speed (mm/sec):')
speedlabel.pack(side=Tkinter.LEFT)
speedfield=Tkinter.Entry(speedframe, width=5)
speedfield.insert(Tkinter.END, "0.5")
speedfield.pack(side=Tkinter.RIGHT)

cancelbutton=Tkinter.Button(root,text='Cancel Engraving', command=cancel)
cancelbutton.pack()
shutdownbutton=Tkinter.Button(root,text='Shutdown', command=shutdown)
shutdownbutton.pack()
root.mainloop()

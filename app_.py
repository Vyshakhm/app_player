from tkinter import *
from pygame import mixer
import os
from tkinter import filedialog
import tkinter.messagebox
from mutagen.mp3 import MP3
import threading
import time

os.system("clear")
#declaring tk
root=Tk()

#initializing variables as string
current_time=StringVar()
length=StringVar()
track=StringVar()
file=StringVar()
status=StringVar()

#constructing labelframe as listframe
listframe=LabelFrame(root , text="List", font=("times new roman", 15, "bold"), bg="lightgrey" ,bd=3, relief=GROOVE)
listframe.place(x=319, y=0, width=130, height=200)
#creating scrollbar and listbox for listing out the musics
scrol_y = Scrollbar(listframe, orient=VERTICAL)
playlist=Listbox(listframe, yscrollcommand=scrol_y.set, selectbackground="blue", selectmode=SINGLE, font=( "times new roman" , 12, "bold"), bg="silver", fg="black", bd=5, relief=GROOVE)
scrol_y.pack(side=RIGHT, fill=Y)
scrol_y.config(command=playlist.yview)
playlist.pack(fill=BOTH)

#function for menubar(open)
def openfile():
	#opening file directories
	filename=filedialog.askdirectory()
	#assigning directory path to os
	os.chdir(filename)
	global songlists
	songlists=os.listdir()
	#looping each song and inserting it into playlist 
	for track in songlists:
		playlist.insert(END, track)
#defining menu
menubar=Menu(root)
#configuring menubar as menu
root.config(menu=menubar)
#subsidiary menu
sub=Menu(menubar,tearoff=0)
#creating menu elements
menubar.add_cascade(label="File",menu=sub)
sub.add_command(label="Open",command=openfile)
sub.add_command(label="Exit",command=root.destroy)

#function for menubar(about)
def about():
	tkinter.messagebox.showinfo("About","All credits owned by the owner..!!Well it's not a lol... owner--unknown company--Not even exist")

sub=Menu(menubar,tearoff=0)

menubar.add_cascade(label="Help",menu=sub)
sub.add_command(label="About",command=about)
#initializing mixer
mixer.init()
#defining title,size,icon..
root.title("MUSIC")
root.geometry("450x250")
root.iconbitmap("icons/music.png")
root.resizable(False,False)
#creating label frame for main frame
label_frame=LabelFrame(root).place(x=0,y=0,width=320,height=200)
label=Label(label_frame,text="Let's start Music" ,font=("times new roman",15,"bold")).place(x=80,y=1)

#function for adding music length
def show_details():
	file_data=os.path.splitext(playlist.get(ACTIVE))
	print(file_data[1])
	audio=MP3(playlist.get(ACTIVE))
	track_length=audio.info.length
	print(track_length)
	#using divmod for determining song length
	mins,sec=divmod(track_length,60)
	#rounding it for avoiding fractional part we dont want it actually
	mins=round(mins)
	sec=round(sec)
	#formatting the time format
	length_format='{:02d}:{:02d}'.format(mins,sec)
	print(length_format)
	length.set("track_Length-"+length_format)

	#threading:
	#actually threading is the thing that help the counter to perform multiple things at a time!!!.. 
	t1=threading.Thread(target=start_count,args=(track_length,))
	t1.start()

#function that sets the current time of music when it start playing
def start_count(t):
	global Paused
	x=0
	#This while loop allows us to pause the current time when we pause the song as well as stop
	while x<t and mixer.music.get_busy():
		if Paused:
			continue
		else:
			mins,sec=divmod(x,60)
			mins=round(mins)
			sec=round(sec)
			current_format='{:02d}:{:02d}'.format(mins,sec)
			current_time.set("current_time-"+current_format)
			time.sleep(1)
			x+=1

#play function
def play():
	global Paused
	if Paused:
		mixer.music.unpause()
		status.set("Resumed")
		Paused=FALSE
	else:
		try:
			mixer.music.load(playlist.get(ACTIVE))			
			mixer.music.play()
			track.set("Now playing"+" -"+os.path.basename(playlist.get(ACTIVE)))
			show_details()
		except NameError:
			tkinter.messagebox.showerror("File not found:","Error occured" )

#pause function
Paused=FALSE
def pause():
	global Paused
	Paused=TRUE
	mixer.music.pause()
	status.set("Paused")
#stop function
def stop():
	mixer.music.stop()
	status.set("Stoped")
#adding volume
def volume(val):
	volume=int(val)/200
	mixer.music.set_volume(volume)
	
#Buttons
playbtn=Button(label_frame,text="Play",width=6,bg="lightgreen",command=play).place(x=50,y=150)
pausebtn=Button(label_frame,text="Pause",width=6,bg="lightgreen",command=pause).place(x=125,y=150)
stopbtn=Button(label_frame,text="Stop",width=6,bg="lightgreen",command=stop).place(x=200,y=150)
#scaling for volume 
scale=Scale(root,from_=0,to=100,orient=VERTICAL,command=volume)
scale.set(50)
mixer.music.set_volume(0.9)
scale.place(x=260,y=75)
#labels for displaying status 
status_frame=LabelFrame(root).place(x=0,y=200,width=450,height=50)
status_label=Label(status_frame,textvariable=status,font=("times new roman",10,"bold")).place(x=130,y=210)
status_track=Label(status_frame,textvariable=track,font=("times new roman",10,"bold")).place(x=5,y=230)
status_length=Label(root,textvariable=length,font=("times new roman",10,"bold")).place(x=320,y=200)
status_length=Label(root,textvariable=current_time,font=("times new roman",10,"bold")).place(x=80,y=35)

#Wrapping mainloop
root.mainloop()

import sys
import os
from time import *
import Tkinter as tk

#f = open("countdown_room", "r")
#room = f.read(16)

room = open("countdown_room","r").read().split('\n')[0]

#room = "sanctuary"
#room = "resistance"

debugmode = False

root = tk.Tk()
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
#w, h = 400, 300
root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))
root.configure(background='black')
root.focus_set()
#root.bind("<Escape>", lambda e: root.quit())

timelabeltext = tk.StringVar()
labeltext = tk.StringVar()
smallclocktext = tk.StringVar()

timelabel = tk.Label(root, textvariable = timelabeltext, bg="black", fg="white", font=("Helvetica", h/3))
label = tk.Label(root, textvariable = labeltext, bg="black", fg="white", font=("Helvetica", h/7))
smallclocklabel = tk.Label(root, textvariable = smallclocktext, bg="black", fg="white", font=("Helvetica", h/70))

timelabel.pack(pady=(h/10, 0))
label.pack()
smallclocklabel.pack(pady=(h/8, 0))

def setroom():
    global services, names, times, stopat
    if room == "sanctuary":
        services = [[5, 18, 55], [6, 9, 25], [6, 10, 55]]
        wday = localtime().tm_wday
        mday = localtime().tm_mday
        if (wday == 5 and (mday > 0 and mday < 8)) or (wday == 6 and (mday > 1 and mday < 9) and False):
            #first "full weekend", communion weekend
            names = ["Countdown",   "Worship",   "Communion",   "Meet+Greet",   "Tithe Message",    "Sermon",   "Altar"]
            times = [5,             18,	         6,             2,			    5,					34,			8]
            stopat = [0,            0,           0,             0,              0,                  0,          -7]
        else:
            #regular weekend
            names = ["Countdown",   "Worship", "Transition",   "Meet+Greet",   "Tithe Message",    "Sermon",   "Altar"]
            times = [5,             20,        3,				3,				5,					34,			8]
            stopat = [0,            0,         0,               0,              0,                  0,          -7]
    if room == "resistance":
        services = [[6, 11, 0]]
        names = ["Worship", "Meet+Greet",   "Host Intro",   "Communion/Tithe",  "Intro/Giveaway",   "Message",  "Transition",   "Game/Connect"]
        times = [25,        5,              1,              4,                  2,                  15,         1,              15]
        stopat = [0,        0,              0,              0,                  0,                  0,          0,              0]
    if room == "sanctuary2":
	services = [[5, 18, 55], [6, 9, 25], [6, 10, 55]]
	names =  ["Countdown",	"Worship",	"Transition",	"Tithe/Ann.",	"Teaching",	"Worship",	"Altar",	"Worship",	"Video"]
	times =  [5,		8,		3,		5,		25,		10,		5,		7,		1]
	stopat = [0,		0,		0,		0,		0,		0,		0,		0,		0]
    if room == "testing":
        services = [[localtime().tm_wday, localtime().tm_hour, localtime().tm_min]]
        names = ["Worship", "Sermon",   "Altar"]
        times = [.03,       .03,        .03]
        stopat = [0,        0,          -.2]


current = 0
running = False
currenttime = 0
endtime = 0

def debug(debugtext):
    if debugmode:
		print(debugtext)

def nexttimer():
    global current, endtime
    current += 1
    if current == len(times):
        reset()
        root.after(30000, master) #start running again after 30 seconds
    else:
        endtime = time() + (times[current] * 60)
        root.after(0, master)


def reset():
    global current, endtime, running
    setroom()
    debug("in reset")
    current = 0
    endtime = 0
    timelabeltext.set("--:--")
    labeltext.set("-")
    label.configure(fg = "white")
    timelabel.configure(fg = "white")
    running = False

def start():
    global endtime, running
    debug("in start")
    reset()
    endtime = time() + (times[current] * 60)
    running = True
    root.after(50, master)

def master():
    global currenttime
    debug("in master")
    daytime = [localtime().tm_wday, localtime().tm_hour, localtime().tm_min]
    if running:
        debug("-is running")
        currenttime = endtime - time()
        smallclocktext.set('Day: %s Time: %s:%s' % (strftime("%a"), daytime[1], daytime[2]))
        if currenttime < stopat[current] * 60:
            nexttimer()
        else:
            m, s = divmod(abs(currenttime), 60)
            timelabeltext.set('%s%02d:%02d' % (("-" if currenttime < 0 else ""), m, s))
            labeltext.set('%s' % names[current])
            if currenttime < 0:
                label.configure(fg = "red")
                timelabel.configure(fg = "red")
            else:
                label.configure(fg = "white")
                timelabel.configure(fg = "white")
            root.after(250, master)
    else:
        debug("-not running")
        if daytime[0] in [x[0] for x in services]: #== 3: #6
            smallclocktext.set('Day: %s Time: %s:%s' % (strftime("%a"), daytime[1], daytime[2]))
            if daytime in services:
                start()
            else:
                root.after(1000, master)
        else: #not right day
            root.after(3600000, master) #wait an hour (3,600,000 ms)
            smallclocktext.set('Day: %s' % (strftime("%a")))


reset()
root.after(250, master)

root.mainloop()

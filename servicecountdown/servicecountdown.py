import sys
import os
from time import *
import Tkinter as tk

f = open("countdown_room", "r")
room = f.read(16)

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

timelabel = tk.Label(root, textvariable = timelabeltext, bg="black", fg="white", font=("Helvetica", h/3))
label = tk.Label(root, textvariable = labeltext, bg="black", fg="white", font=("Helvetica", h/7))

timelabel.pack(pady=(h/10, 0))
label.pack()

if room == "sanctuary":
    names = ["Worship", "Transition",   "Meet+Greet",   "Tithe Message",    "Sermon",   "Altar"]
    times = [20,        3,				3,				5,					34,			8]
    services = [[5, 7, 0], [6, 9, 30], [6, 11, 0]]
if room == "resistance":
    names = ["Worship", "Meet+Greet",   "Host Intro",   "Communion/Tithe",  "Intro/Giveaway",   "Message",  "Transition",   "Game/Connect"]
    times = [25,        5,              1,              4,                  2,                  15,         1,              15]
    services = [[6, 11, 0]]

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
    debug("in reset")
    current = 0
    endtime = 0
    timelabeltext.set("--:--")
    labeltext.set("-")
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
    if running:
        debug("-is running")
        currenttime = endtime - time()
        if currenttime < 0:
            nexttimer()
        else:
            m, s = divmod(currenttime, 60)
            timelabeltext.set('%02d:%02d' % (m, s))
            labeltext.set('%s' % names[current])
            root.after(250, master)
    else:
        debug("-not running")
        daytime = [localtime().tm_wday, localtime().tm_hour, localtime().tm_min]
        if daytime[0] in [x[0] for x in services]: #== 3: #6
            if daytime in services:
                start()
            else:
                root.after(1000, master)
            '''
            debug("--right day")
            if localtime().tm_hour == 11: #11
                debug("---right hour")
                if localtime().tm_min == 13: #0
                    debug("----right minute")
                    start()
                else: #not right minute
                    root.after(1000, master)
            else: #not right hour
                root.after(1000, master) #wait 1 second
            '''
        else: #not right day
            root.after(3600000, master) #wait an hour (3,600,000 ms)


reset()
root.after(250, master)

root.mainloop()

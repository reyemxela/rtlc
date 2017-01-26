import sys
import os
import time
import glob
import Tkinter as tk
from PIL import Image, ImageTk

root = tk.Tk()

canvw, canvh = 480, 270
# canvw, canvh = 1920, 1080
numscreens = 3

# w, h = root.winfo_screenwidth(), root.winfo_screenheight()
w, h = canvw*numscreens, canvh


root.overrideredirect(1)
root.geometry("%dx%d+0+0" % (w, h))
root.configure(background='black')
root.focus_set()

framerate = 1.0/60.0
duration = 10.0
fadeduration = .5
imagedir = '/Users/alexmeyer/Documents/_Programming/rtlc/slideshowimages/'

canvas = [None]*numscreens
canvasimage = [None]*numscreens
blend = [None]*numscreens

files = []
# newfiles = []
# images = []

current = 0

for i in range(0, numscreens):
    canvas[i] = (tk.Canvas(root, width=canvw, height=canvh, borderwidth=0, highlightthickness=0))
    canvas[i].pack(side=tk.LEFT)
    canvasimage[i] = canvas[i].create_image(0, 0, image=None, anchor=tk.NW)

def LoadFiles():
    global files, images
    filetypes = ("*.jpg", "*.png")
    newfiles = []
    for type in filetypes:
        newfiles.extend(glob.glob(imagedir + type))
    if newfiles != files:
        files = newfiles
        images = []
        for i in range(0, len(files)):
            images.append(Image.open(files[i]))
            if images[i].size != (canvw, canvh):
                images[i] = images[i].resize((canvw, canvh), Image.BICUBIC)


def Main():
    global current
    #       [i%numscreens] ?
    while True:
        if current == 0:
            LoadFiles()
        alpha = 0.0
        while alpha <= 1.0:
            for i in range(0, numscreens):
                blend[i] = ImageTk.PhotoImage( Image.blend( images[(current + i) % len(files)], images[(current + i + 1) % len(files)], alpha ) )
                canvas[i].itemconfig(canvasimage[i], image=blend[i])
            root.update()
            time.sleep(framerate)
            alpha += framerate / fadeduration
        current = (current + 1) % len(files)
        time.sleep(duration)


# LoadFiles()
Main()

root.mainloop()

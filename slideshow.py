import sys
import os
import time
import glob
import Tkinter as tk
from PIL import Image, ImageTk, ImageCms

root = tk.Tk()

# canvw, canvh = 480, 270
canvw, canvh = 1920, 1080
numscreens = 3
offsetx = 0 #root.winfo_screenwidth() #get first monitor width for offset

# w, h = root.winfo_screenwidth(), root.winfo_screenheight()
w, h = canvw*numscreens, canvh


root.overrideredirect(1)
root.geometry("%dx%d+%d+0" % (w, h, offsetx))
root.configure(background='black')
root.focus_set()

framerate = 1.0/30.0
duration = 15.0
fadeduration = .5
imagedir = 'slideshowimages/'

canvas = [None]*numscreens
canvasimage = [None]*numscreens
currentimage = [None]*numscreens
# blend = [None]*numscreens

files = []
# newfiles = []
# images = []

current = 0

for i in range(0, numscreens):
    canvas[i] = tk.Canvas(root, width=canvw, height=canvh, borderwidth=0, highlightthickness=0)
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
            if images[i].mode == "CMYK":
                # images[i] = images[i].convert("RGB")
                images[i] = ImageCms.profileToProfile(images[i], 'USWebCoatedSWOP.icc', 'sRGB_v4_ICC_preference.icc', renderingIntent=0, outputMode='RGB')


def Main():
    global current, images, files
    #       [i%numscreens] ?
    if current == 0:
        LoadFiles()
    for i in range(0, numscreens):
        # print("screen: %s, current: %s, current + i mod files: %s" % (i,current,(current + i) % len(files)))
        # blend[i] = ImageTk.PhotoImage( Image.blend( images[(current + i) % len(files)], images[(current + i + 1) % len(files)], 0 ) )
        currentimage[i] = ImageTk.PhotoImage( images[(current + i) % len(files)] )
        canvas[i].itemconfig(canvasimage[i], image=currentimage[i] )
    root.update()
    current = (current + 1) % len(files)
    # time.sleep(duration)
    root.after(int(duration) * 1000, Main)


# LoadFiles()
# Main()
root.after(10, Main)

root.mainloop()

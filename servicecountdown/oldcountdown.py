#!/usr/bin/env python
# ----------------------------------------------------------------------------
# A fork of pyglet's timer.py by Luke Macken
#
# Copyright (c) 2006-2008 Alex Holkner
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

'''A full-screen minute:second countdown timer.  Leave it in charge of your conference
lighting talks.

Once there is 5 minutes left, the timer goes red.  This limit is easily
adjustable by hacking the source code.

Press spacebar to start, stop and reset the timer.
'''

import sys
import time
import pyglet

#window = pyglet.window.Window(fullscreen=True)
window = pyglet.window.Window()

names = ["Worship", "Meet+Greet",   "Host Intro",   "Communion/Tithe",  "Intro/Giveaway",   "Message",  "Transition",   "Game/Connect"]
times = [25,        5,              1,              4,                  2,                  15,         1,              15]
#times = [.2, .2]


#COUNTDOWN = int(sys.argv[1])


class Timer(object):
    def __init__(self):
        self.start = '--:--' #'%s:00' % times[current] #COUNTDOWN
        self.timelabel = pyglet.text.Label(self.start, font_size=window.height/3,
                                       x=window.width//2, y=window.height//2,
                                       anchor_x='center', anchor_y='center')

        self.label = pyglet.text.Label("", font_size=window.height/8,
                                       x=window.width//2, y=window.height/6,
                                       anchor_x='center', anchor_y='center')
        self.reset()

#font = 360
    def timecheck(self, dt):
        #print("Checking...")
        if self.running == False: #0, 11, 00
            if (time.strftime("%w") == "0") and \
                (time.strftime("%H") == "12") and \
                (time.strftime("%M") == "10"):
                #print("True")
                self.running = True
                #pyglet.clock.unschedule(self.timecheck)
                pyglet.clock.schedule_interval(timer.update, .1)
            else:
                #print("False")
                pyglet.clock.schedule_once(self.timecheck, 5)

    def reset(self):
        self.current = 0
        self.time = times[self.current] * 60 #COUNTDOWN * 60
        self.running = False
        self.timelabel.text = self.start
        self.timelabel.color = (255, 255, 255, 255)
        self.label.text = ''
        #pyglet.clock.schedule_once(self.timecheck, 5)
        #pyglet.clock.unschedule(self.update)

    def next(self):
        self.current += 1
        if self.current == len(times):
            #self.reset()
            pyglet.app.exit()
        else:
            self.time = times[self.current] * 60
            self.timelabel.color = (255, 255, 255, 255)

    def update(self, dt):
        #print("Update called")
        if self.running:
            #print("Update running")
            self.time -= dt
            if self.time < 0:
                self.next()
                return
            m, s = divmod(self.time, 60)
            self.timelabel.text = '%02d:%02d' % (m, s)
            self.label.text = '%s' % names[self.current]
            #self.label.text = '%s' % pyglet.clock.get_fps()
            if self.time < 30:
                self.timelabel.color = (180, 0, 0, 255)


@window.event
def on_key_press(symbol, modifiers):
    if symbol == pyglet.window.key.SPACE:
        if timer.running:
            timer.running = False
        else:
            timer.running = True
    elif symbol == pyglet.window.key.ESCAPE:
        window.close()
    elif symbol == pyglet.window.key.ENTER:
        timer.next()


@window.event
def on_draw():
    window.clear()
    timer.timelabel.draw()
    timer.label.draw()

timer = Timer()
#timer.timecheck(1)

timer.running = True
pyglet.clock.schedule_interval(timer.update, .1)
#pyglet.clock.schedule_interval_soft(timer.timecheck, 1)
pyglet.app.run()

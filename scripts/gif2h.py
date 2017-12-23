#!/usr/bin/python
from __future__ import print_function
import os
from PIL import Image
import sys

if len(sys.argv) < 3:
	print("usage: gif2h.py filename.gif variable-prefix\n\nFor example 'gif2h.py puppy.gif puppy'")
	sys.exit(1)

giffile = sys.argv[1]
name = sys.argv[2]

frame = Image.open(giffile)
numFrames = 1
try:
	while 1:
		frame.seek(frame.tell() + 1)
		numFrames = numFrames + 1
except EOFError:
	pass

frame.seek(0)
#print(frame.format, frame.size, frame.mode, frame.info["transparency"], frame.info["background"])
print("static int", name, end="")
print("Width =", frame.size[0], ";")
print("static int", name, end="")
print("Height =", frame.size[1], ";")
print("static int", name, end="")
print("NumFrames =", numFrames, ";")
print("static int", name, end="")
print("Duration = ", frame.info["duration"], ";")
print("const int", name, end="")
print("Frames[",numFrames*frame.size[0]*frame.size[1],"] = {")


def printPixels(frame):
	palette = frame.getpalette()
	intpalette = []
	rgb = 0
	for value in palette:
		if rgb == 2:
			b = value
       	        	intpalette.append( (r<<16) + (g<<8) + b)
		elif rgb == 1:
			g = value
		elif rgb == 0:
			r = value
		rgb = (rgb + 1) % 3

	intpalette[frame.info["transparency"]] = 0


	data = list(frame.getdata())


	for x in range(0,len(data)):
		print(intpalette[data[x]],end="")
		print (",",end="")

	print()


for frameNum in range(0,numFrames):
	frame.seek(frameNum)
	printPixels(frame)
print("};")

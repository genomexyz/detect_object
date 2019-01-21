#!/usr/bin/python

import tkinter as tk # this is in python 3.4. For python 2.x import Tkinter
from PIL import Image, ImageTk
import os

#setting
wCanvas = 700
hCanvas = 500
datasave = 'box.csv'
dirimg = '/home/genomexyz/odetection'


class ExampleApp(tk.Tk):
	def __init__(self):
		tk.Tk.__init__(self)
		self.x = self.y = 0
		self.canvas = tk.Canvas(self, width=wCanvas, height=hCanvas, cursor="cross")
		self.canvas.pack(side="top", fill="both", expand=True)
		self.canvas.bind("<ButtonPress-1>", self.on_button_press)
		self.canvas.bind("<B1-Motion>", self.on_move_press)
		self.canvas.bind("<ButtonRelease-1>", self.on_button_release)

		#add button
		self.buttonOk = tk.Button(self, text="Ok")
		self.buttonOk.bind("<ButtonPress-1>", self.saveboxcord)
		
		self.buttonDelete = tk.Button(self,text="Delete")
		self.buttonDelete.bind("<ButtonPress-1>", self.resetbox)

		self.buttonNext = tk.Button(self, text="Next")
		self.buttonNext.bind("<ButtonPress-1>", self.nextimg)
		
		self.buttonPrev = tk.Button(self, text="Prev")
		self.buttonPrev.bind("<ButtonPress-1>", self.previmg)

		self.buttonOk.pack()
		self.buttonNext.pack()
		self.buttonPrev.pack()
		self.buttonDelete.pack()
		
		#add label of numbering
		self.numbering = tk.Label(self, text='0')
		self.numbering.pack()
		
		#open data save
		self.allimg = sorted(os.listdir(dirimg))
		self.imgptr = 0
		
		self.boxdata = None
#		self.boxdata = open(datasave, 'a')
#		self.boxdata.write('gambar,x_min,y_min,x_max,y_max')
#		self.boxdata.close()

		self.allcord = []

		self.allrect = []
		self.rect = None

		self.start_x = None
		self.start_y = None
		self.end_x = None
		self.end_y = None


		self._draw_image()


	def _draw_image(self):
		self.im = Image.open(dirimg+'/'+self.allimg[self.imgptr])
		self.tk_im = ImageTk.PhotoImage(self.im)
		self.canvas.create_image(0,0,anchor="nw",image=self.tk_im)

	def saveboxcord(self, event):
		self.boxdata = open(datasave, 'a+')
		for i in xrange(len(self.allcord)):
			self.boxdata.write(self.allimg[self.imgptr]+','+
			str(self.allcord[i][0])+','+
			str(self.allcord[i][1])+','+
			str(self.allcord[i][2])+','+
			str(self.allcord[i][3])+'\n')
		for i in xrange(len(self.allrect)):
			self.canvas.delete(self.allrect[i])
		del self.allcord[:]
		del self.allrect[:]
		self.boxdata.close()
	
	def resetbox(self, event):
		for i in xrange(len(self.allrect)):
			self.canvas.delete(self.allrect[i])
		del self.allcord[:]
		del self.allrect[:]
	
	def nextimg(self, event):
		for i in xrange(len(self.allrect)):
			self.canvas.delete(self.allrect[i])
		del self.allcord[:]
		del self.allrect[:]
		self.canvas.delete("all")

		self.imgptr += 1
		if self.imgptr > len(self.allimg)-1:
			self.imgptr = 0
		self._draw_image()
		self.numbering.configure(text=str(self.imgptr))

	def previmg(self, event):
		for i in xrange(len(self.allrect)):
			self.canvas.delete(self.allrect[i])
		del self.allcord[:]
		del self.allrect[:]
		self.canvas.delete("all")

		self.imgptr -= 1
		if self.imgptr < 0:
			self.imgptr = len(self.allimg)-1
		self._draw_image()
		self.numbering.configure(text=str(self.imgptr))


	def on_button_press(self, event):
		# save mouse drag start position
		self.start_x = event.x
		self.start_y = event.y

		# create rectangle if not yet exist
		#if not self.rect:
		self.rect = self.canvas.create_rectangle(self.x, self.y, 1, 1, outline='green', width=3)

	def on_move_press(self, event):
		curX, curY = (event.x, event.y)

		if curX > wCanvas:
			curX = wCanvas
		if curY > hCanvas:
			curY = hCanvas

		self.end_x = curX
		self.end_y = curY

		# expand rectangle as you drag the mouse
		self.canvas.coords(self.rect, self.start_x, self.start_y, curX, curY)



	def on_button_release(self, event):
		#pass
		print self.start_x, self.start_y, self.end_x, self.end_y
		self.allcord.append([self.start_x, self.start_y, self.end_x, self.end_y])
		self.allrect.append(self.rect)
		print len(self.allcord)


if __name__ == "__main__":
	app = ExampleApp()
	app.mainloop()

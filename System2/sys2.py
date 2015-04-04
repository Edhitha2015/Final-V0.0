from Tkinter import *
import tkFileDialog as tk
import tkMessageBox
import os.path
import cv2
import queue1
import numpy as np
import glob
import easygui

pathToFilteredCtopsDir = './filteredCropsMAIN/'	

def colourProcess():
	queue1.mainProcess(1)
	return

def shapeProcess():
	pass

def alphabetProcess():
	queue1.mainProcess(2)
	return

def showImages():
	queue1.viewImages(pathToFilteredCtopsDir)
	return

if __name__=='__main__':
#def tkInterface():
	windowA = Tk()
	frameA = Frame(windowA)

	folderFilteredCrops = Button(frameA, text = "Filtered Crops", command = showImages).grid(row = 0, column= 0)
	colourID = Button(frameA, text = 'Color?', command = colourProcess).grid(row=0, column=1)
	shapeID  = Button(frameA, text = 'Shape?', command = shapeProcess).grid(row=0, column=2)
	shapeID  = Button(frameA, text = 'Which Alphabet?', command = alphabetProcess).grid(row=0, column=3)

	labelFrameA = Label(windowA, text = "SYSTEM 2 \n Press ESC to quit").pack()
	frameA.pack()
	windowA.mainloop()
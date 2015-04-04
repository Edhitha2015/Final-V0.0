import collections # for deque
import cv2
import numpy as np
import os.path
import Queue as Q
import glob
import easygui
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import utils

# global imagePath

pathSource = './filteredCropsMAIN/'
noNew = './noNew.JPG'

def viewImages(imPath):
	for i,img in enumerate([os.path.join(imPath,fn) for fn in next(os.walk(imPath))[2]]):
		cv2.imshow("Image Verifier", cv2.imread(img))
		if cv2.waitKey(0)==27:
			cv2.destroyAllWindows()
			break
	if cv2.waitKey(0):
		cv2.destroyAllWindows()
	return

def folderSize(path):
	num = len([f for f in os.listdir(path) 
			if os.path.isfile(os.path.join(path, f))])
	return num

def qDeq(x):
	q = Q.PriorityQueue()
	d = collections.deque()
	for i in x:
		dirName, fileName = os.path.split(i)
		shortName,_ = os.path.splitext(fileName)
		_,fir= shortName.split('_')
		print fir	
		q.put(int(fir))
	while not q.empty():
		d.append(q.get())
	print d
	return d

def colourAuto(d, folderSizeBefore, sizFlag):
	if (sizFlag):
		x = folderSizeBefore -1# works over x = folderSizeBefore o.O idk why. Works in a strange way too. Starts looking at the folder last img first.
	else:
		x = 0
	randomVariableName = easygui.msgbox("Press 'y' if you're satisfied with the output\n Press 'm' if it's a manual crop ", title = "Hello!")
	for  i in range(x, len(d)):
		# try:
		imagePath = pathSource+'crop_%d.JPG'%(d[i])
		image = cv2.imread(imagePath,1)
		cv2.imshow("Colour?", image)
		(bar, sorted_D) = colourAutoSubProcess(imagePath)
		cv2.imshow("bar",  cv2.cvtColor(bar, cv2.COLOR_BGR2RGB))
		k = cv2.waitKey(0)
		if k== 27:
			cv2.destroyAllWindows()
			break
		else:
			try:
				colourChoiceALPHA = easygui.choicebox(msg= 'Which colour is the ALPHANUMERAL?', title= 'Colour?', choices=(sorted_D, 'None'))
				colourChoiceSHAPE = easygui.choicebox(msg= 'Which colour is the SHAPE?', title= 'Colour?', choices=(sorted_D, 'None'))
				print 'colour of alphanumeral is'+colourChoiceALPHA,'\ncolor of shape is'+colourChoiceSHAPE #TODO write to .csv file instead
			except TypeError:
				print 'colour of alphanumeral is N/A','\ncolor of shape is N/A'#TODO write to .csv file instead

			k2 = cv2.waitKey(0)
			if k2 == ord('m'):
				(colouOfAlpha,colourOfShape) = colourManual()
				try:
					print 'colour of alphanumeral is'+colouOfAlpha,'\ncolor of shape is'+colourOfShape #TODO write to .csv file inst
				except TypeError:
					print 'colour of alphanumeral is N/A','\ncolor of shape is N/A'#TODO write to .csv file instead

				if k2 == 27:
					cv2.destroyAllWindows()
					break

	return 0

def colourAutoSubProcess(imagePath):
	# load the image and convert it from BGR to RGB so that we can dispaly it with matplotlib
	image = cv2.imread(imagePath)
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

	# reshape the image to be a list of pixels
	image = image.reshape((image.shape[0] * image.shape[1], 3))

	# cluster the pixel intensities
	clt = KMeans(n_clusters = 5)
	clt.fit(image)

	# build a histogram of clusters and then create a figure representing the number of pixels labeled to each color
	hist = utils.centroid_histogram(clt)
	#print clt.cluster_centers_
	bar,sorted_D = utils.plot_colors(hist, clt.cluster_centers_)

	return (bar, sorted_D)

def colourManual():
	alphaColour = easygui.enterbox(msg='What is the colour of the ALPHANUMERAL?', title=' Which colour?', default='', strip=True)
	shapeColour = easygui.enterbox(msg='What is the colour of the SHAPE?', title=' Which colour?', default='', strip=True)
	return alphaColour, shapeColour

def alphabetDetectProcess(d, folderSizeBefore, sizFlag):
	if (sizFlag):
		x = folderSizeBefore -1# works over x = folderSizeBefore o.O idk why. Works in a strange way too. Starts looking at the folder last img first.
	else:
		x = 0
	for  i in range(x, len(d)):
		imagePath = pathSource+'crop_%d.JPG'%(d[i])
		cv2.imshow("alphabet?", cv2.imread(imagePath))
		cv2.waitKey(0)
		alphaNumeral = easygui.enterbox(msg='Enter the Alphanumeral.', title=' Which letter?', default='', strip=True)
		print alphaNumeral, 'crop_%d.JPG'%(d[i])
		
		if cv2.waitKey(0)==27:
			cv2.destroyAllWindows()
			break
	
	return

#if __name__ == '__main__':
def mainProcess(processFlag):
	siz = 0
	sizFlag = 0
	while True:
		x = glob.glob(pathSource+'*.JPG')
		print "size is%d"%(siz)
		if siz !=folderSize(pathSource):
			folderSizeBefore = siz
			siz = folderSize(pathSource)
			print "new size is%d"%(siz)
			sizFlag = 1		
			d = qDeq(x)
			if processFlag==1:
				colourAuto(d, folderSizeBefore, sizFlag)
			elif processFlag==2:
				alphabetDetectProcess(d,folderSizeBefore, sizFlag)
			else:
				print 111234567890
			
		else :
			sizFlag = 0
			print "waiting..."
			k = cv2.waitKey(0)
			if k:
				cv2.imshow("currentIm", cv2.imread(noNew))
		if cv2.waitKey(0)==27:
			cv2.destroyAllWindows()
			break
	return
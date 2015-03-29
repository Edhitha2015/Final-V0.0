import cv2
import numpy as np
import cv2.cv as cv
from time import time
from decimal import *
import queue1
import easygui

boxes = []
cropsPath = '/home/praneeta/Desktop/Tkin/System1/allCrops1/'
filteredCropsDirectory= '/home/praneeta/Desktop/Tkin/System1/filteredCrops2/'

def masking(image):
	hsv = cv2.cvtColor( image, cv2.COLOR_BGR2HSV)
	mask = cv2.inRange(hsv, np.array([50,100,100], dtype = np.uint8), np.array([70,255,255], dtype = np.uint8))
	mask_inv = cv2.bitwise_not(mask)
	res= cv2.bitwise_and(image, image, mask = mask_inv)
	return res

def extractblob(im):
	imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(imgray,0,255,0)
	contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
	z=0
	for cnt in contours:   	  	
	        if cv2.contourArea(cnt)>100 and cv2.contourArea(cnt)<10000:
				cv2.drawContours(im,[cnt],0,(0,0,0),1)
	 			x,y,w,h = cv2.boundingRect(cnt)
				rect=cv2.minAreaRect(cnt)
				box=cv2.cv.BoxPoints(rect)
				box=np.int0(box)
				
				cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),1)
				c=Decimal(rect[1][0])/Decimal(rect[1][1])
				d=Decimal(rect[1][1])/Decimal(rect[1][0])
				if c>Decimal(4)/Decimal(2.5) or d>Decimal(4)/Decimal(2.5):
				   continue
				crop=im[y:y+h,x:x+w]
				maskedCrop = masking(crop)
				cv2.imwrite(filteredCropsDirectory+"crop_%d.JPG"%(queue1.folderSize(filteredCropsDirectory)+001),maskedCrop)
				cv2.imshow("crop%d"%(z),maskedCrop)
				z=z+1
	cv2.imshow("hello",cv2.resize(im, None, fx = 0.25, fy = 0.25))
	cv2.waitKey(0)
	return

def backproject(filename):
	im = cv2.imread(filename)
	
	#image => hsv, hist
	hsv = cv2.cvtColor( im, cv2.COLOR_BGR2HSV)
	imHist = cv2.calcHist([hsv], [0,1], None, [180, 256],[0,180,0,256])

	bckP = cv2.calcBackProject([hsv], [0,1], imHist,[0,180,0,256], 1)
	kernel = cv2.getStructuringElement( cv2.MORPH_ELLIPSE, (3,3))
	closing = cv2.morphologyEx(bckP, cv2.MORPH_CLOSE, kernel)



	ret,thresh = cv2.threshold(closing, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

	fm1 =  cv2.merge((thresh,thresh,thresh))
	res1 = cv2.bitwise_and(im, fm1, mask = None)# mask here has no significance
	
	#make (lower bound) G= 180 for proper target. G= 90 makes its edges disappear a leeettle
	mask = cv2.inRange(hsv, np.array([5,90,50], dtype = np.uint8), np.array([49,255,205], dtype = np.uint8)) 
	mask_inv = cv2.bitwise_not(mask)
	res = cv2.bitwise_and(res1, res1, mask = mask_inv)
	res=cv2.erode(res,kernel,iterations=1)
	extractblob(res)

def edgeCase(imPath):
	im = cv2.imread(imPath,1)
	hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)
	imInv = 255- cv2.cvtColor(im, cv2.COLOR_RGB2GRAY)

	ret,thresh = cv2.threshold(imInv,30,255,cv2.THRESH_BINARY) # replace parameter 2 w/ appropriate value to get proper target shape

	threshInv = cv2.bitwise_not(thresh)
	threshM = cv2.merge((threshInv,threshInv,threshInv))
	mask = cv2.inRange(hsv, np.array([240,240,240], dtype = np.uint8), np.array([255,255,255], dtype = np.uint8))
	mask_inv = cv2.bitwise_not(mask)
	res = cv2.bitwise_and(im,threshM, mask = mask_inv)
	cv2.imshow("hello", cv2.resize( res, None, fx = .25, fy = .25)) 
	extractblob(res)
	
def on_mouse(event, x, y, flags, params):
    # global img
    t = time()

    if event == cv.CV_EVENT_LBUTTONDOWN:
         print 'Start Mouse Position: '+str(x)+', '+str(y)
         sbox = [x, y]
         boxes.append(sbox)
    elif event == cv.CV_EVENT_LBUTTONUP:
        print 'End Mouse Position: '+str(x)+', '+str(y)
        ebox = [x, y]
        boxes.append(ebox)
        print boxes
        crop = img[boxes[-2][1]*4:boxes[-1][1]*4,boxes[-2][0]*4:boxes[-1][0]*4]
        cv2.imshow('crop',crop)
        k =  cv2.waitKey(0)
        if ord('q')==k:
            cv2.imwrite(cropsPath+'manualCrop_%d.JPG'%(queue1.folderSize(cropsPath)+1),crop) # saved directly into filteredCrops2 folder!!
            # print cropsPath+'crop_%d.JPG'%(queue1.folderSize(cropsPath)+1)
            #print "Written to file"
	    i = easygui.msgbox("Manual crop written to folder successfully! Press Esc to move to next image!", title = "Success!")

def manualCropProcess(imPath):
    count = 0
    while(1):
        count += 1
        global img 
        img= cv2.imread(imPath,1)
        #img = cv2.resize(img, None, fx = 0.25,fy = 0.25)
        #height, width,_=img.shape
        cv2.namedWindow('real image')
        # cv2.resizeWindow('real image',int(width*.30),int(height*.30))
        cv.SetMouseCallback('real image', on_mouse, 0)
        imgRes = cv2.resize(img,None , fx = 0.25, fy = 0.25)
        cv2.imshow('real image', imgRes)
        if count < 50:
            if cv2.waitKey(33) == 27:
                cv2.destroyAllWindows()
                break
        elif count >= 50:
            if cv2.waitKey(0) == 27:
                cv2.destroyAllWindows()
                break
            count = 0
'''	
#if __name__=='__main__':
def mainProcess(imPath):
	#imPath = "/home/praneeta/Desktop/Tkin/System1/alphaNumeralTargets/DSC_0893.JPG"
	edgeCase(imPath)	'''

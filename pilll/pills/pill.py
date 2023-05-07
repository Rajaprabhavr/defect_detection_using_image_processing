import cv2
import numpy as np
import random
def loadGoldenTemplate(imgpath):
    goldenTemplate = cv2.imread(imgpath)
    goldenTemplate =cv2.resize(goldenTemplate,(574,424))
    goldenTemplateGray = cv2.cvtColor(goldenTemplate, cv2.COLOR_BGR2GRAY)
    goldenTemplateHisteqaul_frame = cv2.equalizeHist(goldenTemplateGray)
    blur_frame = cv2.GaussianBlur(goldenTemplateHisteqaul_frame, (5, 5), 5)
    cv2.imshow("golden",goldenTemplateHisteqaul_frame)
    cv2.waitKey(0)
    gray_correct = np.array(255 * (blur_frame / 255) ** 1.2 , dtype='uint8')
    thresh = cv2.adaptiveThreshold(gray_correct, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 255, 19)
    thresh = cv2.bitwise_not(thresh)
    kernel = np.ones((15,15), np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)
    img_erode = cv2.erode(img_dilation,kernel, iterations=1)# clean all noise after dilatation and erosionimg_erode = cv.medianBlur(img_erode, 7)
    img_erode = cv2.medianBlur(img_erode, 7)
    img_erode=cv2.bitwise_not(img_erode)
    contours = cv2.findContours(img_erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
    mask = np.zeros_like(img_erode)
    arealist =list()
    for contour in contours:
        area = cv2.contourArea(contour)
        if (area > 5000) & (area < 10300) :
            arealist.append(area)
            cv2.fillPoly(mask, [contour], 255)
        else :
            cv2.fillPoly(mask,contour, [255, 255, 255])
    mask = cv2.erode(mask, None, iterations=5)
    cv2.imwrite("goldenmask.jpg",mask)

    ret, labels = cv2.connectedComponents(mask)
    label_hue = np.uint8(179 * labels / np.max(labels))
    blank_ch = 255 * np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
    labeled_img[label_hue == 0] = 0
    cv2.imshow("golden",labeled_img)
    cv2.waitKey(0)
    return ret-1 ,labels

def loadSampleImage(imgpath):
    sampleImage = cv2.imread(imgpath)
    sampleImage =cv2.resize(sampleImage,(574,424))
    print(sampleImage.shape)
    sampleImageGray = cv2.cvtColor(sampleImage, cv2.COLOR_BGR2GRAY)
    sampleImageHisteqaul_frame = cv2.equalizeHist(sampleImageGray)
    #blur_frame = cv2.GaussianBlur(sampleImageHisteqaul_frame, (5, 5), 5)
    cv2.imshow("sample",sampleImageHisteqaul_frame)
    cv2.waitKey(0)
    
    gray_correct = np.array(255 * (sampleImageHisteqaul_frame / 255) ** 1.2 , dtype='uint8')

    thresh = cv2.adaptiveThreshold(gray_correct, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 255, 19)
    thresh = cv2.bitwise_not(thresh)
    kernel = np.ones((15,15), np.uint8)
    #im2, contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #print(im2)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)
    img_erode = cv2.erode(img_dilation,kernel, iterations=1)# clean all noise after dilatation and erosionimg_erode = cv.medianBlur(img_erode, 7)
    img_erode = cv2.medianBlur(img_erode, 7)
    img_erode=cv2.bitwise_not(img_erode)
    contours = cv2.findContours(img_erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
    mask = np.zeros_like(img_erode)
    arealist =list()
    for contour in contours:
        area = cv2.contourArea(contour)
        if (area > 3000) & (area < 10300) :
            arealist.append(area)
            cv2.fillPoly(mask, [contour], 255)
        else :
            cv2.fillPoly(mask,contour, [255, 255, 255])
    
    mask = cv2.erode(mask, None, iterations=5)
    cv2.imshow("sample erd",mask)
    cv2.imwrite("samlemask.jpg",mask)
    cv2.waitKey(0)
    ret, labels = cv2.connectedComponents(mask)
    label_hue = np.uint8(179 * labels / np.max(labels))
    blank_ch = 255 * np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
    labeled_img[label_hue == 0] = 0
    cv2.imshow("sample",labeled_img)
    cv2.waitKey(0)
    return ret-1,labels



def segmentationAndComparison():
    DefectCount = 0
    ReqularCount = 0 
    goldenTemplatecount,goldenTemplateSegment = loadGoldenTemplate('goldcut.jpg')
    sampleImagecount,sampleImageSegment = loadSampleImage("pil.jpg")
    
    if goldenTemplatecount != sampleImagecount :
        missing = goldenTemplatecount-sampleImagecount
        print(str(missing)+" tablets are missing")
    else :
        print("sample has correct number of tablets.")
    r = random.randrange(0,goldenTemplatecount-1 )
    for i in range(sampleImagecount):
        if np.array_equal(sampleImageSegment[i],goldenTemplateSegment[r]):
            ReqularCount += 1
        else :
            DefectCount += 1
    print("No. of defected pill "+str(DefectCount))
    

def loadRoundGoldenTemplate(imgpath):
    goldenTemplate = cv2.imread(imgpath)
    goldenTemplate =cv2.resize(goldenTemplate,(574,424))
    goldenTemplateGray = cv2.cvtColor(goldenTemplate, cv2.COLOR_BGR2GRAY)
    goldenTemplateHisteqaul_frame = cv2.equalizeHist(goldenTemplateGray)
    gray_correct = np.array(255 * (goldenTemplateHisteqaul_frame / 255) ** 1.2 , dtype='uint8')
    thresh = cv2.adaptiveThreshold(gray_correct, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 255, 19)
    thresh = cv2.bitwise_not(thresh)
    kernel = np.ones((15,15), np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)
    img_erode = cv2.erode(img_dilation,kernel, iterations=1)
    img_erode = cv2.medianBlur(img_erode, 7)
    img_erode=cv2.bitwise_not(img_erode)
    contours = cv2.findContours(img_erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
    mask = np.zeros_like(img_erode)
    arealist =list()
    for contour in contours:
        area = cv2.contourArea(contour)
        arealist.append(area)
        cv2.fillPoly(mask, [contour], 255)
    
    threshval=[min(arealist),max(arealist)]
    
    cv2.imwrite("mask.jpg",np.uint8(mask))
    ret, labels = cv2.connectedComponents(mask)
    cv2.imshow("golden background",np.uint8(mask))
    cv2.waitKey(0)
    return ret-1 ,labels,threshval

def loadRoundSampleImage(imgpath,threshval):
    sampleImage = cv2.imread(imgpath)
    sampleImage =cv2.resize(sampleImage,(574,424))
    sampleImageGray = cv2.cvtColor(sampleImage, cv2.COLOR_BGR2GRAY)
    sampleImageHisteqaul_frame = cv2.equalizeHist(sampleImageGray)
    gray_correct = np.array(255 * (sampleImageHisteqaul_frame / 255) ** 1.2 , dtype='uint8')
    thresh = cv2.adaptiveThreshold(gray_correct, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 255, 19)
    thresh = cv2.bitwise_not(thresh)
    kernel = np.ones((15,15), np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)
    img_erode = cv2.erode(img_dilation,kernel, iterations=1)
    img_erode = cv2.medianBlur(img_erode, 7)
    img_erode=cv2.bitwise_not(img_erode)
    contours = cv2.findContours(img_erode, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0]
    mask = np.zeros_like(img_erode)
    cv2.imshow("im",img_erode)
    cv2.waitKey(0)
    
    for contour in contours:
        area = cv2.contourArea(contour)
        if (area <= threshval[0]) | (area >= threshval[1]):
            cv2.fillPoly(mask,contour, [255, 255, 255])
        else :
            cv2.fillPoly(mask, [contour], 255)
            

    
    mask = cv2.erode(mask, None, iterations=5)
    cv2.imwrite("smask.jpg",np.uint8(mask))
    ret, labels = cv2.connectedComponents(mask)
    cv2.imshow("sample background",np.uint8(mask))
    cv2.waitKey(0)
    return ret-1 ,labels



def roundTableForgroundBackground():
    goldenTemplatecount,goldenTemplateSegment,threshval = loadRoundGoldenTemplate('roundgold.jpg')
    sampleImagecount,sampleImageSegment = loadRoundSampleImage("roundsample.jpg",threshval)
    
    if goldenTemplatecount == sampleImagecount :
        print("sample has correct number of tablets.")
    elif goldenTemplatecount > sampleImagecount :
        missing = goldenTemplatecount - sampleImagecount
        print(str(missing)+" tablets are missing and defected.")
    else :
        print("issue with same segmntation got :-",sampleImagecount)

def singleColorPill():
    return True

def multiColorPill():
    return True


segmentationAndComparison()
roundTableForgroundBackground()
import cv2
import numpy as np
import random
def loadGoldenTemplate(imgpath):
    goldenTemplate = cv2.imread(imgpath)
    goldenTemplateGray = cv2.cvtColor(goldenTemplate, cv2.COLOR_BGR2GRAY)
    goldenTemplateHisteqaul_frame = cv2.equalizeHist(goldenTemplateGray)
    gray_correct = np.array(255 * (goldenTemplateHisteqaul_frame / 255) ** 1.2 , dtype='uint8')
    thresh = cv2.adaptiveThreshold(gray_correct, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 255, 19)
    thresh = cv2.bitwise_not(thresh)
    kernel = np.ones((15,15), np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)
    img_erode = cv2.erode(img_dilation,kernel, iterations=1)# clean all noise after dilatation and erosionimg_erode = cv.medianBlur(img_erode, 7)
    img_erode=cv2.bitwise_not(img_erode)
    ret, labels = cv2.connectedComponents(img_erode)
    label_hue = np.uint8(179 * labels / np.max(labels))
    blank_ch = 255 * np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
    labeled_img[label_hue == 0] = 0
    
    return ret-1 ,labels

def loadSampleImage(imgpath):
    sampleImage = cv2.imread(imgpath)
    sampleImageGray = cv2.cvtColor(sampleImage, cv2.COLOR_BGR2GRAY)
    sampleImageHisteqaul_frame = cv2.equalizeHist(sampleImageGray)
    gray_correct = np.array(255 * (sampleImageHisteqaul_frame / 255) ** 1.2 , dtype='uint8')
    thresh = cv2.adaptiveThreshold(gray_correct, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 255, 19)
    thresh = cv2.bitwise_not(thresh)
    kernel = np.ones((15,15), np.uint8)
    img_dilation = cv2.dilate(thresh, kernel, iterations=1)
    img_erode = cv2.erode(img_dilation,kernel, iterations=1)# clean all noise after dilatation and erosionimg_erode = cv.medianBlur(img_erode, 7)
    img_erode=cv2.bitwise_not(img_erode)
    ret, labels = cv2.connectedComponents(img_erode)
    label_hue = np.uint8(179 * labels / np.max(labels))
    blank_ch = 255 * np.ones_like(label_hue)
    labeled_img = cv2.merge([label_hue, blank_ch, blank_ch])
    labeled_img = cv2.cvtColor(labeled_img, cv2.COLOR_HSV2BGR)
    labeled_img[label_hue == 0] = 0
  
    return ret-1,labels



def segmentationAndComparison():
    DefectCount = 0
    ReqularCount = 0 
    goldenTemplatecount,goldenTemplateSegment = loadGoldenTemplate('gold.jpg')
    sampleImagecount,sampleImageSegment = loadSampleImage('pil.jpg')
    if goldenTemplatecount != sampleImagecount :
        missing = goldenTemplatecount-sampleImagecount
        print(str(missing)+" tablets are missing")
    else :
        print("sample has correct number of tablets.")
    r = random.randrange(2,goldenTemplatecount-2 )
    for i in range(sampleImagecount):
        if np.array_equal(sampleImageSegment[i],goldenTemplateSegment[r]):
            ReqularCount += 1
        else :
            DefectCount += 1
    print("No. of defected pill "+str(DefectCount))



segmentationAndComparison()

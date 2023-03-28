import cv2
def loadGoldenTemplate(imgpath):
    goldenTemplate = cv2.imread(imgpath)
    cv2.imshow("Golden template",goldenTemplate)
    cv2.waitKey(0)
    goldenTemplateGray = cv2.cvtColor(goldenTemplate, cv2.COLOR_BGR2GRAY)
    goldenTemplateHisteqaul_frame = cv2.equalizeHist(goldenTemplateGray)
    return cv2.threshold(goldenTemplateHisteqaul_frame,70,255,0)

def loadSampleImage(imgpath):
    sampleImage = cv2.imread(imgpath)
    cv2.imshow("Sample Image",sampleImage)
    cv2.waitKey(0)
    sampleImageGray = cv2.cvtColor(sampleImage, cv2.COLOR_BGR2GRAY)
    sampleImageHisteqaul_frame = cv2.equalizeHist(sampleImageGray)
    return cv2.threshold(sampleImageHisteqaul_frame,70,255,0)

def main():
    goldenTemplateret,goldenTemplateBinary = loadGoldenTemplate('gold.jpg')
    cv2.imshow("Golden template Binary",goldenTemplateBinary)
    cv2.waitKey(0)
    sampleImageret,sampleImageBinary = loadSampleImage("pil.jpg")
    cv2.imshow("Sample Image Binary",sampleImageBinary)
    cv2.waitKey(0)

main()

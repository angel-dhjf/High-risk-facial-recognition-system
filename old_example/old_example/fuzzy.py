import cv2

import cv2

def main():
    image = cv2.imread("imagesA/17_15_06.jpg")
    img2gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()
    print(imageVar)

def fuzzycritical(imgs):
    try:
        img2gray = cv2.cvtColor(imgs, cv2.COLOR_BGR2GRAY)
        imageVar = cv2.Laplacian(img2gray, cv2.CV_64F).var()
        if imageVar >= 30:
            return True
        else:
            return False
    except:
        pass

def getImageVar(orgimg, newimg):
    # image = cv2.imread(orgimgPath)

    orgimg2gray = cv2.cvtColor(orgimg, cv2.COLOR_BGR2GRAY)
    orgimageVar = cv2.Laplacian(orgimg2gray, cv2.CV_64F).var()

    newimg2gray = cv2.cvtColor(newimg, cv2.COLOR_BGR2GRAY)
    newimageVar = cv2.Laplacian(newimg2gray, cv2.CV_64F).var()

    if newimageVar > orgimageVar:
        return True
    else:
        return False




if __name__ == '__main__':
    main()




# getImageVar('0.jpg')

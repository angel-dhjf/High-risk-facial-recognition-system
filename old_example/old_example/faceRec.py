import numpy as np
import csv,os,gc,face_recognition,cv2
from datetime import datetime
import Attendance,fuzzy

gc.collect(generation=2)
path = "0729/imagesA"
images = []
classNames = []
myList = os.listdir(path)

for cla in myList:
    curImg = cv2.imread(f'{path}/{cla}')
    images.append(curImg)
    classNames.append(os.path.splitext(cla)[0])  # 擷取檔案名稱[0]<-Elon mask [1]<-.jpg


def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


encodeListKnow = findEncodings(images)
print('Encoding complete')


def faceRec(imgS, camnum):
    facesCurFrame = face_recognition.face_locations(imgS)
    encodeCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeface, faceLoc in zip(encodeCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnow, encodeface)
        faceDis = face_recognition.face_distance(encodeListKnow, encodeface)
        mathIndex = np.argmin(faceDis)
        if camnum:
            if matches[mathIndex]:
                name = classNames[mathIndex]
                print(name)
                if fuzzy.getImageVar(images[mathIndex], imgS):
                    cv2.imwrite('0729/imagesA/' + classNames[mathIndex] + '.jpg', imgS)
                y1, x2, y2, x1 = faceLoc
                # cv2.rectangle(imgS, (x1, y1), (x2, y2), (0, 25
                # 5, 0), 2, cv2.LINE_AA)
                # cv2.putText(imgS, name, (x1, y1), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 1)
                
                Attendance.markAttendance(name, 1)
                cv2.imwrite('0729/Wally/' + classNames[mathIndex] + '.jpg', imgS)

            else:
                now = datetime.now()
                filetime = now.strftime('%Y_%m_%d_%H_%M_%S')
                # Attendance.markAttendance(filetime, 1)
                Attendance.markfirst(filetime, 1)
                cv2.imwrite('0729/Wally/' + filetime + '.jpg', imgS)
                cv2.imwrite('0729/imagesA/' + filetime + '.jpg', imgS)

                # os.mkdir("Temp/" + filetime)
                # cv2.imwrite(f'Temp/{filetime}/' + filetime + '.jpg', imgS)

                imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
                images.append(imgS)
                classNames.append(filetime)
                print(classNames)
                encode = face_recognition.face_encodings(imgS)[0]
                encodeListKnow.append(encode)
        else:
            if matches[mathIndex]:
                name = classNames[mathIndex]
                Attendance.markAttendance(name, 0)
                try:
                    os.remove('0729/Wally/' + name + '.jpg')
                    print(name, "Leave")
                except OSError as e:
                    pass
                else:
                    print("File is deleted successfully")


def main():
    img = cv2.imread("0729/Elon_test.jpg")
    faceRec(img, 1)
    # cv2.imshow('0',img)
    # cv2.waitKey(0)

    # print("main")


if __name__ == '__main__':
    main()

# cap.release()
# cv2.destroyAllWindows()

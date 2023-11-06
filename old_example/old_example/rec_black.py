import numpy as np
import csv,os,gc,face_recognition,cv2
from datetime import datetime
import Attendance,fuzzy
import requests
url = 'https://notify-api.line.me/api/notify'
token = 'o69Q2giPQdVGjGjzTm2n4xmjfoiHP31ie2yz1fvesiP'
headers = { "Authorization": "Bearer " + token }


gc.collect(generation=2)
path = "0729/black"
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
                #print(name)
                data = {
                            'message':'可疑人物出現！'
                        }
                with open('0729/black/'+str(name)+'.jpg', 'rb') as f:
                                files={'imageFile':f}
                                data = requests.request("POST",url, headers=headers, data=data,files=files)
            
        else:
            if matches[mathIndex]:
                name = classNames[mathIndex]
                data = {
                            'message':'可疑人物離開！'
                        }
                with open('0729/black/'+str(name)+'.jpg', 'rb') as f:
                                files={'imageFile':f}
                                data = requests.request("POST",url, headers=headers, data=data,files=files)

           


def main():
    img = cv2.imread("0729/Elon_test.jpg")
    faceRec(img, 1)
    # cv2.imshow('0',img)
    # cv2.waitKey(0)

    # print("main")



'''
def post_data(message, token):
    try:
        url = "https://notify-api.line.me/api/notify"
        headers = {
            'Authorization': f'Bearer {token}'
        }
        payload = {
            'message': message,
            
        }
        with open('0729/black/2022_12_01_17_18_58.jpg', 'rb') as f:
                files={'imageFile':f}
                response = requests.request(
                    "POST",
                    url,
                    headers=headers,
                    data=payload,
                    files=files
                )
        if response.status_code == 200:
            print(f"Success -> {response.text}")
    except Exception as _:

        print(_)

if __name__ == "__main__":
    token = "o69Q2giPQdVGjGjzTm2n4xmjfoiHP31ie2yz1fvesiP" # 您的 Token
    message = "test"     # 要發送的訊息
    post_data(message, token)'''
if __name__ == "__main__":
    main()
# cap.release()
# cv2.destroyAllWindows()

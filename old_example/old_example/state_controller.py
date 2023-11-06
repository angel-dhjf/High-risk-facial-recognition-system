import os
import cv2
import csv
import faceRec
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import *
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
from datetime import datetime

now = datetime.now()
filetime = now.strftime('%Y_%m_%d_%H_%M_%S')

def programinit():
    classNames = []
    myList = os.listdir("0729/imagesA")
    for cla in myList:
        classNames.append(os.path.splitext(cla)[0])
    print(classNames)


def initAttendance():
    classNames = []
    myList = os.listdir("0729/imagesA")
    for cla in myList:
        classNames.append(os.path.splitext(cla)[0])
    print(classNames)

    head = ("Name", "EnterTime", "LeaveTime", "State")
    with open('0729/Attendance.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, head)
        writer.writeheader()
        for name in classNames:
            writer.writerow({'Name': name, 'EnterTime': '', 'LeaveTime': '', 'State': 'INITIAL'})
        f.close()
        

    
def inithistory():
    head = ("Name", "EnterTime", "LeaveTime", "State")
    with open('0729/history.csv', 'w', newline='') as f:
        writer = csv.DictWriter(f, head)
        f.close()



def main():
    programinit()
    while True:
        img = cv2.imread("0729/Elon_test.jpg")
        Key = input("KEY IN:")

        if Key == str('quit'):
            os._exit(0)

        if Key == str('init'):
            initAttendance()
            print("Attendance....DONE")

        if Key == str('enter'):
            faceRec.faceRec(img, 1)

        if Key == str('leave'):
            faceRec.faceRec(img, 0)

        if Key == str('initchis'):
            inithistory()
            print("clear history....DONE")

        if Key == str('ls'):
            print('------------------Attendance.csv------------------------')
            with open('0729/Attendance.csv', 'r', newline='') as f:
                text = f.read()
                print(text)
                f.close()
            print('================================================================')
        
        if Key == str('history'):
            print('------------------history.csv------------------------')
            with open('0729/history.csv', 'r', newline='') as f:
                text = f.read()
                print(text)
                f.close()
            print('================================================================')
        if Key == str('enrollblack'):
            def store(name,behavior):
                print('------------------black_behavior.csv------------------------')
                with open('0729/black_behavior.csv', 'a', newline='') as f:
                    
                    writer = csv.writer(f)
                    writer.writerow([name,behavior])
                    f.close()
                print('================================================================')

            def enroll(img):
                cv2.imwrite('0729/black/'+str(filetime)+'.jpg',img)

            def OpenFile():
                filename = askopenfilename()
                img = cv2.imdecode(np.fromfile(filename, dtype = np.uint8), cv2.IMREAD_COLOR)
                global black_img
                black_img = img
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = cv2.resize(img,(150,150))
                im = Image.fromarray(img)
                photo = ImageTk.PhotoImage(im)

                # 調整圖片位置
                #labelImg = tk.Label(img = photo)
                #labelImg.pack()
                labelimg.configure(image = photo)
                labelimg.place(x = 20, y = 72)
                labelimg.image = photo
                
            # 創建Tkinter視窗
            window = tk.Tk()
            window.title('黑名單登入系統')
            # 設定視窗大小為 640x720，視窗（左上角）在螢幕上的座標位置為 (300, 150)
            window.geometry("600x300+300+150")

            # widget 功能設定
            labelimg = tk.Label(window, image = "")
            button_1 = tk.Button(window, text ='開啟', height = 4, width = 15, bg ='gray90', font = ("標楷體", 16), command = OpenFile)
            button_2 = tk.Button(window, text = '儲存', height = 4, width = 15, bg ='gray90', font = ("標楷體", 16), command = lambda:[store(filetime,msg.get()),enroll(black_img)])
            #button_3 = tk.Button(window, text = '歷史紀錄', height = 1, width = 15, bg ='gray85', font = ("標楷體", 14))
            msg = tk.StringVar() 
            #label_1 = tk.Label(window, text = "不良行為:", height = 1, width = 10, font = ("標楷體", 20, "bold"))
            #entry_1 = tk.Entry(window, borderwidth = 5, font = ("標楷體", 14), textvariable=msg)

            # widget 位置設定                
            labelimg.place(x = 1, y = 1)
            button_1.place(x = 230, y = 10)
            button_2.place(x = 230, y = 120)
            #button_3.place(x = 230, y = 110)
            #label_1.place(x = 240, y = 170)
            #entry_1.place(x = 260, y = 220, width = 100, height = 40)

            window.mainloop()
if __name__ == '__main__':
    main()

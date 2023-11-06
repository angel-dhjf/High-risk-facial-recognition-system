import csv
import os
import pandas
from datetime import datetime
import cv2

attcsv = '0729/Attendance.csv'
def markfirst(name, state):
    now = datetime.now()
    dtString = now.strftime('%Y:%m:%d:%H:%M:%S')
    df = pandas.read_csv(attcsv)
    if state:
        try:
            df.to_csv(attcsv, index=False)
            with open(attcsv, 'a+', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([name, dtString, '', 'ENTER'])
                print("written")
        except:
            print("markfirst fail")



def markAttendance(name, state):
    
    now = datetime.now()
    dtString = now.strftime('%Y:%m:%d:%H:%M:%S')
    df = pandas.read_csv(attcsv)
    # print(df)
    
    if state:
        for i in range(len(df)):
            # print(str(df["Name"][i]),name)
            if str(df["Name"][i]) == name:
                df.drop(i, inplace=True)
                df.to_csv(attcsv, index=False)
                with open(attcsv, 'a+', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerow([name, dtString, '', 'ENTER'])
                    # print("written")
                    f.close()
                break
    else:
        for i in range(len(df)):
            if str(df["Name"][i]) == name:
                if df["State"][i] == 'INITIAL':
                    print(name, "not exist")
                    break
                if df["State"][i] == 'ENTER' or (df["State"][i] == 'LEAVE' and df["LeaveTime"][i] == dtString):
                    entertime = df["EnterTime"][i]
                    df.drop(i, inplace=True)
                    df.to_csv(attcsv, index=False)
                    with open(attcsv, 'a', newline='') as f:
                        writer = csv.writer(f)
                        writer.writerow([name, "", "", "INITIAL"])
                    with open('0729/history.csv', 'a', newline='') as f1:
                        writer1 = csv.writer(f1)
                        writer1.writerow([name, entertime, dtString, "DONE"])
                    f.close()
                    f1.close()
                else:
                    # print(df["State"].isnull().T.any())
                    print("error occurs..\"State\" wrong")
                # if df["State"][i] == 'LEAVE' and df["EnterTime"][i].isnull().T.any() \
                #         and df["LeaveTime"][i].isnull().T.any():
                #
                # if not os.path.isfile(f'history/{name}'):
                #     os.mkdir("history/" + name)
                #
                # cv2.imwrite(f'history/{name}/' + name + '.jpg', imgS)

                # with open('Attendance.csv', 'a', newline='') as f:
                #     writer = csv.writer(f)
                #     writer.writerow([name, 'State wrong', dtString, "LEAVE"])
                # f.close()

                # if df["State"][i] == 'LEAVE' and df["LeaveTime"][i]==dtString:

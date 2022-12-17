# import PySimpleGUI as sg
# import cv2
# import numpy as np
# import time
# import datetime
# import pandas
# import os
# from humanize import naturalsize

# def doThis():    
#         pass

# def storePref(lr,md,nf):
#     with open("db.txt","w") as f:
#         f.write(str(lr)+"\n")
#         f.write(str(md)+"\n")
#         f.write(str(nf))
#         f.close()

# def loadPref():
#     with open("db.txt","r") as f:
#         return f.readlines()

# def main():
#     #Storage Buffer Check
#     size = 0
#     storage = "Local Storage/"

#     for path, dirs, files in os.walk(storage):
#         for f in files:
#             fp = os.path.join(path, f)
#             size += os.path.getsize(fp)

#     # print("Folder size: " + naturalsize(size))
#     if size>1000000000: #more than 1 gb
#         doThis()

#     startTime = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
#     os.mkdir(f"{storage}/{startTime}")
#     os.mkdir(f"{storage}/{startTime}/Faces")
#     os.mkdir(f"{storage}/{startTime}/Recordings")
#     cap = cv2.VideoCapture(0)

#     face_cascade = cv2.CascadeClassifier(
#         cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
#     body_cascade = cv2.CascadeClassifier(
#         cv2.data.haarcascades + "haarcascade_fullbody.xml")

#     data = []
#     df = pandas.DataFrame(columns = ["Start", "End", "Face", "Recording"])

#     lr,md,nf = loadPref()
#     lr = int(lr)
#     md = int(md)
#     nf = int(nf)

#     detection = False
#     detection_stopped_time = None
#     timer_started = False
#     SECONDS_TO_RECORD_AFTER_DETECTION = 1
#     # sct = mss()

#     cap.set(3, 1280)
#     cap.set(4, 720)
#     frame_size = (int(cap.get(3)), int(cap.get(4)))
#     fourcc = cv2.VideoWriter_fourcc(*"mp4v")

#     sg.theme('DarkGreen2')

#     # define the window layout
#     layout = [[sg.Text('OpenCV Demo', size=(40, 1), justification='center', font='Helvetica 20')],
#               [sg.Image(filename='', key='image')],
#               [sg.Button('Record', size=(10, 1), font='Helvetica 14'),
#                sg.Button('Stop', size=(10, 1), font='Any 14'),
#                sg.Button('Exit', size=(10, 1), font='Helvetica 14')], 
#                  [sg.Checkbox('Live Recording:', default=lr, key="-IN-"),
#                  sg.Checkbox('Motion Detection:', default=md, key="md"),
#                  sg.Checkbox('Notifications:', default=nf, key="nf")]]

#     # create the window and show it without the plot
#     window = sg.Window('Demo Application - OpenCV Integration',
#                        layout, location=(800, 400))

#     # ---===--- Event LOOP Read and display frames, operate the GUI --- #
#     recording = False

#     while True:
#         event, values = window.read(timeout=20)
#         if event == 'Exit' or event == sg.WIN_CLOSED:
#             storePref(lr,md,nf)
#             print(lr,md,nf)
#             return

#         elif event == 'Record':
#             recording = True

#         elif event == 'Stop':
#             recording = False
#             img = np.full((480, 640), 255)
#             # this is faster, shorter and needs less includes
#             imgbytes = cv2.imencode('.png', img)[1].tobytes()
#             window['image'].update(data=imgbytes)

#         elif values["-IN-"] == 0:
#             lr = 0
        
#         elif values["md"] == 0:
#             md = 0
        
#         elif values["nf"] == 0:
#             nf = 0

#         elif values["-IN-"] == 1:
#             lr = 1
        
#         elif values["md"] == 1:
#             md = 1
        
#         elif values["nf"] == 1:
#             nf = 1

#         if recording:
#             _, frame = cap.read()
#             imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
#             window['image'].update(data=imgbytes)
#             _, frame = cap.read()
#             live = cv2.VideoWriter(
#                         f"{storage}/{startTime}/live.mkv", fourcc, 20, frame_size)
#             gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#             faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#             bodies = face_cascade.detectMultiScale(gray, 1.3, 5)
#             counter = len(data)+1
#             if len(faces) + len(bodies) > 0:
#                 if detection:
#                     timer_started = False
#                 else:
#                     detection = True
#                     timeIn = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
#                     cv2.imwrite(f"{storage}/{startTime}/Faces/face{counter}.jpg",frame)
#                     out = cv2.VideoWriter(
#                         f"{storage}/{startTime}/Recordings/face{counter}.mkv", fourcc, 20, frame_size)
#                     print("Started Recording!")
#             elif detection:
#                 if timer_started:
#                     if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
#                         detection = False
#                         timer_started = False
#                         out.release()
#                         timeOut = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
#                         print(f'Stop Recording!')
#                         data.append([timeIn, timeOut, f"{storage}/{startTime}/Faces/face{counter}.png",f"{storage}/Recordings/face{counter}.png"])
#                 else:
#                     timer_started = True
#                     detection_stopped_time = time.time()

#             if detection:
#                 out.write(frame)
#             live.write(frame)
#             # cv2.imshow("Security Camera", frame)

#             if cv2.waitKey(1) == ord('q'):
#                 break

#     print("Live Recording off!")
#     for i in data:
#         df = df.append({"Start":i[0], "End":i[1], "Face":i[2], "Recording":i[3]}, ignore_index = True)
#     endTime = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
#     df.to_csv(f"{storage}/{startTime}/Security Data {startTime} to {endTime}.csv")
#     out.release()
#     cap.release()
#     cv2.destroyAllWindows()
#     storePref(lr,md,nf)
#     print(lr,md,nf)

# main()

import PySimpleGUI as sg
import cv2
import numpy as np
import time
import datetime
import pandas
import os
from humanize import naturalsize
import threading
from client import sendData 
from motionDetection import motion_detection

data = []
dcounter = 0
def listener():
    global dcounter    
    if len(data) > dcounter:
        print(sendData(data[-1],"shs"))
    dcounter = len(data)

def storePref(lr,md,nf):
    with open("db.txt","w") as f:
        f.write(str(int(lr))+"\n")
        f.write(str(int(md))+"\n")
        f.write(str(int(nf)))
        f.close()

def loadPref():
    with open("db.txt","r") as f:
        return f.readlines()

def main():
    #Storage Buffer Check
    size = 0
    storage = "Local Storage/"

    for path, dirs, files in os.walk(storage):
        for f in files:
            fp = os.path.join(path, f)
            size += os.path.getsize(fp)

    # print("Folder size: " + naturalsize(size))
    if size>1000000000: #more than 1 gb
        # doThis()
        pass

    startTime = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    os.mkdir(f"{storage}/{startTime}")
    os.mkdir(f"{storage}/{startTime}/Faces")
    os.mkdir(f"{storage}/{startTime}/Recordings")
    cap = cv2.VideoCapture(0)

    df = pandas.DataFrame(columns = ["Start", "End", "Face", "Recording"])

    lr,md,nf = loadPref()
    lr = int(lr)
    md = int(md)
    nf = int(nf)

    detection = False
    detection_stopped_time = None
    timer_started = False
    SECONDS_TO_RECORD_AFTER_DETECTION = 1

    cap.set(3, 1280)
    cap.set(4, 720)
    frame_size = (int(cap.get(3)), int(cap.get(4)))
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    sg.theme('DarkGreen2')

    # define the window layout
    layout = [[sg.Text('OpenCV Demo', size=(40, 1), justification='center', font='Helvetica 20')],
              [sg.Image(filename='', key='image')],
              [sg.Button('Record', size=(10, 1), font='Helvetica 14'),
               sg.Button('Stop', size=(10, 1), font='Any 14'),
               sg.Button('Exit', size=(10, 1), font='Helvetica 14')], 
                 [sg.Checkbox('Live Recording', default=lr, key="lr"),
                 sg.Checkbox('Motion Detection', default=md, key="md"),
                 sg.Checkbox('Notifications', default=nf, key="nf")]]

    # create the window and show it without the plot
    window = sg.Window('Demo Application - OpenCV Integration',
                       layout, location=(800, 400))

    # ---===--- Event LOOP Read and display frames, operate the GUI --- #
    recording = False

    while True:
        event, values = window.read(timeout=20)
        if event == 'Exit' or event == sg.WIN_CLOSED:
            
            storePref(lr,md,nf)
            print(lr,md,nf)
            return

        elif event == 'Record':
            recording = True

        elif event == 'Stop':
            recording = False
            img = np.full((480, 640), 255)
            # this is faster, shorter and needs less includes
            imgbytes = cv2.imencode('.png', img)[1].tobytes()
            window['image'].update(data=imgbytes)
        lr,md,nf = values["lr"],values["md"],values["nf"]

        if recording:
            _, frame = cap.read()
            imgbytes = cv2.imencode('.png', frame)[1].tobytes()  # ditto
            window['image'].update(data=imgbytes)
            _, frame = cap.read()
            live = cv2.VideoWriter(
                        f"{storage}/{startTime}/live.mkv", fourcc, 20, frame_size)
            
            counter = len(data)+1
            motionDetector = threading.Thread(target=motion_detection(frame))
            detection = motionDetector.start()
            if detection:
                timer_started = False
            else:
                detection = True
                timeIn = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                cv2.imwrite(f"{storage}/{startTime}/Faces/face{counter}.jpg",frame)
                out = cv2.VideoWriter(
                    f"{storage}/{startTime}/Recordings/face{counter}.mkv", fourcc, 20, frame_size)
                print("Started Recording!")
        elif detection:
            if timer_started:
                if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
                    detection = False
                    timer_started = False
                    out.release()
                    timeOut = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
                    print(f'Stop Recording!')
                    data.append([timeIn, timeOut, f"{storage}/{startTime}/Faces/face{counter}.png",f"{storage}/Recordings/face{counter}.png"])
            else:
                timer_started = True
                detection_stopped_time = time.time()

        if detection:
            out.write(frame)
            live.write(frame)
            cv2.imshow("Security Camera", frame)

            if cv2.waitKey(1) == ord('q'):
                break

    print("Live Recording off!")
    for i in data:
        df = df.append({"Start":i[0], "End":i[1], "Face":i[2], "Recording":i[3]}, ignore_index = True)
    endTime = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
    df.to_csv(f"{storage}/{startTime}/Security Data {startTime} to {endTime}.csv")
    # out.release()
    cap.release()
    cv2.destroyAllWindows()
    storePref(int(lr),int(md),int(nf))
    # print(lr,md,nf)
main = threading.Thread(target=main())
listener = threading.Thread(target=listener())
main.start()
listener.start()
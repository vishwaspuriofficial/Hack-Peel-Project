import cv2
import time
import datetime
import pandas
import os
from humanize import naturalsize

def doThis():    
    pass

#Storage Buffer Check
size = 0
storage = "Local Storage/"

for path, dirs, files in os.walk(storage):
    for f in files:
        fp = os.path.join(path, f)
        size += os.path.getsize(fp)

print("Folder size: " + naturalsize(size))
if size>1000000000: #more than 1 gb
    doThis()

startTime = datetime.datetime.now().strftime("%d-%m-%Y %H-%M-%S")
os.mkdir(f"{storage}/{startTime}")
os.mkdir(f"{storage}/{startTime}/Faces")
os.mkdir(f"{storage}/{startTime}/Recordings")
cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
body_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_fullbody.xml")

data = []
df = pandas.DataFrame(columns = ["Start", "End", "Face", "Recording"])

detection = False
detection_stopped_time = None
timer_started = False
SECONDS_TO_RECORD_AFTER_DETECTION = 1
# sct = mss()

cap.set(3, 1280)
cap.set(4, 720)
frame_size = (int(cap.get(3)), int(cap.get(4)))
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

while True:
    _, frame = cap.read()
    live = cv2.VideoWriter(
                f"{storage}/{startTime}/live.mkv", fourcc, 20, frame_size)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = face_cascade.detectMultiScale(gray, 1.3, 5)
    counter = len(data)+1
    if len(faces) + len(bodies) > 0:
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
out.release()
cap.release()
cv2.destroyAllWindows()
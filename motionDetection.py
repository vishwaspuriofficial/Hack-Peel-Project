import cv2

def motion_detection(frame):
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    body_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + "haarcascade_fullbody.xml")
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    bodies = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    if len(faces) + len(bodies) > 0:
        return True
        
            # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            # bodies = face_cascade.detectMultiScale(gray, 1.3, 5)
            #     if detection:
            #     timer_started = False
            # else:
            #     detection = True
            #     timeIn = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            #     cv2.imwrite(f"{storage}/{startTime}/Faces/face{counter}.jpg",frame)
            #     out = cv2.VideoWriter(
            #         f"{storage}/{startTime}/Recordings/face{counter}.mkv", fourcc, 20, frame_size)
            #     print("Started Recording!")
            # elif detection:
            #     if timer_started:
            #         if time.time() - detection_stopped_time >= SECONDS_TO_RECORD_AFTER_DETECTION:
            #             detection = False
            #             timer_started = False
            #             out.release()
            #             timeOut = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            #             print(f'Stop Recording!')
            #             data.append([timeIn, timeOut, f"{storage}/{startTime}/Faces/face{counter}.png",f"{storage}/Recordings/face{counter}.png"])
            #     else:
            #         timer_started = True
            #         detection_stopped_time = time.time()

            # if detection:
            #     out.write(frame)

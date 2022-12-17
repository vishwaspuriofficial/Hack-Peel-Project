import zeroconf
import zeroconf.asyncio
import socket
import asyncio
import tkinter as tk
import threading
import vlc
import os
from time import sleep

    

instance = zeroconf.Zeroconf()
ip = ""
port = 4338
size = 1024

# Register a socket service on tcp with service name "CameraServer"
info = zeroconf.ServiceInfo(
    "_http._tcp.local.",
    "CameraServer._http._tcp.local.",
    port=port,
)
instance.register_service(info=info)
def VideoReceiver():
    # Create a socket and bind it to the port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((ip, port))
    while True:
        # Listen for connections
        s.listen(1)

        # Accept a connection
        conn, addr = s.accept()

        # Receive data
        # First receive the name of the file
        filename = conn.recv(size).decode(encoding="UTF-8", errors="ignore")
        # Then receive the file and write it to output/
        # avoid null character issues on windows
        print(filename)
        with open("output/"+filename, 'wb') as f:
            while True:
                data = conn.recv(size)
                if not data:
                    break
                f.write(data)
            f.close()


        # Close the connection
        conn.close()

# Create a video receiver thread
thread = threading.Thread(target=VideoReceiver)
thread.start()

# Create a tkinter window
root = tk.Tk()
root.title("Camera Server")
# start maximized
root.state('zoomed')
# create a menu
menubar = tk.Menu(root)
# display all the different cameras
for camera in os.listdir("output"):
    # create a menu item for each camera
    menubar.add_command(label=camera)
    # create a frame for each camera
    frame = tk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True)
    # create a canvas for each camera
    canvas = tk.Canvas(frame)
    canvas.pack(fill=tk.BOTH, expand=True)
    # create a label for each camera
    label = tk.Label(canvas)
    label.pack(fill=tk.BOTH, expand=True)
    # For each camera, in the folder output/camera, there are regular files and motion detected files
    # The regular files are the lower resolution videos
    # The motion detected files are the higher resolution videos
    # The regular files are named with the format "YYYY-MM-DD HH-MM-SS.mp4"
    # and are a minute long each
    # The motion detected files are named with the format "YYYY-MM-DD HH-MM-SS Motion.mp4"
    # and there is no limit to the length of the video

    # Display a list of all of the timeframes that have motion detected videos
    # and a list of all of the timeframes that have regular videos
    # The user can click on a timeframe to view the video
    # The user can also click on a timeframe to view the motion detected video
    # create a scrolldown menu for each list
    scrolldownRegular = tk.Scrollbar(canvas)
    scrolldownRegular.pack(side=tk.RIGHT, fill=tk.Y)
    scrolldownMotion = tk.Scrollbar(canvas)
    scrolldownMotion.pack(side=tk.RIGHT, fill=tk.Y)
    # create a listbox for each list
    listboxRegular = tk.Listbox(canvas, yscrollcommand=scrolldownRegular.set)
    listboxRegular.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    listboxMotion = tk.Listbox(canvas, yscrollcommand=scrolldownMotion.set)
    listboxMotion.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    # Create a list of all of the regular videos
    regularvideos = []
    # Create a list of all of the motion detected videos
    motionvideos = []
    # For each file in the camera folder
    for file in os.listdir("output/"+camera):
        # If the file is a regular video
        if file[-4:] == ".mkv" and "Motion" not in file:
            # Add the file to the regular videos list
            regularvideos.append(file)
        # If the file is a motion detected video
        elif file[-4:] == ".mp4" and "Motion" in file:
            # Add the file to the motion detected videos list
            motionvideos.append(file)
    # Sort the regular videos list
    regularvideos.sort()
    # Sort the motion detected videos list
    motionvideos.sort()
    # display the regular videos list
    for video in regularvideos:
        listboxRegular.insert(tk.END, video)
    # display the motion detected videos list
    for video in motionvideos:
        listboxMotion.insert(tk.END, video)
# Create a function to play a video
def playVideo(video):
    # Create a video player
    player = vlc.MediaPlayer("output/"+camera+"/"+video)
    # Play the video
    player.play()
    # Create a function to stop the video
    def stopVideo():
        # Stop the video
        player.stop()
    # Create a button to stop the video
    button = tk.Button(root, text="Stop", command=stopVideo)
    button.pack()

# tkinter mainloop
root.mainloop()



# Unregister the service
instance.unregister_service(info=info)

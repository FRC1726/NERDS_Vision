import cv2
import numpy as np
import VisionGuide

#robot_width = 34
robot_width = 25
camera_z = 22.5
camera_x = -9
camera_y = 13

cap = cv2.VideoCapture(1)
guide = VisionGuide.RobotGuide(68.5, [640, 480], 22)
guide.set_offset(camera_x, camera_y, camera_z)
guide.add_marker(60, [255,0,0])
guide.add_marker(117.5, [0,255,0])
guide.add_marker(0, [0,0,255])

target = VisionGuide.Reticle(68, [640, 480])
target.set_offset(0,0,2)
target.add_marker((0,10,0), 2, [255,0,0])

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    #print(frame.shape)

    guide.draw(frame)
    target.draw(frame)

    cv2.imshow("Show", frame)

    if cv2.waitKey(60) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
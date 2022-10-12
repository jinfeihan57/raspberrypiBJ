import cv2

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('M','J','P','G'))
#cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('H','2','6','4'))
#cap.set(cv2.CAP_PROP_BUFFERSIZE, 10)
cap.set(cv2.CAP_PROP_FPS, 10) #30 can not change
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320.0) #640 can not big 调低分辨率延时更低
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480.0) #480 can not big
print(cap.get(cv2.CAP_PROP_BUFFERSIZE))
print(cap.get(cv2.CAP_PROP_FPS))
print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    cv2.imshow('MediaPipe Holistic', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()

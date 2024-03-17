
# Import necessary modules
from django.http import StreamingHttpResponse
from django.views.decorators import gzip
import cv2
import os

# Initialize pose detector and webcam capture
from cvzone.PoseModule import PoseDetector

detector = PoseDetector()
cap = cv2.VideoCapture(0)
shirtFolderPath = "stream/resources/Shirts"
listShirts = os.listdir(shirtFolderPath)
fixedRatio = 334 / 49
shirtRatioHeightWidth = 900 / 500

# Define the streaming view
@gzip.gzip_page
def video_feed(request):
    def frame_generator():
        while True:
            success, img = cap.read()
            img = detector.findPose(img)
            img = cv2.flip(img,1)
            lmList, bboxInfo = detector.findPosition(img, draw=False, bboxWithHands=False)
            if lmList:
                lm11 = lmList[11][1:3]
                lm12 = lmList[12][1:3]
                imgShirt = cv2.imread(os.path.join(shirtFolderPath,listShirts[0]),cv2.IMREAD_UNCHANGED)
                imgShirt = cv2.resize(imgShirt,(0,0),None,0.5,0.5)

                widthOfShirt = int(lm11[0]-lm12[0]) * fixedRatio
                currentScale = (lm11[0] - lm12[0]) / 190
                offset = int(44 * currentScale), int(48 * currentScale)
                try:
                    img = cvzone.overlayPNG(img, imgShirt, (lm12[0]-offset[0],lm12[1]-offset[1]))
                except:
                    pass

            ret, jpeg = cv2.imencode('.jpg', img)
            frame_bytes = jpeg.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n\r\n')

    return StreamingHttpResponse(frame_generator(), content_type='multipart/x-mixed-replace; boundary=frame')


import numpy as np
import cv2 as cv
import time
import argparse
confidence_threshold = 0.5
nms_threshold = 0.4
num_classes = 80

ap.add_argument("-gpu", "--use-gpu", type=number, default=1, help="Use GPU if the config -gpu=1")
args = vars(ap.parse_args())

print("[INFO] loading YOLO from disk...")
net = cv.dnn.readNet(model="../yolos/yolov3.weights", config="../yolos/yolov3.cfg")

if(arg["use-gpu"] == 1):
	print("[INFO] Using GPU: setting preferable backend and target to CUDA...")
	net.setPreferableBackend(cv.dnn.DNN_BACKEND_CUDA)
	net.setPreferableTarget(cv.dnn.DNN_TARGET_CUDA)
else:
	print("[INFO] Using CPU.")

image = cv.imread("../yolos/dog.jpg")
blob = cv.dnn.blobFromImage(image, 0.00392, (416, 416), [0, 0, 0], True, False)

# warmup
for i in range(3):
	net.setInput(blob)
	detections = net.forward(net.getUnconnectedOutLayersNames())

# benchmark
start = time.time()
for i in range(100):
	net.setInput(blob)
	detections = net.forward(net.getUnconnectedOutLayersNames())
end = time.time()

ms_per_image = (end - start) * 1000 / 100

print("Time per inference: %f ms" % (ms_per_image))
print("FPS: ", 1000.0 / ms_per_image)

import cv2
import numpy as np
import time
import sys
import os

# Check if the image path is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python detect.py <image_path>")
    sys.exit(1)

image_path = sys.argv[1]

# loading class labels YOLO model was trained on
labelsPath = 'obj.names'
LABELS = open(labelsPath).read().strip().split("\n")

# load weights and cfg
weightsPath = 'crop_weed_detection.weights'
configPath = 'crop_weed.cfg'
# color selection for drawing bbox
COLORS = np.random.randint(0, 255, size=(len(LABELS), 3), dtype="uint8")
print("Loading Images from disk...")
net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

# load our input image and grab its spatial dimensions
image = cv2.imread('static/uploads/user_image.jpg')
(H, W) = image.shape[:2]

# parameters
confi = 0.5
thresh = 0.5

# determine only the *output* layer names that we need from YOLO
ln = net.getLayerNames()
ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

# construct a blob from the input image and then perform a forward
# pass of the YOLO object detector, giving us our bounding boxes and
# associated probabilities
blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (512, 512), swapRB=True, crop=False)
net.setInput(blob)
start = time.time()
layerOutputs = net.forward(ln)
end = time.time()

# show timing information on YOLO
print("YOLO took {:.6f} seconds".format(end - start))

# initialize our lists of detected bounding boxes, confidences, and
# class IDs, respectively
boxes = []
confidences = []
classIDs = []

# loop over each of the layer outputs
for output in layerOutputs:
    # loop over each of the detections
    for detection in output:
        # extract the class ID and confidence (i.e., probability) of
        # the current object detection
        scores = detection[5:]
        classID = np.argmax(scores)
        confidence = scores[classID]

        # filter out weak predictions by ensuring the detected
        # probability is greater than the minimum probability
        if confidence > confi:
            # scale the bounding box coordinates back relative to the
            # size of the image, keeping in mind that YOLO actually
            # returns the center (x, y)-coordinates of the bounding
            # box followed by the boxes' width and height
            box = detection[0:4] * np.array([W, H, W, H])
            (centerX, centerY, width, height) = box.astype("int")

            # use the center (x, y)-coordinates to derive the top and
            # and left corner of the bounding box
            x = int(centerX - (width / 2))
            y = int(centerY - (height / 2))

            # update our list of bounding box coordinates, confidences,
            # and class IDs
            boxes.append([x, y, int(width), int(height)])
            confidences.append(float(confidence))
            classIDs.append(classID)

# apply non-maxima suppression to suppress weak, overlapping bounding
# boxes
idxs = cv2.dnn.NMSBoxes(boxes, confidences, confi, thresh)
print("Detections done\nDrawing bounding boxes...")
# ensure at least one detection exists
if len(idxs) > 0:
    # loop over the indexes we are keeping
    for i in idxs.flatten():
        # extract the bounding box coordinates
        (x, y) = (boxes[i][0], boxes[i][1])
        (w, h) = (boxes[i][2], boxes[i][3])

        # draw a bounding box rectangle and label on the image
        color = [int(c) for c in COLORS[classIDs[i]]]
        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
        print("[ACCURACY] : accuracy -> ", confidences[i])
        print("[OUTPUT]   : detected label -> ", LABELS[classIDs[i]])
        text = "{} : {:.4f}".format(LABELS[classIDs[i]], confidences[i])
        cv2.putText(image, text, (x, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)

# Display the image
# cv2.imshow('Output', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Save the annotated image
output_folder = 'static/output'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

output_image_path = os.path.join(output_folder, 'annotated_image.jpg')
cv2.imwrite(output_image_path, image)

# Print the output image path
print(output_image_path)

# Prepare the detection results as a JSON response
detection_results = {
    'accuracy': confidences[i],
    'detected_label': LABELS[classIDs[i]]
}

# Save accuracy and detected label to a text file for unique detections
output_text_path = os.path.join(output_folder, 'detection_results.txt')
with open(output_text_path, 'w') as text_file:
    seen_labels = set()
    for i in range(len(boxes)):
        detected_label = LABELS[classIDs[i]]
        if detected_label not in seen_labels:
            text_file.write("Accuracy -> {:.4f}\n".format(confidences[i]))
            text_file.write("Detected Label -> {}\n".format(detected_label))
            seen_labels.add(detected_label)

# Print the output paths
print("Output image saved at:", output_image_path)
print("Detection results saved at:", output_text_path)

print("[STATUS]   : Completed")
print("[END]")

# Output the detection results as JSON
import json
print(json.dumps(detection_results))    

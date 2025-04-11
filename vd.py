import cv2
import numpy as np
import csv
import datetime as dt
import streamlit as st

def logic(image_path):
    # Load YOLO pre-trained model for vehicle detection
    net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")

    # Load the COCO names file (contains class names)
    classes = []
    with open("coco.names", "r") as f:
        classes = f.read().strip().split("\n")

    # Load the image
    #image_path = "image1.jpg"
    image = cv2.imread(image_path)

    # Get image dimensions
    height, width, _ = image.shape

    # Preprocess the image for YOLO
    blob = cv2.dnn.blobFromImage(image, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

    # Set input blob for the network
    net.setInput(blob)

    # Get output layer names
    output_layers = net.getUnconnectedOutLayersNames()

    # Perform forward pass and get detections
    detections = net.forward(output_layers)

    # Initialize lists for NMS
    boxes = []
    confidences = []
    class_ids = []

    # Loop through detections
    for detection in detections:
        for obj in detection:
            scores = obj[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5 and (class_id == 2 or class_id == 0):  # Class ID for cars is 2, person is 0 (for bikes)
                center_x = int(obj[0] * width)
                center_y = int(obj[1] * height)
                w = int(obj[2] * width)
                h = int(obj[3] * height)

                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    # Apply Non-Maximum Suppression
    indices = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    vehicle_count = len(indices)

    # Correctly access indices
    for i in indices.flatten():
        box = boxes[i]
        x, y, w, h = box[0], box[1], box[2], box[3]

        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image, "Vehicle", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


    with open('vehicle_log.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([dt.datetime.now(), vehicle_count])

    # Display the image with detections

    # Convert the image from BGR (OpenCV default) to RGB (Streamlit requirement)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    # Add a border (frame) around the image
    frame_thickness = 10  # Thickness of the border
    border_color = (0, 0, 0)  # Black border in RGB
    framed_image = cv2.copyMakeBorder(
        image_rgb,
        frame_thickness,
        frame_thickness,
        frame_thickness,
        frame_thickness,
        cv2.BORDER_CONSTANT,
        value=border_color,
    )
    # Display the image in Streamlit
    st.write("The below image shows the identified vehicles")
    st.image(framed_image, caption="Displayed Using OpenCV", use_column_width=True)

    #cv2.imshow("Vehicle Detection", image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

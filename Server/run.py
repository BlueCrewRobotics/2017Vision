import cv2
import networktables
from networktables import NetworkTable
from grip_normal import GripPipeline

def extra_processing(pipeline):
    center_x_positions = []
    center_y_positions = []
    widths = []
    heights = []

    # Find the bounding boxes of the contours to get x, y, width, and height
    for contour in pipeline.filter_contours_output:
        x, y, w, h = cv2.boundingRect(contour)
        center_x_positions.append(x + w / 2)  # X and Y are coordinates of the top-left corner of the bounding box
        center_y_positions.append(y + h / 2)
        widths.append(w)
        heights.append(y)
    
    # Publish to the '/vision' network table
    table = NetworkTable.getTable("/vision")
    table.putValue("centerX", center_x_positions)
    table.putValue("centerY", center_y_positions)
    table.putValue("width", widths)
    table.putValue("height", heights)

def main():
    print('Initializing NetworkTables')
    NetworkTable.setClientMode()
    NetworkTable.setIPAddress('localhost')
    NetworkTable.initialize()

    print('Creating Video Capture')
    cap = cv2.VideoCapture(1)

    print('Creating Pipeline')
    pipeline = GripPipeline()

    print('Running Pipeline')
    while cap.isOpened():
        have_frame, frame = cap.read()
        if have_frame:
            pipeline.process(frame)
            extra_processing(pipeline)

    print('Capture Closed')


if __name__ == '__main__':
    main()
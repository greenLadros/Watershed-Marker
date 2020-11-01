#ivri korem 2020
'''
app that lets you create costum seed markers 
on an image for the watershed algorithm,
and shows the result.
'''

#init
from matplotlib import cm
import cv2
import numpy as np

#reading image
img = cv2.imread('img.jpg')

# the image we see
img_copy = np.copy(img)

#the image keeping track of the markers
marker_image = np.zeros(img.shape[:2],dtype=np.int32)

# the result
segments = np.zeros(img.shape,dtype=np.uint8)

#creating colors to draw with
colors = []
n_markers = 10

def create_rgb(i):
    x = np.array(cm.tab10(i))[:3]*255
    return tuple(x)

for i in range(n_markers):
    colors.append(create_rgb(i))


# Default settings
current_marker = 1
marks_updated = False

def mouse_callback(event, x, y, flags, param):
    global marks_updated 

    if event == cv2.EVENT_LBUTTONDOWN:
        
        # TRACKING FOR MARKERS
        cv2.circle(marker_image, (x, y), 10, (current_marker), -1)
        
        # DISPLAY ON USER IMAGE
        cv2.circle(img_copy, (x, y), 10, colors[current_marker], -1)
        marks_updated = True

cv2.namedWindow('Image')
cv2.setMouseCallback('Image', mouse_callback)

while True:
    
    # Show the 2 windows
    cv2.imshow('WaterShed Segments', segments)
    cv2.imshow('Image', img_copy)
        
        
    # Close everything if Esc is pressed
    k = cv2.waitKey(1)

    if k == 27:
        break
        
    # Clear all colors and start over if 'c' is pressed
    elif k == ord('c'):
        img_copy = img.copy()
        marker_image = np.zeros(img.shape[0:2], dtype=np.int32)
        segments = np.zeros(img.shape,dtype=np.uint8)
        
    # If a number 0-9 is chosen index the color
    elif k > 0 and chr(k).isdigit():
        # chr converts to printable digit
        current_marker  = int(chr(k))
    
    # If we clicked somewhere, call the watershed algorithm on our chosen markers
    if marks_updated:
        
        marker_image_copy = marker_image.copy()
        cv2.watershed(img, marker_image_copy)
        segments = np.zeros(img.shape,dtype=np.uint8)
        
        for color_ind in range(n_markers):
            segments[marker_image_copy == (color_ind)] = colors[color_ind]
        
        marks_updated = False
        
cv2.destroyAllWindows()
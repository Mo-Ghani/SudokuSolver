from PIL import Image, ImageDraw, ImageFont
import imageio
import numpy as np
import os
import cv2

image_folder = 'sudoku'
video_name = 'solve.avi'

images = [img for img in os.listdir(image_folder) if img.endswith(".PNG")]
frame = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = frame.shape

video = cv2.VideoWriter(video_name, 0, 30, (width,height))

for image in images:
    video.write(cv2.imread(os.path.join(image_folder, image)))

cv2.destroyAllWindows()
video.release()





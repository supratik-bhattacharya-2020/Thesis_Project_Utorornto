import cv2
import numpy as np
img1 = cv2.imread('ann_black_9-11.png')
img2 = cv2.imread('full-black_9-11.png')
sub_img = cv2.subtract(img1,img2)
cv2.imshow('Image after sub:',sub_img)
cv2.imwrite('annotate_for_b-w.png(2)',sub_img)
cv2.waitKey(10)

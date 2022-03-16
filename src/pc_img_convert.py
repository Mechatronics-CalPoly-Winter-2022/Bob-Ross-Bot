import sys
import os
import cv2
import numpy as np
from matplotlib import pyplot as plt

# fix the path for the os
def fixpath(path):
    return os.path.abspath(os.path.expanduser(path))

if __name__ == '__main__':
    if len(sys.argv) > 1:
        img = cv2.imread(sys.argv[1], cv2.IMREAD_UNCHANGED)
    else:
        img = cv2.imread('data/img/SimpleDino.jpg', cv2.IMREAD_UNCHANGED)

    # make the image square
    h, w, c = img.shape
    h = w = min(h, w)
    img = img[:h, :w, :c]

    # resize the image to 200x200
    size = (100, 100)
    img = cv2.resize(img, size, interpolation=cv2.INTER_LANCZOS4)

    # convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # thresholding the image
    ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY or cv2.THRESH_OTSU)

    # reducing noise
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    cv2.imshow('orig', img)
    cv2.imshow('thresh', thresh)
    cv2.imshow('opening', opening)
    cv2.waitKey(0)

    # output = cv2.connectedComponentsWithStats(opening, 8, cv2.CV_32S)
    # num_labels, labels, stats, centroids = output

    # for i in range(0, num_labels):
    #     if i == 0:
    #         text = f"examining component {i+1}/{num_labels} (background)"
    #     else:
    #         text = f"examining component {i+1}/{num_labels}"

    #     print(f"[INFO] {text}")

    #     x = stats[i, cv2.CC_STAT_LEFT]
    #     y = stats[i, cv2.CC_STAT_TOP]
    #     w = stats[i, cv2.CC_STAT_WIDTH]
    #     h = stats[i, cv2.CC_STAT_HEIGHT]
    #     area = stats[i, cv2.CC_STAT_AREA]
    #     (cX, cY) = centroids[i]

    #     output = img.copy()
    #     cv2.rectangle(output, (x, y), (x + w, y + h), (0, 255, 0), 3)
    #     cv2.circle(output, (int(cX), int(cY)), 4, (0, 0, 255), -1)

    #     component_mask = (labels == i).astype(np.uint8) * 255

    #     color, _, _, _ = cv2.mean(opening, component_mask)

    #     if color == 255:
    #         print('---skipped')
    #         continue

    #     cv2.imshow("Output", output)
    #     cv2.imshow("Connected Component", component_mask)
    #     cv2.waitKey(0)

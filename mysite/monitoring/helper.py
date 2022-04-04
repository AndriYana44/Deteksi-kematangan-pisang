import numpy as np
import cv2

def getPercentage(objLow, objHigh, imgHsv):
    low = np.array(objLow, np.uint8)
    high = np.array(objHigh, np.uint8)
    mask = cv2.inRange(imgHsv, low, high)
    percentage = np.round((cv2.countNonZero(mask) / (imgHsv.size/3)) * 100, 2)
    return percentage

def getResult(img_hsv):
    weight = {}
    # mentah
    weight['mentah'] = getPercentage([33, 20, 60], [60, 200, 255], img_hsv)
    # matang
    weight['matang'] = getPercentage([25, 20, 60], [32, 200, 255], img_hsv)
    # sangat matang
    weight['sangat matang'] = getPercentage([18, 20, 60], [24, 200, 255], img_hsv)
    return weight

def percentageFIX(obj):
    total = float(obj['sangat matang']) + float(obj['matang']) + float(obj['mentah'])
    percentage_mentah = (float(obj['sangat matang']) / total) * 100
    percentage_matang = (float(obj['matang']) / total) * 100
    percentage_sangat_matang = (float(obj['mentah']) / total) * 100
    res = {1:round(percentage_sangat_matang, 2), 2:round(percentage_matang, 2), 3:round(percentage_mentah, 2)}
    return res
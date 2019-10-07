from __future__ import print_function
import sys
import numpy as np
import cv2 


def angle_cos(p0, p1, p2):
    d1, d2 = (p0-p1).astype('float'), (p2-p1).astype('float')
    return abs( np.dot(d1, d2) / np.sqrt( np.dot(d1, d1)*np.dot(d2, d2) ) )

def find_squares(img):
    # ノイズ除去
    img = cv2.GaussianBlur(img, (5, 5), 0)
    squares = []
    for gray in cv2.split(img):
        for thrs in range(0, 255, 26
        ):
            if thrs == 0:
                bin = cv2.Canny(gray, 0, 50, apertureSize=5)
                bin = cv2.dilate(bin, None)
            else:
                # 画像二値化
                _retval, bin = cv2.threshold(gray, thrs, 255, cv2.THRESH_BINARY)
            # 矩形領域を抽出
            contours, _hierarchy = cv2.findContours(bin, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contours:
                cnt_len = cv2.arcLength(cnt, True)
                cnt = cv2.approxPolyDP(cnt, 0.02*cnt_len, True)
                if len(cnt) == 4 and cv2.contourArea(cnt) > 1000 and cv2.isContourConvex(cnt):
                    cnt = cnt.reshape(-1, 2)
                    max_cos = np.max([angle_cos( cnt[i], cnt[(i+1) % 4], cnt[(i+2) % 4] ) for i in range(4)])
                    if max_cos < 0.1:
                        squares.append(cnt)
    return squares

def main(img_path):
    from glob import glob
    for fn in glob(img_path):
        img = cv2.imread(fn)
        squares = find_squares(img)
        contours_img = cv2.drawContours(img, squares, -1, (0, 255, 0), 3 )
        cv2.imwrite("./squares.jpg", contours_img)
        # cv2.imshow('squares', img)
        # ch = cv2.waitKey()
    print('Done')

def detect_squares(img):
    # img = cv2.imread(img_path)
    squares = find_squares(img)
    contours_img = cv2.drawContours(img, squares, -1, (0, 255, 0), 3)
    return contours_img


if __name__ == '__main__':
    main("./postit.jpg")

import cv2
import numpy as np

def centerFromImage(ori_img, hue_min, hue_max):
    image = cv2.cvtColor(ori_img, cv2.COLOR_BGR2HSV)
    hue = image[:, :, 0]

    # Filter out green postit note color
    # yellow is 90-100
    # pink is 137-150
    # green is 80-90
    hue[hue < hue_min] = 0
    hue[hue > hue_max] = 0
    hue[hue > 0] = 255

    hue = cv2.erode(hue, None, iterations=2)
    hue = cv2.dilate(hue, None, iterations=2)

    contours, hierarchy = cv2.findContours(
        hue,
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE
    )
    print(contours)
    img = cv2.drawContours(ori_img, contours, -1, (0,255,0), 3)
    cv2.imwrite("./contours.jpg", img)
    # center = [0, 0]

    # if len(contours) > 0:
    #     contour = contours[0]
    #     area = cv2.contourArea(contour)

    #     for c in contours:
    #         if cv2.contourArea(c) > area:
    #             area = cv2.contourArea(c)
    #             contour = c
    #             print(contour)
    #     m = cv2.moments(contour)
    #     center = [0, 0]
    #     if m['m00'] != 0:
    #         center = [m['m10'] / m['m00'], m['m01'] / m['m00']]

    #     center = [int(center[0]), int(center[1])]

    # return center


def hsv_crop(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # hsvLower = np.array([30, 153, 255])
    # hsvUpper = np.array([30, 135, 255])
    # hsv_mask = cv2.inRange(hsv, hsvLower, hsvUpper)

    # result = cv2.bitwise_and(img, img, mask=hsv_mask)
    return hsv


def getRectByPoints(points):
    # prepare simple array 
    points = list(map(lambda x: x[0], points))

    points = sorted(points, key=lambda x:x[1])
    top_points = sorted(points[:2], key=lambda x:x[0])
    bottom_points = sorted(points[2:4], key=lambda x:x[0])
    points = top_points + bottom_points

    left = min(points[0][0], points[2][0])
    right = max(points[1][0], points[3][0])
    top = min(points[0][1], points[1][1])
    bottom = max(points[2][1], points[3][1])
    return (top, bottom, left, right)

def getPartImageByRect(rect):
    img = cv2.imread(image_dir + image_file, 1)
    return img[rect[0]:rect[1], rect[2]:rect[3]]


def detect_postit(img_path):
    img = cv2.imread(img_path)    

    # // Convert your image into HSV
    image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # // Blur to reduce noise
    # blur(imgHSV, imgHSV, Size(3,3), Point(-1,-1));
    imgHSV = cv2.GaussianBlur(img, (5, 5), 0)


    # // Threshold image to only accept a certain saturation
    # inRange(imgHSV, Scalar(0, 127, 0), Scalar(255, 255, 255)), imgHSV);
    imgHSV = cv2.inRange(imgHSV, (0, 127, 0), (255,255,255), imgHSV)

    # // If you have to much noise you can erode and dilate at this point


    # // Find contours in your image
    # vector<vector<Point> > contours;
    # vector<Vec4i> hierarchy;
    # findContours(imgHSV, contours, hierarchy, CV_RETR_TREE, CV_CHAIN_APPROX_SIMPLE, Point(0, 0));
    contours, hierarchy = cv2.findContours(
        imgHSV,
        cv2.RETR_LIST,
        cv2.CHAIN_APPROX_SIMPLE
    )

    detect_img = cv2.drawContours(img, contours, -1, (0,255,0), 3)
    cv2.imwrite("./detect.jpg", img)

if __name__ == "__main__":
    # img_path = "./post_it.jpg"
    # im = cv2.imread(img_path, 1) #(A)
    # im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) #(B)
    # im_blur = cv2.GaussianBlur(im_gray, (11, 11), 0) #(C)
    # cv2.imwrite("./im_blur.jpg", im_blur)

    # int_im = cv2.threshold(im_blur, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)[1]
    # cv2.imwrite("./th.jpg", int_im)

    # img = (np.abs(im[:,:,2] - im[:,:,1]) + np.abs(im[:,:,2] - im[:,:,0]))
    # cv2.imwrite("./binary.jpg", img)

    # detect_postit("./postit.jpg")
    img = cv2.imread("./postit.jpg")
    centerFromImage(img, 90, 100)

    # cv2.imwrite("./result.jpg", result)
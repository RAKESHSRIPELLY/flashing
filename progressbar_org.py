import cv2
import math
import sys

img_path = "image.png"
screen_size = "34Inch"
expected_filled_percentage = '0.75'
min_value = '0'
max_value = '100'

if screen_size == "8Inch" or screen_size == "11Inch":

    tmp_img = cv2.imread(img_path)

    gray = cv2.cvtColor(tmp_img, cv2.COLOR_BGR2GRAY)

    # apply threshold
    thresh = cv2.threshold(gray, 30, 255, cv2.THRESH_BINARY)[1]

    # Horizontal Lines
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50,1))
    horizontal_mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel, iterations=1)

    # Horizontal  Lines Detections
    edges = cv2.Canny(horizontal_mask,50,150, apertureSize=3)
    lines = cv2.HoughLinesP(edges, 1, math.pi/2, 2, None, 30)
    point = []
    for i in range(len(lines)):
        line = lines[i]
        pt1 = line[0][1]
        pt2 = line[0][3]
        if pt1 == pt2:
            pt3 = line[0][2]
            pt4 = line[0][0]
            coordinate = (pt1, pt3, pt4)
            point.append(coordinate)
    result = sorted(point)
    z, y, x = result[0]
    zmax, y_max, x_max = result[-1]
    dist1 = y_max - x_max
    dist2 = y - x_max
    per = (dist2*100)/dist1
    if per >= 99.5:
        if len(lines)!= 2:
            per = 0
    print(f"Filled percentage of bar :{per}")
    print(f"Expected percentage of bar: {expected_filled_percentage}")
    if round(float(expected_filled_percentage)-0.5) <= (float(per)) <= round(float(expected_filled_percentage)+0.5):
        print("True")
    else:
        print("False")

    # color detection
    cx = int(y / 2 + 10)
    cy = int(z + 5)
    b, g, r = tmp_img[cy, cx]
    print(r, g, b)

    if (r <= 195 and b <= 195 and g <= 195 and abs(int(r) - int(g)) <= 30 and abs(int(g) - int(b)) <= 30 and abs(
            int(r) - int(b)) <= 30):
        if (r >= 70 and b >= 70 and g >= 70):
            print("filled bar color is grey")
        else:
            print("filled bar color is black")
    elif (r <= 153 and b < 153 and g >= 102):
        print("filled bar color is green")
    elif (r > 153 and b < 51 and g < 70):
        print("filled bar color is red")
    elif (r > 230 and b < 50 and g > 130 and g < 204):
        print("filled bar color is amber")
    elif (r > 204 and b < 50 and g >= 70 and g <= 130):
        print("filled bar color is orange")
    elif (r > 204 and b < 102 and g > 204):
        print("filled bar color is yellow")
    elif (r < 153 and b >= 153 and g >= 70 and g <= 102):
        print("filled bar color is blue")
    elif (r < 102 and b >= 153 and g < 70):
        print("filled bar color is violet")
    elif (r > 195 and b > 195 and g > 195):
        print("filled bar color is white")

    # Vertical lines detections
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1,20))
    vertical_mask = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel, iterations=1)
    vertical_edges = cv2.Canny(vertical_mask,50,150, apertureSize=3)
    vertical_contours, hierarchy = cv2.findContours(vertical_edges,  cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    # print("Number of Contours found = " + str(len(vertical_contours)))
    vertical_lines = cv2.HoughLinesP(vertical_edges, 1, math.pi/2, 2, None, 20)
    total_vertical_lines = len(vertical_contours)
    # print(total_vertical_lines)
    divide_by = total_vertical_lines - 2
    bar_division_length = 100 / divide_by
    print(f"bar division length is: {bar_division_length}")

    total_distance = int(max_value) - int(min_value)

    display_value = int(min_value) + (per * total_distance/100)

    print(f"Display value is : {display_value}")

elif screen_size == "34Inch":
    tmp_img = cv2.imread(img_path)
    gray = cv2.cvtColor(tmp_img, cv2.COLOR_BGR2GRAY)
    Blur = cv2.GaussianBlur(gray, (5, 5), 1)  # apply blur to roi
    Canny = cv2.Canny(Blur, 10, 50)
    contours, hierarchy = cv2.findContours(Canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.imshow('cy',Canny)
    bar_length = []
    shadow_length = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        print(x, y, w, h)
        if h >= 30:
            bar_length.append(w)
        elif h > 0 :
            shadow_length.append(w)
        img = cv2.rectangle(tmp_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #cv2.imshow('tmp',tmp_img)
        #cv2.waitKey(0)
    per = None
    print(bar_length)
    print(shadow_length)
    if len(bar_length) == 8:
        shadow_length = len(shadow_length)
        per = (shadow_length / 8) * 100
    elif len(bar_length) == 9 or len(bar_length) ==2 :
        if len(shadow_length) == 0:
            per = 0
        else:
            per = (sum(shadow_length) / 704) * 100

    print(f"filled bar percentage is {per}")

    if round(float(expected_filled_percentage)-0.5) <= (float(per)) <= round(float(expected_filled_percentage)+0.5):
        print("True")
    else:
        print("False")

    total_distance = int(max_value) - int(min_value)

    display_value = int(min_value) + (per * total_distance / 100)

    print(f"Display value is : {display_value}")

    cont = contours[-1]
    x, y, w, h = cv2.boundingRect(cont)
    M = cv2.moments(cont)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    r, g, b = tmp_img[cy, cx]
    if (r <= 195 and b <= 195 and g <= 195 and abs(int(r) - int(g)) <= 30 and abs(int(g) - int(b)) <= 30 and abs(
            int(r) - int(b)) <= 30):
        if (r >= 70 and b >= 70 and g >= 70):
            print("filled bar color is grey")
        else:
            print("filled bar color is black")
    elif (r <= 153 and b < 153 and g >= 102):
        print("filled bar color is green")
    elif (r > 153 and b < 51 and g < 70):
        print("filled bar color is red")
    elif (r > 230 and b < 50 and g > 130 and g < 204):
        print("filled bar color is amber")
    elif (r > 204 and b < 50 and g >= 70 and g <= 130):
        print("filled bar color is orange")
    elif (r > 204 and b < 102 and g > 204):
        print("filled bar color is yellow")
    elif (r < 153 and b >= 153 and g >= 70 and g <= 102):
        print("filled bar color is blue")
    elif (r < 102 and b >= 153 and g < 70):
        print("filled bar color is violet")
    elif (r > 195 and b > 195 and g > 195):
        print("filled bar color is white")


elif screen_size == "34InchFE":
    tmp_img = cv2.imread(img_path)
    gray = cv2.cvtColor(tmp_img, cv2.COLOR_BGR2GRAY)
    Blur = cv2.GaussianBlur(gray, (5, 5), 1)  # apply blur to roi
    Canny = cv2.Canny(Blur, 10, 50)
    contours, hierarchy = cv2.findContours(Canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    bar_length = []
    thickness = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        x, y, w, h = cv2.boundingRect(cnt)
        if h == 31 or h == 32:
            bar_length.append(w)
            thickness.append(h)
        img = cv2.rectangle(tmp_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
    per = None
    if len(bar_length) == 1:
        print(thickness[0])
        if thickness[0] >= 31:
            per = 100
        else:
            per = 0
    elif len(bar_length) == 2:
        filled_bar = bar_length[1]
        total_len = sum(bar_length)
        per = (filled_bar/total_len) * 100

    print(f"filled bar percentage is {per}")
    print(round(float(per)))

    if (round(float(per)) == int(expected_filled_percentage)):
        print("True")
    else:
        print("False")

    total_distance = int(max_value) - int(min_value)

    display_value = int(min_value) + (per * total_distance / 100)

    print(f"Display value is : {display_value}")

    if len(bar_length) == 1:
        if thickness[0] >= 31:
            per = 100
        else:
            per = 0
    elif len(bar_length) == 2:
        filled_bar = bar_length[1]
        total_len = sum(bar_length)
        per = (filled_bar / total_len) * 100

    print(f"filled bar percentage is {per}")

    # color detection for 34InchFE
    if len(contours) == 2:
        cont = contours[1]
    else:
        cont = contours[0]
    x, y, w, h = cv2.boundingRect(cont)
    M = cv2.moments(cont)
    cx = int(M['m10'] / M['m00'])
    cy = int(M['m01'] / M['m00'])
    r, g, b = tmp_img[cy, cx]
    if (r <= 195 and b <= 195 and g <= 195 and abs(int(r) - int(g)) <= 30 and abs(int(g) - int(b)) <= 30 and abs(
            int(r) - int(b)) <= 30):
        if (r >= 70 and b >= 70 and g >= 70):
            print("filled bar color is grey")
        else:
            print("filled bar color is black")
    elif (r <= 153 and b < 153 and g >= 102):
        print("filled bar color is green")
    elif (r > 153 and b < 51 and g < 70):
        print("filled bar color is red")
    elif (r > 230 and b < 50 and g > 130 and g < 204):
        print("filled bar color is amber")
    elif (r > 204 and b < 50 and g >= 70 and g <= 130):
        print("filled bar color is orange")
    elif (r > 204 and b < 102 and g > 204):
        print("filled bar color is yellow")
    elif (r < 153 and b >= 153 and g >= 70 and g <= 102):
        print("filled bar color is blue")
    elif (r < 102 and b >= 153 and g < 70):
        print("filled bar color is violet")
    elif (r > 195 and b > 195 and g > 195):
        print("filled bar color is white")



        ListA = [1,3,'A',3.5,'python']




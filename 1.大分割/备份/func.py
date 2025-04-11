import cv2
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import os

def unify(line):
    if(line[0] == line[2]):
        if(line[1] > line[3]):
            return (line[0],line[3],line[2],line[1])
        else:
            return line
    else:
        if(line[0] > line[2]):
            return (line[2],line[1],line[0],line[3])
        else:
            return line

def one_channel_2_three_channel(image):
    """
    Convert a single-channel image to a three-channel image.
    """
    return cv2.merge((image, image, image))

def expand_line(line1, lines, threshold=10):
    """
    Expand a line to include another line.
    """
    for i, line2 in enumerate(lines):
        x1, y1, x2, y2 = line1
        x3, y3, x4, y4 = line2
        line1 = unify(line1)
        line2 = unify(line2)
        if same_kind(line1, line2) and (x1 == x2) and (abs(line1[0] - line2[0]) < threshold):
            lines[i] = (line1[0], min(y1, y3), line1[0], max(y2, y4))
            return
        if same_kind(line1, line2) and (y1 == y2) and (abs(line1[1] - line2[1]) < threshold):
            lines[i] = (min(x1, x3), line1[1], max(x2, x4), line1[1])
            return

def same_kind(line1, line2):
    """
    Check if two lines are both vertical or horizontal.
    """
    return (line1[0] == line1[2] and line2[0] == line2[2]) or (line1[1] == line1[3] and line2[1] == line2[3])

def similar(line1, lines,threshold=5):
    """
    Check if a line is similar to any line in a list of lines.
    """
    for line2 in lines:
        #竖线相近
        if same_kind(line1, line2) and (line1[0] == line1[2]) and (abs(line1[0] - line2[0]) < threshold):
            return True
        #横线相近
        elif same_kind(line1,line2) and (line1[1] == line1[3]) and (abs(line1[1] - line2[1]) < threshold):
            return True
    return False


def remove_similar(lines):
    """
    Remove similar lines from a list of lines.
    
    Args:
        lines: A list of lines, each represented as a tuple of four integers.
        
    Returns:
        A list of lines with similar lines removed.
    """
    unique_lines = []
    for line in lines:
        line = unify(line)
        if not similar(line, unique_lines):
            unique_lines.append(line)
        else:
            # print("Here expand")
            expand_line(line, unique_lines)
    return unique_lines

def vertical_horizontal_lines(image,apertureSize=3,minLineLength=300,maxLineGap=10):
    # 读取图像并转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 使用 Canny 边缘检测，调整阈值
    edges = cv2.Canny(gray, 50, 150, apertureSize=apertureSize)

    # 使用概率霍夫变换检测直线
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=minLineLength, maxLineGap=maxLineGap)

    new_lines = []
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            new_lines.append((x1, y1, x2, y2))

    for line in new_lines:
        line = unify(line)
        print(line)
    print("-----------------")
    new_lines = remove_similar(new_lines)
    vertical = []
    horizontal = []
    for line in new_lines:
        print(line)
        x1, y1, x2, y2 = line
        if(x1 == x2):
            vertical.append(x1)
        if(y1 == y2):
            horizontal.append(y1)
        # cv2.line(image, (x1, y1), (x2, y2), (255, 0, 0), 3)  # 蓝色线条，厚度为1

    vertical.sort()
    horizontal.sort()
    return vertical,horizontal,new_lines

def length(line):
    """
    Calculate the length of a line.
    """
    x1, y1, x2, y2 = line
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

#某个区域内是否有水平线
def horizontal_line_in_area(lines,top_left,bottom_right):
    """
    Check if a horizontal line is in a given area.
    """
    print("line is: ",lines)
    print("top_left is: ",top_left)
    print("bottom_right is: ",bottom_right)
    for i in range(len(lines)):
        if(lines[i][1]!=lines[i][3]):
            continue
        elif(length(lines[i]) < bottom_right[0]-top_left[0] and lines[i][0] > top_left[0] and lines[i][0] < bottom_right[0] and lines[i][1] > top_left[1] and lines[i][1] < bottom_right[1] and lines[i][2] > top_left[0] and lines[i][2] < bottom_right[0]):
            return True
    return False

def final_horizontal_line_in_area(lines,top_left,bottom_right):
    """
    Check if there are remaining horizontal lines in the given area.
    """
    print("line is: ",lines)
    print("top_left is: ",top_left)
    print("bottom_right is: ",bottom_right)
    remaining_horizontal = []
    for i in range(len(lines)):
        if(lines[i][1]!=lines[i][3]):
            continue
        elif(length(lines[i]) < bottom_right[0]-top_left[0] and lines[i][0] > top_left[0] and lines[i][0] < bottom_right[0] and lines[i][1] > top_left[1] and lines[i][1] < bottom_right[1] and lines[i][2] > top_left[0] and lines[i][2] < bottom_right[0])or abs(abs(lines[i][2]-lines[i][0])-abs(bottom_right[0]-top_left[0])) < 30:
            remaining_horizontal.append(lines[i])
            # return True
    if len(remaining_horizontal) > 1:
        return remaining_horizontal
    return False

def is_blank(image,threshold=0.9965):
    """
    Check if an image is blank.
    An image is considered blank if more than 95% of its pixels are white.
    """

    # 获取图像的宽度和高度
    height, width = image.shape[:2]

    # 计算中间90%区域的起始和结束坐标
    x_start = int(width * 0.05)
    y_start = int(height * 0.05)
    x_end = int(width * 0.95)
    y_end = int(height * 0.95)

    # 截取中间90%区域
    image = image[y_start:y_end, x_start:x_end]

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    
    # Get the total number of pixels in the image
    total_pixels = image.shape[0] * image.shape[1]
    min_val, max_val, _, _ = cv2.minMaxLoc(thresh)
    # Count the number of non-zero (non-black) pixels
    non_zero_pixels = cv2.countNonZero(thresh)
    print(non_zero_pixels)
    print(total_pixels)
    print(non_zero_pixels / total_pixels)
    # cv2.imshow('img', thresh)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    if(non_zero_pixels / total_pixels > threshold):
        print("blank")
    else:
        print("not blank")
    return non_zero_pixels / total_pixels > threshold or total_pixels < 10000


#遍历base_output_dir文件夹的每一个文件，调用final_horizontal_line_in_area函数
def process_output_files(output_dir):
    # 遍历 output_dir 及其子目录中的所有文件
    for root, dirs, files in os.walk(output_dir):
        for file in files:
            # 跳过隐藏文件
            if file.startswith('.'):
                continue
            
            # 获取文件的完整路径
            output_file = os.path.join(root, file)
            print("Here")
            print(output_file)
            # 读取图像
            image = cv2.imread(output_file)
            # cv2.imshow('img', image)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            # # 检查图像是否成功读取
            # if image is None:
            #     print(f"Failed to read {output_file}. Skipping...")
            #     continue
            
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            _, thresh = cv2.threshold(gray, 250, 255, cv2.THRESH_BINARY)

            # 获取图像的高度和宽度
            height, width, _ = image.shape
            top_left = (0, 0)
            bottom_right = (width, height)
            vertical, horizontal, new_lines = vertical_horizontal_lines(one_channel_2_three_channel(thresh))
            # print(new_lines)
            
            # # 处理图像
            if final_horizontal_line_in_area(new_lines, top_left, bottom_right):
                print(f"There are remaining horizontal lines in the given area in {output_file}.")
                #依照horizontal切割
                for i in range(len(horizontal)-1):
                    new_img = image[horizontal[i]:horizontal[i+1], :]
                    # 保存处理后的图像，覆盖原文件
                    cv2.imwrite(output_file, new_img)
            else:
                print(f"There are no remaining horizontal lines in the given area in {output_file}.")

import cv2
import numpy as np
import matplotlib.pyplot as plt
from func import *
import os

def process_image(parody_file, original_file, output_dir):
    # 获取 original_file 的文件名（不带路径和扩展名）
    original_file_name = os.path.splitext(os.path.basename(original_file))[0]
    # 创建与 original_file 同名的文件夹
    specific_output_dir = os.path.join(output_dir, original_file_name)
    os.makedirs(specific_output_dir, exist_ok=True)

    # 读取图像
    image = cv2.imread(parody_file)
    original_image = cv2.imread(original_file)
    vertical, horizontal, new_lines = vertical_horizontal_lines(image)

    # 显示原图
    # plt.figure(figsize=(10, 5))
    # plt.subplot(1, 2, 1)
    # plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
    # plt.title('Original Picture')
    # plt.axis('off')
    # plt.show()

    count = 0

    if len(new_lines) == 0:
        # cv2.imshow('img', original_image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # 使用 count 值命名文件
        unique_output_file = os.path.join(specific_output_dir, f"output_{count}.png")
        cv2.imwrite(unique_output_file, original_image)
        count += 1
    else:
        for i in range(len(vertical) - 1):
            img = original_image[:, vertical[i]:vertical[i + 1]]
            height, width, _ = img.shape
            top_left = (vertical[i], 0)
            bottom_right = (vertical[i + 1], height)
            print(new_lines)
            if horizontal_line_in_area(new_lines, top_left, bottom_right):
                for j in range(len(horizontal) - 1):
                    new_img = img[horizontal[j]:horizontal[j + 1], :]
                    # 使用 count 值命名文件
                    if(is_blank(new_img)):
                        continue
                        # cv2.imshow('img', new_img)
                        # cv2.waitKey(0)
                        # cv2.destroyAllWindows()
                    if not(is_blank(new_img)):
                        unique_output_file = os.path.join(specific_output_dir, f"output_{count}.png")
                        cv2.imwrite(unique_output_file, new_img)
                        count += 1
            else:
                if(is_blank(img)):
                    cv2.imshow('img', img)
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                # 使用 count 值命名文件
                if not (is_blank(img)):
                    unique_output_file = os.path.join(specific_output_dir, f"output_{count}.png")
                    cv2.imwrite(unique_output_file, img)
                    count += 1

def process_all_images(parody_file_dir, original_file_dir, base_output_dir):
    # 获取所有parody文件
    parody_files = [os.path.join(parody_file_dir, f) for f in os.listdir(parody_file_dir) if not f.startswith('.')]
    # 获取所有original文件
    original_files = [os.path.join(original_file_dir, f) for f in os.listdir(original_file_dir) if not f.startswith('.')]
    
    for parody_file, original_file in zip(parody_files, original_files):
        # 处理图像
        process_image(parody_file, original_file, base_output_dir)

parody_file_dir = '//Users/tony/Desktop/black_white/'
original_file_dir = '/Users/tony/Desktop/original/'
base_output_dir = '/Users/tony/Desktop/大分割/'

process_all_images(parody_file_dir, original_file_dir, base_output_dir)
        
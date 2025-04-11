import os
import cv2
import numpy as np
import time
from func import *

input_image_path = '/Users/tony/Desktop/testoutnew/'# 原始图像路径
# output_dir = '/Users/tony/Desktop/小分割/'#小分割图像保存路径

#遍历input_image_path下的所有文件
# for root, dirs, files in os.walk(input_image_path):
#     for file in files:
#         if file.endswith('.png') or file.endswith('.jpg'):
#             input_image_path = os.path.join(root, file)
#             # 读取原始图像
#             image = cv2.imread(input_image_path)
#             if image is None:
#                 print("Error: Image not found or path is incorrect.")
#                 exit()
#             else:
#                 segmentation_display(input_image_path)

remove_empty_dirs(input_image_path)
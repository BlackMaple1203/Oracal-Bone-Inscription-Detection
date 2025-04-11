import os
from func import *
import cv2
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
            
            # 获取图像的高度和宽度
            height, width, _ = image.shape
            top_left = (0, 0)
            bottom_right = (width, height)
            vertical, horizontal, new_lines = vertical_horizontal_lines(image)
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


output_dir = '/Users/tony/Desktop/testout/'
process_output_files(output_dir)
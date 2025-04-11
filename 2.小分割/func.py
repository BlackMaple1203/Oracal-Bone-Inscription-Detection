import cv2
import numpy as np
import os

# def create_dir(dir):
#     exclude_dirs = set()  # 用于存储新创建的文件夹路径

#     for root, dirs, files in os.walk(dir):
#         # 排除新创建的文件夹
#         dirs[:] = [d for d in dirs if os.path.join(root, d) not in exclude_dirs]

#         for file in files:
#             if file.startswith('.') or file in exclude_dirs:
#                 continue
#             parent = os.path.basename(root)
#             new_folder = os.path.join(root, file)
#             new_folder_base = os.path.basename(new_folder)
#             last_folder = os.path.dirname(new_folder)
#             last_folder_base = os.path.basename(last_folder)
#             foldername = str(last_folder_base) + '_' + str(new_folder_base)
#             new_folder_path = os.path.join(last_folder, foldername)
            
#             # 创建文件夹并添加到排除列表
#             os.makedirs(new_folder_path, exist_ok=True)
#             exclude_dirs.add(new_folder_path)
#             print(f"New folder '{foldername}' created successfully at {new_folder_path}")

def create_dir(dir):
    exclude_dirs = set()  # 用于存储新创建的文件夹路径

    for root, dirs, files in os.walk(dir):
        # 排除新创建的文件夹
        dirs[:] = [d for d in dirs if os.path.join(root, d) not in exclude_dirs]

        for file in files:
            if file.startswith('.'):
                continue
            parent = os.path.basename(root)
            new_folder = os.path.join(root, file)
            new_folder_base = os.path.basename(new_folder)
            last_folder = os.path.dirname(new_folder)
            last_folder_base = os.path.basename(last_folder)
            foldername = str(last_folder_base) + '_' + str(new_folder_base)
            new_folder_path = os.path.join(last_folder, foldername)
            
            # 创建文件夹并添加到排除列表
            os.makedirs(new_folder_path, exist_ok=True)
            exclude_dirs.add(new_folder_path)
            print(f"New folder '{foldername}' created successfully at {new_folder_path}")


def segmentation_display(input_image_path):

    # os.makedirs(output_dir, exist_ok=True)

    # 读取原始图像
    image = cv2.imread(input_image_path)
    if image is None:
        print("Error: Image not found or path is incorrect.")
        exit()

    # 显示原始图像
    # cv2.imshow('Original Image', image)
    # cv2.waitKey(0)

    # 进行高斯模糊处理以减少噪声
    blurred = cv2.GaussianBlur(image, (5, 5), 0)  # 增加内核大小
    # cv2.imshow('Blurred Image', blurred)  # 显示模糊后的图像
    # cv2.waitKey(0)

    # 转换为灰度图像
    gray = cv2.cvtColor(blurred, cv2.COLOR_BGR2GRAY)
    # cv2.imshow('Gray Image', gray)  # 显示灰度图像
    # cv2.waitKey(0)

    # 使用 Canny 边缘检测
    edges = cv2.Canny(gray, 30, 200)  # 调整阈值以增强边缘检测
    # cv2.imshow('Edges', edges)  # 显示边缘检测结果
    # cv2.waitKey(0)

    # 使用形态学操作（膨胀和闭运算）来连接轮廓
    kernel = np.ones((6, 6), np.uint8)  # 增加结构元素的大小
    dilated = cv2.dilate(edges, kernel, iterations=2)
    morph = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel)
    # cv2.imshow('Morphological Result', morph)  # 显示形态学处理后的结果
    # cv2.waitKey(0)

    # 进行轮廓检测
    contours, hierarchy = cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 打印轮廓数量
    print(f"Number of contours found: {len(contours)}")

    # 记录切割图像的文件名
    cut_image_paths = []
    create_dir(os.path.dirname(input_image_path))
    # 遍历所有轮廓并保存切割图像
    for i, contour in enumerate(contours):
        x, y, w, h = cv2.boundingRect(contour)
        area = cv2.contourArea(contour)  # 计算轮廓面积

        print(f"Contour {i}: x={x}, y={y}, w={w}, h={h}, area={area}")  # 打印轮廓的 (x, y, w, h)

        # 判断轮廓是否有效并保存
        if (h > 100 and w > 30 and 900000 > area > 2000 and abs(h - w) <= 400):
            cut_image = image[y:y + h, x:x + w]

            # 保存切割图像
            # cut_image_path = os.path.join(output_dir, f'cut_image_{i + 1}.png')
            image_name = os.path.basename(input_image_path)
            folder_name = os.path.basename(os.path.dirname(input_image_path))
            output_folder = folder_name + '_' + image_name
            cut_image_path = os.path.join(os.path.dirname(input_image_path),output_folder,f'cut_image_{i + 1}.png')
            
            cv2.imwrite(cut_image_path, cut_image)  # 仅保存切割图像
            cut_image_paths.append(cut_image_path)
            print(f"Saved cut image: {cut_image_path}")

            # 显示切割的图像
            # cv2.imshow(f'Cut Image {i + 1}', cut_image)
            # cv2.waitKey(0)  # 等待按键输入以继续

    # 检查切割图像是否有效
    if cut_image_paths:
        print(f"Total cut images saved: {len(cut_image_paths)}")
    else:
        print("No valid cut images were saved.")

    # 关闭所有 OpenCV 窗口
    cv2.destroyAllWindows()

            
def remove_empty_dirs(path):
    # 遍历目录
    for root, dirs, files in os.walk(path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            # 检查文件夹是否为空
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
                print(f"Removed empty directory: {dir_path}")

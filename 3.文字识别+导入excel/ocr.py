import os
import csv
import cv2
import re
from paddleocr import PaddleOCR
import openpyxl    
from openpyxl.drawing.image import Image


#分割出来文字部分识别会更准确，但是序号和解释可能会反
#序号和解释可能没有分开
#解释可能识别不出来

def get_page(input_image_path):
    parent_folder_path = os.path.dirname(input_image_path)
    parent_folder_name = os.path.basename(parent_folder_path)

    if '_' in parent_folder_name:
        number = parent_folder_name.split('_')[-1]
    else:
        number = None
    return number

def initial_process_image(input_image_path):
    #获取图片的ocr结果
    image = cv2.imread(input_image_path)
    if image is None:
        print("Error: Image not Supported or Input Path Incorrect.")
        return None
    
    ocr = PaddleOCR(use_angle_cls=True, lang='ch')
    ocr_result = ocr.ocr(input_image_path, cls=False)
    
    if not ocr_result or not ocr_result[0]:
        print("Error: No OCR result found.")
        return None
    
    return ocr_result[0]

def extract_text_image(input_image_path, ocr_result):
    #获取文字的范围，然后截取出来
    if not ocr_result:
        print("Error: Invalid OCR result.")
        return

    temp_image = cv2.imread(input_image_path)
    if temp_image is None:
        print("Error: Image not Supported or Input Path Incorrect.")
        return

    left_upper = [10000,10000]
    right_lower = [0,0]
    
    shape = temp_image.shape

    for i in range(len(ocr_result)):
        if ocr_result[i][1][1] < 0.75:
            continue
        if ocr_result[i][0][0][0] < left_upper[0]:
            left_upper[0] = int(ocr_result[i][0][0][0])
        if ocr_result[i][0][0][1] < left_upper[1]:
            left_upper[1] = int(ocr_result[i][0][0][1])
        if ocr_result[i][0][2][0] > right_lower[0]:
            right_lower[0] = int(ocr_result[i][0][2][0])
        if ocr_result[i][0][2][1] > right_lower[1]:
            right_lower[1] = int(ocr_result[i][0][2][1])

    image = temp_image[left_upper[1]:right_lower[1], 0:shape[0]]
    output_path = '/Users/tony/Desktop/文字图像/text.png'
    cv2.imwrite(output_path, image)
    return output_path

def save_image_to_excel(image_path, excel_path, sheet_name, cell):
    # 打开 Excel 文件
    workbook = openpyxl.load_workbook(excel_path)
    sheet = workbook[sheet_name]

    # 加载图片
    img = Image(image_path)

    # 将图片添加到指定单元格
    sheet.add_image(img, cell)

    # 保存 Excel 文件
    workbook.save(excel_path)



def process_image(excel_path, input_image, row, input_image_path):
    workbook = openpyxl.load_workbook(excel_path)
    sheet = workbook['Sheet1']

    if input_image is None:
        print("Error: Image not Supported or Input Path Incorrect.")
        return
    
    ocr = PaddleOCR(use_angle_cls = True,lang='ch')

    ocr_result = ocr.ocr(input_image,cls=False)
    final_text = ""

    number_pattern = re.compile(r'^\d{5}$')

    text_list = []
    for line in ocr_result:
        if line is not None and len(line) > 0:  # 确保 line 不是 None 且长度大于0
            for word_info in line:
                text = word_info[1][0]  # 获取识别的文本

                # 检查是否为空字符
                if not text or text.strip() == "":
                    continue  # 跳过空白

                # 将有效文本添加到列表
                text_list.append(text.strip())
    
    # 处理文本之间的逗号和换行
    previous_number = None  # 用于记录前一个编号

    for i, text in enumerate(text_list):
        # 检查当前文本是否为编号
        if number_pattern.match(text):
            if previous_number is not None and previous_number != text:
                # 如果当前编号与前一个编号不同，则换行
                final_text += "\n"

            final_text += text  # 添加当前编号
            previous_number = text  # 更新前一个编号
        else:
            # 不是编号的文本
            if i > 0:  # 从第二个文本开始添加逗号
                final_text += ","  # 在文本之间添加逗号
            final_text += text  # 添加当前文本

    # 检查编号后是否有逗号，如果没有则添加
    final_text = re.sub(r'(\d{5})(?!,)', r'\1,', final_text)

    final_text_list = final_text.split(',')

    page_number = get_page(input_image_path)
    if final_text_list[0].isdigit():
        if len(final_text_list) == 5:
            for i in range(len(final_text_list)):
                column_letter = chr(ord('A')+i)
                position = column_letter + str(row)
                page_position = "F" + str(row)
                print("Current position is : " + position)
                sheet[position] = final_text_list[i]
                sheet[page_position] = page_number
                workbook.save(excel_path)
        elif len(final_text_list) == 4:
            for i in range(len(final_text_list)):
                if i == 0:
                    column_letter = chr(ord('A')+i)
                    position = column_letter + str(row)
                    sheet[position] = final_text_list[i]
                    workbook.save(excel_path)
                else:
                    column_letter = chr(ord('B')+i)
                    position = column_letter + str(row)
                    page_position = "F" + str(row)
                    print("Current position is : " + position)
                    sheet[position] = final_text_list[i]
                    sheet[page_position] = page_number
                    workbook.save(excel_path)
        return 1
    else:
        return -1

def main():
    input_folder = '/Users/tony/Desktop/备份/3.大分割'
    files = os.walk(input_folder)
    excel_path = '/Users/tony/Desktop/陶文目录一导出.xlsx'
    row = 1
    for root,dirs,filenames in files:
        for filename in filenames:
            input_image_path = os.path.join(root,filename)

            ocr_result = initial_process_image(input_image_path)
            text_image = extract_text_image(input_image_path,ocr_result)

            flag = process_image(excel_path,text_image,row,input_image_path)
            if flag == -1:
                print("Not a target")
            else:
                print("Written success")
                row += 1

if __name__ == "__main__":
    main()
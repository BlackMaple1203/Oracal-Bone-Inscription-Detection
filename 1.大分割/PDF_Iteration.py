from pdf2image import convert_from_path
import os

# PDF file path
pdf_path = '/Users/tony/Desktop/Tony/大学/实验室/数字人文研究院任务/任务1/02.中国古代封泥全集·图版编2.pdf'

# Output image directory    
output_dir = '/Users/tony/Desktop/original/'

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Convert PDF pages to images with higher DPI for better quality
images = convert_from_path(pdf_path,dpi=300)  # Increase DPI to 300 or higher


dpi = (300,300)
# Save each page as an image

for i, image in enumerate(images):
    if(i < 163):
        continue
    image_path = os.path.join(output_dir, f'page_{i + 1}.png')
    image.save(image_path, 'PNG',dpi=dpi)
    print(f'Page {i + 1} has been saved to the directory.')

print(f'All pages of the PDF have been successfully converted to images and saved in {output_dir}.')

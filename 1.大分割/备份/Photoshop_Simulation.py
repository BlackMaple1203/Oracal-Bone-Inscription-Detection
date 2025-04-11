import cv2
import numpy as np
import matplotlib.pyplot as plt

def adjust_exposure(image, exposure):
    return cv2.convertScaleAbs(image, alpha=exposure, beta=0)

def adjust_contrast(image, contrast):
    return cv2.convertScaleAbs(image, alpha=contrast, beta=0)

def adjust_whites_blacks(image, whites, blacks):
    image = np.clip(image + whites, 0, 255)
    image = np.clip(image - blacks, 0, 255)
    return image

# 读取图像
image = cv2.imread('/Users/tony/Desktop/test.png')

# 保存原始图像
original_image = image.copy()

# 调整图像
image = adjust_exposure(image, 0.8)
image = adjust_contrast(image, 1.5)

# 同时显示前后图像
plt.figure(figsize=(10, 5))

# 显示原始图像
plt.subplot(1, 2, 1)
plt.imshow(cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB))
plt.title('Original Image')
plt.axis('off')

# 显示调整后的图像
plt.subplot(1, 2, 2)
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.title('Adjusted Image')
plt.axis('off')

plt.show()
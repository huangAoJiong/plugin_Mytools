# 图像增强算法，图像锐化算法
# 1）基于直方图均衡化 2）基于拉普拉斯算子 3）基于对数变换 4）基于伽马变换 5)CLAHE 6)retinex-SSR 7)retinex-MSR
# 其中，基于拉普拉斯算子的图像增强为利用空域卷积运算实现滤波
# 基于同一图像对比增强效果
# 直方图均衡化:对比度较低的图像适合使用直方图均衡化方法来增强图像细节
# 拉普拉斯算子可以增强局部的图像对比度
# log对数变换对于整体对比度偏低并且灰度值偏低的图像增强效果较好
# 伽马变换对于图像对比度偏低，并且整体亮度值偏高（对于相机过曝）情况下的图像增强效果明显


from PIL import Image
import numpy as np
import cv2

def clahe(image):
    # 将PIL图像转换为NumPy数组
    np_image = np.array(image)

    # 将RGB图像转换为灰度图像
    gray_image = Image.fromarray(np_image).convert('L')

    # 进行CLAHE直方图均衡化
    clahe = Image.fromarray(np.array(gray_image))
    return clahe
def clahe_color(image):
    # 将PIL图像转换为NumPy数组
    np_image = np.array(image)

    # 将RGB图像转换为Lab颜色空间
    lab_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2LAB)

    # 将Lab颜色空间中的亮度通道提取出来
    l_channel, a_channel, b_channel = cv2.split(lab_image)

    # 对亮度通道进行CLAHE直方图均衡化
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_l_channel = clahe.apply(l_channel)

    # 将增强后的亮度通道与原始a和b通道组合回Lab图像
    enhanced_lab_image = cv2.merge((enhanced_l_channel, a_channel, b_channel))

    # 将增强后的Lab图像转换回RGB颜色空间
    enhanced_rgb_image = cv2.cvtColor(enhanced_lab_image, cv2.COLOR_LAB2RGB)

    # 将NumPy数组转换回PIL图像并返回
    enhanced_pil_image = Image.fromarray(enhanced_rgb_image)
    
    return enhanced_pil_image

if __name__ == "__main__":
    # 读取图像
    input_image = Image.open("../../tmp/new_image.jpg")

    # 调用CLAHE函数处理图像
    output_image = clahe(input_image)

    # 保存处理后的图像
    output_image.save("output_image_clahe.jpg")


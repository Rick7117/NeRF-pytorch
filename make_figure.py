import cv2
import os
import cv2
import sys
#####################################################################################################################
# 获取文件夹中的所有图像文件名
def getImageFiles(dir):
    # 输入文件夹，返回所有图像文件名列表
    image_files = []
    for item in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, item)):
            # 检查是否为图像文件
            if item.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp', '.tiff')):
                image_files.append(item)
    return sorted(image_files)  # 排序确保处理顺序一致

# 从环境变量或命令行参数读取数据集名称
name = os.environ.get('DATA', 'cup')  # 默认为'cup'，可通过环境变量DATA覆盖
if len(sys.argv) > 1:
    name = sys.argv[1]  # 如果有命令行参数，使用第一个参数作为数据集名称
image_files = getImageFiles(f"./data/nerf_llff_data/{name}/images")  # 获取所有图像文件名
filenum = len(image_files)
print(f"找到 {filenum} 个图像文件")

# 创建输出目录
# 从命令行参数读取下采样因子，默认为8
n = 8
if len(sys.argv) > 2:
    try:
        n = int(sys.argv[2])  # 第二个参数为下采样因子
        print(f"使用命令行指定的下采样因子: {n}")
    except ValueError:
        print(f"警告: 无效的下采样因子 '{sys.argv[2]}'，使用默认值 {n}")
else:
    print(f"使用默认下采样因子: {n}")
output_dir = f"./data/nerf_llff_data/{name}/images_{n}"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

index = 1  # 保存图片编号
num = 0  # 处理图片计数
for filename in image_files:
    ########################################################
    # 1.读取原始图片
    input_path = f"./data/nerf_llff_data/{name}/images/{filename}"
    print(f"处理文件: {input_path}")
    original_image = cv2.imread(input_path)
    
    if original_image is None:
        print(f"警告: 无法读取图像 {filename}")
        continue
        
    # 2.下采样
    if n == 4:
        img_1 = cv2.pyrDown(original_image)
        img_1 = cv2.pyrDown(img_1)
    elif n == 8:
        img_1 = cv2.pyrDown(original_image)
        img_1 = cv2.pyrDown(img_1)
        img_1 = cv2.pyrDown(img_1)
    else:
        img_1 = original_image
        
    # 3.将下采样图片保存到指定路径当中，保持原始文件名
    output_path = f"./data/nerf_llff_data/{name}/images_{n}/{filename}"
    cv2.imwrite(output_path, img_1)
    print(f"正在为 {filename} 图片采样......")
    index += 1
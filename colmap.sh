#!/bin/bash

# 设置路径变量
DATA="cup"
export DATA  # 导出DATA变量供make_figure.py使用
DATASET_PATH="./data/nerf_llff_data/$DATA"
IMAGE_PATH="./data/nerf_llff_data/$DATA/images"
IMAGE4_PATH="./data/nerf_llff_data/$DATA/images_4"
IMAGE8_PATH="./data/nerf_llff_data/$DATA/images_8"
DATABASE_PATH="./data/nerf_llff_data/$DATA/database.db"
OUTPUT_PATH="./data/nerf_llff_data/$DATA/sparse"

mkdir -p "$IMAGE4_PATH"
mkdir -p "$IMAGE8_PATH"
mkdir -p "$OUTPUT_PATH"

# 运行图像预处理脚本
python ./make_figure.py $DATA 4
python ./make_figure.py $DATA 8

# 创建输出目录和数据库文件
touch "$DATABASE_PATH"

# 1. 特征提取
echo "开始特征提取..."
colmap feature_extractor \
    --database_path "$DATABASE_PATH" \
    --image_path "$IMAGE_PATH" \
    --ImageReader.camera_model PINHOLE

# 2. 特征匹配
echo "开始特征匹配..."
colmap exhaustive_matcher \
    --database_path "$DATABASE_PATH"

# 3. 稀疏重建
echo "开始稀疏重建..."
colmap mapper \
    --database_path "$DATABASE_PATH" \
    --image_path "$IMAGE_PATH" \
    --output_path "$OUTPUT_PATH"

python imgs2poses.py $DATASET_PATH

echo "COLMAP处理完成！"
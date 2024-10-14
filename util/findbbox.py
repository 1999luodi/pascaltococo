import json

# 读取COCO JSON文件
json_path = "/home/luodi23/mmdetection/data/PennisetumGlaucum/JSON/AnnotationsTest.json"  # 替换为你的COCO JSON文件路径
with open(json_path, 'r') as f:
    coco_data = json.load(f)

# 设定一个阈值，查找 area 小于该值的边界框
area_threshold = 1024  # 你可以根据需要调整这个阈值
small_bboxes = []

# 遍历 annotations，查找满足条件的边界框
for annotation in coco_data['annotations']:
    area = annotation['area']
    if area < area_threshold:
        small_bboxes.append({
            'bbox_id': annotation['id'],
            'image_id': annotation['image_id'],
            'area': area
        })

# 统计边界框个数
bbox_count = len(small_bboxes)

# 输出边界框数量和每个图像对应的bbox信息
print(f"总共有 {bbox_count} 个边界框面积小于 {area_threshold}。")

# 显示这些边界框及其所在图像的ID
if bbox_count>0:
    for bbox_info in small_bboxes:
        print(f"边界框 ID: {bbox_info['bbox_id']}，图像 ID: {bbox_info['image_id']}，面积: {bbox_info['area']}")

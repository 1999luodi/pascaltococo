import os
# 源数据的根路径设置
ROOT = r"/home/luodi23/mmdetection/data/archive"

#源数据的类别
CATEGORY_LIST = ["ungerminated", "germinating","germinated","primary root","secondary root"]

# 这个配置不要变动

MODE = {
    "trainval": "trainval2017",
    "train": "train2017",
    "val": "val2017",
    "test": "test2017",
}

#源数据的XML注释根路径
ANNOTATION_ROOT=os.path.join(ROOT,"Annotations/Annotations")
#源数据的图像根路径
IMG_ROOT = ROOT

#####################################################################

#划分的txt存储路径 该txt存放划分好训练数据的xml的文件名
IMAGESET=os.path.join(ROOT,"ImageSets")
# 输出coco格式的存放路径,为了避免与原来的注释文件重名，起名为coco_annotations
JSONPATH=os.path.join(ROOT,"coco_annotations")


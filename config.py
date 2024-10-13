import os
## 源数据的根路径设置
ROOT="./dataset"

#源数据的类别pg_im
# CATEGORY_LIST = ["ungerminated", "germinating","germinated","primary root","secondary root"]
CATEGORY_LIST=["pg_im","pg_el"]

#源数据的XML注释根路径
ANNOTATION_ROOT=os.path.join(ROOT,"annotations")
#源数据的图像根路径
IMG_ROOT = os.path.join(ROOT,"img") 
# 划分比例
SPLITSCALE=(0.8,0.1,0.1)

#####################################################################
## 目标数据集（转换好的数据集）

# 转换后的数据名
DATANAME="coco_data"
# 转换后的img的存放地址
IMAGEPATH=os.path.join(ROOT,DATANAME)
#划分的txt存储路径 该txt存放划分好训练数据的xml的文件名
IMAGESET=os.path.join(IMAGEPATH,"ImageSets")
# 输出coco格式的存放路径,为了避免与原来的注释文件重名，起名为coco_annotations
JSONPATH=os.path.join(IMAGEPATH,"annotations")


######################################################################
# 这个配置不要变动
MODE = {
    "trainval": "trainval2017",
    "train": "train2017",
    "val": "val2017",
    "test": "test2017",
}

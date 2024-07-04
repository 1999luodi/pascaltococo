import shutil

from tqdm import tqdm
import sys, os, json, glob
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt
import config


"""
data format below
"""
"""basic data structure:
{
    "info": info,
    "images": [image],
    "annotations": [annotation],
    "licenses": [license],
}

info
{
    "year": int,
    "version": str,
    "description": str,
    "contributor": str,
    "url": str,
    "date_created": datetime,
}

image
{
    "id": int,
    "width": int,
    "height": int,
    "file_name": str,
    "license": int,
    "flickr_url": str,
    "coco_url": str,
    "date_captured": datetime,
}

license
{
    "id": int,
    "name": str,
    "url": str,
}
"""
"""
annotation{
"id": int, "image_id": int, "category_id": int, "segmentation": RLE or [polygon], "area": float, "bbox": [x,y,width,height], "iscrowd": 0 or 1,
}

categories[{
"id": int, "name": str, "supercategory": str,
}]
"""


def convert_to_cocodetection(dir, datasets_name, output_dir):
    """
    input:
        dir:the path to DIOR dataset
        output_dir:the path write the coco form json file
    """
    annotations_path = config.ANNOTATION_ROOT
    ImageSets_path = config.TARGETROOT
    Root_path=config.ROOT
    DATASET_NAME=config.DATASET_NAME


    # 将数据集的类别信息 存放到字典中
    #  数据集的类型
    category_list = config.CATEGORY_LIST
    label_ids = {name: i + 1 for i, name in enumerate(category_list)}
    categories = []
    for k, v in label_ids.items():
        categories.append({"id": v, "name": k})

    # 读取xml文件并转化为json
    for mode in config.MODE:
        images = []
        annotations = []
        object_count = 0  # xml中的object数量也是bbox的个数

        #打开分类好的txt文件 得图片名
        with open(os.path.join(ImageSets_path, '%s' % mode + '.txt'), 'r') as f:
            file = f.read().strip().split()
            # 依次读取训练集或测试集中的每一张图片的名字
            with tqdm(total=len(file), desc="%s" % mode + ".json loading") as pbar:
                for idx, name in enumerate(file):

                    filename = name + ".jpg"
                    annotation_name = name + ".xml"
                    # xml标注文件信息解析
                    tree = ET.parse(annotations_path + "\\" + annotation_name)
                    root = tree.getroot()

                    # images信息处理
                    ROOT_true = os.path.join(Root_path, DATASET_NAME)
                    path_mode=os.path.join(ROOT_true,mode)
                    path_img=os.path.join(path_mode,filename)
                    img=plt.imread(path_img)
                    height,width=img.shape[:2]
                    images.append(dict(
                        id=idx,
                        file_name=filename,
                        height=height,
                        width=width))


                    # annotation 注释信息
                    for obj in root.iter('object'):
                        annotation = {}
                        # 获得类别 =string 类型
                        category_name = obj.find('name').text
                        # 如果类别不是对应在我们预定好的class文件中则跳过
                        if category_name not in category_list:
                            continue
                        # 找到bndbox 对象
                        xmlbox = obj.find('bndbox')
                        # 获取对应的bndbox的数组 = ['xmin','xmax','ymin','ymax']
                        bbox = (float(xmlbox.find('xmin').text), float(xmlbox.find('ymin').text),
                                float(xmlbox.find('xmax').text), float(xmlbox.find('ymax').text))
                        # 整数化
                        bbox = [int(i) for i in bbox]
                        # 将voc的xyxy坐标格式，转换为coco的xywh格式
                        bbox = xyxy_to_xywh(bbox)
                        # 将xml中的信息存入annotations
                        annotation["id"] = object_count
                        annotation["image_id"] = idx
                        annotation["category_id"] = get_id_by_name(category_name,categories)
                        annotation["segmentation"] = []
                        annotation["area"] = bbox[2] * bbox[3]
                        annotation["bbox"] = bbox
                        annotation["iscrowd"] = 0
                        object_count += 1
                        annotations.append(annotation)
                    pbar.update(1)

            # 汇总所有信息，保存在字典中
            dataset_dict = {}
            dataset_dict["images"] = images
            dataset_dict["annotations"] = annotations
            dataset_dict["categories"] = categories
            json_str = json.dumps(dataset_dict)
            save_file = f'{output_dir}/instances_{mode}.json'
            with open(save_file, 'w') as json_file:
                json_file.write(json_str)

    print("json file write done...")


def xyxy_to_xywh(boxes):
    width = boxes[2] - boxes[0]
    height = boxes[3] - boxes[1]
    return [boxes[0], boxes[1], width, height]

def get_id_by_name(name, categories):
    for category in categories:
        if category['name'] == name:
            return category['id']
    return None  # 如果没有找到对应的名称，返回None
def voco2coco():
    # 数据集的路径
    DATASET_ROOT = config.ROOT
    # 数据集名称
    DATASET_NAME = config.DATASET_NAME
    # 输出coco格式的存放路径
    ROOT_true = os.path.join(config.ROOT, config.DATASET_NAME)
    JSON_ROOT = os.path.join(ROOT_true, 'annotations')
    # 递归删除之前存放json的文件夹，并新建一个
    try:
        shutil.rmtree(JSON_ROOT)
    except OSError:
        pass
    os.mkdir(JSON_ROOT)
    convert_to_cocodetection(dir=DATASET_ROOT, datasets_name=DATASET_NAME, output_dir=JSON_ROOT)

if __name__ == '__main__':
    voco2coco()
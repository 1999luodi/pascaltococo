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


def convert_to_cocodetection(imageSets_path,output_dir):
    """
    input:
        dir:the path to DIOR dataset
        output_dir:the path write the coco form json file
    """
    ImageSets_path=imageSets_path
    
    

    ## 将数据集的类别信息 存放到字典中
    #  数据集的类型
    category_list = config.CATEGORY_LIST
    label_ids = {name: i + 1 for i, name in enumerate(category_list)}
    categories = []
    for k, v in label_ids.items():
        categories.append({"id": v, "name": k})

    # 读取xml文件并转化为json
    for mode in config.MODE.values():
        
        ## 将图像信息 注释信息放入
        images = []
        annotations = []
        object_count = 0  # xml中的object数量也是bbox的个数

        #打开分类好的txt文件 得图片路径
        with open(os.path.join(ImageSets_path, '%s' % mode + '.txt'), 'r') as f:
            file = f.read().strip().split()
            # 依次读取训练集或测试集中的每一张图片的名字
            with tqdm(total=len(file), desc="%s" % mode + ".json loading") as pbar:
                for idx, namepath in enumerate(file):
                    #由于数据集图像的结构dataset/01/xxx.img  ->01/xxx.img
                    # namepath xx/xxdataset/10/img2994 ->10/img2294 +.jpg
                    # 使用 split 方法
                    name = "/".join(namepath.split("/")[-2:])  # 从倒数第2个元素开始拼接
                    
                    basename=os.path.basename(namepath)
                    #josn文件所存的图像相对地址 这里需要和图像所存的结构相匹配
                    '''
                        如果图像的路径为data/img/xxx.jpg 
                        annotation文件json路径在data/annotations/train.json

                        那么json其中images中filename:xxx.jpg 
                    
                    '''
                    filename = name + ".jpg"
                    annotation_name = namepath + ".xml"
                    #图像所在路径
                    img_path=namepath+ ".jpg"

                    # xml标注文件信息解析
                    tree=ET.parse(annotation_name)
                    root = tree.getroot()

                    # images信息处理
                    size = root.find('size')
                    if size is None:
                        #当 xml中没有size属性时，读取所指图像，获取尺寸
                       
                        img=plt.imread(img_path) # （高度、宽度和通道数）
                        height,width=img.shape[:2]
                        height,width=img.shape[:2]
                    else:
                        height = int(size.find('height').text)  # 提取高度
                        width = int(size.find('width').text)  # 提取宽度

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
                        bbox = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text),
                                int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
                        bbox=check_and_correct_bndbox(bbox)
                      
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

def check_and_correct_bndbox(bbox):
    xmin, ymin, xmax, ymax = bbox
    
    # 检查并修正 xmin 和 xmax
    if xmin > xmax:
        xmin, xmax = xmax, xmin
    
    # 检查并修正 ymin 和 ymax
    if ymin > ymax:
        ymin, ymax = ymax, ymin
    
    # 返回修正后的值
    return xmin, ymin, xmax, ymax

def xyxy_to_xywh(boxes):
    width = boxes[2] - boxes[0]
    height = boxes[3] - boxes[1]
    return [boxes[0], boxes[1], width, height]

def get_id_by_name(name, categories):
    for category in categories:
        if category['name'] == name:
            return category['id']
    return None  # 如果没有找到对应的名称，返回None
def voc2coco():
    # 数据集的路径
    DATASET_ROOT = config.ROOT
    # 数据集划分txt路径
    ImageSets_path = config.IMAGESET
    JSON_ROOT=config.JSONPATH
    # 递归删除之前存放json的文件夹，并新建一个
    try:
        shutil.rmtree(JSON_ROOT)
    except OSError:
        pass
    os.mkdir(JSON_ROOT)
    convert_to_cocodetection(imageSets_path=ImageSets_path,output_dir=JSON_ROOT)

if __name__ == '__main__':
    voc2coco()
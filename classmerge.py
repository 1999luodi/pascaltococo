import json
import numpy as np
import os
import glob #读取文件
from config import JSONPATH
# 原始类型和类别
original_types = ["ungerminated", "germinating", "germinated", "primary root", "secondary root"]
original_classes = np.arange(1,len(original_types)+1)

# 需要保留的类型
new_types = ["ungerminated", "germinated"]
original_classes = [1, 2, 2, 2,0]



def transformjson(json_path,newdirpath,newcategorieslist):
    '''
    args:
        json_path:json文件的地址
        newdirpath:新json文件的存放文件夹
        newcategorieslist:新的类列表
    '''
    #获取文件名
    filename=os.path.basename(json_path)
    # 读取原始 COCO 格式的 JSON 文件
    with open(json_path, 'r') as f:
        coco_data = json.load(f)

    # 更新 categories 为单一类
    newcategories=[]
    for i,value in enumerate(newcategorieslist):
        newcategories.append({"id":i,"name":value})
    newcategories.append({"id":2,"name":"secondary root"})
    coco_data['categories'] = newcategories

    # 修改 annotations 中的 category_id，将所有 1 改为 0
    for annotation in coco_data['annotations']:
        modifyid=annotation['category_id']
        if modifyid >1 and modifyid<4:
            annotation['category_id'] = 1
        elif modifyid==4:
            annotation['category_id'] = 2

    # 将修改后的数据写回新的 JSON 文件
    newjsonpath=os.path.join(newdirpath,filename)
    #创建newjson的文件夹
    if not os.path.exists(newdirpath):
        os.makedirs(newdirpath)
    with open(newjsonpath, 'w') as f:
        json.dump(coco_data, f, indent=4)
    print("COCO 文件已成功更新！")
 
def task():
    json_file=JSONPATH
    jsonlist=glob.glob(os.path.join(json_file,"*.json"))
    for jsonfile in jsonlist:
        transformjson(json_path=jsonfile,newdirpath=os.path.join(json_file,"newjson"),newcategorieslist=new_types)

if __name__=="__main__":
    task()
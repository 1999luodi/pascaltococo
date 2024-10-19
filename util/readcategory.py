import json
import os

jsonpath=""

def extract_category_list(json_file_path):
    with open(json_file_path,"r") as file:
        data=json.load(file)
    category_list=[category['name'] for category in data['categories']]
    return category_list
if __name__=="__main__":
    jsonpath="/home/luodi23/mmdetection/data/PestData/annotations/instances_val2017.json"
    list=extract_category_list(jsonpath)
    print(repr(list),len(list)) # 使用 repr() 确保输出中的引号被包含
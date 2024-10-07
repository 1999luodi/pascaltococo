import os
import random
import shutil
import config
from config import MODE

'''
对图片数据集进行随机分类 生成Imagset
train:val:test 比例可以自己调控
生成3个txt文件存划分文件名

'''



def get_xml_files(annotations_folder):
    '''
    return:得到文件中所有子文件夹的xml列表
    '''
    xml_files = []
    for root, _, files in os.walk(annotations_folder):
        for file in files:
            if file.endswith('.xml'):
                xml_files.append(os.path.join(root, file)) # /path/to/annotations/folder/example.xml
    return xml_files


def makeTXT_811(trainpercent,valpercent,testpercent):
    xmlfilepath = config.ANNOTATION_ROOT  # 获取你源数据的注释路径
    txtsavepath = config.IMAGESET  # 设置你txt的保存路径
    # 递归删除之前存放txt的文件夹，并新建一个
    try:
        shutil.rmtree(txtsavepath)
    except OSError:
        pass
    os.makedirs(txtsavepath, exist_ok=True)

    # 当注释文件夹有多个子文件时将不能获取全部的xml文件
    # total_xml = os.listdir(xmlfilepath)  # 获取xml文件列表
    total_xml=get_xml_files(xmlfilepath)

    num = len(total_xml)  # 获取xml文件的数量
    list_indices = list(range(num))  # 获取xml文件的序列号
    random.shuffle(list_indices)  # 使用shuffle函数打乱列表的次序

    trainp = trainpercent
    valp = valpercent
    testp= testpercent
    tv = int(num * (trainp+valp))  
    tr=int(num*trainp) # 划分训练集的数量
    val = int(num * valp)  # 划分验证集的数量


    trainval = random.sample(list_indices, tv)
    train = random.sample(trainval, tr)

    with open(os.path.join(txtsavepath, MODE["trainval"]+'.txt'), 'w') as ftrainval, \
            open(os.path.join(txtsavepath, MODE["train"]+'.txt'), 'w') as ftrain, \
            open(os.path.join(txtsavepath, MODE["val"]+'.txt'), 'w') as fval, \
            open(os.path.join(txtsavepath, MODE["test"]+'.txt'), 'w') as ftest:
        for i in list_indices:
            # 获取文件名称中.xml之前的部分 ('/path/to/file/example', '.xml')
            name = os.path.splitext(total_xml[i])[0] + '\n'

            if i in trainval:
                ftrainval.write(name)
                if i in train:
                    ftrain.write(name)
                else:
                    fval.write(name)
            else:
                ftest.write(name)

if __name__ == '__main__':
    makeTXT_811(0.8,0.2,0)
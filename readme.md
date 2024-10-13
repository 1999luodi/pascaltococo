# 使用说明
1. 修改config.py 更改源数据的路径信息
2. 更改划分的比例
3. 执行main.py文件


# 文件介绍
1. maketxt.py 首先检索xml的文件名，根据划分比例生成划分好的txt文件
2. split_datasets.py 根据txt文件copy数据的照片
3. pascal2coco.py 根据txt文件中的文件名，生成annotation文件夹，其中包含各个划分的json文件
4. classmerge.py 根据要求将源数据集的class类合并想要的新class类，生成新的标准json文件


# coco 数据集
coco的annotiaon.json主要部分
```    
包括以下字段：
images部分：
    id：唯一标识图像的ID。
    file_name：图像文件的文件名。
    width：图像宽度（以像素为单位）。
    height：图像高度（以像素为单位）。
    license（可选）：图像的许可证信息。
    
annotations部分：
    id：唯一标识注释的ID。
    image_id：与注释相关联的图像的ID。
    category_id：对象的类别ID，对应于categories部分中的类别。
    segmentation：对象的分割掩码，通常表示为多边形或掩码的像素坐标。
    area：对象的像素面积。    
    bbox：对象的边界框，格式为[x, y, width, height]。
    iscrowd：标志位，指示对象是否是“杂乱”（例如，一群对象被视为单个对象）。
    
categories部分：
    id：唯一标识类别的ID。
    name：类别的名称。
    supercategory：类别的超类别，用于组织相关类别。
```
# 用法
```
只有通过 maketxt.py 生成txt文件，才能通过 pascal2coco.py 生成json文件和通过 split_imgcopy.py 拷贝图像到新的文件夹从而建立一个独立的数据集文件

```
- 目录结构

![目录](/resource/structure.jpg)

- maketxt





# 其他：MMD框架格式转换

在 MMDetection 和 MMYOLO 里，几乎所有的训练都是依靠 COCO JSON 标注文件，因此我们需要先将在 labelme 中转化得到的 voc 数据转化为 coco 格式的数据才能正常的进行训练。幸运的是，在 MMDetection 源码中就提供了这样的一个脚本来帮我们进行转化，我们利用这个脚本就能实现 voc 格式数据集转化成 coco 格式数据集。但是前提是要在 MMDeteciton 源码下的 mmdet/evaluation/functional/class_names.py 这个 Python 文件里找到coco_classes 和 voc_classes 的位置（按ctrl+F搜索即可）并添加我们需要的标签。不然将无法进行转化。在这里我们要添加的标签就是“helmet”、“person”、“head”。
![image](https://github.com/1999luodi/pascaltococo/assets/75122356/3105aee7-344d-4e53-955a-a76e9c1bcd70)

接下来我们就需要进入源码中找到 tools/dataset_converters/pascal_voc.py 文件，并了解其所需要的文件结构和转化后的内容。由于官方提供的代码转换出来的格式并不符合预期，我对该代码进行了修正，从而让 VOC 转出来的 COCO 格式直接可以用于实际的训练当中（修改后删除了 trainval.txt 和 test.txt 的转换，所以我们只需要考虑训练集和验证集的内容即可。另外还将根据 xml 的标注文件将图片文件按照官方 COCO 数据集的形式复制进入，那么我们就不再需要额外的脚本进行此类操作）。



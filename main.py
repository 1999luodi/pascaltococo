import maketxt
import split_datasets
import pascal2coco 
maketxt.maketxt(0.8,0.2,0) # train:val:test ->得到trainval、train、val、test的注释json文件
# split_datasets.split() # 这个图像的复制，后期决定不使用
pascal2coco.voco2coco()
import maketxt
import split_imgcopy
import pascal2coco 
from config import SPLITSCALE
maketxt.makeTXT_811(*SPLITSCALE) # train:val:test ->得到trainval、train、val、test的注释json文件
split_imgcopy.split() 
pascal2coco.voc2coco()
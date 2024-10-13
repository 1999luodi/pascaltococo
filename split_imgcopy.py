"""
用于数据集的划分，将全部图片分为train和val，并拷贝到不同文件夹下
"""
import shutil
import os
from config import IMG_ROOT,ANNOTATION_ROOT,IMAGEPATH, IMAGESET
from tqdm import tqdm

sets = ['train2017', 'val2017', 'test2017', 'trainval2017']  # 划分数据集的类型'train','val','test'
path_prefix_length=len(ANNOTATION_ROOT.split('/'))
def split():
    
    for img_set in sets:
        # 生成新的数据的存储路径
        new_img_root = os.path.join(IMAGEPATH, img_set)  # 获取存放的train val test的数据路径

        # 递归删除之前的文件夹，并新建一个
        try:
            shutil.rmtree(new_img_root)
        except OSError:
            pass
        os.makedirs(new_img_root, exist_ok=True)
        with open(os.path.join(IMAGESET, '%s.txt' % (img_set)), 'r') as file:
            # 获取imageset划分好的数据 ./dataset/annotations/pg1_1_img002
            img_paths = file.read().strip().split()
            '''
            read():读取数据
            strip()：移除两端空白数据
            split():分割数据
            '''
            # 使用tqdm来创建一个进度条，这里我们使用len(img_ids)作为总数
            with tqdm(total=len(img_paths), desc='%s ' % img_set + 'Copying images') as pbar:
                for img_path in img_paths:
                    imgbasename=os.path.basename(img_path)+'.jpg'
                    suffix='/'.join(img_path.split('/')[path_prefix_length:])+'.jpg'                 
                    src_root = os.path.join(IMG_ROOT, suffix)  # 源图片路径
                    tar_root = os.path.join(new_img_root, imgbasename)  # 复制的图片路径
                    shutil.copy(src=src_root, dst=tar_root)
                    # 更新进度条
                    pbar.update(1)


if __name__ == '__main__':
    split()

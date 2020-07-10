import os
from django.shortcuts import render
from fanphotos import settings
from PIL import Image
#  glob 文件名模式匹配，不用遍历整个目录判断每个文件是不是符合。
import glob
from back import modelform
import math
from io import BytesIO
import rawpy
import imageio


# im = Image.open('C:/Users/Administrator/Desktop/test.png')
# im.thumbnail((200, 100))
# im.save('C:/Users/Administrator/Desktop/thumbnail.png', 'PNG')
# 获取所有相册名称
def get_all_photo_album_name():
    data = os.listdir(settings.PHOTO_ROOT)
    # 排除缓存文件
    a = set(data).difference([settings.CACHE_FILE_NAME])
    return a


# 初始化文件夹
def project_init():
    path = os.path.join(settings.PHOTO_ROOT, settings.CACHE_FILE_NAME)
    print(path)
    try:
        os.makedirs(path)
    except Exception as e:
        print(e)


# 新建相册
def create_photo_album(photo_album_name):
    path = os.path.join(settings.PHOTO_ROOT, photo_album_name)
    print(path)
    try:
        os.makedirs(path)
    except Exception as e:
        print(e)


# 导入相册
def import_photo_album(photo_album_name):
    all_photo_album_name = get_all_photo_album_name()
    pass


# photo_album 相册名, raw_img_name相片名称
def create_image_cache(photo_album, raw_img_name):
    thumb_photo(photo_album, raw_img_name)


def list_dir(dir, filter=None):
    list = os.listdir(dir)  # 列出目录下的所有文件和目录
    i = 1
    out = ''
    for line in list:
        # __img = Image.open(dir + '/' + line)
        cut_photo(dir + '/' + line, '%s-375.jpg' % str(i), 375)
        cut_photo(dir + '/' + line, '%s-480.jpg' % str(i), 400)
        cut_photo(dir + '/' + line, '%s-800.jpg' % str(i), 800)
        cut_photo(dir + '/' + line, '%s-1600.jpg' % str(i), 1600)
        thumb_photo(dir + '/' + line, 'thumb-%s.jpg' % str(i))
        out = out + "<li class=\"col-xs-6 col-sm-4 col-md-3\" data-responsive=\"photo/%s-375.jpg 375, photo/%s-480.jpg 480, photo/%s-800.jpg 800\" data-src=\"photo/%s-1600.jpg\" data-sub-html=\"<h4>%s</h4>\"><a href=\"\"><img class=\"img-responsive\" src=\"photo/thumb-%s.jpg\"></a></li>\n" % (
            str(i), str(i), str(i), str(i), line, str(i))
        i = i + 1
    print(out)


def cut_photo(photo_album, raw_img_name, size_width):
    photo_album_path = os.path.join(settings.PHOTO_ROOT, settings.CACHE_FILE_NAME, photo_album)
    # 目录不存在，先创建
    if not os.path.isdir(photo_album_path):
        os.makedirs(photo_album_path)
    image_name, image_suffix = os.path.splitext(raw_img_name)
    __img = Image.open(os.path.join(settings.PHOTO_ROOT, photo_album, raw_img_name))
    # __img = Image.open(file_path)
    print(__img.format, __img.size, __img.mode)
    if __img.size[0] > size_width:
        newWidth = size_width
        newHeight = float(size_width) / __img.size[0] * __img.size[1]
        __img.thumbnail((newWidth, newHeight), Image.ANTIALIAS)
    __img.save(os.path.join(photo_album_path, image_name + ".png"), "JPEG")


# 缩略图
def thumb_photo(photo_album, raw_img_name, _im=None):
    # 计算缩放比例，先缩放原图，能框住box， 然后从中间剪裁出缩略图
    # 并且尽可能的裁剪出图片的中间部分,一般人摄影都会把主题放在靠中间
    photo_album_path = os.path.join(settings.PHOTO_ROOT, settings.CACHE_FILE_NAME, photo_album)
    # 目录不存在，先创建
    if not os.path.isdir(photo_album_path):
        os.makedirs(photo_album_path)
    image_name, image_suffix = os.path.splitext(raw_img_name)
    if _im:
        __img = _im
    else:
        __img = Image.open(os.path.join(settings.PHOTO_ROOT, photo_album, raw_img_name))
    # 先缩放，能框住box， 然后从中间剪裁出缩略图
    # 1920*1080   800*600
    _width = int(__img.size[0])
    _height = int(__img.size[1])
    box_width = int(settings.CACHE_IMG_SIZE[0])
    box_height = int(settings.CACHE_IMG_SIZE[1])
    # 裁切的框
    box = ()
    # 缩放后大小
    scaling_size = None
    # 计算缩放比例
    scaling_ratio = box_width / _width
    if scaling_ratio * _height >= box_height:
        # math.ceil 向上取整数
        scaling_size = (math.ceil(_width * scaling_ratio), math.ceil(_height * scaling_ratio))
    else:
        scaling_ratio = box_height / _height
        scaling_size = (math.ceil(_width * scaling_ratio), math.ceil(_height * scaling_ratio))
    # 图像等比例缩放
    __img.thumbnail(scaling_size)
    width = int(__img.size[0])
    height = int(__img.size[1])
    top = width / 2 - box_width / 2
    right = height / 2 - box_height / 2
    buttom = width / 2 + box_width / 2
    left = height / 2 + box_height / 2
    box = (top, right, buttom, left)
    print(box)
    region = __img.crop(box)
    region.thumbnail(settings.CACHE_IMG_SIZE, Image.ANTIALIAS)
    region.save(os.path.join(photo_album_path, image_name + ".png"), "JPEG")


# photo_album 相册名, raw_img_name相片名称
def create_raw_image_cache(photo_album, raw_img_name):
    path = os.path.join(settings.PHOTO_ROOT, photo_album, raw_img_name)
    thumb = None
    with rawpy.imread(path) as raw:
        thumb = raw.extract_thumb()
        print(thumb.format)
    if thumb.format == rawpy.ThumbFormat.JPEG:
        print("if")
        # 将bytes结果转化为字节流
        bytes_stream = BytesIO(thumb.data)
        with Image.open(bytes_stream) as im:
            thumb_photo(photo_album, raw_img_name, im)
    elif thumb.format == rawpy.ThumbFormat.BITMAP:
        # thumb.data is an RGB numpy array, convert with imageio
        _im = imageio.imsave(imageio.RETURN_BYTES, thumb.data)
        with Image.open(_im) as im:
            thumb_photo(photo_album, raw_img_name, im)
    else:
        print("else")


if __name__ == "__main__":
    pass

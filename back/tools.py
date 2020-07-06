import os
from django.shortcuts import render
from fanphotos import settings
from PIL import Image
#  glob 文件名模式匹配，不用遍历整个目录判断每个文件是不是符合。
import glob
from back import modelform


# im = Image.open('C:/Users/Administrator/Desktop/test.png')
# im.thumbnail((200, 100))
# im.save('C:/Users/Administrator/Desktop/thumbnail.png', 'PNG')
# 获取所有相册名称
def get_all_photo_album_name():
    data = os.listdir(settings.PHOTO_ROOT)
    # 排除缓存文件
    a = set(data).difference([settings.CACHE_FILE_NAME])
    print(a)
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
    im = Image.open(os.path.join(settings.PHOTO_ROOT, photo_album, raw_img_name))
    # 相册缓存路径
    photo_album_path = os.path.join(settings.PHOTO_ROOT, settings.CACHE_FILE_NAME, photo_album)
    # 目录不存在，先创建
    if not os.path.isdir(photo_album_path):
        os.makedirs(photo_album_path)
    # 图片压缩
    im.thumbnail((200, 100))
    image_name, image_suffix = os.path.splitext(raw_img_name)
    im.save(os.path.join(photo_album_path, image_name + ".png"), "PNG")


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
    image_name, image_suffix = os.path.splitext(raw_img_name)
    __img = Image.open(os.path.join(settings.PHOTO_ROOT, photo_album, raw_img_name))
    # __img = Image.open(file_path)
    print(__img.format, __img.size, __img.mode)
    if __img.size[0] > size_width:
        newWidth = size_width
        newHeight = float(size_width) / __img.size[0] * __img.size[1]
        __img.thumbnail((newWidth, newHeight), Image.ANTIALIAS)
    __img.save(os.path.join(photo_album_path, image_name + ".png"), "JPEG")


def thumb_photo(photo_album, raw_img_name):
    photo_album_path = os.path.join(settings.PHOTO_ROOT, settings.CACHE_FILE_NAME, photo_album)
    image_name, image_suffix = os.path.splitext(raw_img_name)
    __img = Image.open(os.path.join(settings.PHOTO_ROOT, photo_album, raw_img_name))
    box = clipimage(__img.size)
    size = (100, 100)
    region = __img.crop(box, size)

    region.thumbnail(size, Image.ANTIALIAS)
    region.save(os.path.join(photo_album_path, image_name + ".png"), "JPEG")


# 取宽和高的值小的那一个来生成裁剪图片用的box
# 并且尽可能的裁剪出图片的中间部分,一般人摄影都会把主题放在靠中间的,个别艺术家有特殊的艺术需求我顾不上
def clipimage(img_size, box_size):
    # 1920*1080   800*600
    width = int(img_size[0])
    height = int(img_size[1])
    box_width = int(box_size[0])
    box_height = int(box_size[1])
    box = ()
    if (width > height):
        dx = width - height
        # box = (dx / 2, 0, height + dx / 2, height)
        top = (width - box_width) / 2
        right = (height - box_height) / 2
        buttom = top + box_width
        left = None
        box = (top, right, buttom, left)
    else:
        dx = height - width
        box = (0, dx / 2, width, width + dx / 2)
    return box


# photo_album 相册名, raw_img_name相片名称
def create_raw_image_cache(photo_album, raw_img_name):
    photo_album_path = os.path.join(settings.PHOTO_ROOT, settings.CACHE_FILE_NAME, photo_album)
    image_name, image_suffix = os.path.splitext(raw_img_name)
    # import cv2
    # import SimpleITK as sitk
    # import matplotlib.pyplot as plt
    import numpy as np
    path = os.path.join(settings.PHOTO_ROOT, photo_album, raw_img_name)
    # image = sitk.ReadImage(path)
    # image = sitk.GetArrayFromImage(image)
    # image = np.squeeze(image[slice, ...])  # if the image is 3d, the slice is integer
    # plt.imshow(image, cmap='gray')
    # plt.axis('off')
    # plt.show()
    # cv2.imwrite('1.png', image)
    ############################################################
    import rawpy
    import imageio
    # import matplotlib.pylab as plt
    # with rawpy.imread(path) as raw:
    #
    #     # 直接调用postprocess可能出现偏色问题
    #     # rgb = raw.postprocess()
    #     # 以下两行可能解决偏色问题，output_bps=16表示输出是 16 bit (2^16=65536)需要转换一次
    #     im = raw.postprocess(use_camera_wb=True, half_size=False, no_auto_bright=True, output_bps=16)
    #
    # rgb = np.float32(im / 65535.0 * 255.0)
    # rgb = np.asarray(rgb, np.uint8)
    # imageio.imsave(os.path.j
    # oin(photo_album_path, image_name + ".png"), rgb)
    ############################################################

    with rawpy.imread(path) as raw:
        # raises rawpy.LibRawNoThumbnailError if thumbnail missing
        # raises rawpy.LibRawUnsupportedThumbnailError if unsupported format
        thumb = raw.extract_thumb()
        print(thumb.format)
    if thumb.format == rawpy.ThumbFormat.JPEG:
        print("if")
        # thumb.data is already in JPEG format, save as-is
        # im = Image.open(thumb.data)
        # with Image.open(thumb.data) as im:
        #     im.thumbnail((200, 100))
        #     im.save(os.path.join(photo_album_path, image_name + ".png"), "PNG")
        # with open('thumb.jpeg', 'wb') as f:
        #     # f.write(thumb.data)
        # 将bytes结果转化为字节流
        from io import BytesIO
        bytes_stream = BytesIO(thumb.data)
        # print(thumb.data.decode())
        # print(type(thumb.data))
        # img = thumb.data.decode()
        with Image.open(bytes_stream) as im:
            im.thumbnail((500, 500))
            im.save(os.path.join(photo_album_path, image_name + ".png"), "PNG")
        # im.save('C:/Users/Administrator/Desktop/thumbnail.png', 'PNG')

        # with open('thumb.jpeg', 'wb') as f:
        #     f.write(im)
    elif thumb.format == rawpy.ThumbFormat.BITMAP:
        # thumb.data is an RGB numpy array, convert with imageio
        imageio.imsave('thumb.jpeg', thumb.data)
    else:
        print("else")

    ##################################################################
    # im = Image.open(os.path.join(settings.PHOTO_ROOT, photo_album, raw_img_name))
    # # 相册缓存路径
    # photo_album_path = os.path.join(settings.PHOTO_ROOT, settings.CACHE_FILE_NAME, photo_album)
    # # 目录不存在，先创建
    # if not os.path.isdir(photo_album_path):
    #     os.makedirs(photo_album_path)
    # # 图片压缩
    # im.thumbnail((200, 100))
    # image_name, image_suffix = os.path.splitext(raw_img_name)
    # # im.save('C:/Users/Administrator/Desktop/thumbnail.png', 'PNG')
    # im.save(os.path.join(photo_album_path, image_name + ".png"), "PNG")




if __name__ == "__main__":
    # create_photo_album("asfaf")
    create_image_cache("aaaa", "1.jpg")
    pass
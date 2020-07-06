import os
from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage

# Create your views here.
from .tools import *
from django.views.static import serve


def index(request):
    root_list = glob.glob(settings.PHOTO_ROOT + '/*')
    print("root_list:", root_list)
    _photo_album = get_all_photo_album_name()
    data = os.listdir(settings.PHOTO_ROOT)
    project_init()
    # path = settings.PHOTO_URL
    # create_raw_image_cache("aaaa", "_DSC0012.ARW")
    # cut_photo("aaaa", "1.jpg", 100)
    # thumb_photo("aaaa", "1.jpg")
    # 创建相册

    return render(request, "index.html", {'data': data, "photo_album": _photo_album})


def flash_cache(request):
    album_list = get_all_photo_album_name()
    for album_name in album_list:
        Folderpath = os.path.join(settings.PHOTO_ROOT, album_name) + "/*[jpg,png]"
        # 删选出jpg和png格式的图片
        pictures_path = glob.glob(Folderpath)
        print("pictures_path", pictures_path)
        for i in pictures_path:
            print("create_image_cache", album_name, os.path.basename(i))
            create_image_cache(album_name, os.path.basename(i))
    return HttpResponse("ok")


def album(request, album_name, page="1"):
    if request.is_ajax():
        real_list = os.listdir(os.path.join(settings.PHOTO_ROOT, settings.CACHE_FILE_NAME, album_name))
        paginator = Paginator(real_list, 10)
        try:
            users = paginator.page(page)
        # 如果页数不是整数，返回第一页
        except PageNotAnInteger:
            users = paginator.page(1)
        # 如果页数不存在/不合法，返回最后一页
        except InvalidPage:
            users = paginator.page(paginator.num_pages)
        # 分别为是否有上一页false/true，是否有下一页false/true，总共多少页，当前页面的数据
        result = {'has_previous': users.has_previous(),
                  'has_next': users.has_next(),
                  'this_page': users.number,
                  'num_pages': users.paginator.num_pages,
                  'data': users.object_list,
                  "album_name": album_name
                  }
        print(result)
        return JsonResponse(result)
    if request.method == "POST":
        real_list = os.listdir(os.path.join(settings.PHOTO_ROOT, settings.CACHE_FILE_NAME, album_name))
        paginator = Paginator(real_list, 10)
        _photo_album = get_all_photo_album_name()
        data = paginator.page(page)
        print("data", data)
        return render(request, "index.html", {'data': data, "photo_album": _photo_album, "album_name": album_name})

    # root_list = glob.glob(settings.PHOTO_ROOT + '/*')
    # print("root_list:", root_list)
    # file_dir = os.path.join(settings.CACHE_FILE_NAME, album_name)
    _dir = os.path.join(settings.PHOTO_ROOT, settings.CACHE_FILE_NAME, album_name)
    if not os.path.isdir(_dir):
        os.makedirs(_dir)
    real_list = os.listdir(_dir)
    paginator = Paginator(real_list, 10)
    _photo_album = get_all_photo_album_name()
    data = paginator.page(page)
    print("data", data)
    return render(request, "index.html", {'data': data, "photo_album": _photo_album, "album_name": album_name})


def CreatePhotoAlbum(request):
    # 创建相册

    if request.method == "GET":
        data = modelform.PhotoAlbumForm()
        return render(request, "list.html", {'data': data, })
    elif request.method == "POST":
        data = modelform.PhotoAlbumForm(request.POST)
        if data.is_valid():
            # 创建文件
            create_photo_album(data.data.get("photo_album_name"))
            data.save()
            print("aa")
            return redirect("/")
    return render(request, "index.html", )

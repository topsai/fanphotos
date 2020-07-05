from django.db import models


# Create your models here.
# 相册
class PhotoAlbum(models.Model):
    photo_album_name = models.CharField(max_length=256)
    # 相册别名
    photo_album_alias_name = models.CharField(max_length=256)
    photo_album_Introduction = models.CharField(max_length=256)


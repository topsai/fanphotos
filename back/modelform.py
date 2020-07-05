#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.forms import ModelForm

"""
@Time :    2020/7/5 1:56
@Author:  "范斯特罗夫斯基" John
@File: modelform.py
@Software: PyCharm
"""
from back import models


class PhotoAlbumForm(ModelForm):
    class Meta:
        model = models.PhotoAlbum
        # fields = ('name', 'title')
        fields = "__all__"

    # def clean_name(self):
    #     if 1:
    #         return self.clean_data['name']
    #     else:
    #         raise ValidationError("")

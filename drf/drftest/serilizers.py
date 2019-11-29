# -*- coding: utf-8 -*-
# -*- author: 任士梅-*-

from rest_framework import serializers
from .models import Student

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student   #指定序列化的模型类
        fields = "__all__"  #显示表中的所有字段
        # fields = ('id','name')  显示指定的几个字段

# -*- coding: utf-8 -*-
# -*- author: 任士梅-*-

"""
我们可以使用ModelSerializer来完成模型类序列化器的声明，
这种基于ModelSerializer声明序列化器的方式有三个优势：
1.可以直接通过声明当前序列化器中指定的模型中把字段声明引用过来
2.ModelSerializer是继承了Serializer的所有工作和方法，同时还编写update和create
3.模型中同一个字段中关于验证的选项，也会被引用到序列化器中一并作为选项参与验证
"""

from drftest.models import Student
from rest_framework import serializers
class StudentModelSerializer(serializers.ModelSerializer):
    #字段声明[如果模型中没有的字段，还需要用户提交，则需要手动这里声明]

    #指定引用的模型和属性字段
    class Meta:
        model = Student
        fields = "__all__"  #指定返回所有字段
        # fields = ["id","name","age","is_18"]  #返回指定字段  "is_18"自定义方法

    """验证多个字段的数据"""

    def validate(self, data_dict):  # data_dict 表示客户端提交的所有数据
        # 从数据中提取要验证的字段
        name = data_dict.get("name")
        age = data_dict.get("age")
        # 验证名称的合法性
        if name == "大笨蛋":
            raise serializers.ValidationError("对不起当前网站已经使用了该昵称,请更换后再试")


        # 验证年龄的合法性
        if age < 1:
            raise serializers.ValidationError("对不起，您这个年龄还没有出生》")

        return data_dict
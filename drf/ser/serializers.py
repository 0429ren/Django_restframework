# -*- coding: utf-8 -*-
# -*- author: 任士梅-*-

#声明序列化器
from rest_framework import serializers

# 所有的序列化器必须直接或间接继承于 serializers.Serializer
class StudentSerializers(serializers.Serializer):
    # 1.字段声明[要转换的字段,当然，如果写了第二部分代码，有时候也可以不写声明字段]
        id = serializers.IntegerField()
        name = serializers.CharField()
        age = serializers.IntegerField()
        sex = serializers.BooleanField()
        class_null = serializers.CharField()
        description = serializers.CharField()
    # 2.可选 [如果序列化器继承的是ModelSerializer,则需要声明对应的模型类和字段，ModelSerializer 是Serializer的子类]

    # 3.可选 [用于把客户端提交的数据进行验证]
    # 4. 可选 [用于把通过验证的数据进行数据库操作，保存到数据库]
"""
在drf中，对于客户端提供的数据，往往需要验证数据的有效性，这部分代码是写在序列化器中的。
在序列化器中，已经提供三个地方给我们针对客户端提交的数据进行验证。
1.内置选项，字段声明的小圆括号中，以选项存在作为验证提交
2.自定义方法，在序列化器中作为对象方法来提供验证[这部分验证的方法，必须以'validate_<字段>'或者"validate"作为方法名]
3.自定义函数，在序列化器外部，提前声明一个验证代码，然后在字段声明的小圆括号中，通过"validators=[验证函数1,验证函数2...]"
"""




def check_user(data):
    if data == "luffy":
        raise serializers.ValidationError("用户名不能是luffy")
    return data

from drftest.models import Student

# 所有的序列化器必须直接或间接继承于 serializers.Serializer
class Student3Serializers(serializers.Serializer):
    # 1.字段声明[要转换的字段,当然，如果写了第二部分代码，有时候也可以不写声明字段]
        name = serializers.CharField(max_length=20,min_length=3,validators=[check_user])   #设置内置选项，指定最小最大长度
        age = serializers.IntegerField(max_value=150,min_value=0)  #设置内置选项，指定最大年龄最小年龄范围
        sex = serializers.BooleanField(required=True)  #设置内置选项 必填项
        class_null = serializers.CharField()
        description = serializers.CharField()
    # 2.可选 [如果序列化器继承的是ModelSerializer,则需要声明对应的模型类和字段，ModelSerializer 是Serializer的子类]

    # 3.可选 [用于把客户端提交的数据进行验证]
        """验证单个字段的数据  validate_字段名"""
        def validate_name(self,data):
            if data == "root":
                raise serializers.ValidationError('当前字段不能叫root')  #抛出错误
            #验证方法结束时必须返回本次验证内容
            return data
        def validate_age(self,data):
            if data <= 10:
                raise serializers.ValidationError('当前注册年龄必须是十岁以上！')  #抛出错误
            return data

        """验证多个字段的数据"""
        def validate(self, data_dict): #data_dict 表示客户端提交的所有数据
            # 从数据中提取要验证的字段
            name = data_dict.get("name")
            if name == "大笨蛋":
                raise serializers.ValidationError("对不起当前网站已经使用了该昵称,请更换后再试")
            return data_dict


    # 4. 可选 [用于把通过验证的数据进行数据库操作，保存到数据库]
    # """  在完成数据验证以后,drf 提供了request和response()来接收和返回数据
    #         1.create
    #         2.update
    # """
        def create(self,validate):
            """接收客户端提交的新增数据"""
            name = validate.get("name")
            age = validate.get("age")
            sex = validate.get("sex")
            class_null = validate.get("class_null")
            description = validate.get("description")

            instance = Student.objects.create(
                name = name,
                age = age,
                sex =sex,
                class_null = class_null,
                description = description
            )
            return instance

        def update(self,instance,validated_data):
            """用于在反序列化中对于验证完成的数据进行保存更新"""
            name = validated_data.get("name")
            age = validated_data.get("age")
            sex = validated_data.get("sex")
            class_null = validated_data.get("class_null")
            description = validated_data.get("description")

            instance.name = name
            instance.age = age
            instance.sex = sex
            instance.class_null = class_null
            instance.description = description

            instance.save()

            return instance

"""
我们可以使用ModelSerializer来完成模型类序列化器的声明，
这种基于ModelSerializer声明序列化器的方式有三个优势：
1.可以直接通过声明当前序列化器中指定的模型中把字段声明引用过来
2.ModelSerializer是继承了Serializer的所有工作和方法，同时还编写update和create
3.模型中同一个字段中关于验证的选项，也会被引用到序列化器中一并作为选项参与验证
"""

from drftest.models import Student
class StudentModelSerializer(serializers.ModelSerializer):
    #字段声明[如果模型中没有的字段，还需要用户提交，则需要手动这里声明]

    #指定引用的模型和属性字段
    class Meta:
        model = Student
        fields = "__all__"  #指定返回所有字段
        fields = ["id","name","age","is_18"]  #返回指定字段  "is_18"自定义方法

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







"""开发中往往一个资源的序列化反序列化都是写在一个序列化器中的，
所以我们可以把上面的两个阶段合并起来
以后我们再次写序列化器，则直接按照以下风格编写即可"""

class Student4Serializer(serializers.Serializer):
    # 字段声明
    id = serializers.IntegerField(read_only=True)   #read_only = True 设置为只能后台给数据  write_only = True 设置为只能前端填数据
    name = serializers.CharField(max_length=20, min_length=3, validators=[check_user]) #设置内置选项，指定最小最大长度
    age = serializers.IntegerField(max_value=150, min_value=0)  # 设置内置选项，指定最大年龄最小年龄范围
    sex = serializers.BooleanField(required=True)  # 设置内置选项 必填项
    class_null = serializers.CharField()
    description = serializers.CharField()

    """验证多个字段的数据"""

    def validate(self, data_dict):  # data_dict 表示客户端提交的所有数据
        # 从数据中提取要验证的字段
        name = data_dict.get("name")
        if name == "大笨蛋":
            raise serializers.ValidationError("对不起当前网站已经使用了该昵称,请更换后再试")
        return data_dict

    def create(self, validate):
        """接收客户端提交的新增数据"""
        name = validate.get("name")
        age = validate.get("age")
        sex = validate.get("sex")
        class_null = validate.get("class_null")
        description = validate.get("description")

        instance = Student.objects.create(
            name=name,
            age=age,
            sex=sex,
            class_null=class_null,
            description=description,
        )

        return instance


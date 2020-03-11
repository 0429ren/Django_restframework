import sys
import os
sys.path.append(os.path.abspath(os.path.pardir))
from django.http import HttpResponse
from django.shortcuts import render
from rest_framework.response import Response
from .serializers import StudentSerializers,Student3Serializers,Student4Serializer
# 快速导包 windows :alt+enter  os:fn+option+enter
from django.views import View
from drftest.models import Student
# Create your views here.
class Student1View(View):
    """
    使用序列化器进行数据的序列化操作
    """
    """
    序列化器转换一条数据[模型对象转换成字典]
    """

    def get (self,request,pk):
        # 接收客户端的参数
        student = Student.objects.get(pk=pk)

        # 转换数据格式
        # 1.实例化序列化器类
        """
        StudentSerializers(instance =模型对象或者模型列表，客户端提交的数据，额外要传递到序列化器中使用的数据)
        """

        serializer = StudentSerializers(instance=student)
        # 2.获取序列化器转换的结果
        print(serializer.data,type(serializer.data))
        return HttpResponse(str(serializer.data))
        # HttpResponse 一定是字符串格式的数据
        # return HttpResponse('ok')

class Student2View(View):
    def get(self,request):
        student_list = Student.objects.all()
        """
        序列化器转换多条数据[模型转换成字典]
        """
        # 序列化器转换多个数据
        # many = True  表示本次序列化器转换如果有多个模型对象列表参数，则必须声明many = True

        serializer = StudentSerializers(student_list,many=True)
        """
        [OrderedDict([('id', 1), ('name', '徐菲'), ('age', 17), ('sex', True), ('class_null', '404'), ('description', '越努力越幸运')]),
         OrderedDict([('id',ame', '徐伟松'), ('age', 26), ('sex', False), ('class_null', '502'), ('description', '布朗布朗滚儿,哈哈')])]

        """
        print(serializer.data)
        return HttpResponse(serializer.data)

class Student3View(View):
    def post(self,request):
        # data_string = request.body.decode()
        # print(data_string)
        # import json
        # data_dict = json.loads(data_string)
        # print(data_dict)

        # 模拟用户提交数据
        data_dict = {"name": "luffy","sex": 1,"age": 18,"class_null": "405","description": "好黑"}
        """
        在客户端提交数据时对数据进行验证
        """
        serializer = Student3Serializers(data=data_dict)

        # # 调用序列化器进行实例化
        # # is_valid 在执行的时候，会自动先后调用字段的内置选项，自定义验证方法，自定义验证函数
        # # 调用序列化器中写好的验证代码
        # # raise_exception = True 抛出验证错误信息，并阻止代码继续往后运行
        result = serializer.is_valid(raise_exception=True)
        print('验证的结果为: %s' % result)
        #
        # # 获取验证的错误信息
        print('错误信息:%s'%serializer.error_messages)
        #
        # # 获取被验证后的客户端数据
        print("验证后的数据：%s"% serializer.validated_data)
        #
        return HttpResponse('ok')


from .serializers import Student3Serializers
from drftest.models import Student
class Student4View(View):
    # 在数据库中添加数据
    def post(self,request):
        # 模拟用户提交数据
        data_dict =  {"name": "xiaoming","sex": 1,"age": 18,"class_null": "405","description": "好黑"}
        """在客户端提交数据时，对数据进行验证"""
        serializer = Student3Serializers(data=data_dict)
        serializer.is_valid(raise_exception=True)
        #  save 表示让序列化器开始执行反序列化的代码操作，create和update的代码

        student = serializer.save()  #将字典转换成对象

        print(student)

        return HttpResponse('ok')




from .serializers import Student3Serializers
from drftest.models import Student
class Student5View(View):

    def put (self,request,pk):
        """在更新中调用序列化器完成数据的更新操作"""
        student_object = Student.objects.get(pk=pk)
        print(student_object)
        #模拟用户提交数据
        data_dict = {"name": "xiaohua", "sex": 1, "age": 18, "class_null": "405", "description": "好黑"}

        #实例化序列化器，
        serializer = Student3Serializers(instance=student_object,data=data_dict)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save() #将字典转换成对象
        print(instance)
        return HttpResponse('ok')

from .serializers import Student4Serializer
from drftest.models import Student
import json
import demjson
from django.http.response import JsonResponse
from django.views import View
class Student6View(View):
    def get(self,request):
        """获取所有数据"""
        student_list = Student.objects.all()
        # 实例化序列化器 当有好多个序列化器时，指定many = True
        serializer = Student4Serializer(instance=student_list,many=True)
        # 返回json格式的数据 多条数据的时候，要用到 safe = False
        return JsonResponse(serializer.data,safe=False)

    def post(self,request):
        """添加数据"""
        data_string = request.body.decode()
        print(data_string,type(data_string))
        data_dict = json.loads(data_string)
        print(data_dict)

        #调用序列化器
        serializer = Student4Serializer(data=data_dict)

        #  执行验证
        serializer.is_valid(raise_exception=True)

        #执行序列的反序列化
        instance = serializer.save()

        return JsonResponse(serializer.data,safe=False)





"""使用模型类序列化器ModelSerializer"""
from .serializers import StudentModelSerializer
from drftest.models import Student
import json
from django.http.response import JsonResponse
from django.views import View

class Student7View(View):
    def get(self,request):
        """获取所有数据"""
        student_list = Student.objects.all()
        # 实例化序列化器 当有好多个序列化器时，指定many = True  instance 传入的模型对象
        serializer = StudentModelSerializer(instance=student_list,many=True)
        # 返回json格式的数据 多条数据的时候，要用到 safe = False
        return JsonResponse(serializer.data,safe=False)

    def post(self,request):
        """添加数据"""
        #jsondata = request.data
        data_string = request.body.decode()
        print(data_string,type(data_string))
        data_dict = json.loads(data_string)
        print(data_dict)

        #调用序列化器  实现反序列化 data =  用于传入反序列化时客户端传入的数据
        serializer = StudentModelSerializer(data=data_dict)

        #  执行验证
        serializer.is_valid(raise_exception=True)

        #执行序列的反序列化
        instance = serializer.save()

        return JsonResponse(serializer.data,safe=False)







from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import GenericViewSet

"""
测试代码：方便区分django的View 和DRF的APIView
"""

from django.views import View
from django.http.response import JsonResponse
class Student1View(View):
    def post(self,request):
        data_dict = {"name":"小明","age":19}
        print(request)
        """打印效果
        <WSGIRequest: GET '/req/students1/'>  #这是django原生HttpRequest类
        """
        return JsonResponse(data_dict)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
class Student1APIView(APIView):
    def get(self,request):
        print(request)
        # print(request.query_params)   针对HTTPRequest.GET的别名设置而已，获取查询字符串
        """打印效果
        <rest_framework.request.Request object at 0x10eb60090>
        """
        data_dict = [{"name":"小明","age":19}]
        return Response(data_dict,status=status.HTTP_204_NO_CONTENT,headers={"COMPANY":"qishisiqi",})




"""
使用APIview提供学生信息的5个API接口
GET  /req/students3/  获取全部数据
POST /req/students3/  添加数据
GET  /req/students3/(?p<pk>\d+)  #根据ID获取一条数据
PUT  /req/students3/(?p<pk>\d+)  #根据ID更新一条数据
DELETE  /req/students3/(?p<pk>\d+)  #根据ID删除一条数据
"""


from rest_framework.views import APIView
from rest_framework.response import Response
from drftest.models import Student
from .serializers import StudentModelSerializer
class Student2APIView(APIView):
    def get(self,request):
        """获取所有数据"""
        #获取模型数据
        student_list = Student.objects.all()

        #调用序列化器
        serializer = StudentModelSerializer(instance=student_list,many=True)

        return Response(serializer.data)

    def post(self,request):
        """添加数据"""
        #接收post请求数据
        data_dict = request.data
        #调用序列化器
        serializer = StudentModelSerializer(data=data_dict)
        #验证
        serializer.is_valid(raise_exception=True)

        #反序列化 保存数据
        serializer.save()

        #响应数据
        return Response(serializer.data)

"""
使用GenericAPIView提供学生信息的5个API接口
GET  /req/students4/     获取全部数据
POST /req/students4/      添加数据
GET  /req/students4/(?P<pk>\d+)    #获取一条数据
PUT  /req/students4/(?P<pk>\d+)    #更新一条数据
DELETE /req/students4/(?P<pk>\d+)  #删除一条数据
"""
from rest_framework.generics import GenericAPIView
class Student4GenericAPIView(GenericAPIView):
    queryset = Student.objects.all()    #当前视图类中操作的公共数据，先从数据库查询出来
    serializer_class = StudentModelSerializer  #设置视图中所有方法共有调用的序列化类
    def get(self,request):
        """获取所有数据"""
        #获取模型数据    get_queryset() 获取多条数据
        student_list = self.get_queryset()
        #调用序列化器
        # serializer = StudentModelSerializer(instance=student_list,many=True)
        serializer = self.get_serializer(instance=student_list,many = True)
        return Response(serializer.data)
    def post(self,request):
        """添加数据"""
        #获取客户端提交的数据
        # serializer = StudentModelSerializer(data=request.data)
        serializer = self.get_serializer(data = request.data)
        #使用序列化器进行验证
        serializer.is_valid(raise_exception=True)
        #反序列化
        instance = serializer.save()
        #返回结果
        return Response(serializer.data)


class Student5GenericAPIView(GenericAPIView):
    queryset = Student.objects.all()  #当前视图类中操作的公共数据，先从数据库查询出来
    serializer_class = StudentModelSerializer    #设置视图中所有方法共有调用的序列化类

    def get(self,request,pk):      #这里的参数名必须叫PK,否则要配置另外一个名称，如果不配置，则报错

        #get_object()获取某一条数据
        instance = self.get_object()
        serializer = self.get_serializer(instance=instance)
        return Response(serializer.data)

    def put(self,request,pk):
        instance = self.get_object()

        #获取客户端提交的数据
        data = request.data

        #实例化序列化器
        serializer = self.get_serializer(instance = instance,data=data)

        #验证
        serializer.is_valid(raise_exception=True)

        #反序列化
        serializer.save()

        #返回响应
        return Response(serializer.data)

    def delete(self,request,pk):
        instance = self.get_object()



"""
使用GenericAPIView结合视图MiXing扩展类，快速实现数据接口的APi View
ListModelMixin 可以实现查询所有数据功能
CreateModelMixin 实现添加数据的功能
RetrieveModelMixin 实现查询一条数据的功能
UpdateModelMixin  实现更新一条数据的功能
DestoryModelMixin 删除一条数据的功能
"""
from rest_framework.mixins import ListModelMixin,CreateModelMixin,UpdateModelMixin
class Student6GenericAPIView(GenericAPIView,ListModelMixin,CreateModelMixin):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    def get(self,request):
        return self.list(request)
    def post(self,request):
        return self.create(request)


from rest_framework.mixins import RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin,ListModelMixin
class Student7GenericAPIView(GenericAPIView,ListModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
        queryset = Student.objects.all()
        serializer_class = StudentModelSerializer
        def get(self,request,pk):
            return self.retrieve(request)
        def delete(self,request,pk):
            print(pk)
            return self.destroy(request)

        def put(self,request,pk):
            return self.update(request)


from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin,DestroyModelMixin,UpdateModelMixin,ListModelMixin
class Student8GenericAPIView(GenericViewSet,ListModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
        queryset = Student.objects.all()
        serializer_class = StudentModelSerializer




"""DRF下面，内置了一些同时继承了GenericAPIView和Mixins扩展类的子类，我们可以直接继承这些子类就可以生成对应的API接口

"""
#ListAPIView 获取所有数据
#添加数据 CreateAPIView
#RetreiveAPIView 获取一条数据
#UpdateAPIView 更新一条数据
#DestoryAPIView 删除一条数据
#RetrieveUpdateDestoryAPIView  上面三个的缩写

from rest_framework.generics import ListAPIView,CreateAPIView
class Student9GenericAPIView(ListAPIView,CreateAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

#RetrieveAPIView 获取一条数据
#UpdateAPIView 更新一条数据
#DestoryAPIView 删除一条数据
#RetrieveUpdateDestoryAPIView  上面三个的缩写
from rest_framework.generics import RetrieveUpdateDestroyAPIView
class Student10RetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer


"""
视图集
上面5个接口使用了8行代码生成，但是我们发现有一半的代码重复了
所以我们要把这些重复的代码进行处理整合，但是依靠原来的类视图，其实有2方面产生冲突的
1.查询所有数据、添加数据是不需要声明pk主键的，而其他接口需要（路由冲突了）
2.查询所有数据和查询一条数据，都是属于get请求【请求方面冲突了】
为了解决上面的2个问题，所以drf 提供了视图集来解决这个问题
"""

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin,ListModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin
class StudentModelViewSet(GenericViewSet,CreateModelMixin,ListModelMixin,RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin):
        queryset = Student.objects.all()
        serializer_class = StudentModelSerializer


""""""

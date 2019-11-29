from django.shortcuts import render

# Create your views here.


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

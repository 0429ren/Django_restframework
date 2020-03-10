from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.throttling import UserRateThrottle

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,IsAdminUser
"""
用户的身份认证和权限识别
"""

"""只允许登陆后的用户进行访问"""
class DemoAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self,request):
        """个人中心"""
        return Response("个人中心")


"""只允许管理员访问"""
class Demo2APIView(APIView):
    permission_classes = [IsAdminUser]
    def get(self,request):
        """管理员个人中心"""
        return Response("管理员个人中心")

from rest_framework.permissions import BasePermission
class MyPermission(BasePermission):
    def has_permission(self, request, view):
        """针对访问视图进行页面的权限判断"""
        """
        :param request 本次操作的http
        :param view 本次访问路由对应的视图对象
        """
        if request.query_params.get("user") == "sky":
            return True
        else:
            return False
class Demo3APIView(APIView):
    permission_classes = [MyPermission]
    def get(self,request):
        """个人中心"""
        return Response("我的个人中心")

class Demo4APIView(APIView):
    throttle_classes = [UserRateThrottle]
    def get(self,request):
        """投票页面"""
        return Response("投票页面")

"""过滤功能"""
from drftest.models import Student
from rest_framework.generics import GenericAPIView
from opt.serializers import StudentModelSerializer
class Demo5APIView(GenericAPIView):
    queryset = Student.objects.all()
    serializer_class =StudentModelSerializer
    filter_fields = ("age",)
    def get(self,request):
        student_list = self.get_queryset()

        serializer = self.get_serializer(instance=student_list,many=True)

        return Response(serializer.data)


"""排序功能"""
from drftest.models import Student
from rest_framework.generics import GenericAPIView
from opt.serializers import StudentModelSerializer
from django_filters.rest_framework import OrderingFilter
class Demo6APIView(GenericAPIView):
    queryset = Student.objects.all()
    serializer_class =StudentModelSerializer

    #排序
    filter_backends = [OrderingFilter]
    ordering_fields = ['id','age']
    filter_fields = ("age",)
    def get(self,request):
        student_list = self.get_queryset()

        serializer = self.get_serializer(instance=student_list,many=True)

        return Response(serializer.data)

"""分页功能"""
from drftest.models import Student
from rest_framework.generics import GenericAPIView
from opt.serializers import StudentModelSerializer
from django_filters.rest_framework import OrderingFilter
class Demo7APIView(GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer

    def get(self,request):
        student_list = self.get_queryset()

        serializer = self.get_serializer(instance=student_list,many=True)

        return Response(serializer.data)

"""
#页码分页
page =1 limit 0,10
page =2 limit 10,10
#偏移量分页
start=0    limit 0,10
start=10   limit 10,10
start=20   limit 10,10
"""

class Demo8APIview(APIView):
    def get(self,request):
        1/0
        return Response('ok')
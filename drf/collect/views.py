from django.shortcuts import render
# Create your views here.
from rest_framework.viewsets import ViewSet
from drftest.models import Student
from rest_framework.generics import GenericAPIView
from .serializers import StudentModelSerializer
from rest_framework.response import Response

"""ViewSet视图集，继承于APIView,所以APIView有的功能，他也有，APIView没有的功能，她也没有"""
"""视图集"""
class StudentViewSet(ViewSet,GenericAPIView):
    serializer_class = StudentModelSerializer
    queryset = Student.objects.all()
    def get_4(self,request):

        #获取前四条数据
        student_list = self.get_queryset()[:4]

        serializer = self.get_serializer(instance=student_list,many=True)

        return Response(serializer.data)

    def get_one(self,request,pk):

        student = self.get_object()
        serializer = self.get_serializer(instance=student)

        return Response(serializer.data)

    def get_5_girl(self,request):

        #筛选表中性别为false的数据的前五条数据
        student_list = self.get_queryset().filter(sex=False)[:5]
        serializer = self.get_serializer(instance=student_list,many=True)
        return Response(serializer.data)
"""如果希望在视图集中调用GenericAPIView的功能，则需要继承GenericAPIView"""

"""上面的方式虽然实现了视图集中调用GenericAPIView,但是我们要多了一些类的继承。所以我们可以直接继承GenericViewSet"""

from rest_framework.viewsets import GenericViewSet
class Student2GenericViewSet(GenericViewSet):
    serializer_class = StudentModelSerializer
    queryset = Student.objects.all()

    def get_4(self,request):

        #获取前四条数据
        # student_list = Student.objects.all()[:4]
        student_list = self.get_queryset()[:4]

        serializer = self.get_serializer(instance=student_list,many=True)

        return Response(serializer.data)


    def get_5_girl(self,request):

        #筛选表中性别为false的数据的前五条数据
        student_list = self.get_queryset().filter(sex=False)[:5]
        serializer = self.get_serializer(instance=student_list,many=True)
        return Response(serializer.data)

"""
在使用GenericViewSet时，虽然已经提供了基本调用数据集（queryset）和序列化器属性，但是我们要编写一些基本的API时，还是要调用DRF提供的模型扩展类[Mixins]
"""

from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin,DestroyModelMixin,UpdateModelMixin,CreateModelMixin
class Students3GenericViewSet(GenericViewSet,ListModelMixin,CreateModelMixin,DestroyModelMixin,UpdateModelMixin):
   serializer_class = StudentModelSerializer
   queryset = Student.objects.all()



# ModelViewSet视图集 默认提供了5个API接口
from rest_framework.viewsets import ModelViewSet
class Student4ModelViewSet(ModelViewSet):
    serializer_class = StudentModelSerializer
    queryset = Student.objects.all()


#只读模型视图集
from rest_framework.viewsets import ReadOnlyModelViewSet
class Student5ModelViewSet(ReadOnlyModelViewSet):
    serializer_class = StudentModelSerializer
    queryset = Student.objects.all()


"""路由的使用"""
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
class Students6ModelViewSet(ModelViewSet):
    serializer_class = StudentModelSerializer
    queryset = Student.objects.all()

    #methods 指定允许哪些http请求访问当前视图方法
    #detail 指定生成的路由地址中是否要夹带pk值
    @action(methods=["GET"],detail=True)   #detail =1 包含ID detail = False 不包含ID
    def get_18(self,request):
        return Response({'age':'18'})



"""在多个视图类合并成一个视图类后，那么有时候会出现一个类中需要调用多个序列化器"""

"""在视图类中调用多个序列化器"""
"""原来的视图类中基本上一个视图类只会调用一个序列化器，当然如果要调用多个序列化器"""
from .serializers import StudentInfoModelSerializer
class Student7APIView(GenericAPIView):
    queryset = Student.objects.all()
    serializer_class = StudentInfoModelSerializer

    #GenericAPI内部调用序列化器的方法，我们可以重写这个方法来实现根据不同的需求来调用序列化器
    def get_serializer_class(self):
        print(self.request.method)
        if self.request.method == "GET":
            #两个字段
            return StudentInfoModelSerializer
        else:
            #全部字段
            return StudentModelSerializer

    #序列化
    def get(self,request):
        """获取所有数据的id和name"""
        student_list = self.get_queryset()
        serializer = self.get_serializer(instance = student_list,many=True)
        return Response(serializer.data)
    #反序列化
    def post(self,request):
        """添加数据"""
        data = request.data
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


"""在视图集中调用多个序列化器"""
class Student8ViewSet(ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentModelSerializer
    """要求：列表数据list，返回2个字段，详情数据retrieve，返回所有字段"""

    def get_serializer_class(self):
        #本次客户端请求时调用的方法名
        print(self.action)
        if self.action == "list":
            return StudentInfoModelSerializer
        else:
            return StudentModelSerializer



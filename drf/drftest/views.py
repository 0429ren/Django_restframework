from rest_framework.viewsets import ModelViewSet
from .models import Student
from .serilizers import StudentSerializer
class StudentApiView(ModelViewSet):
    queryset = Student.objects.all()   #指定结果集
    serializer_class = StudentSerializer  #指定要序列化的类


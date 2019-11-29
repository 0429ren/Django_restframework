# -*- coding: utf-8 -*-
# -*- author: 任士梅-*-

from django.urls import re_path,path
from . import views
urlpatterns = [
    re_path('students1/(?P<pk>\d)/',views.Student1View.as_view()),
    path('students2/',views.Student2View.as_view()),
    #对数据提交时进行验证
    path('students3/',views.Student3View.as_view()),
    #对数据进行增加并保存到数据库
    path('students4/',views.Student4View.as_view()),
    # 对数据进行修改并保存到数据库
    re_path('students5/(?P<pk>\d)/',views.Student5View.as_view()),
    #一个序列化器同时实现序列化和反序列化
    path('students6/',views.Student6View.as_view()),
    #使用模型类序列化器
    path('students7/',views.Student7View.as_view()),
]
# -*- coding: utf-8 -*-
# -*- author: 任士梅-*-

from django.urls import re_path,path
from . import views

urlpatterns = [

    #不要在同一个路由的as_view中书写两个同样的键的的请求方法，会产生覆盖
    #使用ViewSet
    path("students1/",views.StudentViewSet.as_view({"get":"get_4"})),
    path("students1/get_5_girl/",views.StudentViewSet.as_view({"get":"get_5_girl"})),
    re_path("students1/(?P<pk>\d+)/",views.StudentViewSet.as_view({"get":"get_one"})),
    #使用GenericViewSet
    re_path("students2/",views.Student2GenericViewSet.as_view({"get":"get_4"})),
    re_path("students2/get_5_girl/",views.Student2GenericViewSet.as_view({"get":"get_5_girl"})),
    #GenericViewSet 可以和模型扩展类进行组装快速生成基本的API
    path("students3/",views.Students3GenericViewSet.as_view({"get":"list","post":"create"})),
    #ModelViewSet 默认提供了5个API接口
    path("students4/",views.Student4ModelViewSet.as_view({"post":"create","get":"list"})),
    re_path("students4/(?P<pk>\d+)/",views.Student4ModelViewSet.as_view({"get":"retrieve","put":"update","delete":"destroy"})),

    #ReadOnlyModelViewSet
    path("students5/",views.Student5ModelViewSet.as_view({"get":"list"})),
    re_path("students5/(?P<pk>\d+)/",views.Student5ModelViewSet.as_view({"get":"retrieve"})),
    #一个视图类中调用多个序列化器
    path("students7/",views.Student7APIView.as_view()),

    #在一个视图集中调用多个序列化器
    path("students8/",views.Student8ViewSet.as_view({"get":"list"})),
    re_path("students8/(?P<pk>\d+)/",views.Student8ViewSet.as_view({"get":"retrieve"})),

]


"""
有了视图集以后，视图文件中多个视图类可以合并成一个，但是，路由的代码变得复杂了，需要我们经常在as_view方法，
编写http请求和视图方法的对应关系，事实上，在路由中,drf也提供了一个路由类给我们对路由的代码进行简写
当然这个路由仅针对于视图集才可以使用
"""

#实例化路由类
#路由类默认只会给视图集中的基本API生成地址[获取一条/获取多条/添加，删除，修改]
from django.urls import reverse
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
# router.register("访问地址前缀","视图集类","访问别名")

#注册视图集类
router.register("students6",views.Students6ModelViewSet)

# 把路由列表注册到django项目中，让
urlpatterns += router.urls

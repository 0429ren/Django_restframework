# -*- coding: utf-8 -*-
# -*- author: 任士梅-*-

from django.urls import re_path,path

from rest_framework.routers import DefaultRouter
from . import views


#
# router = DefaultRouter()
# router.register("students8", views.Student8GenericAPIView, basename="students8")
# urlpatterns = router.urls




urlpatterns = [
    path("students1/",views.Student1View.as_view()),
    path("students2/",views.Student1APIView.as_view()),
    path("students3/",views.Student2APIView.as_view()),
    path("students4/",views.Student4GenericAPIView.as_view()),
    re_path("students5/(?P<pk>\d+)",views.Student5GenericAPIView.as_view()),
    path("students6/",views.Student6GenericAPIView.as_view()),
    re_path("students7/(?P<pk>\d+)",views.Student7GenericAPIView.as_view()),
    path("students9/",views.Student9GenericAPIView.as_view()),
    re_path("students10/(?P<pk>\d+)",views.Student10RetrieveUpdateDestroyAPIView.as_view()),

    #下节课的内容，视图集
    path("students11/",views.StudentModelViewSet.as_view({"get":"list","post":"create"})),
    re_path("students11/(?P<pk>\d+)/",views.StudentModelViewSet.as_view({"get":"retrieve","put":"update","delete":"destroy"}))
]

# -*- coding: utf-8 -*-
# -*- author: 任士梅-*-

from django.urls import path
from opt import views
urlpatterns = [
    path("auth/",views.DemoAPIView.as_view()),
    path("auth2/",views.Demo2APIView.as_view()),
    path("auth3/",views.Demo3APIView.as_view()),
    path("auth4/",views.Demo4APIView.as_view()),
    path("data5/",views.Demo5APIView.as_view()),
    path("data6/",views.Demo6APIView.as_view()),
    path("data8/",views.Demo8APIview.as_view()),
]
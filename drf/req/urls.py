# -*- coding: utf-8 -*-
# -*- author: 任士梅-*-

from django.urls import re_path,path

from . import  views

urlpatterns = [
    path("students1/",views.Student1View.as_view()),
    path("students2/",views.Student1APIView.as_view()),
    path("students3/",views.Student2APIView.as_view()),
]
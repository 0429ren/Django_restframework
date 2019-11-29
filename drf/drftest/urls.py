# -*- coding: utf-8 -*-
# -*- author: 任士梅-*-
urlpatterns = []

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
from . import views
router.register('students',views.StudentApiView)

urlpatterns += router.urls

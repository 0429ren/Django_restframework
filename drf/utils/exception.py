# -*- coding: utf-8 -*-
# -*- author: 任士梅-*-
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
def custom_exception_handler(exc,context):
    """
    自定义异常函数
    :param exec: 发生异常时的异常类对象
    :param context: 发生异常时的执行上下文
    :return:
    """
    response = exception_handler(exc,context)
    if response is None:
        """response 为空！无非2种情况：
        1.没有错误发生
        2.有异常 但drf本身无法处理
        """
        if isinstance(exc,ZeroDivisionError):
            print("报错了，0不能作为除数！")
            return Response("服务器内部错误",status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return response
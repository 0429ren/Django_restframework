# -*- coding: utf-8 -*-
# -*- author: 任士梅-*-
class test():
    name = 'weisong'
    def run(self):
        return '123'
t= test()
#hasattr() 判断对象是否有该属性
print(hasattr(t,'age'))
print(hasattr(t,'name'))
print(hasattr(t,'run'))

#getattr()  #获取对象的某个属性，存在就打印出来 不存在就报错 所以一般使用时要设置默认值None 即getattr(对象名,属性名,None) 当getattr(对象名,方法名)() 可直接运行该方法
print(getattr(t,'name'))
print(getattr(t,'run'))
print(getattr(t,'run')())
print(getattr(t,'run2','属性不存在'))


#setattr()  #为对象设置属性 不提示
print(hasattr(t, 'age'))
setattr(t, 'age', '18')
print(hasattr(t, 'age'))

import datetime
print(datetime.datetime.now())
#获取当前日期中的秒
print(datetime.datetime.now().second)
#截取日期中的年月日
print(datetime.datetime.now().date())

print('测试1')
# -*- coding: utf-8 -*-
"""
Задание 12.5

Создать примесь InheritanceMixin с двумя методами:

* subclasses - отображает дочерние классы
* superclasses - отображает родительские классы

Методы должны отрабатывать и при вызове через класс и при вызове
через экземпляр:
In [2]: A.subclasses()
Out[2]: [__main__.B, __main__.D]

In [3]: A.superclasses()
Out[3]: [__main__.A, __main__.InheritanceMixin, object]

In [4]: a.subclasses()
Out[4]: [__main__.B, __main__.D]

In [5]: a.superclasses()
Out[5]: [__main__.A, __main__.InheritanceMixin, object]

В задании заготовлена иерархия классов, надо сделать так, чтобы у всех
этих классов повились методы subclasses и superclasses.
Определение классов можно менять.
"""


class InheritanceMixin:
    @classmethod
    def subclasses(cls):
        return cls.__subclasses__()

    @classmethod
    def superclasses(cls):
        return list(cls.__mro__)

class A(InheritanceMixin):
    pass


class B(A, InheritanceMixin):
    pass


class C(InheritanceMixin):
    pass


class D(A, C, InheritanceMixin):
    pass


if __name__ == "__main__":
    a1 = A()
    b1 = B()
    c1 = C()
    d1 = D()
    print("class A")
    print(A.subclasses())
    print(A.superclasses())
    print("instance a1")
    print(a1.subclasses())
    print(a1.superclasses())

    print("class B")
    print(B.subclasses())
    print(B.superclasses())
    print(b1.subclasses())
    print(b1.superclasses())

    print("class C")
    print(C.subclasses())
    print(C.superclasses())
    print("instance a1")
    print(c1.subclasses())
    print(c1.superclasses())

    print("class D")
    print(D.subclasses())
    print(D.superclasses())
    print("instance a1")
    print(d1.subclasses())
    print(d1.superclasses())

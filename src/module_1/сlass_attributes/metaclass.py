import datetime


class CreatedAtAttrMetaclass(type):
    def __new__(cls, name, bases, attrs):
        attrs["created_at"] = datetime.datetime.now()
        return super().__new__(cls, name, bases, attrs)


class MyClass(metaclass=CreatedAtAttrMetaclass):
    pass


my1 = MyClass()

print(my1.created_at)

class Singleton(object):
    _instance = None

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance


class Logger(Singleton):
    pass


logger1 = Logger()
logger2 = Logger()

print(logger1 is logger2)

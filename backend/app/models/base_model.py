
beta_data = {
    17260: {
        'title': 'Python std buffer problem.',
        'summary': 'Some log issue while using "print()"',
        'image': 'http://ac-hcebow9l.clouddn.com/a72529f44be3cdb0d620.jpeg',
        'tags': ['Python', '日志'],
        'id': 17260
    },
    17261: {
        'title': 'World of Warcraft used to be a world, now it\'s a piece of SHIT.',
        'summary': 'And it\'s even getting worse.',
        'image': 'http://ac-hcebow9l.clouddn.com/b841287d9467f01353b7.jpeg',
        'tags': ['游戏', '魔兽世界', '吐槽'],
        'id': 17261
    },
}


class_map = {}


def cache_class(**kw):

    def decorator(func):
        def wrap(*args, **kw):
            res = func(*args, **kw)
            class_map[args[1]] = res
            return res
        return wrap
    return decorator


class BaseModelMetaClass(type):

    @cache_class()
    def __new__(cls, name, base, attr):
        return super(BaseModelMetaClass, cls).__new__(cls, name, base, attr)


def with_metaclass(metaclass, *bases):

    class tmp_metaclass(type):
        def __new__(cls, name, base, attr):
            return metaclass.__new__(metaclass, name, bases, attr)
    return type.__new__(tmp_metaclass, 'tmp_metaclass', (), {})


class BaseModel(with_metaclass(BaseModelMetaClass, object)):

    def __init__(self, _id=None):
        pass

    def save(self):
        pass

    @classmethod
    def _load_model_by_id(cls, _id):
        pass


class Article(BaseModel):

    def __inie__(self):
        pass


if __name__ == "__main__":
    print(BaseModel.__class__)
    print(Article.__class__)

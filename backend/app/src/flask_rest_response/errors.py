
import functools

from .utils import formatted


_errors_by_code = {}
_errors_by_name = {}


def get_error(code_or_name, code=None, name=None):
    try:
        int(code_or_name)
        code = code_or_name
    except ValueError:
        name = code_or_name

    if code:
        return _errors_by_code[str(code)]
    return _errors_by_name[name]


def get_error_with_collection(collection, code_or_name, code=None, name=None):
    try:
        int(code_or_name)
        code = code_or_name
    except ValueError:
        name = code_or_name

    if code:
        return get_error_by_code_with_collection(collection, str(code))
    return get_error_by_name_with_collection(collection, name)


def get_error_by_code_with_collection(collection, code):
    res = _errors_by_code.get(code)
    if res:
        return res
    return _errors_by_code['{}{}'.format(collection.code, code)]


def get_error_by_name_with_collection(collection, name):
    res = _errors_by_name.get(name)
    if res:
        return res
    name = ('{}.{}'.format(collection.name, name or '')).strip()
    return _errors_by_name[name]


class Error(object):

    def __init__(self, code=None, errmsg=None, jsonify=None):
        self.code = code
        self.errmsg = errmsg
        self.jsonify = jsonify

        self._code_collection = [code]
        self._errmsg_collection = [errmsg]
        self._name_collection = []

        _errors_by_code[code] = self

    @property
    def complete_code(self):
        return ('{}' * len(self._code_collection)).format(*self._code_collection)

    @property
    def complete_errmsg(self):
        return ('{}' * len(self._errmsg_collection)).format(
            *[str(name or '') for name in self._errmsg_collection])

    @property
    def name(self):
        name = ('{}.' * len(self._name_collection)).format(
            *[name for name in self._name_collection])
        if not name:
            return None
        name = name.strip('.')
        return name

    def __call__(self, errmsg=None, data=None):
        return formatted(self.complete_code, errmsg or self.complete_errmsg, data, jsonify=self.jsonify)

    def _upper_set(self, name, code, errmsg=None, erroname=None):
        _errors_by_code.pop(self.complete_code)
        if self.name:
            _errors_by_name.pop(self.name)
        if erroname:
            self._name_collection.insert(0, erroname)

        self._code_collection.insert(0, code)
        self._errmsg_collection.insert(0, errmsg)
        self._name_collection.insert(0, name)

        _errors_by_code[self.complete_code] = self
        _errors_by_name[self.name] = self


class CollectionMetaClass(type):

    def __new__(cls, name, bases, dct):
        code = dct.get('code')
        errmsg = dct.get('errmsg')

        if code is None and name != 'Collection':
            raise AttributeError('property "code" is necessary.')

        dct['name'] = name
        dct['_code_collection'] = None
        dct['_errmsg_collection'] = None
        dct['complete_code'] = None
        dct['complete_errmsg'] = None

        for k, v in dct.items():
            if isinstance(v, (Error)):
                v._upper_set(name, code, errmsg, erroname=k)
        return super(CollectionMetaClass, cls).__new__(cls, name, bases, dct)


class Collection(object, metaclass=CollectionMetaClass):
    __abstract__ = True
    jsonify = None

    def __call__(self, target):
        target.get_error = functools.partial(get_error_with_collection, self.__class__)
        return target

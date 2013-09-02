import re


class GenericObject(object):

    """ generic object with magic functions implemented
    """

    def __init__(self, **kwargs):
        self.__dict__.update(self.__get_class_arg("_default_args", {}))
        self._pre_init(kwargs)
        self.__dict__.update(kwargs)
        self._post_init()
        self.__validate_args()

    def __repr__(self):
        regex = r"<class '.*\.(\w+)'>"
        return "{}(**{})".format(re.search(regex, repr(self.__class__)).group(1), repr(self.__dict__))

    def __str__(self):
        return repr(self)

    def __call__(self, **kwargs):
        self.__dict__.update(**kwargs)

    def _pre_init(self, kwargs):
        pass  # override me

    def _post_init(self):
        pass  # override me

    def __validate_args(self):
        for arg in self.__get_class_arg("_required_args", ()):
            assert arg in self.__dict__, arg

    def __get_class_arg(self, name, default=None):
        return self.__class__.__dict__.get(name, default)

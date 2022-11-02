""" Singleton metaclass implementation

    Found on Stackoverflow: Creating a singleton in Python - Stack Overflow
    https://stackoverflow.com/questions/6760685/creating-a-singleton-in-python

    Use:
    Use class declaration:
    class <some-class-name>(metaclass=Singleton):

    Note that subclasses of the singleton metaclass will themselves become singletons as their own object.
    x = SingletonClass()
    y = DerivedFromSingletonClass()
    x != y

"""


class Singleton(type):
    """ Singleton metaclass to provide a single place for all configuration and shared resources like DB connections """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

# EOF

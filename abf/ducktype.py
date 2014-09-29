import abc
import collections

__all__ = ['DuckType', 'DuckMeta']

def _hasattr(C, attr):
    try:
        return any(attr in B.__dict__ for B in C.__mro__)
    except AttributeError:
        # Old-style class
        return hasattr(C, attr)
def _hasall(C, attrs):
    return all(
        _hasattr(C, name) for name in attrs
    )
def _nonfunc(*args, **kwargs):
    return NotImplemented
def _abstractmethod(func=_nonfunc):
    return abc.abstractmethod(func)
def ensure_tuple(obj):
    """Ensure that object is a tuple, or is wrapped in one. 
    Also handles some special cases.
    Tuples are unchanged; NonStringSequences and Iterators are converted into
    a tuple containing the same elements; all others are wrapped by a tuple.
    """
    #Tuples - unchanged
    if isinstance(obj, tuple):
        return obj
    #Sequences - convert to tuple containing same elements.
    #elif isinstance(obj, NonStringSequence):
    elif isinstance(obj, collections.Sequence) and not isinstance(obj, basestring):
        return tuple(obj)
    #Iterators & Generators - consume into a tuple
    elif isinstance(obj, collections.Iterator):
        return tuple(obj)
    #Other Iterables, Strings, and non-Iterables - wrap in iterable first
    else:
        return tuple([obj])


class DuckMeta(type):
    """Metaclasses inherit from type.
    This version NOT descended from ABCMeta."""
    #__metaclass__ = abc.ABCMeta
    def __new__(mcls, cls_name, bases, namespace): #pylint: disable=C0202
         
         
        if not '__abstractmethods__' in namespace:
            raise TypeError("{0} missing required property: __abstractmethods__")
        # Create function stubs
        # ... is this unnecessary ???
        for name in namespace.get('__abstractmethods__', frozenset([])):
            namespace[name] = abc.abstractmethod(lambda *a,**kw: NotImplemented)
         
        cls = super(DuckMeta, mcls).__new__(mcls, cls_name, bases, namespace)
        return cls

    def __instancecheck__(self, instance):
        #classes are instances of type, instancesof classes are not
        if isinstance(instance, type):
            return False
        else:
            return all(
                _hasattr(instance, name) for name in self.__abstractmethods__
            )
    def __subclasscheck__(self, subklass):
        #print('subclasscheck', self, instance)
        #classes are instances of type, instancesof classes are not
        if isinstance(subklass, type):
            return all(
                _hasattr(instance, name) for name in self.__abstractmethods__
                )
        else:
            return False


class DuckType(object):
    """A metaclass, used for quick method based type-checking."""
    __abstractmethods__ = frozenset([])
    __metaclass__ = DuckMeta
    def __new__(cls, *abstracts, **keywords):
        
        return DuckMeta(
            keywords.get('name', 'Duckling'),
            (cls, ),
            {'__abstractmethods__': cls.__abstractmethods__.union(frozenset(abstracts))}
        ) 
    @classmethod
    def branch(cls, *abstracts, **keywords):
        return cls(*abstracts, **keywords)

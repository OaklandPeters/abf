"""
Provides a metaclass which allows creation of functional-style 'Operators' -
classes which behave as functions. These classes have initialization step 
(__init__), and hence no 'state' (in the classic OOP sense).
    When invoked, IE MyABF(*args), control proceeds from __new__ directly
to __call__. All methods defined at class creation are automatically 
converted to classmethods.

@todo: Have this check that __call__ is overridden.
@todo: Add documentation for ability to 'carry abstracts forward' by reassigning them
@todo: Consider whether to automatically cast methods to classmethods
"""
from __future__ import absolute_import
import types
import abc

from .error import ABFAbstractError
__all__ = ['ABFMeta']


class ABFMeta(abc.ABCMeta):
    """
    Inheriting from this creates a class which is callable (__call__),
    but whose __init__ or __new__ are NOT called by 'cls(arguments)' calls.
    
    It also does:
    () Checks for abstract methods during class inheritance (not instantiation).
        ... to temporarily override this behavior, simply 
            redeclare the attribute as abstract.
    () Coerces all function/lambda attributes into classmethods automatically.
    
    Future ideas for support for:
    __validate__
    __dispatch__
    __signature__
    __meets__    (compares signatures)
    """
    # Delete this assignment?
    __abstractmethods__ = frozenset(['__call__'])

    def __new__(mcls, cls_name, bases, namespace): #pylint: disable=C0202
        """This is used to check for abstract methods.
        ABFMeta.__call__ is injected as an abstractmethod.
        """
        # Construct class
        cls = super(ABFMeta, mcls).__new__(mcls, cls_name, bases, namespace)

        # Record abstract methods
        cls.__abstractmethods__ = frozenset(_all_abstracts(cls))
        
        # Check for abstract methods unassigned in current namespace
        unassigned = _unassigned_abstracts(cls)
        if unassigned:
            raise ABFAbstractError(str.format(
                ("Can't construct abstract function class {0} "
                "with abstract methods: {1}"),
                cls_name, ", ".join(unassigned)
            ))
        
        return cls

    @abc.abstractmethod
    def __call__(cls, *args, **kwargs):
        """
        This IS triggered for:      MyClass('foo')
        But NOT for:                MyClass.__call__('foo')
        """
        return cls.__call__(*args, **kwargs)




    
#==============================================================================
#    Local Utility functions
#==============================================================================
def _unroll(converter=iter):
    def outer(func):
        def inner(*args, **kwargs):
            return converter(func(*args, **kwargs))
        return inner
    return outer    

@_unroll(dict)
def _force_classmethods(namespace):
    """Does this have a problem with converting abstractmethods?"""
    for name, attr in namespace.items():
        #If function/lambda, but not if callable class
        if isinstance(attr, (types.FunctionType, types.LambdaType)):
            yield (name, classmethod(attr))
        else:
            yield (name, attr)

@_unroll(frozenset)
def _all_abstracts(cls):
    """
    Why is '__call__' added to dir(cls) explicitly?
    Because of abc.ABCMeta. It makes '__call__' not show up in the __mro__
    of a class 'cls' ABFMeta operates on. Hence, dir(cls) does not include
    __call__. But... we want __call__ to be an abstract method, so that
    the user has to override it (otherwise you get infinite recursion
    errors).
    """
    for name in dir(cls) + ['__call__']:
        if hasattr(getattr(cls, name),'__isabstractmethod__'):
            yield name
    if hasattr(cls, '__call__'):
        if hasattr(getattr(cls, name), '__isabstractmethod__'):
            yield '__call__'

@_unroll(frozenset)
def _unassigned_abstracts(cls):
    for name in _all_abstracts(cls):
        if name not in cls.__dict__:
            yield name

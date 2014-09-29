
__all__ = ['DeoptionError', 'ABFAbstractError']

class DeoptionError(TypeError):
    """Raised when deoption() called without a valid
    default or default-execute argument."""
    _defaultmsg = ("Cannot deoption: neither 'default' nor "
        "'execute' were provided.")
    def __init__(self, message=_defaultmsg):
        super(DeoptionError, self).__init__(message)


def addspace(_string):
    if isinstance(_string, basestring):
        return " " + _string
    else:
        return repr_string

def prepend(_str):
    if len(_str) > 1:
        return " "+_str
    else:
        return _str

def str_conversion(obj):
    if isinstance(obj, basestring):
        return obj
    elif isinstance(obj, type(None)):
        return ""
    elif isinstance(obj, type): # a class
        return obj.__name__
    #non-string sequence
    elif isinstance(obj, collections.Sequence):
        return ", ".join(str(elm) for elm in obj)
    else:
        return str(obj)

class ABFAbstractError(NotImplementedError):
    """Derived from NotImplementedError (and hence also RuntimeError).
    Raised when a user-defined class inherits from an 
    abstract-base-function class, without overriding an abstract method.
    """
    _defaulttemplate = (
        "Can't construct abstract-base-function class{klass}"
        " with abstract methods{methods} unless reassigned.")
    _defaultmsg = _defaulttemplate.format(klass="", methods="")
    
    def __init__(self, message=_defaultmsg):
        super(ABFAbstractError, self).__init__(message)
    
    @classmethod
    def template(cls, klass=None, methods=None):
        """Alternate constructor, for forming message via parameters.
        Example:
            ABFAbstractError.template(myclass, ['get']
        """
        return cls(
            cls._defaulttemplate.format(
                klass=cls._validate_klass(klass),
                methods=cls._validate_methods(methods)
            )
        )
    @classmethod
    def _validate_klass(cls, klass=None):
        # Should append a space unless empty
        if isinstance(klass, type(None)):
            return ""
        else:
            try:
                return klass.__name__ + " "
            except AttributeError:
                return repr(klass) + " "
    @classmethod
    def _validate_methods(cls, methods=None):
        # Should append a space unless empty
        if isinstance(methods, type(None)):
            return ""
        elif isinstance(methods, basestring):
            if not methods[-1] == " ":
                return methods + " "
            else:
                return methods
        else:
            try:
                return ", ".join(str(method) for method in methods) + " "
            except TypeError:
                return repr(methods) + " "




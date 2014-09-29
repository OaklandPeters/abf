from __future__ import absolute_import
import unittest
if __name__ == "__main__":
    import sys
    sys.path.append('..')
    from abf.ducktype import *
else:
    from .ducktype import *

class DuckTypeTests(unittest.TestCase):
    def test_basic(self):
        pop = DuckType('pop')
        popget = DuckType('pop', 'get')
        popinsert = DuckType('pop', 'insert')

        self.assert_(isinstance([], pop))
        self.assert_(not isinstance([], popget))
        self.assert_(isinstance([], popinsert))
        
        self.assert_(isinstance({}, pop))
        self.assert_(isinstance({}, popget))
        self.assert_(not isinstance({}, popinsert))

    def test_structure(self):
        attrs = ['foo', 'bar', 'baz']
        quack = DuckType(*attrs)
        for name in attrs:
            self.assert_(hasattr(quack, name))
            
    def test_blank(self):
        nullduck = DuckType()
        self.assert_(not isinstance(dict, nullduck))
        
    
    def test_type(self):
        self.assert_(not isinstance(dict, DuckType))
        self.assert_(isinstance(DuckType, DuckMeta))
        self.assert_(isinstance(DuckType, type))
        self.assert_(isinstance(DuckMeta, type))
        
        attrs = ['foo', 'bar', 'baz']
        quack = DuckType(*attrs)
        self.type_bank(quack)

    
    def type_bank(self, quack):
        # quack is not an instance (it is a class)
        self.assert_(not isinstance(quack, DuckType))
        self.assert_(issubclass(quack, DuckType)) 
        self.assert_(isinstance(quack, type))
        self.assertEqual(quack.__metaclass__, DuckMeta)
        self.assert_(DuckType in quack.__mro__)
        self.assert_(object in quack.__mro__)
        
    def test_inheritance(self):         
        class MyDuckClass(DuckType):
            __abstractmethods__ = frozenset(['get'])

        self.assert_(isinstance({}, MyDuckClass))
        self.assert_(not isinstance([], MyDuckClass))

        def erroring_class():
            class ErroringDuckClass(DuckType):
                def irrelevant_methods(self):
                    pass
            return ErroringDuckClass
        self.assertRaises(TypeError,
            lambda: erroring_class()
        )

    def test_branch(self):
        pop = DuckType('pop', '__str__')
        popget = pop('get')
        popinsert = pop('insert', 'index')
        
        self.assertEqual(
            frozenset(['pop', '__str__', 'insert', 'index']),
            popinsert.__abstractmethods__
        )
        
        # Test branching
        self.type_bank(popget)
        self.type_bank(popinsert)

        self.assert_(isinstance([], pop))
        self.assert_(not isinstance([], popget))
        self.assert_(isinstance([], popinsert))
        
        self.assert_(isinstance({}, pop))
        self.assert_(isinstance({}, popget))
        self.assert_(not isinstance({}, popinsert))

if __name__ == "__main__":
    unittest.main()
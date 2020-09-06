import collections
import unittest
from unittest.mock import MagicMock

from engine import Engine, BdfCallbacks, Registry
from object import Object

class TestBdfApi(unittest.TestCase):
    def test_bdf_called_on_tick(self):
        a_bdf = MagicMock()
        cut = Engine(a_bdf)
        cut.tick()
        a_bdf.assert_called_once()

    def test_all_api_functions_defined(self):
        def a_bdf(api: BdfCallbacks):
            self.assert_(isinstance(api.activate, collections.Callable))
            self.assert_(isinstance(api.check, collections.Callable))
            self.assert_(isinstance(api.is_prepared, collections.Callable))
            self.assert_(isinstance(api.prepare, collections.Callable))
            self.assert_(isinstance(api.register, collections.Callable))
        cut = Engine(a_bdf)
        cut.tick()

    def test_api_constructor(self):
        a_registry = MagicMock()
        api = BdfCallbacks(a_registry)
        self.assertEqual(api.registry, a_registry)

    def test_api_check__unregistered_object_raises_exception(self):
        api = BdfCallbacks(Registry())
        self.assertRaises(Exception, api.check, 'unregistered_object', '-')

    def test_api_check__non_existent_field_returns_false(self):
        api = BdfCallbacks(Registry())
        a_object = api.register('a_object', Object)
        self.assertFalse(api.check(a_object, 'non_existent_field'))

    def test_api_check__boolean_field(self):
        registry = Registry()
        api = BdfCallbacks(registry)
        a_object = api.register('a_object', Object)
        a_object_instance = registry.get_instance(a_object)
        a_object_instance.boolean_field = False
        self.assertFalse(api.check(a_object, 'boolean_field'))
        a_object_instance.boolean_field = True
        self.assertTrue(api.check(a_object, 'boolean_field'))

    def test_api_check__activates_object(self):
        aObject = Object
        aObject.on_activation = MagicMock()
        registry = Registry()
        api = BdfCallbacks(registry)
        a_object = api.register('a_object', aObject)
        a_object_instance = registry.get_instance(a_object)
        api.check(a_object, "any_field")
        a_object_instance.on_activation.assert_called_once()

    def test_api_activate__on_activate_called_once_after_multiple_activate_calls(self):
        aObject = Object
        aObject.on_activation = MagicMock()
        registry = Registry()
        api = BdfCallbacks(registry)
        a_object = api.register('a_object', aObject)
        a_object_instance = registry.get_instance(a_object)
        api.activate(a_object)
        a_object_instance.on_activation.assert_called_once()
        api.activate(a_object)
        api.activate(a_object)
        a_object_instance.on_activation.assert_called_once()

    def test_api_activate__unregistered_object_raises_exception(self):
        api = BdfCallbacks(Registry())
        self.assertRaises(Exception, api.activate, "unregistered_object")
    

class TestEngine(unittest.TestCase):

    def test_constructor(self):
        a_bdf = MagicMock()
        cut = Engine(a_bdf)
        self.assertEqual(cut.bdf, a_bdf)
import unittest
from unittest.mock import MagicMock

from conformity.engine import Engine, BdfCallbacks
from conformity.object import Object


class TestIntegration(unittest.TestCase):
    
    def test_simple_conditional_behavior(self):
        condition_value = [False]

        class ACondition(Object):
            def on_tick(self):
                self.a_condition_field = condition_value[0]

        class ABehavior(Object):
            pass
        

        def bdf(api: BdfCallbacks):
            c = api.register('a_condition', ACondition)
            b = api.register('a_behavior', ABehavior)

            if api.check(c, 'a_condition_field'):
                api.activate(b)

        def introspection(data):
            introspection.data = data 

        cut = Engine(bdf)
        cut.set_registry_introspection(introspection)

        cut.tick()
        self.assertTrue('a_condition' in introspection.data)
        self.assertTrue('a_behavior' in introspection.data)
        self.assertEqual(introspection.data['a_condition'], 'active')
        self.assertEqual(introspection.data['a_behavior'], 'deleted')

        cut.tick()
        self.assertEqual(introspection.data['a_behavior'], 'deleted')
        
        condition_value[0] = True
        cut.tick()
        self.assertEqual(introspection.data['a_behavior'], 'active')
        
        condition_value[0] = False
        cut.tick()
        self.assertEqual(introspection.data['a_behavior'], 'deleted')


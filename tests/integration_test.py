import unittest
from unittest.mock import MagicMock

from conformity.engine import Engine, BdfCallbacks
from conformity.object import Object

class TestIntegration(unittest.TestCase):
    
    def test_simple_conditional_behavior(self):
        condition_value = [False]
        behavior_active = [False]

        class ACondition(Object):
            def on_tick(self):
                self.a_condition_field = condition_value[0]

        class ABehavior(Object):
            def on_activation(self):
                behavior_active[0] = True
            def on_deactivation(self):
                behavior_active[0] = False
        

        def bdf(api: BdfCallbacks):
            c = api.register('a_condition', ACondition)
            b = api.register('a_behavior', ABehavior)

            if api.check(c, 'a_condition_field'):
                api.activate(b)

        cut = Engine(bdf)

        cut.tick()
        cut.tick()
        self.assertFalse(behavior_active[0])
        
        condition_value[0] = True
        cut.tick()
        self.assertTrue(behavior_active[0])
        
        condition_value[0] = False
        cut.tick()
        self.assertFalse(behavior_active[0])


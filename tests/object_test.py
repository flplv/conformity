import unittest
from unittest.mock import MagicMock

from conformity.object import Object, ObjectState


def make_mocked_object():
    cut = Object
    cut.on_activation = MagicMock()
    cut.on_deactivation = MagicMock()
    cut.on_preparation = MagicMock()
    cut.on_preparation_cancel = MagicMock()
    cut.on_preparation_tick = MagicMock()
    cut.on_setup = MagicMock()
    cut.on_teardown = MagicMock()
    cut.on_tick = MagicMock()
    return cut("test")


class TestObject(unittest.TestCase):

    def test_constructors(self):
        cut = Object("test")
        self.assertEqual(cut.name, "test")

    def test_normal_life_cycle(self):
        # setup
        cut = make_mocked_object()
        cut.on_setup.assert_called_once()
        self.assertEqual(cut.state, ObjectState.DEACTIVE)

        # prepare
        cut.on_preparation.assert_not_called()
        cut.prepare() 
        cut.on_preparation.assert_called_once()
        self.assertEqual(cut.state, ObjectState.PREPARING)
        
        # preparing tick and prepared
        cut.on_preparation_tick.assert_not_called()
        cut.tick()
        cut.on_preparation_tick.assert_called_with()
        self.assertEqual(cut.state, ObjectState.PREPARING)
        cut.on_preparation_tick = MagicMock(return_value = False)
        cut.tick()
        cut.on_preparation_tick.assert_called_with()
        self.assertEqual(cut.state, ObjectState.PREPARING)
        cut.on_preparation_tick = MagicMock(return_value = True)
        cut.tick()
        cut.on_preparation_tick.assert_called_with()
        self.assertEqual(cut.state, ObjectState.PREPARED)

        # active
        cut.on_activation.assert_not_called()
        cut.activate() 
        cut.on_activation.assert_called_once()
        self.assertEqual(cut.state, ObjectState.ACTIVE)

        # tick
        cut.on_tick.assert_not_called()
        cut.tick() 
        cut.on_tick.assert_called_once_with()
        self.assertEqual(cut.state, ObjectState.ACTIVE)
        
        # deactive
        cut.on_deactivation.assert_not_called()
        cut.deactivate() 
        cut.on_deactivation.assert_called_once()
        self.assertEqual(cut.state, ObjectState.DEACTIVE)

        # teardown
        cut.on_teardown.assert_not_called()
        cut.tear_down()
        cut.on_teardown.assert_called_once()

    def test_teardown_from_preparing(self):
        cut = make_mocked_object()
        cut.prepare() 
        self.assertEqual(cut.state, ObjectState.PREPARING)

        cut.on_preparation_cancel.assert_not_called()
        cut.tear_down()
        cut.on_preparation_cancel.assert_called_once()
        self.assertEqual(cut.state, ObjectState.DEACTIVE)
        
        cut.on_activation.assert_not_called()
        cut.on_deactivation.assert_not_called()
        
    def test_teardown_from_active(self):
        cut = make_mocked_object()
        cut.activate() 
        self.assertEqual(cut.state, ObjectState.ACTIVE)

        cut.tear_down()
        self.assertEqual(cut.state, ObjectState.DEACTIVE)
        
        cut.on_preparation.assert_not_called()
        cut.on_preparation_cancel.assert_not_called()
        
    def test_object_is_true(self):
        cut = make_mocked_object()
        self.assertFalse(cut.is_true("aaa"))
        cut.aaa = False
        self.assertFalse(cut.is_true("aaa"))
        cut.aaa = True
        self.assertTrue(cut.is_true("aaa"))

import collections
import unittest
from unittest.mock import MagicMock

from engine import Engine, BdfCallbacks

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

class TestEngine(unittest.TestCase):

    def test_constructor(self):
        a_bdf = MagicMock()
        cut = Engine(a_bdf)
        self.assertEqual(cut.bdf, a_bdf)
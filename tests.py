import unittest
from boolsimplifier import *


class TestBoolSimplifier(unittest.TestCase):
    def test_expr_equality(self):
        self.assertTrue(Expr.AND("B", "C", False) == Expr.AND("B", "C", False))
        self.assertTrue(Expr.AND("B", "C", False) != Expr.AND(False, "B", "C"))

if __name__ == '__main__':
    unittest.main()
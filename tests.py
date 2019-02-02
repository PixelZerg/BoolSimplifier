import unittest
from boolsimplifier import *


class TestBoolSimplifier(unittest.TestCase):
    def assertSimplified(self, e1:Expr, e2:Symbol):
        self.assertEqual(e1.simplify()[-1].sym, e2)
        # if expr equality fails or e1.simplify() returns empty list, etc,
        # errors will be raised and this test will fail

    def test_expr(self):
        # equality comparison
        self.assertEqual(Expr.AND("B", "C", False), Expr.AND("B", "C", False))
        self.assertNotEqual(Expr.AND("B", "C", False), Expr.AND(False, "B", "C"))

    def test_simp(self):
        # reorder
        self.assertSimplified(Expr.AND("D", "B", "C"), Expr.AND("B", "C", "D"))

        # null
        self.assertSimplified(Expr.AND("B", "C", False),Constant(False))

        # identity
        self.assertSimplified(Expr.AND("C", "B", True), Expr.AND("B", "C"))

if __name__ == '__main__':
    unittest.main()
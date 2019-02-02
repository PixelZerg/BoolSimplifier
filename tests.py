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

        # todo test initialisation warnings/exceptions

    def test_simp(self):
        # todo add OR variants too
        # reorder
        self.assertSimplified(Expr.AND("D", "B", "C"), Expr.AND("B", "C", "D"))

        # null
        self.assertSimplified(Expr.AND("B", "C", False),Constant(False))

        # identity
        self.assertSimplified(Expr.AND("C", "B", True), Expr.AND("B", "C"))

        # inverse
        self.assertSimplified(Expr.AND("B","C",Expr.NOT("B")), Constant(False))

        # involution
        self.assertSimplified(Expr.NOT(Expr.NOT('A')),Variable('A'))

        # idempotent
        self.assertSimplified(Expr.AND("A", "A"),Variable("A"))

if __name__ == '__main__':
    unittest.main()
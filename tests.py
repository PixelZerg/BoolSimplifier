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
        # reorder
        self.assertSimplified(Expr.AND("D", "B", "C"), Expr.AND("B", "C", "D"))
        self.assertSimplified(Expr.OR("D", "B", "C"), Expr.OR("B", "C", "D"))

        # null
        self.assertSimplified(Expr.AND("B", "C", False),Constant(False))
        self.assertSimplified(Expr.OR("B", "C", True),Constant(True))

        # identity
        self.assertSimplified(Expr.AND("C", "B", True), Expr.AND("B", "C"))
        self.assertSimplified(Expr.OR("C", "B", False), Expr.OR("B", "C"))

        # inverse
        self.assertSimplified(Expr.AND("B","C",Expr.NOT("B")), Constant(False))
        self.assertSimplified(Expr.OR("B","C",Expr.NOT("B")), Constant(True))

        # involution
        self.assertSimplified(Expr.NOT(Expr.NOT('A')),Variable('A'))

        # idempotent
        self.assertSimplified(Expr.AND("A", "A"),Variable("A"))
        self.assertSimplified(Expr.OR("A", "A"),Variable("A"))

if __name__ == '__main__':
    unittest.main()
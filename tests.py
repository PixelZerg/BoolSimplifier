import unittest
from boolsimplifier import *


class TestBoolSimplifier(unittest.TestCase):
    def test_expr_equality(self):
        self.assertEqual(
            Expr.AND("B", "C", False),
            Expr.AND("B", "C", False)
        )

if __name__ == '__main__':
    unittest.main()
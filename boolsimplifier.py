import abc
import warnings
from enum import Enum
from typing import List


class Symbol(abc.ABC):

    @abc.abstractmethod
    def render(self, **kwargs):
        """
        render into a human-readable string format.
        """
        pass

    @abc.abstractmethod
    def clone(self):
        """
        polymorphic cloning
        """
        pass

    # region string overloading
    def __str__(self):
        return self.render()

    def __repr__(self):
        return self.render()
    # endregion

class Variable(Symbol):

    def __init__(self, name:str):
        self.name = name

        # input checking
        if self.name == '1' or self.name == '0':
            warnings.warn("Variable: Using {} as variable name. "
                          "You might have meant to instantiate a Constant instead.".format(self.name), stacklevel=2)

    def render(self, **kwargs):
        return self.name

    def clone(self):
        return Variable(self.name)

    def __eq__(self, other):
        if not type(self) is type(other): return False
        return self.name == other.name

class Constant(Symbol):

    def __init__(self, value:bool):
        self.value = value

    def render(self,**kwargs):
        return "1" if self.value else "0"

    def clone(self):
        return Constant(self.value)

    def __eq__(self, other):
        if not type(self) is type(other): return False
        return self.value == other.value

class StepType(Enum):
    UNKNOWN=0
    INPUT=1
    REORDER=2
    IDENTITY_LAW=3
    NULL_LAW=4
    INVERSE_LAW=5
    INVOLUTION_LAW=6
    IDEMPOTENT_LAW=7

    @property
    def nice_name(self):
        """
        Get human-friendly description of StepType
        """
        return self.name.replace('_',' ').title()

class Step:
    def __init__(self, sym:Symbol, step_type:StepType):
        self.sym = sym
        self.step_type = step_type

    # region string overloading
    def __str__(self):
        return self.step_type.nice_name.ljust(20) + str(self.sym)
    # endregion

class ExprType(Enum):
    # order of precedence (highest last)
    NONE=0
    OR=1
    AND=2
    NOT=3

    # region comparison overloading
    def __gt__(self, other):
        return self.value > other.value

    def __lt__(self, other):
        return self.value < other.value
    # endregion

class Expr(Symbol):
    def __init__(self, typ:ExprType, *inputs):
        self.type:ExprType = typ
        self.inputs:List[Symbol] = list(inputs)

        # region input checking
        if self.type is ExprType.NOT:
            if len(inputs) != 1:
                raise ValueError("{} operator: Exactly 1 input required. {} provided."
                                 .format(self.type.name, len(inputs)))
        elif len(inputs) < 2:
            raise ValueError("{} operator: At least 2 inputs required. {} provided."
                             .format(self.type.name, len(inputs)))
        elif self.type is ExprType.NONE:
            raise ValueError("{} operator: Should not be directly instantiated"
                             .format(self.type.name))
        # endregion

    # region static initialisers
    @staticmethod
    def __inst_inputs(*inputs):
        """
        Given a list of bools/variablenames/Exprs, produce corresponding list of symbols
        """
        ret = []
        for inp in inputs:
            if isinstance(inp, str):
                ret.append(Variable(inp))
            elif isinstance(inp, bool):
                ret.append(Constant(inp))
            else:
                ret.append(inp)
        return ret

    @staticmethod
    def NOT(*inputs):
        return Expr(ExprType.NOT, *Expr.__inst_inputs(*inputs))

    @staticmethod
    def OR(*inputs):
        return Expr(ExprType.OR, *Expr.__inst_inputs(*inputs))

    @staticmethod
    def AND(*inputs):
        return Expr(ExprType.AND, *Expr.__inst_inputs(*inputs))
    # endregion

    def __eq__(self, other):
        if not type(self) is type(other): return False
        if self.type != other.type: return False
        return self.inputs == other.inputs

    def clone(self):
        cloned_inputs = []

        for inp in self.inputs:
            cloned_inputs.append(inp.clone())
        return Expr(self.type, *cloned_inputs)

    def render(self, **kwargs):
        # param work
        sym_not = kwargs.get("sym_not", "!")
        sym_or = kwargs.get("sym_or", "+")
        sym_and = kwargs.get("sym_and", "")
        sym_lbrac = kwargs.get("sym_lbrac", "(")
        sym_rbrac = kwargs.get("sym_rbrac", ")")
        parent_type = kwargs.get("parent_type", ExprType.NONE)

        rend = ""

        # NOT prefix
        if self.type is ExprType.NOT:
            rend += sym_not

        # load operator string to sym
        sym = ""
        if self.type is ExprType.AND: sym = sym_and
        elif self.type is ExprType.OR: sym = sym_or
        elif self.type is not ExprType.NOT:
            # instantiating an Expr object with type NONE should already have been prevented, but still (for future):
            raise ValueError("Unsupported operator type: {}".format(self.type.name))

        # pad sym
        if sym is not '':
            sym = ' ' + sym + ' '

        # recursive inner expr rendering
        for i, inp in enumerate(self.inputs):
            kwargs.update({"parent_type":self.type}) # update kwargs' parent_type
            rend += inp.render(**kwargs) # NB: non-expr types will ignore passed kwargs (polymorphism)

            if 0 <= i < len(self.inputs)-1:
                # add operator string
                rend += sym

        if self.type > parent_type:
            # self's precedence greater than that of parent = no need to wrap
            return rend
        else:
            # wrap in brackets to show precedence explicitly
            return sym_lbrac + rend + sym_rbrac

    def simplify(self) -> List[Step]:
        """
        simplify the expression, with steps
        :return: list of Step objects
        """
        # init steps list (including current state as first step)
        steps:List[Step] = [Step(self.clone(), StepType.INPUT)]

        # recursively simplify inputs
        for i, inp in enumerate(self.inputs):
            if isinstance(inp, Expr):
                for step in inp.simplify():
                    # get all steps in the simplification of sub-expression
                    if step.step_type != StepType.INPUT:
                        new_sym = self.clone()
                        new_sym.inputs[i] = step.sym
                        # new step: copy current expression but sub in step of sub-expression
                        steps.append(Step(new_sym,step.step_type))

        simp_methods = [
            Expr.__simp_reorder,

            Expr.__simp_null,
            Expr.__simp_inverse,

            Expr.__simp_involution,
            Expr.__simp_identity,
            Expr.__simp_idempotent
        ]

        # execute simplification methods and push steps when necessary
        while True:
            stepped = False # whether steps were pushed

            for method in simp_methods:
                last_sym = steps[-1].sym
                if not isinstance(last_sym, Expr):
                    # if last_sym not Expr, no further simplification possible
                    break
                step = method(last_sym)

                if step is not None:
                    stepped = True
                    steps.append(step)

            if not stepped:
                # no steps were made = simplification finished
                break

        return steps

    # region private helper methods
    @staticmethod
    def __order_index(sym:Symbol):
        """
        returns a string which serves as an index for the given Symbol - for use in ordering
        """
        ret = ""
        if isinstance(sym, Symbol):
            ret = "\u0000" # front alphabetically
        if isinstance(sym, Expr):
            ret = u"\uFFFF" # end alphabetically

        ret += sym.render()
        return ret
    # endregion

    # region simplification methods
    # simplification methods:
    #       input: reference to last expression pushed to steps
    #       return: Step objects or None

    @staticmethod
    def __simp_reorder(expr):
        """
        reordering of terms
        """
        expr = expr.clone() # remember: expr is reference - do not want to modify previous step
        before = expr.clone()

        expr.inputs.sort(key=lambda x: Expr.__order_index(x))

        if expr != before: # has changed
            return Step(expr, StepType.REORDER)

    @staticmethod
    def __simp_identity(expr):
        expr = expr.clone()

        search = expr.type == ExprType.AND
        found = False

        i = 0
        while i < len(expr.inputs):
            if isinstance(expr.inputs[i], Constant) and expr.inputs[i].value == search:
                del expr.inputs[i]
                found = True
                # do not increment i because just deleted
            else:
                i += 1

        if found:
            return Step(expr, StepType.IDENTITY_LAW)

    @staticmethod
    def __simp_null(expr):
        search = expr.type == ExprType.OR
        for inp in expr.inputs:
            if isinstance(inp, Constant) and inp.value == search:
                # no need to keep iterating
                return Step(Constant(search), StepType.NULL_LAW)

    @staticmethod
    def __simp_inverse(expr):
        for inp1 in expr.inputs:
            if isinstance(inp1, Expr) and inp1.type == ExprType.NOT:
                e1 = inp1.inputs[0]
                for inp2 in expr.inputs:
                    if inp2 == e1:
                        # inp1 is an inverted version of inp2
                        # because of Null law, now the entire thing can be simplified
                        # no need to keep iterating
                        return Step(Constant(expr.type == ExprType.OR), StepType.INVERSE_LAW)

    @staticmethod
    def __simp_involution(expr):
        """
        AKA: Double Negation Law
        """
        if expr.type == ExprType.NOT:
            e = expr.inputs[0]
            if isinstance(e, Expr) and e.type == ExprType.NOT:
                return Step(e.inputs[0].clone(),StepType.INVOLUTION_LAW)

    @staticmethod
    def __simp_idempotent(expr):
        # rebuild inputs, without duplicates (this law works same on OR/AND)
        new_inputs = []
        for inp in expr.inputs:
            if inp not in new_inputs:
                new_inputs.append(inp.clone())

        if new_inputs != expr.inputs:
            if len(new_inputs) > 1:
                return Step(Expr(expr.type,*new_inputs), StepType.IDEMPOTENT_LAW)
            else:
                return Step(new_inputs[0], StepType.IDEMPOTENT_LAW)

    # endregion

if __name__ == '__main__':
    e = Expr.OR(Expr.NOT("A"),Expr.AND("A","A"))

    for s in e.simplify():
        print(s)
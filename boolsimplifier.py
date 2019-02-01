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

class Constant(Symbol):

    def __init__(self, value:bool):
        self.value = value

    def render(self,**kwargs):
        return "1" if self.value else "0"

    def clone(self):
        return Constant(self.value)

class StepType(Enum):
    UNKNOWN=0
    INPUT=1
    REORDER=2
    IDENTITY=3

    @property
    def description(self):
        """
        Get human-friendly description of StepType
        """
        return [
            "",
            "Input",
            "Reorder",
            "Identity Law",
        ][self.value]

class Step:
    def __init__(self, step:Symbol, step_type:StepType):
        self.step = step
        self.step_type = step_type

    # region string overloading
    def __str__(self):
        return self.step_type.description.ljust(20) + str(self.step)
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

        # private simplification methods list
        self.__simp_methods = [
            (self.__simp_reorder, StepType.REORDER),
            (self.__simp_identity, StepType.IDENTITY),
        ]

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

        # todo recursive simp inputs here

        while True:
            stepped = False # whether any steps were pushed

            # execute simplification methods and push steps to list if necessary
            for simp_method, step_type in self.__simp_methods:
                output = simp_method()

                push_step = False
                if output is None:
                    if self.__has_changed(steps):
                        push_step = True

                if push_step or output:
                    # push step
                    stepped = True
                    steps.append(Step(self.clone(),step_type))

            if not stepped:
                # no steps made = simplification process done
                break

        return steps

    # region private helper methods
    def __has_changed(self, steps):
        """
        Whether the Expr has changed in comparison to the last step
        """
        return steps[-1].step.render() != self.render()

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
    # simplification methods will return boolean if state needs to be pushed to steps
    # or can return None if unsure (__simp_step will handle it in this case)

    def __simp_reorder(self):
        """
        reordering of terms
        """
        self.inputs.sort(key=lambda x: self.__order_index(x))
        return None

    # noinspection PyUnresolvedReferences
    def __simp_identity(self):
        search = self.type == ExprType.AND
        found = False

        i = 0
        while i < len(self.inputs):
            if isinstance(self.inputs[i], Constant) and self.inputs[i].value == search:
                del self.inputs[i]
                found = True
                # do not increment i because just deleted
            else:
                i += 1

        return found
    # endregion

# e = Expr.NOT(Expr.OR('A',Expr.AND('B','C',True)))
e = Expr.AND("B","C",False)

for step in e.simplify():
    print(step)

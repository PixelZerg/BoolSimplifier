from enum import Enum
from typing import List


class Variable:
    def __init__(self, name, is_constant=False):
        # auto constant detection
        if isinstance(name, int) and name == 0 or name == 1:
            is_constant = True

        if is_constant:
            self.value = name
            self.name = str(name)

            if self.value not in (0,1):
                raise ValueError("Invalid constant: {}".format(name))
        else:
            self.name = name

        self.is_constant = is_constant

    def __eq__(self, other):
        return self.name == other.name

    def __str__(self):
        return self.name


class Step(BaseException):
    # can be 'raised' to above scope

    def __init__(self, expr, comment):
        self.expr = expr
        self.comment = comment

    def __str__(self):
        return "{:<20}{}".format(str(self.expr),self.comment)

class NotationStyle:
    DEFAULT = ('!','+',None) # !(A + BC)
    CSTYLE = ('!','||','&&') # !(A || B && C)
    WRITTEN = ('not','or','and') # not(A or B and C)
    MATHEMATICAL = ('¬','∨','∧') # ¬(A ∨ B ∧ C)
    LATEX = ('\\overline','+',None,'(',')','{','}') # \overline{A + BC}


class ExprType(Enum):
    NONE=-1
    OR=0
    AND=1
    NOT=2

class Expr:
    def __init__(self, typ:ExprType, *inputs):
        self.type:ExprType = typ
        self.inputs:List = list(inputs)

        # input checking
        if self.type is ExprType.NOT:
            if len(inputs)!=1:
                raise ValueError('{} operator: Exactly 1 input required. {} provided.'
                                 .format(self.type.name, len(inputs)))
        elif len(inputs)<2:
            raise ValueError('{} operator: At least 2 inputs required. {} provided.'
                             .format(self.type.name, len(inputs)))

    # region static initialisers
    @staticmethod
    def __inst_inputs(*inputs):
        """
        Given a list of variablenames/Exprs, produce corresponding list of *variables*/Exprs
        """
        ret=[]
        for inp in inputs:
            if isinstance(inp,str):
                ret.append(Variable(inp))
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

    def render(self,
               formatting=NotationStyle.DEFAULT,
               indent=None):
        """
        Render into a human-readable string format.
        Usage: render(NotationStyle.CSTYLE)

        :param formatting: tuple defining the formatting. See `NotationStyle` for some templates.
        :param indent: no spaces to indent with, otherwise `None`
        :raises ValueError: if invalid formatting input
        """
        # param work
        sym_not,\
        sym_or,\
        sym_and,\
        *sym_brac_extra = formatting

        sym_lbrac, sym_rbrac = '()'
        sym_lbrac_special, sym_rbrac_special = None, None

        if len(sym_brac_extra)>0:
            sym_lbrac,\
            sym_rbrac,\
            sym_lbrac_special,\
            sym_rbrac_special = sym_brac_extra
            # raises ValueError (unpack error) if invalid input

        if sym_lbrac_special is None:
            sym_lbrac_special = sym_lbrac
        if sym_rbrac_special is None:
            sym_rbrac_special = sym_rbrac

        # rendering
        s=''
        if self.type is ExprType.NOT:
            s+=sym_not
            if isinstance(self.inputs[0],Expr):
                s += sym_lbrac_special
                s += self.inputs[0].render(formatting,indent)
                s += sym_rbrac_special
            else:
                # no brackets needed
                s += str(self.inputs[0])
        elif self.type is ExprType.OR or self.type is ExprType.AND:
            for i, inp in enumerate(self.inputs):
                if isinstance(inp, Expr):
                    if inp.type is self.type:
                        s += sym_lbrac
                        s += inp.render(formatting, indent)
                        s += sym_rbrac
                    else:
                        # operator precedence means brackets not needed
                        s += inp.render(formatting, indent)
                else:
                    # no brackets needed
                    s += str(inp)

                if 0 <= i < len(self.inputs)-1:
                    # add operator
                    sym = sym_or if self.type is ExprType.OR else sym_and
                    s += ' '+sym+' ' if sym is not None else ''

        return s

    def __str__(self):
        return self.render()

    def simplify(self,cur_level=0):
        # steptrace = traces steps taken to simplify
        steptrace= []

        # recursively simplify inputs themselves (if they are Exprs)
        for inp in self.inputs:
            if isinstance(inp,Expr):
                steptrace.append(inp.simplify(cur_level=cur_level+1)) # append sub-steptrace

        while True:
            try:
                self.step_rewrite()

                # if got to here, no additional steps were made, so break
                break
            except Step as step:
                steptrace.append(step)
                print(('\t'*cur_level)+str(step))

        return steptrace

    def step_rewrite(self):
        if len(self.inputs)>1:
            # sort terms, custom compare function
            pass

# e = Expr(ExprType.AND,Variable('A'),Variable('A'))
# x=e.simplify()
e = Expr.NOT(Expr.OR('A',Expr.AND('B','C','1')))
e.simplify()
print(e)

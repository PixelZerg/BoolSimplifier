#ifndef BOOLSIMPLIFIER_EXPR_H
#define BOOLSIMPLIFIER_EXPR_H
#include <list>
#include "Symbol.h"

enum ExprType{
    OR,
    AND,
    NOT,
};

const char* ExprTypeStrs[] = {"OR","AND","NOT"};

class Expr:public Symbol {
public:
    ExprType type;
    std::list<Symbol> inputs;

    Expr(ExprType type, std::list<Symbol> inputs);
    std::string render() override;
};


#endif //BOOLSIMPLIFIER_EXPR_H

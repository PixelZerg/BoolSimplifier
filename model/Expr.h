#ifndef BOOLSIMPLIFIER_EXPR_H
#define BOOLSIMPLIFIER_EXPR_H
#include <list>
#include <string>
#include "Symbol.h"

class Expr:public Symbol {
public:
    ExprType type;
    std::list<Symbol*> inputs;

    Expr(ExprType type, std::list<Symbol*> inputs);
    std::string render() override;
    std::string render(
            std::string sym_not,
            std::string sym_or,
            std::string sym_and,
            std::string sym_lbrac,
            std::string sym_rbrac,
            bool wrap,
            ExprType parentType
    ) override;
    std::string render(NotationStyle format);
};


#endif //BOOLSIMPLIFIER_EXPR_H

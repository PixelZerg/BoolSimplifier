#ifndef BOOLSIMPLIFIER_EXPR_H
#define BOOLSIMPLIFIER_EXPR_H
#include <list>
#include <string>
#include <array>
#include "Symbol.h"

class Step;

class Expr:public Symbol {
public:
    ExprType type;
    std::list<Symbol*> inputs;

    Expr(ExprType type, std::list<Symbol*> inputs);
    ~Expr() override;

    std::string render() override;
    std::string render(NotationStyle format);
    std::string
    render(const std::string &sym_not,
           const std::string &sym_or,
           const std::string &sym_and,
           const std::string &sym_lbrac,
           const std::string &sym_rbrac,
           const ExprType &parentType) override;

    std::list<Step*> simplify();
};


#endif //BOOLSIMPLIFIER_EXPR_H

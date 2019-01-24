#ifndef BOOLSIMPLIFIER_EXPR_H
#define BOOLSIMPLIFIER_EXPR_H
#include <list>
#include <string>
#include <array>
#include <vector>
#include "Symbol.h"

class Step;

class Expr:public Symbol {
public:
    ExprType type;
    std::vector<Symbol*> inputs;

    Expr(ExprType type, std::vector<Symbol*> inputs);
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

    Symbol* cloned() override;
    std::list<Step*>* simplify(std::list<Step*>* steps = nullptr);

private:
    void simp_null(std::list<Step *> *steps);
    void simp_inverse(std::list<Step *> *steps);
    void simp_identity(std::list<Step*> *steps);
};


#endif //BOOLSIMPLIFIER_EXPR_H

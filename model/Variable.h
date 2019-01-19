#ifndef BOOLSIMPLIFIER_VARIABLE_H
#define BOOLSIMPLIFIER_VARIABLE_H
#include "Symbol.h"

class Variable: public Symbol {
public:
    std::string name;

    explicit Variable(const char* name);
    std::string render() override;
    Symbol* cloned() override;
};


#endif //BOOLSIMPLIFIER_VARIABLE_H

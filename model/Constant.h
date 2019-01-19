#ifndef BOOLSIMPLIFIER_CONSTANT_H
#define BOOLSIMPLIFIER_CONSTANT_H
#include "Symbol.h"

class Constant: public Symbol {
public:
    bool value;

    explicit Constant(bool value);
    std::string render() override;
    Symbol* cloned() override;
};


#endif //BOOLSIMPLIFIER_CONSTANT_H

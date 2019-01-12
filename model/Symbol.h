#ifndef BOOLSIMPLIFIER_SYMBOL_H
#define BOOLSIMPLIFIER_SYMBOL_H
#include <string>

class Symbol {
public:
    virtual std::string render() = 0;
    friend std::ostream & operator<<(std::ostream &stream, Symbol &v);
};


#endif //BOOLSIMPLIFIER_SYMBOL_H

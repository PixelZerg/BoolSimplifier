#ifndef BOOLSIMPLIFIER_SYMBOL_H
#define BOOLSIMPLIFIER_SYMBOL_H
#include <string>

enum ExprType{
    NONE,
    OR,
    AND,
    NOT,
};
static const char* ExprTypeStrs[] = {"NONE","OR","AND","NOT"};

enum NotationStyle{
    DEFAULT,
    CSTYLE,
    WRITTEN,
    MATHEMATICAL,
    //maybe impl latex
};

class Symbol {
public:
    virtual ~Symbol();
    virtual std::string render();
    virtual std::string render(
            std::string sym_not,
            std::string sym_or,
            std::string sym_and,
            std::string sym_lbrac,
            std::string sym_rbrac,
            bool wrap,
            ExprType parentType
    );

    friend std::ostream & operator<<(std::ostream &stream, Symbol &v);
};


#endif //BOOLSIMPLIFIER_SYMBOL_H

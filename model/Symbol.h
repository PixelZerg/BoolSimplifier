#ifndef BOOLSIMPLIFIER_SYMBOL_H
#define BOOLSIMPLIFIER_SYMBOL_H
#include <string>

enum ExprType{
    // order of precedence (highest last)
    NONE = -1,
    OR = 0,
    AND = 2,
    NOT = 3,

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
    virtual std::string
    render(const std::string &sym_not,
           const std::string &sym_or,
           const std::string &sym_and,
           const std::string &sym_lbrac,
           const std::string &sym_rbrac,
           const ExprType &parentType);

    friend std::ostream & operator<<(std::ostream &stream, Symbol &v);
};


#endif //BOOLSIMPLIFIER_SYMBOL_H

#ifndef BOOLSIMPLIFIER_STEP_H
#define BOOLSIMPLIFIER_STEP_H
#include "Expr.h"

class Step {
public:
    Expr* expr;
    std::string message;

    Step();
    Step(Symbol* expr, const char* message);
    ~Step();

    friend std::ostream &operator<<(std::ostream &stream, Step &v);
};


#endif //BOOLSIMPLIFIER_STEP_H

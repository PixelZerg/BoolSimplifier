#include <iostream>
#include "Step.h"

Step::Step() = default;

Step::Step(Symbol* expr, const char* message){
    this->expr = (Expr*)expr;
    this->message = message;
}

Step::~Step() {
    delete this->expr;
}

std::ostream &operator<<(std::ostream &stream, Step &v) {
    return stream << v.message << ": " << *(v.expr);
}

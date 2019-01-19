#include "Step.h"

Step::Step() = default;

Step::Step(Expr* expr, const char* message){
    this->expr = expr;
    this->message = message;
}

Step::~Step() {
    delete this->expr;
}

std::ostream &operator<<(std::ostream &stream, Step &v) {
    return stream << v.expr->render() + " \t\t" + v.message;
}

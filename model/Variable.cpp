#include "Variable.h"

Variable::Variable(const char *name) {
    this->name = name;
}

std::string Variable::render() {
    return this->name;
}

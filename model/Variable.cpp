#include "Variable.h"

Variable::Variable(const char *name) {
    this->name = name;
}

std::string Variable::render() {
    return this->name;
}

Symbol *Variable::cloned() {
    return new Variable(this->name.c_str());
}

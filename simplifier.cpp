#include "simplifier.h"

std::ostream &operator<<(std::ostream &stream, Symbol &v) {
    return stream << v.render();
}

Variable::Variable(const char *name) {
    this->name = name;
}

std::string Variable::render() {
    return this->name;
}

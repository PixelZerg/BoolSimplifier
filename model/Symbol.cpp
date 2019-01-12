#include "Symbol.h"
#include <stdexcept>

Symbol::~Symbol() = default;

std::ostream &operator<<(std::ostream &stream, Symbol &v) {
    return stream << v.render();
}

std::string Symbol::render() {
    throw std::logic_error("render() not implemented");
}

std::string Symbol::render(std::string sym_not,
                           std::string sym_or,
                           std::string sym_and,
                           std::string sym_lbrac,
                           std::string sym_rbrac,
                           bool wrap,
                           ExprType parentType) {
    return render();
}

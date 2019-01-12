#include "Symbol.h"
#include <stdexcept>

Symbol::~Symbol() = default;

std::ostream &operator<<(std::ostream &stream, Symbol &v) {
    return stream << v.render();
}

std::string Symbol::render() {
    throw std::logic_error("render() not implemented");
}

std::string Symbol::render(const std::string &sym_not,
                           const std::string &sym_or,
                           const std::string &sym_and,
                           const std::string &sym_lbrac,
                           const std::string &sym_rbrac,
                           const ExprType &parentType) {
    return render();
}

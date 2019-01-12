#include "Symbol.h"
#include <stdexcept>

std::ostream &operator<<(std::ostream &stream, Symbol &v) {
    return stream << v.render();
}

std::string Symbol::render() {
    throw std::logic_error("render() not implemented");
}

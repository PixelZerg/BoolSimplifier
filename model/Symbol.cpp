#include "Symbol.h"

std::ostream &operator<<(std::ostream &stream, Symbol &v) {
    return stream << v.render();
}
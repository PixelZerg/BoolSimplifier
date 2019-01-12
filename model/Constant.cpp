#include "Constant.h"

Constant::Constant(bool value) {
    this->value = value;
}

std::string Constant::render() {
    return std::to_string(this->value);
}

#include <iostream>
#include "model/Variable.h"
#include "model/Constant.h"

int main() {
    Constant a = Constant(false);

    std::cout << a << std::endl;
}
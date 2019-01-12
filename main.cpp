#include <iostream>
#include "model/Variable.h"
#include "model/Constant.h"
#include "model/Symbol.h"
#include "model/Expr.h"

int main() {
    auto* const1 = new Constant(true);
    auto* a = new Variable("A");
    Expr e = Expr(ExprType::OR,{const1,a});

//    std::cout << ((Symbol)a).render("","","","","",false) << std::endl;
//    std::cout << ((Symbol)a).render() << std::endl;
//    a.value = false;

    std::cout << e << std::endl;
}
#include <iostream>
#include "model/Expr.h"
#include "model/Variable.h"
#include "model/Constant.h"

int main() {
//    auto* const1 = new Constant(true);
//    auto* a = new Variable("A");
//    Expr e = Expr(ExprType::OR,{const1,a});
      Expr e = Expr(ExprType::NOT,{
              new Expr(ExprType::OR,{
                  new Variable("A"),
                  new Expr(ExprType::AND,{
                          new Variable("B"),
                          new Variable("C"),
                          new Constant(true)
                  })
              })
      });

//    std::cout << ((Symbol)a).render("","","","","",false) << std::endl;
//    std::cout << ((Symbol)a).render() << std::endl;
//    a.value = false;

    std::cout << e << std::endl;
}
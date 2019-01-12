#include <iostream>
#include "model/Expr.h"
#include "model/Variable.h"
#include "model/Constant.h"

int main() {
    //fixme fix memory leaks
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
    std::cout << e.render(NotationStyle::CSTYLE) << std::endl;

    e = Expr(ExprType::OR,{
            new Variable("C"),
            new Expr(ExprType::NOT,{
                    new Expr(ExprType::AND,{
                            new Variable("B"),
                            new Variable("C")
                    })
            })
    });
    std::cout << e.render(NotationStyle::CSTYLE) << std::endl;

    e = Expr(ExprType::NOT,{
            new Constant(true),
    });
    std::cout << e.render(NotationStyle::CSTYLE) << std::endl;

    e = Expr(AND,{
            new Expr(NOT,{
                    new Expr(AND,{
                            new Variable("A"),
                            new Variable("B")
                    })
            }),
            new Expr(OR,{
                    new Expr(NOT,{
                            new Variable("A")
                    }),
                    new Variable("B")
            }),
            new Expr(OR,{
                    new Expr(NOT,{
                            new Variable("B")
                    }),
                    new Variable("B")
            })
    });
    std::cout << e.render(NotationStyle::CSTYLE) << std::endl;
}
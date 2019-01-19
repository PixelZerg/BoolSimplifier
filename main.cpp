#include <iostream>
#include "model/Expr.h"
#include "model/Variable.h"
#include "model/Constant.h"
#include "model/Step.h"

int main() {
      Expr* e = new Expr(ExprType::NOT,{
                new Expr(ExprType::OR,{
                        new Variable("A"),
                        new Expr(ExprType::AND,{
                                new Variable("B"),
                                new Variable("C"),
                                new Constant(true)
                        })
                })
      });
    std::cout << (*e) << std::endl;

    std::list<Step*>* steps = e->simplify();

    for(Step* step : *steps){
        std::cout << *step << std::endl;
    }

    while(!steps->empty()){
        delete steps->front();
        steps->pop_front();
    }

    delete steps;
    delete e;

//    e = new Expr(ExprType::OR,{
//            new Variable("C"),
//            new Expr(ExprType::NOT,{
//                    new Expr(ExprType::AND,{
//                            new Variable("B"),
//                            new Variable("C")
//                    })
//            })
//    });
//    std::cout << (*e).render(NotationStyle::CSTYLE) << std::endl;
//    delete e;

//    e = Expr(ExprType::NOT,{
//            new Constant(true),
//    });
//    std::cout << e.render(NotationStyle::CSTYLE) << std::endl;
//
//    e = Expr(AND,{
//            new Expr(NOT,{
//                    new Expr(AND,{
//                            new Variable("A"),
//                            new Variable("B")
//                    })
//            }),
//            new Expr(OR,{
//                    new Expr(NOT,{
//                            new Variable("A")
//                    }),
//                    new Variable("B")
//            }),
//            new Expr(OR,{
//                    new Expr(NOT,{
//                            new Variable("B")
//                    }),
//                    new Variable("B")
//            })
//    });
//    std::cout << e.render(NotationStyle::CSTYLE) << std::endl;
}
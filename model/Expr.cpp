#include "Expr.h"
#include <stdexcept>


Expr::Expr(ExprType type, std::list<Symbol> inputs) {
    this->type = type;
    this->inputs = inputs;

    // input checking
    if(this->type == ExprType::NOT){
        if(inputs.size() != 1){
            throw std::invalid_argument(
                    std::string(ExprTypeStrs[this->type]) +
                    " operator: Exactly 1 input required. " +
                    std::to_string(inputs.size()) + " provided."
            );
        }
    }else if (inputs.size()<2){
        throw std::invalid_argument(
                std::string(ExprTypeStrs[this->type]) +
                " operator: Exactly At least 2 inputs required. " +
                std::to_string(inputs.size()) + " provided."
        );
    }

}

std::string Expr::render() {
    return ""; //todo
}

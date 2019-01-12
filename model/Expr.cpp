#include "Expr.h"
#include "Constant.h"
#include <stdexcept>
#include <utility>


Expr::Expr(ExprType type, std::list<Symbol*> inputs) {
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
                " operator: At least 2 inputs required. " +
                std::to_string(inputs.size()) + " provided."
        );
    }
}

std::string Expr::render(
        std::string sym_not,
        std::string sym_or,
        std::string sym_and,
        std::string sym_lbrac = "(",
        std::string sym_rbrac = ")",
        bool wrap = false) {
    std::string rend;

    // NOT prefix
    if(this->type == ExprType::NOT){
        rend += sym_not;
    }

    // load operator string to sym
    std::string sym;

    switch(this->type){
        case ExprType::AND:
            sym = std::move(sym_and);
        case ExprType::OR:
            sym = std::move(sym_or);
        case NOT:break;
    }

    if(!sym.empty()){
        sym = " " + sym + " ";
    }

    // inner expr rendering
    int i = 0;
    for (auto& input : this->inputs) {
        rend += (*input).render();

        if(0 <= i && i < this->inputs.size()-1){
            // add operator
            rend += sym;
        }
        i++;
    }

    return rend; //todo

}

std::string Expr::render(NotationStyle format) {
    switch(format){
        case NotationStyle::DEFAULT:
            return render("!","+","");
        case NotationStyle::CSTYLE:
            return render("!","||","&&");
        case NotationStyle::WRITTEN:
            return render("not","or","and");
        case NotationStyle::MATHEMATICAL:
            return render("¬","∨","∧");
    }
    return render(NotationStyle::DEFAULT);
}

std::string Expr::render() {
    return render(NotationStyle::DEFAULT);
}
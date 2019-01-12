#include "Expr.h"

Expr::Expr(ExprType type, std::list<Symbol*> inputs) {
    this->type = type;
    this->inputs = inputs;

    // input checking
    if(this->type == ExprType::NONE){
        throw std::invalid_argument(
                std::string(ExprTypeStrs[this->type]) +
                " operator: Cannot be instantiated."
        );
    }
    else if(this->type == ExprType::NOT){
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

Expr::~Expr() {
    inputs.clear();
}


/*
 * Render into a human-readable string format.
 * NB: wrap and parentType are for internal use - needed for brackets optimisation
 */
std::string Expr::render( // NOLINT
        const std::string &sym_not,
        const std::string &sym_or,
        const std::string &sym_and,
        const std::string &sym_lbrac = "(",
        const std::string &sym_rbrac = ")",
        const ExprType &parentType = ExprType::NONE) {
    std::string rend;

    // NOT prefix
    if(this->type == ExprType::NOT){
        rend += sym_not;
    }

    // load operator string to sym
    std::string sym;

    switch(this->type){
        case ExprType::AND:
            sym = sym_and;
            break;
        case ExprType::OR:
            sym = sym_or;
            break;
        case NOT:break;
        case NONE: break;
    }

    if(!sym.empty()){
        sym = " " + sym + " ";
    }

    // inner expr rendering
    int i = 0;
    for (auto& input : this->inputs) {
        //NB: non-expr types will ignore the params passed
        rend += (*input).render(
                sym_not,
                sym_or,
                sym_and,
                sym_lbrac,
                sym_rbrac,
                this->type
        );

        if(0 <= i && i < this->inputs.size()-1){
            // add operator
            rend += sym;
        }
        i++;
    }

    if(this->type > parentType){
        // this' precedence greater than parent's = no need to wrap
        return rend;
    }else{
        return sym_lbrac + rend + sym_rbrac;
    }

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

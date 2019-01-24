#include <iostream>
#include "Expr.h"
#include "Step.h"
#include "Variable.h"
#include "Constant.h"

Expr::Expr(ExprType type, std::vector<Symbol*> inputs) {
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
    // NB: must free mem like this. inputs.clear() will cause leaks
    while(!inputs.empty()){
        delete inputs.back();
        inputs.pop_back();
    }
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

Symbol* Expr::cloned() {
    std::vector<Symbol*> c_inputs;

    for(Symbol* inp : this->inputs){
        c_inputs.push_back(inp->cloned());
    }
    return new Expr(this->type,c_inputs);
}

std::list<Step*>* Expr::simplify(std::list<Step*>* steps) {
    if(steps == nullptr){
        steps = new std::list<Step*>();
        steps->push_back(new Step(this->cloned(),"Input"));
    }
    simp_null(steps);
    simp_inverse(steps);
    return steps;
}

void Expr::simp_null(std::list<Step*> *steps) {
    Symbol* x = steps->back()->expr; // get last symbol in step list
    auto * cur = dynamic_cast<Expr*>(x); // cast to Expr
    if(cur == nullptr){
        return; // if not Expr, return
    }

    bool found = false;
    bool search = cur->type == ExprType::OR;

    for(auto* inp : cur->inputs){
        auto* c = dynamic_cast<Constant*>(inp);
        if(c != nullptr){
            if(c->value == search){
                found = true;
                break;
            }
        }
    }

    if(found){
        steps->push_back(new Step((Symbol*)(new Constant(search)),"Null Law"));
    }
}

void Expr::simp_inverse(std::list<Step*>* steps) {
    Symbol* x = steps->back()->expr; // get last symbol in step list
    auto * cur = dynamic_cast<Expr*>(x); // cast to Expr
    if(cur == nullptr){
        return; // if not Expr, return
    }

    bool found = false;

    for(auto* inp : cur->inputs){
        auto* v = dynamic_cast<Variable*>(inp);
        if(v != nullptr){
            // try find negated version of this
            for(auto* inp1 : cur->inputs){
                auto* n = dynamic_cast<Expr*>(inp1);
                if(n != nullptr){
                    if(n->type == ExprType::NOT){
                        auto* v2 = dynamic_cast<Variable*>(n->inputs.front());
                        if(v2 != nullptr){
                            if(v2->name == v->name){
                                // found negated match
                                found = true;
                            }
                        }
                    }
                }
            }
        }
    }

    if(found){
        steps->push_back(new Step(new Constant(cur->type == ExprType::OR),"Inverse Law"));
        // because of Null law, as long as there is one pair, the entire thing can be simplified
    }
}

void Expr::simp_identity(std::list<Step *> *steps) {
    Symbol* x = steps->back()->expr; // get last symbol in step list
    auto * cur = dynamic_cast<Expr*>(x); // cast to Expr
    if(cur == nullptr){
        return; // if not Expr, return
    }

    auto * cl = (Expr*)cur->cloned();
    bool search = cur->type == ExprType::AND;

    for(unsigned long i = cl->inputs.size()-1; i>=0; i--){
        auto* c = dynamic_cast<Constant*>(cl->inputs.at(i));
        if(c != nullptr){
            if(c->value == search){
                // todo remove this and return
            }
        }
    }
}

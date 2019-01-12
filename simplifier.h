#pragma once
#include <string>
#include <utility>

class Symbol {
public:
    virtual std::string render() = 0;
    friend std::ostream & operator<<(std::ostream &stream, Symbol &v);
};

class Variable:Symbol {
public:
    std::string name;

    explicit Variable(const char* name);
    std::string render() override;
};
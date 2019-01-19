cmake_minimum_required(VERSION 3.13)
project(BoolSimplifier)

SET(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -g -std=c++11")

set(SOURCE_FILES
        main.cpp
        model/Symbol.cpp
        model/Symbol.h
        model/Variable.cpp
        model/Variable.h
        model/Constant.cpp
        model/Constant.h
        model/Expr.cpp
        model/Expr.h model/Step.cpp model/Step.h)
add_executable(BoolSimplifier ${SOURCE_FILES})
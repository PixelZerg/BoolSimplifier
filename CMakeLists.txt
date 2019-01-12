cmake_minimum_required(VERSION 3.13)
project(BoolSimplifier)

set(CMAKE_CXX_STANDARD 11)

set(SOURCE_FILES
        main.cpp
        model/Symbol.cpp
        model/Symbol.h model/Variable.cpp model/Variable.h model/Constant.cpp model/Constant.h)
add_executable(BoolSimplifier ${SOURCE_FILES})
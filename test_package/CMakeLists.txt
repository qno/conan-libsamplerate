cmake_minimum_required(VERSION 3.5)
project(LibSampleRateTest)

set(CMAKE_CXX_STANDARD 11)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()

add_executable(libsampleratetest libsampleratetest.cpp)

conan_target_link_libraries(libsampleratetest)

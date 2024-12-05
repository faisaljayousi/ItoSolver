#ifndef BINDINGS_PY_H
#define BINDINGS_PY_H

#include <pybind11/numpy.h>
#include <pybind11/pybind11.h>
#include <string>

namespace py = pybind11;

std::string read_markdown(const std::string &file_path);

void init_bindings(){};

#endif
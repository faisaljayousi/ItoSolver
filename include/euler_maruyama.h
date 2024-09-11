#ifndef EULER_MARUYAMA_H
#define EULER_MARUYAMA_H

#include <iostream>
#include <functional>
#include <random>
#include <stdexcept>
#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <pybind11/complex.h>
#include <pybind11/functional.h>
#include <pybind11/chrono.h>

using array_t = pybind11::array_t<double>;

array_t euler_maruyama(std::function<double(double)> f,
                       std::function<double(double)> g,
                       array_t bounds,
                       int N,
                       double X0,
                       int num_sims,
                       unsigned long seed);

std::mt19937 initialise_generator(unsigned long seed = -1);

void initialise_array(array_t &arr, double val, int num_sims);

void checkBounds(const array_t &bounds);

#endif
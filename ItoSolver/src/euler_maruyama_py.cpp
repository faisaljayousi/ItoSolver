#ifndef EULER_MARUYAMA_PY
#define EULER_MARUYAMA_PY

#include "euler_maruyama.h"
#include "euler_maruyama_py.h"

void init_bindings(py::module &m)
{
    m.doc() = "SDE Solver";

    m.def("euler_maruyama", &euler_maruyama, "Euler",
          py::arg("f"),
          py::arg("g"),
          py::arg("bounds"),
          py::arg("N"),
          py::arg("X0"),
          py::arg("num_sims"),
          py::kw_only(),
          py::arg("seed") = std::time(nullptr)),
        py::call_guard<py::gil_scoped_release>();
}

PYBIND11_MODULE(itosolver, m)
{
    init_bindings(m);
}

#endif
#include "bindings.h"
#include "euler_maruyama.h"
#include "ula.h"
#include <fstream>
#include <sstream>

std::string read_markdown(const std::string &filepath)
{
    std::ifstream file(filepath);
    if (!file.is_open())
    {
        throw std::runtime_error("Could not open README.md.");
    }

    std::stringstream buffer;
    buffer << file.rdbuf();
    file.close();
    return buffer.str();
}

void init_bindings(py::module &m)
{

    std::string doc_content = read_markdown("README.md");
    m.doc() = doc_content.c_str();

    // Binding for euler_maruyama function
    m.def("euler_maruyama", &euler_maruyama, "Euler-Maruyama solver",
          py::arg("f"),                          // Function f
          py::arg("g"),                          // Function g (stochastic part)
          py::arg("bounds"),                     // Time bounds
          py::arg("N"),                          // Number of steps
          py::arg("X0"),                         // Initial condition
          py::arg("num_sims"),                   // Number of simulations
          py::kw_only(),                         // Keyword-only arguments from here
          py::arg("seed") = std::time(nullptr)); // Seed with default value (current time)

    // // Binding for ULA function
    // m.def("ula", &ula, "Unadjusted Langevin Algorithm (ULA) solver",
    //       py::arg("x"),
    //       py::arg("V") // Potential function
    // );
    // m.def("add_tensors", &add_tensors, "Add two tensors");

    py::call_guard<py::gil_scoped_release>();
}

PYBIND11_MODULE(itosolver, m)
{
    init_bindings(m);
}

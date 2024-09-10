#include "euler_maruyama.h"

void initialise_array(array_t &arr, double val, int num_sims)
{
    auto mutable_arr = arr.mutable_unchecked<2>();
    for (int i = 0; i < num_sims; ++i)
    {
        mutable_arr(i, 0) = val;
    }
}

array_t euler_maruyama(std::function<double(double)> f,
                       std::function<double(double)> g,
                       array_t bounds,
                       int N,
                       double X0,
                       int num_sims)
{
    // Logic checks
    checkBounds(bounds);

    array_t output_array({num_sims, N});
    auto output = output_array.mutable_unchecked<2>();
    initialise_array(output_array, X0, num_sims);

    // output(0, 0) = X0;

    double lb{static_cast<double>(bounds.at(0))};
    double ub{static_cast<double>(bounds.at(1))};
    double length{ub - lb};

    double dt{length / N};

    // Initialise generator
    std::random_device rd;
    std::mt19937 gen(rd());
    std::normal_distribution<double> d(0.0, std::sqrt(dt));

    for (int n = 1; n < num_sims; ++n)
    {
        for (int i = 1; i < N; ++i)
        {
            // double t = ub + (i - 1) * dt;
            auto xn = output(n, i - 1);
            output(n, i) = xn + f(xn) * dt + d(gen) * g(xn);
        }
    }

    return output_array;
}

void checkBounds(const array_t &bounds)
{
    int size = bounds.size();

    if (size != 2)
    {
        throw std::invalid_argument("Argument bounds must be 2D. Got " + std::to_string(size) + ".");
    }

    double lb = static_cast<double>(bounds.at(0));
    double ub = static_cast<double>(bounds.at(1));

    if (lb >= ub)
    {
        throw std::invalid_argument("Lower bound must be less than upper bound.");
    }
}
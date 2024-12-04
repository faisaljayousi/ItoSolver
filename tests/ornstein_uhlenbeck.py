"""
TODO
"""

import logging

import itosolver
import numpy as np

from utils import compute_error, plot_results, setup_logging, wiener_process


def main():
    """Main function to run simulation and plot results."""

    # Set up logging
    setup_logging()

    # Simulation parameters
    config = {
        "kappa": 0.4,
        "sigma": 0.2,
        "theta": 0.0,
        "X0": 1.0,  # Initial value
        "bounds": [0.0, 1.0],  # Time interval [start, end]
        "num_paths": 1000,  # Number of simulated paths
        "N": 10000,  # Number of time steps
    }

    t = np.arange(config["bounds"][0], config["bounds"][1], 1 / config["N"])

    # Run simulation
    logging.info("Running simulation...")
    solution, paths = run_simulation(
        config["kappa"],
        config["theta"],
        config["sigma"],
        config["X0"],
        config["bounds"],
        config["N"],
        config["num_paths"],
    )

    # Compute means
    logging.info("Computing means...")
    solution_mean = solution.mean(axis=0)
    paths_mean = paths.mean(axis=0)

    # Compute errors
    logging.info("Computing error metrics...")
    err = compute_error(solution_mean, paths_mean)
    logging.info(f"Errors: {err}")

    # Plot results
    logging.info("Plotting results...")
    plot_results(t, solution_mean, paths_mean, save_fig=True)


def f(x, kappa, theta):
    """Drift term function"""
    return kappa * (theta - x)


def g(x, sigma):
    """Diffusion term function"""
    return sigma


def analytic_solution(dt, kappa, theta, sigma, X0, N, num_sims):
    """
    Compute the analytical solution for the Ornstein-Uhlenbeck process.
    """
    # Time array
    t = np.linspace(0, dt * (N - 1), N)

    # Generate Wiener process
    W = wiener_process(dt, N, num_sims)

    drift = X0 * np.exp(-kappa * t) + theta * (1 - np.exp(-kappa * t))

    diffusion = (
        sigma * np.sqrt((1 - np.exp(-2 * kappa * t)) / (2 * kappa)) * W
    )

    # Combine drift and diffusion
    solution = drift + diffusion
    return solution


def run_simulation(kappa, theta, sigma, X0, bounds, N, num_paths):
    dt = (bounds[1] - bounds[0]) / N

    # Compute solution
    solution = analytic_solution(dt, kappa, theta, sigma, X0, N, num_paths)

    # Euler-Maruyama
    paths = itosolver.euler_maruyama(
        lambda x: f(x, kappa, theta),
        lambda x: g(x, sigma),
        bounds,
        N,
        X0,
        num_paths,
    )

    return solution, paths


if __name__ == "__main__":
    main()

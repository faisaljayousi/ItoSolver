"""
TODO
"""

import logging
import os

import itosolver
import matplotlib.pyplot as plt
import numpy as np

from utils import compute_error, plot_results, wiener_process


def main():
    """Main function to run simulation and plot results."""

    # Set up logging
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    # Simulation parameters
    config = {
        "mu": 2.0,  # Drift coefficient
        "sigma": 0.2,  # Volatility (diffusion) coefficient
        "X0": 1,  # Initial value
        "bounds": [0.0, 1.0],  # Time interval [start, end]
        "num_paths": 1000,  # Number of simulated paths
        "N": 10000,  # Number of time steps
    }

    t = np.arange(config["bounds"][0], config["bounds"][1], 1 / config["N"])

    try:
        # Run simulation
        logging.info("Running simulation...")
        solution, paths = run_simulation(
            config["mu"],
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

    except Exception as e:
        logging.error(f"An error occurred: {e}.")


def f(x, mu):
    """Drift term function"""
    return mu * x


def g(x, sigma):
    """Diffusion term function"""
    return sigma * x


def analytic_solution(dt, mu, sigma, X0, N, num_sims):
    W = wiener_process(dt, N, num_sims)
    t = np.linspace(0, 1, N)
    return X0 * np.exp((mu - 0.5 * sigma**2) * t + sigma * W)


def run_simulation(mu, sigma, X0, bounds, N, num_paths):
    dt = (bounds[1] - bounds[0]) / N

    # Compute solution
    solution = analytic_solution(dt, mu, sigma, X0, N, num_paths)

    # Euler-Maruyama
    paths = itosolver.euler_maruyama(
        lambda x: f(x, mu), lambda x: g(x, sigma), bounds, N, X0, num_paths
    )

    return solution, paths


if __name__ == "__main__":
    main()

"""
TODO
"""

import logging
import os

import itosolver
import matplotlib.pyplot as plt
import numpy as np


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
        logging.error(f"An error occurred: {e}")


def f(x, mu):
    """Drift term function"""
    return mu * x


def g(x, sigma):
    """Diffusion term function"""
    return sigma * x


def wiener_process(dt, N, num_sims):
    W = np.sqrt(dt) * np.random.normal(0, 1, (num_sims, N))
    return W.cumsum(axis=1)


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


def plot_results(
    t,
    analytic_solution_mean,
    euler_maruyama_mean,
    show_error=True,
    display_plots=True,
    save_fig=False,
    file_prefix="plot",
    file_format="png",
):
    """
    Plots the mean path of the analytic solution and the
    Euler-Maruyama simulation along with the absolute error.
    """

    # Plot the mean paths
    plt.figure(figsize=(10, 6))
    ax = plt.gca()
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)

    plt.plot(
        t, euler_maruyama_mean, label="Euler-Maruyama Mean Path", color="blue"
    )
    plt.plot(
        t,
        analytic_solution_mean,
        label="Analytic Solution Mean Path",
        linestyle="--",
        color="orange",
    )
    plt.xlabel("$t$")
    plt.ylabel("$X_t")
    plt.legend()
    plt.grid(True)

    if save_fig:
        file = file_prefix + "_paths_mean"
        save_figure(file, file_format)

    plt.tight_layout()

    if display_plots:
        plt.show()

    # Plot absolute error
    if show_error:
        plt.figure(figsize=(10, 6))
        ax = plt.gca()
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        plt.plot(
            t,
            np.abs(analytic_solution_mean - euler_maruyama_mean),
            label="Absolute Error",
            color="red",
        )
        plt.xlabel("$t$")
        plt.ylabel("Absolute Error (log)")
        plt.yscale("log")
        plt.grid(True)

        if save_fig:
            file = file_prefix + "_absolute_error"
            save_figure(file, file_format)

        plt.tight_layout()

        if display_plots:
            plt.show()


def compute_error(analytic_solution_mean, euler_maruyama_mean):
    """Computes the error between the analytic solution and the
    Euler-Maruyama simulation."""
    mean_error_path = np.abs(
        euler_maruyama_mean - analytic_solution_mean
    ).mean()
    final_time_error = np.abs(
        euler_maruyama_mean[-1] - analytic_solution_mean[-1]
    )

    error_estimates = {
        "path_error": mean_error_path,
        "final_time_error": final_time_error,
    }

    return error_estimates


def save_figure(file, format="png"):
    """Saves figure to file."""
    # Create directory if it does not exist
    file_dir = os.path.dirname(__file__)
    save_dir = os.path.join(file_dir, "figures")
    os.makedirs(save_dir, exist_ok=True)

    save_path = os.path.join(save_dir, f"{file}.{format}")

    try:
        plt.savefig(save_path, format=format)
        print(f"Figure saved successfully at: {save_path}")
    except Exception as e:
        print(f"Error saving figure: {e}")


if __name__ == "__main__":
    main()
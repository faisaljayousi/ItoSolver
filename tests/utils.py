import os

import matplotlib.pyplot as plt
import numpy as np


def compute_error(analytic_solution_mean, euler_maruyama_mean):
    """Computes the error between the analytic solution and the
    Euler-Maruyama simulation."""
    mean_error_path = np.abs(euler_maruyama_mean - analytic_solution_mean).mean()
    final_time_error = np.abs(euler_maruyama_mean[-1] - analytic_solution_mean[-1])

    error_estimates = {
        "path_error": mean_error_path,
        "final_time_error": final_time_error,
    }

    return error_estimates


def wiener_process(dt, N, num_sims):
    W = np.sqrt(dt) * np.random.normal(0, 1, (num_sims, N))
    return W.cumsum(axis=1)


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

    plt.plot(t, euler_maruyama_mean, label="Euler-Maruyama Mean Path", color="blue")
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

import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore

class plot:
    file_path = "results/combined_iteration_results.txt" 
    data = np.loadtxt(file_path, skiprows=1)

    # Extract data columns
    compliance = data[:, 0]  # Compliance (X-axis)
    volume_fraction = data[:, 1]  # Volume fraction (Y-axis)
    max_stress = data[:, 2]  # Max stress (Z-axis)
    stress_integral = data[:, 3]  # Stress Integral
    iterations = np.arange(1, len(compliance) + 1)  # Iteration numbers

    fig, axes = plt.subplots(1, 2, figsize=(20, 6))

    # Middle subplot: Volume Fraction, Max Stress, and Compliance vs. Iteration
    ax1 = axes[0]
    ax2 = ax1.twinx()  # Create a twin y-axis for max stress
    ax3 = ax1.twinx()  # Create a second twin y-axis for compliance
    ax3.spines['right'].set_position(('outward', 60))

    # Plot volume fraction, max stress, and compliance
    ln1 = ax1.plot(iterations, volume_fraction, 'b-', label="Volume Fraction")
    ln2 = ax2.plot(iterations, max_stress, 'r-', label="Max Stress (Pa)")
    ln3 = ax3.plot(iterations, compliance, 'g-', label="Compliance (1/Nm)")

    ax1.set_xlabel("Iteration")
    ax1.set_ylabel("Volume Fraction", color='b')
    ax2.set_ylabel("Max Stress (Pa)", color='r')
    ax3.set_ylabel("Compliance (1/Nm)", color='g')
    axes[0].set_title("Volume Fraction, Max Stress, and Compliance vs. Iteration")

    lns = ln1 + ln2 + ln3
    labels = [l.get_label() for l in lns]
    axes[0].legend(lns, labels, loc="upper left")

    ax1.grid(True, linestyle='--', linewidth=0.5)

    # Right subplot: Stress Integrals vs. Iteration
    axes[1].plot(iterations, stress_integral, 'm-', label="Stress Integral")

    axes[1].set_xlabel("Iteration")
    axes[1].set_ylabel("Stress Integrals")
    axes[1].set_title("Stress Integrals vs. Iteration")
    axes[1].legend(loc="upper left")
    axes[1].grid(True, linestyle='--', linewidth=0.5)

    # Adjust layout for clarity
    plt.tight_layout()
    plt.show()
    print(volume_fraction[-1], " ", compliance[-1], " ", max_stress[-1])


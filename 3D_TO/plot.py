import numpy as np
import matplotlib.pyplot as plt # type:ignore

class plot:
    file_path = "results/combined_iteration_results.txt"
    data = np.loadtxt(file_path, skiprows=1)        
    compliance = data[:, 0]  # Compliance (X-axis)
    volume_fraction = data[:, 1]  # Volume fraction (Y-axis)
    max_stress = data[:, 2]  # Max stress (Z-axis)
    iterations = np.arange(1, len(compliance) + 1)  # Iteration numbers

    fig, ax1 = plt.subplots(figsize=(10, 6))

    ln1 = ax1.plot(iterations, volume_fraction, 'b-', label="Volume Fraction")
    ax1.set_xlabel("Iteration")
    ax1.set_ylabel("Volume Fraction", color='b')
    ax1.tick_params(axis='y', labelcolor='b')
    ax1.grid(True, linestyle='--', linewidth=0.5)

    ax2 = ax1.twinx()
    ln2 = ax2.plot(iterations, max_stress, 'r-', label="Max Stress (Pa)")
    ax2.set_ylabel("Max Stress (Pa)", color='r')
    ax2.tick_params(axis='y', labelcolor='r')

    ax3 = ax1.twinx()
    ax3.spines['right'].set_position(('outward', 60))  # Offset third axis
    ln3 = ax3.plot(iterations, compliance, 'g-', label="Compliance (1/Nm)")
    ax3.set_ylabel("Compliance (1/Nm)", color='g')
    ax3.tick_params(axis='y', labelcolor='g')

    lns = ln1 + ln2 + ln3
    labels = [l.get_label() for l in lns]
    ax1.legend(lns, labels, loc="upper left")

    plt.title("Volume Fraction, Max Stress, and Compliance vs. Iteration")
    plt.show()

    print(volume_fraction[-1], " ", compliance[-1], " ", max_stress[-1])

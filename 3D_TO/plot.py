import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore

file_path = "combined_iteration_results.txt" 
data = np.loadtxt(file_path, skiprows=1)

max_stress = data[:, 2]  # Max stress (Z-axis)
volume_fraction = data[:, 1]  # Volume fraction (Y-axis)
compliance = data[:, 0]  # Compliance (X-axis)
iterations = np.arange(1, len(compliance) + 1)  # Iteration numbers

fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Left subplot: Compliance vs. Volume Fraction with color bar for Max Stress
sc = axes[0].scatter(compliance, volume_fraction, c=max_stress, cmap='viridis', s=50)
cbar = plt.colorbar(sc, ax=axes[0])
cbar.set_label("Max Stress (Pa)")
axes[0].set_xscale('log')  # Logarithmic scale for compliance
axes[0].set_xlabel("Compliance (1/Nm)")
axes[0].set_ylabel("Volume Fraction")
axes[0].set_title("Compliance vs. Volume Fraction with Max Stress")
axes[0].grid(True, which='both', linestyle='--', linewidth=0.5)

# Right subplot: Volume Fraction, Max Stress, and Compliance vs. Iteration
ax1 = axes[1]
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
axes[1].set_title("Volume Fraction, Max Stress, and Compliance vs. Iteration")

lns = ln1 + ln2 + ln3
labels = [l.get_label() for l in lns]
axes[1].legend(lns, labels, loc="upper left")

ax1.grid(True, linestyle='--', linewidth=0.5)
plt.tight_layout()
plt.show()

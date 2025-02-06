import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore

file_path = "results/complianceplot.txt" 
data = np.loadtxt(file_path, skiprows=1)

volume_fraction = data[:,0]
compliance = data[:,1]
stress = data[:,2]
fig, ax1 = plt.subplots(figsize=(10, 6))

sc = ax1.scatter(compliance, volume_fraction, c=stress, cmap='viridis', s=50)
cbar = plt.colorbar(sc, ax=ax1)
cbar.set_label("Max Stress (Pa)")
ax1.set_xscale('log')
ax1.set_xlabel("Compliance (1/Nm)")
ax1.set_ylabel("Volume Fraction")
ax1.set_title("Compliance vs. Volume Fraction with Max Stress")
ax1.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.show()
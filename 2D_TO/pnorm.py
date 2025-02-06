import numpy as np
import matplotlib.pyplot as plt # type: ignore

def p_norm_function(von_mises_stress, p_norm, rho_hat):
    return ((von_mises_stress ** p_norm) * rho_hat) ** (1/p_norm)

# Create sample von Mises stress values
von_mises_stress = np.linspace(0, 10, 500)

# P-norm parameter values to plot
p_norm_values = [0.5, 1, 2, 4, 8, 16, 32]

# Rho hat (density) values
rho_hat_values = 0.3

plt.figure(figsize=(10, 6))

# Plot for different p-norm and rho_hat combinations
for p_norm in p_norm_values:
    for rho_hat in rho_hat_values:
        p_norm_result = p_norm_function(von_mises_stress, p_norm, rho_hat)
        plt.plot(von_mises_stress, p_norm_result, 
                 label=f'p={p_norm}, ρ̂={rho_hat}')

plt.title("P-Norm Function Visualization", fontsize=14)
plt.xlabel("Von Mises Stress", fontsize=12)
plt.ylabel("P-Norm Value", fontsize=12)
plt.legend(title="Parameters", bbox_to_anchor=(1.05, 1), loc='upper left')
plt.grid(True, linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
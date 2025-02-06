import numpy as np
import matplotlib.pyplot as plt # type: ignore

# Heaviside projection filter equation
def heaviside_projection(rho, beta, eta0):
    numerator = np.tanh(beta * eta0) + np.tanh(beta * (rho - eta0))
    denominator = np.tanh(beta * eta0) + np.tanh(beta * (1 - eta0))
    return numerator / denominator

eta0 = 0.5  # midpoint of projection filter
rho = np.linspace(0, 1, 500)
beta_values = [0.5, 1, 2, 4, 8, 16, 32]

plt.figure(figsize=(6, 6))
for beta in beta_values:
    rho_hat = heaviside_projection(rho, beta, eta0)
    plt.plot(rho, rho_hat, label=f"$\\beta$ = {beta}")

# Customise the plot
plt.title("Heaviside Projection Filter with Varying Beta", fontsize=14)
plt.xlabel("$\\rho$ (density)", fontsize=12)
plt.ylabel("$\hat{\\rho}$ (filtered density)", fontsize=12)
plt.legend(title="$\\beta$ Values")
plt.grid(True)
plt.show()

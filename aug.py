import firedrake as fd #type: ignore
import firedrake_adjoint as fda #type: ignore
import numpy as np #type: ignore
from pyMMAopt import MMASolver #type: ignore

# Mesh and function space
mesh = fd.BoxMesh(50, 50, 10, 0.5, 0.5, 0.1, hexahedral=False, diagonal='default')
V = fd.VectorFunctionSpace(mesh, "CG", 1)

# Design variable density
z = fd.Function(V, name="density")
z.assign(0.5)  # Initial guess

# Objective function and constraint multipliers
T = fd.as_vector([0, -1])  # Load
lambda_g = fd.Function(V, name="Multiplier")  # Lagrange multipliers
gamma = fd.Constant(10.0)  # Penalty parameter

# Displacement solve
u = fd.TrialFunction(V)
v = fd.TestFunction(V)

# Linear elasticity problem
a = fd.inner(fd.stress(z, u), fd.strain(v)) * fd.dx
L = fd.dot(T, v) * fd.ds(2)
u_sol = fd.Function(V)
fd.solve(a == L, u_sol)

E1, E0 = 2.7e9, 1.0e-6
nu = 0.3
penalisationExponent = 3
E = E0 + (E1 - E0) * (z ** penalisationExponent)
lambda_ = E*nu/((1.0 + nu)*(1.0 -2.0*nu))
mu = (E) / (2 * (1 + nu))
Id = fd.Identity(mesh.geometric_dimension())
def epsilon(u): return 0.5 * (fd.grad(u) + fd.grad(u).T)
def sigma(u): return lambda_ * fd.div(u) * Id + 2 * mu * epsilon(u) 

# stress calculation
DG0 = fd.FunctionSpace(mesh, "DG", 0)

sigma_xx = fd.project(sigma(u)[0, 0], DG0)
sigma_yy = fd.project(sigma(u)[1, 1], DG0)
sigma_zz = fd.project(sigma(u)[2, 2], DG0)
sigma_xy = fd.project(sigma(u)[0, 1], DG0)
sigma_yz = fd.project(sigma(u)[1, 2], DG0)
sigma_zx = fd.project(sigma(u)[2, 0], DG0)

von_mises_stress = fd.sqrt(0.5 * ((sigma_xx - sigma_yy)**2 + (sigma_yy - sigma_zz)**2 + (sigma_zz - sigma_xx)**2 + 6 * (sigma_xy**2 + sigma_yz**2 + sigma_zx**2)))
von_mises_proj = fd.project(von_mises_stress, DG0)

# constraints
sigma_limit = 10
g = von_mises_stress - sigma_limit

# Augmented Lagrangian
objective = fd.assemble(fd.dot(T, u_sol) * fd.ds(2))  # Original objective
g_pos = fd.conditional(fd.gt(g, 0), g, 0)  # Enforce max(g, 0)
augmented_L = objective + fd.assemble(fd.dot(lambda_g, g_pos) * fd.dx + (gamma / 2) * g_pos**2 * fd.dx)

Jhat = fda.ReducedFunctional(augmented_L, fda.Control(z))
gradient = Jhat.derivative()

# Optimization parameters
tol = 1e-6
max_iters = 50
iteration = 0

while iteration < max_iters:
    iteration += 1

    # Solve optimization problem
    problem = fda.MinimizationProblem(Jhat)
    solver = MMASolver(problem, parameters={"acceptable_tol": tol})
    solver.solve()

    # Update Lagrange multipliers
    g_values = g.dat.data[:]  # Extract current constraint values
    lambda_g.dat.data[:] = np.maximum(lambda_g.dat.data[:] + gamma.dat.data * g_values, 0)

    # Optional: Increase penalty parameter (continuation)
    gamma.assign(gamma * 1.5)

    # Check convergence
    max_violation = max(g_values)
    if max_violation < tol:
        print("Convergence reached!")
        break

print("Optimization completed.")

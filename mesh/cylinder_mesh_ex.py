import firedrake as fd  # type: ignore
from firedrake.output import VTKFile # type: ignore
'''
m = fd.CircleManifoldMesh(20, radius=2)
m1 = fd.ExtrudedMesh(m, 5, extrusion_type='radial')
mesh = fd.ExtrudedMesh(m1, 5, extrusion_type='uniform')


nx, ny = 20, 5 
radius = 2
height = 5

base_mesh = fd.PeriodicRectangleMesh(nx, ny, 2 * fd.pi * radius, radius, direction="x")
mesh = fd.ExtrudedMesh(base_mesh, layers=height, extrusion_type="uniform")
vtkfile = VTKFile("cylinder_mesh_ex.pvd")
vtkfile.write(mesh)

import numpy as np
nx, ny, nz = 40, 10, 10
radius = 2
height = 5

base_mesh = fd.PeriodicRectangleMesh(nx, ny, 2 * np.pi * radius, radius, direction="x", quadrilateral=True)
mesh = fd.ExtrudedMesh(base_mesh, layers=nz, extrusion_type="uniform")

V = mesh.coordinates.function_space()

X = fd.Function(V).interpolate(mesh.coordinates)
x, y, z = fd.split(X)  

theta = (x / (2 * np.pi * radius)) * 2 * np.pi
x_new = radius * fd.cos(theta)
y_new = radius * fd.sin(theta)

mesh.coordinates.interpolate(fd.as_vector([x_new, y_new, z]))
mesh = fd.ExtrudedMesh(mesh, 5, extrusion_type='radial')'''

import numpy as np
nr, ntheta, nz = 10, 40, 10  # Radial, angular, and height divisions
r_inner, r_outer = 0.1, 0.2  # Inner and outer radius
height = 0.1  # Cylinder height

# Create a structured 2D (r, θ) mesh using a rectangle
base_mesh = fd.RectangleMesh(nr, ntheta, r_outer - r_inner, 2 * np.pi, quadrilateral=True)

# Extrude in the z-direction to make it 3D
mesh = fd.ExtrudedMesh(base_mesh, layers=nz, extrusion_type="uniform", layer_height=height / nz)

# Convert coordinates to cylindrical form
X = fd.Function(mesh.coordinates.function_space()).interpolate(mesh.coordinates)
r, theta, z = fd.split(X)  # Extract components

# Map from (r, θ, z) to Cartesian (x, y, z)
r_new = r + r_inner  # Shift radial coordinate to start at r_inner
x_new = r_new * fd.cos(theta)
y_new = r_new * fd.sin(theta)

# Assign transformed coordinates
mesh.coordinates.interpolate(fd.as_vector([x_new, y_new, z]))

vtkfile = VTKFile("cylinder_mesh_ex.pvd")
vtkfile.write(mesh)

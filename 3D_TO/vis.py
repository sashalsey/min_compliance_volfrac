import firedrake as fd #type: ignore
from firedrake.output import VTKFile #type: ignore
mesh = fd.Mesh('cylinder_works.msh')
vtkfile = VTKFile("cylinder_works.pvd")
vtkfile.write(mesh)
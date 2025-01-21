import firedrake as fd # type: ignore
from firedrake.output import VTKFile # type: ignore
mesh = fd.Mesh('cylinder.msh')
vtkfile = VTKFile("mesh.pvd")
vtkfile.write(mesh)
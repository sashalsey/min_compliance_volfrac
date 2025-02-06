import firedrake as fd # type: ignore
from firedrake.output import VTKFile # type: ignore

m = fd.Mesh('corner3.msh')
mesh = fd.ExtrudedMesh(m, 5, layer_height = 0.1)
vtkfile = VTKFile("cornerextruded.pvd")
vtkfile.write(mesh)
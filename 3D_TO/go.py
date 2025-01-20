import firedrake as fd # type: ignore
from firedrake.output import VTKFile # type: ignore

nx, ny, nz = 20, 10, 5
lx, ly, lz = 0.2, 0.1, 0.05


m = fd.CircleManifoldMesh(20, radius=2)
mesh = fd.ExtrudedMesh(m, 5, extrusion_type='radial')
mesh = fd.ExtrudedMesh(mesh, 5, layer_height=0.2, extrusion_type='uniform')

vtkfile = VTKFile("3dmesh.pvd")
vtkfile.write(mesh)
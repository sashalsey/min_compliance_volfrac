import numpy as np  # type: ignore
import firedrake as fd  # type: ignore
import firedrake.adjoint as fda  # type: ignore
from firedrake.output import VTKFile # type: ignore
fda.continue_annotation()

class ForwardSolve_p:
    def __init__(self, outputFolder, outputFolder2, beta, penalisationExponent, variableInitialisation, rho0, pnorm):
        # append inputs to class
        self.outputFolder = outputFolder
        self.outputFolder2 = outputFolder2

        # rho initialisation
        self.variableInitialisation = variableInitialisation
        self.penalisationExponent = penalisationExponent
        self.rho0 = rho0

        # material properties
        self.E0 = 1e-6  # [Pa] # void
        self.E1 = 2.7e9  # [Pa] # dense
        self.nu = 0.3  # []

        # pseudo-density functional
        self.beta = beta  # heaviside projection parameter
        self.eta0 = 0.5  # midpoint of projection filter

        self.Vlimit = 0.3
        self.Slimit = 0.3
        self.pnorm = pnorm

    def GenerateMesh(self,):
        self.mesh = fd.BoxMesh(self.nx, self.ny, self.nz, self.lx, self.ly, self.lz, hexahedral=False, diagonal='default')
        self.gradientScale = (self.nx * self.ny * self.nz) / (self.lx * self.ly * self.lz)  # firedrake bug?

    def Setup(self):
        self.nx, self.ny, self.nz = 25, 6, 6
        self.lx, self.ly, self.lz = 0.5, 0.12, 0.12
        self.cellsize = self.lx / self.nx
        self.GenerateMesh()

        # compute mesh volume
        self.meshVolume = fd.assemble(1 * fd.dx(domain=self.mesh))

        # define function spaces
        self.functionSpace = fd.FunctionSpace(self.mesh, "CG", 1)
        self.vectorFunctionSpace = fd.VectorFunctionSpace(self.mesh, "CG", 1)

        # define psuedo-density function
        self.rho = fd.Function(self.functionSpace)

        # number of nodes in mesh
        self.numberOfNodes = len(self.rho.vector().get_local())

        # compute helmholtz filter radius
        self.helmholtzFilterRadius = 1 * (self.meshVolume / self.mesh.num_cells()) ** (1 / self.mesh.cell_dimension())

        # boundary conditions, add ne  by adding new key to dict
        bcDict = {}
        bcDict[0] = fd.DirichletBC(self.vectorFunctionSpace,fd.Constant((0, 0, 0)), 1)
        self.bcs = [bcDict[i] for i in range(len(bcDict.keys()))]

        # define output files
        self.rho_hatFile = VTKFile(self.outputFolder + "rho_hat.pvd")
        self.rho_hatFunction =fd.Function(self.functionSpace, name="rho_hat")

        self.uFile = VTKFile(self.outputFolder + "u.pvd")
        self.uFunction =fd.Function(self.vectorFunctionSpace, name="u")

        self.stressFile = VTKFile(self.outputFolder + "stress.pvd")
        self.stressFunction = fd.Function(self.functionSpace, name="stress")

    def ComputeInitialSolution(self):

        if self.variableInitialisation is True:
            initialisationFunction =fd.Function(self.functionSpace)
            initialisationFunction.vector().set_local(self.rho0)
        else:

            # initialise function for initial solution
            initialisationFunction =fd.Function(self.functionSpace)

            # generate uniform initialisation
            initialisationFunction.assign(self.Vlimit)

        return initialisationFunction.vector().get_local()

    def CacheDesignVariables(self, designVariables, initialise=False):
        if initialise is True:
            # initialise with zero length array
            self.rho_np_previous = np.zeros(0)
            cache = False
        else:
            # determine whether the current design variables were simulated at previous iteration
            if np.array_equal(designVariables, self.rho_np_previous):

                # update cache boolean
                cache = True

            else:
                # new array is unique
                # assign current array to cache
                self.rho_np_previous = designVariables

                # update self.rho
                self.rho.vector().set_local(designVariables)

                # update cache boolean
                cache = False

        return cache

    def Solve(self, designVariables):
        # insert and cache design variables
        # automatically updates self.rho
        identicalVariables = self.CacheDesignVariables(designVariables)

        if identicalVariables is False:
            # Helmholtz Filter
            u = fd.TrialFunction(self.functionSpace)
            v = fd.TestFunction(self.functionSpace)

            # weak variational form
            a = (fd.Constant(self.helmholtzFilterRadius) ** 2) * fd.inner(fd.grad(u), fd.grad(v)) * fd.dx + fd.inner(u, v) * fd.dx
            L = fd.inner(self.rho, v) * fd.dx

            # solve helmholtz equation
            self.rho_ =fd.Function(self.functionSpace, name="rho_")
            fd.solve(a == L, self.rho_)

            # projection filter
            self.rho_hat = (fd.tanh(self.beta * self.eta0) + fd.tanh(self.beta * (self.rho_ - self.eta0))
            ) / (fd.tanh(self.beta * self.eta0) + fd.tanh(self.beta * (1 - self.eta0)))

            # output rho_hat visualisation
            self.rho_hatFunction.assign(fd.project(self.rho_hat, self.functionSpace))
            self.rho_hatFile.write(self.rho_hatFunction)

            # linear elasticity load case
            u = fd.TrialFunction(self.vectorFunctionSpace)
            v = fd.TestFunction(self.vectorFunctionSpace)

            # define surface traction
            x, y, z = fd.SpatialCoordinate(self.mesh)
            T = fd.conditional(fd.gt(x, self.lx - self.cellsize),
                    fd.conditional(fd.gt(y, self.ly / 2 - self.cellsize),
                    fd.conditional(fd.lt(y, self.ly / 2 + self.cellsize),
                                   fd.conditional(fd.gt(z, self.lz / 2 - self.cellsize),
                                    fd.conditional(fd.lt(z, self.lz / 2 + self.cellsize),
                        fd.as_vector([0, -1, 0]),
                        fd.as_vector([0, 0, 0]),),
                    fd.as_vector([0, 0, 0]),),
                fd.as_vector([0, 0, 0]),),
                fd.as_vector([0, 0, 0]),),
                fd.as_vector([0, 0, 0]),)
            
            # elasticity parameters
            self.E = self.E0 + (self.E1 - self.E0) * (self.rho_hat**self.penalisationExponent)
            lambda_ = (self.E * self.nu) / ((1 + self.nu) * (1 - 2 * self.nu))
            mu = (self.E) / (2 * (1 + self.nu))

            # linear elastic weak variational form
            Id = fd.Identity(self.mesh.geometric_dimension())
            def epsilon(u): return 0.5 * (fd.grad(u) + fd.grad(u).T)
            def sigma(u): return lambda_ * fd.div(u) * Id + 2 * mu * epsilon(u)

            a = fd.inner(sigma(u), epsilon(v)) * fd.dx
            L = fd.dot(T, v) * fd.ds(2)

            # solve
            u =fd.Function(self.vectorFunctionSpace)
            fd.solve(a == L, u, bcs=self.bcs)

            # output displacement visualisation
            self.uFunction.assign(u)
            self.uFile.write(self.uFunction)

            # stress calculation
            DG0 = fd.FunctionSpace(self.mesh, "CG", 1)

            sigma_xx = fd.project(sigma(u)[0, 0], DG0)
            sigma_yy = fd.project(sigma(u)[1, 1], DG0)
            sigma_zz = fd.project(sigma(u)[2, 2], DG0)
            sigma_xy = fd.project(sigma(u)[0, 1], DG0)
            sigma_yz = fd.project(sigma(u)[1, 2], DG0)
            sigma_zx = fd.project(sigma(u)[2, 0], DG0)

            von_mises_stress = fd.sqrt(0.5 * ((sigma_xx - sigma_yy)**2 + (sigma_yy - sigma_zz)**2 + (sigma_zz - sigma_xx)**2 + 6 * (sigma_xy**2 + sigma_yz**2 + sigma_zx**2)))
            von_mises_proj = fd.project(von_mises_stress, DG0)
            self.stressFunction.assign(von_mises_proj)
            self.stressFile.write(self.stressFunction)
            max_stress = np.max(von_mises_proj.vector().get_local())

            # assemble objective function
            self.j = fd.assemble(fd.inner(T, u) * fd.ds(2))

            # volume fraction constraint
            volume_fraction = (1 / self.meshVolume) * fd.assemble(self.rho_hat * fd.dx)
            self.c1 = self.Vlimit - volume_fraction

            stressintegral = fd.assemble( ((von_mises_stress ** self.pnorm) * self.rho_hat * fd.dx) ) ** (1/self.pnorm)
            self.c2 = self.Slimit - stressintegral

            # compute objective function sensitivities
            self.djdrho = (fda.compute_gradient(self.j, fda.Control(self.rho)).vector().get_local()) / self.gradientScale

            # compute constraint sensitivities
            self.dc1drho = (fda.compute_gradient(self.c1, fda.Control(self.rho)).vector().get_local()) / self.gradientScale
            self.dc2drho = (fda.compute_gradient(self.c2, fda.Control(self.rho)).vector().get_local()) / self.gradientScale

            # assemble constraint vector
            self.c = np.array([self.c1, self.c2])

            # assemble jacobian vector, np.concatenate((self.dc1drho, self.dc2drho))
            self.dcdrho = np.concatenate((self.dc1drho, self.dc2drho))

            with open(self.outputFolder2 + "combined_iteration_results.txt", "a") as log_file:
                log_file.write(f"{self.j:.3e}\t{volume_fraction:.4f}\t{max_stress:.3e}\t{stressintegral:.3e}\n")

        else:
            pass

        return self.j, self.djdrho, self.c, self.dcdrho

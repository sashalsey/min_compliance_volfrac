#!/usr/bin/env python3
"""
Created on Fri Dec 15 12:07:58 2023

@author: rdm4317
"""

# open-source libraries
import numpy as np
from firedrake import *
from firedrake.adjoint import *
from firedrake.output import VTKFile

continue_annotation()


###############################################################################
class ForwardSolve:

    ###############################################################################
    def __init__(
        self, outputFolder, beta, penalisationExponent, variableInitialisation, rho0
    ):

        # append inputs to class
        self.outputFolder = outputFolder

        # rho initialisation
        self.variableInitialisation = variableInitialisation
        self.penalisationExponent = penalisationExponent
        self.rho0 = rho0

        # material properties
        self.E0 = 1e-6  # [Pa] # void
        self.E1 = 1e0  # [Pa] # dense
        self.nu = 0.3  # []

        # pseudo-density functional
        self.beta = beta  # heaviside projection parameter
        self.eta0 = 0.5  # midpoint of projection filter

    ###############################################################################
    def GenerateMesh(
        self,
    ):
        self.mesh = RectangleMesh(
            self.nx, self.ny, self.lx, self.ly, quadrilateral=True
        )
        self.gradientScale = (self.nx * self.ny) / (self.lx * self.ly)  # firedrake bug?

    ###############################################################################
    def Setup(self):

        # mesh, functionals and associated static parameters
        ###############################################################################
        # generate mesh
        self.nx = 120
        self.ny = 40
        self.lx = 0.3
        self.ly = 0.1
        self.GenerateMesh()

        # compute mesh volume
        self.meshVolume = assemble(1 * dx(domain=self.mesh))

        # define function spaces
        self.functionSpace = FunctionSpace(self.mesh, "DG", 0)
        self.vectorFunctionSpace = VectorFunctionSpace(self.mesh, "CG", 2)

        # define psuedo-density function
        self.rho = Function(self.functionSpace)

        # number of nodes in mesh
        self.numberOfNodes = len(self.rho.vector().get_local())

        # compute helmholtz filter radius
        self.helmholtzFilterRadius = 1 * (self.meshVolume / self.mesh.num_cells()) ** (
            1 / self.mesh.cell_dimension()
        )

        # boundary conditions
        ###############################################################################
        # add new boundary conditions by adding new key to dict
        bcDict = {}
        bcDict[0] = DirichletBC(self.vectorFunctionSpace, Constant((0, 0)), 1)
        self.bcs = [bcDict[i] for i in range(len(bcDict.keys()))]

        # define output files
        ###############################################################################
        # projected psuedo-density output file
        self.rho_hatFile = VTKFile(self.outputFolder + "rho_hat.pvd")
        self.rho_hatFunction = Function(self.functionSpace, name="rho_hat")

        # displacement output file
        self.uFile = VTKFile(self.outputFolder + "u.pvd")
        self.uFunction = Function(self.vectorFunctionSpace, name="u")

    ###############################################################################
    def ComputeInitialSolution(self):

        if self.variableInitialisation is True:
            initialisationFunction = Function(self.functionSpace)
            initialisationFunction.vector().set_local(self.rho0)
        else:

            # initialise function for initial solution
            initialisationFunction = Function(self.functionSpace)

            # generate uniform initialisation
            initialisationFunction.assign(0.3)

        return initialisationFunction.vector().get_local()

    ###############################################################################
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

    ###############################################################################
    def Solve(self, designVariables):

        # insert and cache design variables
        # automatically updates self.rho
        identicalVariables = self.CacheDesignVariables(designVariables)

        if identicalVariables is False:

            # Helmholtz Filter
            ###############################################################################
            # trial and test functions
            u = TrialFunction(self.functionSpace)
            v = TestFunction(self.functionSpace)

            # DG specific relations
            n = FacetNormal(self.mesh)
            h = 2 * CellDiameter(self.mesh)
            h_avg = (h("+") + h("-")) / 2
            alpha = 1

            # weak variational form
            a = (Constant(self.helmholtzFilterRadius) ** 2) * (
                dot(grad(v), grad(u)) * dx
                - dot(avg(grad(v)), jump(u, n)) * dS
                - dot(jump(v, n), avg(grad(u))) * dS
                + alpha / h_avg * dot(jump(v, n), jump(u, n)) * dS
            ) + inner(u, v) * dx
            L = inner(self.rho, v) * dx

            # solve helmholtz equation
            self.rho_ = Function(self.functionSpace, name="rho_")
            solve(a == L, self.rho_)

            # projection filter
            ###############################################################################
            self.rho_hat = (
                tanh(self.beta * self.eta0) + tanh(self.beta * (self.rho_ - self.eta0))
            ) / (tanh(self.beta * self.eta0) + tanh(self.beta * (1 - self.eta0)))

            # output rho_hat visualisation
            self.rho_hatFunction.assign(project(self.rho_hat, self.functionSpace))
            self.rho_hatFile.write(self.rho_hatFunction)

            # linear elasticity load case
            ###############################################################################

            # define trial and test functions
            u = TrialFunction(self.vectorFunctionSpace)
            v = TestFunction(self.vectorFunctionSpace)

            # define surface traction
            # T = Constant((0,-1))
            x, y = SpatialCoordinate(self.mesh)
            T = conditional(
                gt(x, 0.3 - (0.3 / 360) - 1e-8),
                conditional(
                    gt(y, 0.05 - 3 * (0.1 / 120) - 1e-8),
                    conditional(
                        lt(y, 0.05 + 3 * (0.1 / 120) + 1e-8),
                        as_vector([0, -1]),
                        as_vector([0, 0]),
                    ),
                    as_vector([0, 0]),
                ),
                as_vector([0, 0]),
            )

            # elasticity parameters
            self.E = self.E0 + (self.E1 - self.E0) * (
                self.rho_hat**self.penalisationExponent
            )
            lambda_ = (self.E * self.nu) / ((1 + self.nu) * (1 - 2 * self.nu))
            mu = (self.E) / (2 * (1 + self.nu))

            # linear elastic weak variational form
            epsilon = 0.5 * (grad(v) + grad(v).T)
            sigma = (lambda_ * div(u) * Identity(self.mesh.cell_dimension())) + (
                2 * mu * 0.5 * (grad(u) + grad(u).T)
            )
            a = inner(sigma, epsilon) * dx
            L = dot(T, v) * ds(2)

            # solve
            u = Function(self.vectorFunctionSpace)
            solve(a == L, u, bcs=self.bcs)

            # output displacement visualisation
            self.uFunction.assign(u)
            self.uFile.write(self.uFunction)

            # assemble objective function
            self.j = assemble(inner(T, u) * ds(2))

            # volume fraction constraint
            self.c1 = 0.3 - ((1 / self.meshVolume) * assemble(self.rho_hat * dx))

            # compute objective function sensitivities
            self.djdrho = (
                compute_gradient(self.j, Control(self.rho)).vector().get_local()
            ) / self.gradientScale

            # compute constraint sensitivities
            self.dc1drho = (
                compute_gradient(self.c1, Control(self.rho)).vector().get_local()
            ) / self.gradientScale

            # assemble constraint vector
            self.c = np.array([self.c1])

            # assemble jacobian vector
            # self.dcdrho = np.concatenate((self.dc1drho, self.dc2drho))
            self.dcdrho = self.dc1drho

        else:
            pass

        return self.j, self.djdrho, self.c, self.dcdrho

import datetime 
import numpy as np # type: ignore
import sys
from finiteDifferenceValidation import FiniteDifferenceValidation
from forwardSolve import ForwardSolve

class OptimisationLoop:
    def __init__(self):
        # density field bounds
        self.lowerBound = 0
        self.upperBound = 1

        # continuation parameters
        self.beta = None
        self.penalisationExponent = 3  # fixed at present

        # output folder
        self.outputFolder = ("results/TO" + datetime.datetime.now().strftime("%y_%m-%d-%H-%M-%S") + "/")
        self.outputFolder2 = ("results/")
        # finite-difference test flag
        self.finiteDifferenceValidation = False

        # variable initialisation
        self.variableInitialisation = False
        self.rho0 = None

        # scaling parameters
        self.scalingInitialisation = False
        self.gradientScaling = 1
        self.constraintScaling = 1
        self.jacobianScaling = 1

    def OptimisationSetup(self):

        # initialise forward solve class
        self.ForwardSolve = ForwardSolve(
            self.outputFolder,
            self.outputFolder2,
            self.beta,
            self.penalisationExponent,
            self.variableInitialisation,
            self.rho0,)

        # setup forward solve (mesh, function spaces, boundary conditions etc)
        # mesh: needs changing
        self.ForwardSolve.Setup()

        # compute initial solution as a function of spatial coordinates
        self.designVariables0 = self.ForwardSolve.ComputeInitialSolution()

        # perform initial cache of design variables
        self.ForwardSolve.CacheDesignVariables(None, initialise=True)

        if self.finiteDifferenceValidation is True:
            FiniteDifferenceValidation(self)
            sys.exit()
        else:
            pass

        # execute initial forward solve (various parameters derived)
        self.j, self.djdrho, self.c, self.dcdrho = self.ForwardSolve.Solve(self.designVariables0)

        # use user supplied scaling derived from previous continuation iteration
        if self.scalingInitialisation is True:
            pass
        else:

            # gradient scaling (parsed directly to ipopt)
            self.gradientScaling = 1 / np.average(np.abs(self.djdrho))

            # constraint and jacobian scaling
            self.constraintScaling = np.zeros(len(self.c))
            self.jacobianScaling = np.zeros(len(self.c) * self.ForwardSolve.numberOfNodes)
            for i in range(len(self.c)):

                # constraint scaling
                self.constraintScaling[i] = 1 / np.average(
                    np.abs(
                        self.dcdrho[
                            i
                            * self.ForwardSolve.numberOfNodes : (i + 1)
                            * self.ForwardSolve.numberOfNodes]))

                # jacobian scaling
                self.jacobianScaling[
                    i
                    * self.ForwardSolve.numberOfNodes : (i + 1)
                    * self.ForwardSolve.numberOfNodes
                ] = 1 / np.average(
                    np.abs(
                        self.dcdrho[
                            i
                            * self.ForwardSolve.numberOfNodes : (i + 1)
                            * self.ForwardSolve.numberOfNodes]))

    def Objective(self, designVariables):
        self.j, self.djdrho, self.c, self.dcdrho = self.ForwardSolve.Solve(designVariables)
        return self.j

    def Gradient(self, designVariables):
        self.j, self.djdrho, self.c, self.dcdrho = self.ForwardSolve.Solve(designVariables)
        return self.djdrho

    def Constraints(self, designVariables):
        self.j, self.djdrho, self.c, self.dcdrho = self.ForwardSolve.Solve(designVariables)
        return self.c

    def Jacobian(self, designVariables):
        self.j, self.djdrho, self.c, self.dcdrho = self.ForwardSolve.Solve(designVariables)
        return self.dcdrho

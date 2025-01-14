import numpy as np  # type: ignore

def FiniteDifferenceValidation(self, perturbationIndex=0, errorTolerance=5e-2):
    # initial guess
    x0 = self.lowerBound + np.random.rand(self.ForwardSolve.numberOfNodes) * (self.upperBound - self.lowerBound)

    # perturbed initial guess
    perturbation = 1e-4
    x1 = np.copy(x0)
    x1[perturbationIndex] = x1[perturbationIndex] + perturbation

    # execute forward solve
    j0, djdrho0, c0, dcdrho0 = self.ForwardSolve.Solve(x0)
    j1, djdrho1, c1, dcdrho1 = self.ForwardSolve.Solve(x1)

    # initialise error list
    error = []

    # objective function error
    objectiveFiniteDifference = (j1 - j0) / perturbation
    objectiveAdjoint = djdrho0[perturbationIndex]
    error.append(100 * (objectiveFiniteDifference - objectiveAdjoint) / objectiveFiniteDifference)

    # constraint error
    for i in range(len(c0)):
        constraintFiniteDifference = (c1[i] - c0[i]) / perturbation
        constraintAdjoint = dcdrho0[(i * self.ForwardSolve.numberOfNodes) + perturbationIndex]
        error.append(100
            * (constraintFiniteDifference - constraintAdjoint)
            / constraintFiniteDifference)

    # convert error list to numpy array
    self.error = np.array(error)

    # compare against error tolerance %
    if max(abs(self.error)) <= (100 * errorTolerance):
        print("")
        print("Finite difference validation: PASSED")
        print("")
    else:
        print("")
        print("Finite difference validation: FAILED")
        print("")

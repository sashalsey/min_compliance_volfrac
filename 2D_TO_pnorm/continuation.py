from cyIpoptSetup import CyIpoptWrapper
from cyIpoptSetup_p import CyIpoptWrapper_p
from optimise import OptimisationLoop
from optimise_p import OptimisationLoop_p

import time
start = time.time()
# continuation loop
continuationSteps = 4
betaContinuationList = [2 ** (i + 1) for i in range(continuationSteps)]
pnormList = 8

# flake8 initialisation bug
rhoOptimal = None
gradientScaling = None
constraintScaling = None
jacobianScaling = None

outputFolder2 = ("results/")
resultsFile = open(outputFolder2 + "combined_iteration_results.txt", "w")
resultsFile.write("Compliance\tVolume Fraction\tMax Stress\tStress Integral\n")
resultsFile.close()

# Volume constrained only
for i in range(2):
    optimisationClass = OptimisationLoop()
    optimisationClass.maximumNumberOfIterations = 100
    optimisationClass.beta = betaContinuationList[i]

    # determine if this is the first iteration of continuation
    if i == 0:
        pass
    else:
        # initialise design variables with previous solution
        optimisationClass.variableInitialisation = True
        optimisationClass.rho0 = rhoOptimal

        # initialise scaling with initial values (i = 0 scaling)
        optimisationClass.scalingInitialisation = True
        optimisationClass.gradientScaling = gradientScaling
        optimisationClass.constraintScaling = constraintScaling
        optimisationClass.jacobianScaling = jacobianScaling

    # optimisation setup
    optimisationClass.OptimisationSetup()

    # execute optimisation procedure using ipopt
    print("Beta:               ", betaContinuationList[i])
    print("")
    rhoOptimal = CyIpoptWrapper(optimisationClass)

    # output scaling
    gradientScaling = optimisationClass.gradientScaling
    constraintScaling = optimisationClass.constraintScaling
    jacobianScaling = optimisationClass.jacobianScaling

# Volume and stress constrained
for i in range(3):
    optimisationClass = OptimisationLoop_p()
    optimisationClass.maximumNumberOfIterations = 200
    optimisationClass.beta = betaContinuationList[i]
    optimisationClass.pnorm = pnormList

    # determine if this is the first iteration of continuation
    if i == 0:
        pass
    else:
        # initialise design variables with previous solution
        optimisationClass.variableInitialisation = True
        optimisationClass.rho0 = rhoOptimal

        # initialise scaling with initial values (i = 0 scaling)
        optimisationClass.scalingInitialisation = True
        optimisationClass.gradientScaling = gradientScaling
        optimisationClass.constraintScaling = constraintScaling
        optimisationClass.jacobianScaling = jacobianScaling

    # optimisation setup
    optimisationClass.OptimisationSetup()

    # execute optimisation procedure using ipopt
    print("Beta:               ", betaContinuationList[i])
    print("")
    rhoOptimal = CyIpoptWrapper_p(optimisationClass)

    # output scaling
    gradientScaling = optimisationClass.gradientScaling
    constraintScaling = optimisationClass.constraintScaling
    jacobianScaling = optimisationClass.jacobianScaling

end = time.time()
print("Total time ", (end - start))

from plot import plot
plot()
from cyIpoptSetup import CyIpoptWrapper
from optimise import OptimisationLoop
import time
start = time.time()
# continuation loop
continuationSteps = 4
betaContinuationList = [2 ** (i + 1) for i in range(continuationSteps)]

# flake8 initialisation bug
rhoOptimal = None
gradientScaling = None
constraintScaling = None
jacobianScaling = None

for i in range(continuationSteps):

    # initialise optimisation class
    optimisationClass = OptimisationLoop()
    optimisationClass.maximumNumberOfIterations = 20
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
end = time.time()
print("Total time ", (end - start))
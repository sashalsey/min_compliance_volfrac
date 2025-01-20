from cyIpoptSetup import CyIpoptWrapper
from optimise import OptimisationLoop
import time
start = time.time()
# continuation loop
continuationSteps = 4
betaContinuationList = [2,4,8,8] #[2 ** (i + 1) for i in range(continuationSteps)]
pnormList = [2, 3, 4, 8]

# flake8 initialisation bug
rhoOptimal = None
gradientScaling = None
constraintScaling = None
jacobianScaling = None

outputFolder2 = ("results/")
resultsFile = open(outputFolder2 + "combined_iteration_results.txt", "w")
resultsFile.write("Compliance\tVolume Fraction\tMax Stress\n")
resultsFile.close()

contime = [0 * i for i in range(continuationSteps)]
for i in range(continuationSteps):
    cont_start = time.time()
    # initialise optimisation class
    optimisationClass = OptimisationLoop()
    optimisationClass.maximumNumberOfIterations = 100
    optimisationClass.beta = betaContinuationList[i]
    optimisationClass.pnorm = pnormList[i]

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
    cont_end = time.time()
    contime[i] = cont_end - cont_start
end = time.time()
print("Total time ", (end - start))
print("Cont time ", contime)

from plot import plot
plot()
from cyIpoptSetup import CyIpoptWrapper
from optimise import OptimisationLoop
import time

start = time.time()
# continuation loop
continuationSteps = 1
betaContinuationList = 4 #[2 ** (i + 1) for i in range(continuationSteps)]

# flake8 initialisation bug
rhoOptimal = None
gradientScaling = None
constraintScaling = None
jacobianScaling = None

outputFolder2 = ("results/")
resultsFile = open(outputFolder2 + "combined_iteration_results.txt", "w")
resultsFile.write("Compliance\tVolume Fraction\tMax Stress\n")
resultsFile.close()

for i in range(continuationSteps):
    cont_start = time.time()
    # initialise optimisation class
    optimisationClass = OptimisationLoop()
    optimisationClass.maximumNumberOfIterations = 100
    optimisationClass.beta = betaContinuationList #[i]

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
    print("Beta:               ", betaContinuationList)#[i])
    print("")
    rhoOptimal = CyIpoptWrapper(optimisationClass)

    # output scaling
    gradientScaling = optimisationClass.gradientScaling
    constraintScaling = optimisationClass.constraintScaling
    jacobianScaling = optimisationClass.jacobianScaling

end = time.time()
print("Total time ", (end - start))

from plot import plot
plot()
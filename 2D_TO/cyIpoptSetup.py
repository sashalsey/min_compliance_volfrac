import numpy as np # type: ignore
import cyipopt # type: ignore

def CyIpoptWrapper(optimisationClass):
    numberOfVariables = len(optimisationClass.djdrho)
    numberOfConstraints = len(optimisationClass.c)

    # design variable bounds
    lowerBounds = np.ones(numberOfVariables) * optimisationClass.lowerBound
    upperBounds = np.ones(numberOfVariables) * optimisationClass.upperBound

    # constraint bounds
    # constraint 1 - volume fraction constraint
    constraintLowerBounds = np.array([0])
    constraintUpperBounds = np.array([0])

    # cyipopt class
    class OptimisationSetup:
        def __init__(self):
            pass

        def objective(self, designVariables):
            return optimisationClass.Objective(designVariables)

        def gradient(self, designVariables):
            return optimisationClass.Gradient(designVariables)

        def constraints(self, designVariables):
            return optimisationClass.Constraints(designVariables)

        def jacobian(self, designVariables):
            return optimisationClass.Jacobian(designVariables)

    # cyipopt setup
    optimisationProblem = cyipopt.Problem(
        n=numberOfVariables,
        m=numberOfConstraints,
        problem_obj=OptimisationSetup(),
        lb=lowerBounds,
        ub=upperBounds,
        cl=constraintLowerBounds,
        cu=constraintUpperBounds,)

    optimisationProblem.add_option("linear_solver", "ma97")
    optimisationProblem.add_option("max_iter", optimisationClass.maximumNumberOfIterations)
    optimisationProblem.add_option("accept_after_max_steps", 10)
    optimisationProblem.add_option("hessian_approximation", "limited-memory")
    optimisationProblem.add_option("mu_strategy", "adaptive")
    optimisationProblem.add_option("mu_oracle", "probing")
    optimisationProblem.add_option("tol", 1e-5)
    optimisationProblem.set_problem_scaling(obj_scaling=optimisationClass.gradientScaling)
    optimisationProblem.add_option("nlp_scaling_method", "user-scaling")

    # Solve the problem
    xOptimal, info = optimisationProblem.solve(optimisationClass.designVariables0)

    return xOptimal

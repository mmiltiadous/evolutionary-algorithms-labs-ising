import numpy as np
from ioh import get_problem, logger, ProblemClass
from evolutionary_strategies.population import Population
from evolutionary_strategies.individual import Individual
from evolutionary_strategies.recombination import *
from typing import Callable, Tuple

budget = 5000
dimension = 50


def s3801454_s3699463_ES(problem: callable, mu: int, lambda_: int, recombinate: Callable[[Population], Individual] = None) -> float:
    # Set default recombinate function to discrete_recombination_random_parent_selection
    recombinate = discrete_recombination_random_parent_selection if recombinate is None else recombinate

    # create and initialize the population P(0) o mu individuals
    population = Population.new(mu, dimension, problem)

    while problem.state.evaluations + lambda_ <= budget:
        offspring_population = Population()

        for _ in range(lambda_):
            # Recombination
            offspring = recombinate(population)

            # Mutation
            offspring = offspring.mutate()

            fitness = offspring.evaluate(problem)
            offspring.set_fitness(fitness)

            offspring_population.add(offspring)

        # Wipe memory
        population.clear()

        # Select new population
        population = offspring_population.elitist_selection(mu)

        # Wipe memory
        offspring_population.clear()
        del offspring_population

    # Wipe memory
    population.clear()
    del population


def create_problem(fid: int):
    # Declaration of problems to be tested.
    problem = get_problem(fid, dimension=dimension,
                          instance=1, problem_class=ProblemClass.PBO)

    # Create default logger compatible with IOHanalyzer
    # `root` indicates where the output files are stored.
    # `folder_name` is the name of the folder containing all output. You should compress the folder 'run' and upload it to IOHanalyzer.
    l = logger.Analyzer(
        # the working directory in which a folder named `folder_name` (the next argument) will be created to store data
        root="data",
        # the folder name to which the raw performance data will be stored
        folder_name=f'run_f{fid}',
        algorithm_name=f'es_f{id}',  # name of your algorithm
        algorithm_info=f'Practical assignment of the EA course f{fid}',
    )
    # attach the logger to the problem
    problem.attach_logger(l)
    return problem, l


if __name__ == "__main__":
    np.random.seed(42)
    # this how you run your algorithm with 20 repetitions/independent run
    F18, _logger = create_problem(18)
    f18_score = 0
    for run in range(20):
        s3801454_s3699463_ES(
            F18, 10, 112, intermediate_recombination_tournament_parent_selection)
        f18_score += F18.state.y_unconstrained_best
        # print(F18.state.y_unconstrained_best)
        F18.reset()  # it is necessary to reset the problem after each independent run
    _logger.close()  # after all runs, it is necessary to close the logger to make sure all data are written to the folder

    F19, _logger = create_problem(19)
    f19_score = 0
    for run in range(20):
        s3801454_s3699463_ES(
            F19, 18, 111, discrete_recombination_tournament_parent_selection)
        f19_score += F19.state.y_unconstrained_best
        # print(F19.state.y_unconstrained_best)
        F19.reset()
    _logger.close()

    print(f'F18 Average Score: {f18_score / 20}')
    print(f'F19 Average Score: {f19_score / 20}')

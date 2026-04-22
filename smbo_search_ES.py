from ES import create_problem, s3801454_s3699463_ES
from skopt.space import Integer, Categorical
from skopt import gp_minimize
import numpy as np
import argparse
from evolutionary_strategies.recombination import *


parser = argparse.ArgumentParser(
    description="Bayesian Optimization with argparse")
parser.add_argument("--problem", type=int, required=True,
                    help="Specify the problem number")
parser.add_argument("--iter", type=int, required=True,
                    help="Specify the number of iterations")
args = parser.parse_args()

prob, _logger = create_problem(args.problem)


def evaluate(mu: int, lambda_: int, recombinate) -> float:
    scores = 0
    for _ in range(20):
        s3801454_s3699463_ES(prob, mu, lambda_, recombinate)
        scores += prob.state.y_unconstrained_best
        prob.reset()
    _logger.close()

    return scores / 20


def objective_function(params):
    # print(params)
    mu = int(params[0])
    lambda_ = int(params[1])
    recombinate = recombination_functions[params[2]]
    return -evaluate(mu, lambda_, recombinate)


def callback(params):
    print("Current iteration:")
    print("mu:", params.x[0])
    print("lambda_:", params.x[1])
    print("recombinate", params.x[2])
    print("Score:", -params.fun)
    print()


recombination_functions = [
    global_discrete_recombination,
    global_intermediate_recombination,
    discrete_recombination_random_parent_selection,
    discrete_recombination_tournament_parent_selection,
    discrete_recombination_roulette_parent_selection,
    intermediate_recombination_random_parent_selection,
    intermediate_recombination_tournament_parent_selection,
    intermediate_recombination_roulette_parent_selection,
]

# Mapping indices to recombination functions
recombination_mapping = {i: func for i,
                         func in enumerate(recombination_functions)}

if __name__ == '__main__':

    # Define the search space using ConfigSpace values
    space = [Integer(10, 300, name='mu'), Integer(2, 1000, name='lambda_'),
             Categorical(list(range(len(recombination_functions))), name='recombination_function')]

    # Perform Bayesian optimization using gp_minimize
    result = gp_minimize(objective_function, space,
                         n_calls=args.iter, random_state=42, callback=callback)

    # Print the result
    print("Best parameters:")
    print("mu:", result.x[0])
    print("lambda_:", result.x[1])
    print("recombinate:", result.x[2])
    print("Best value:", -result.fun)

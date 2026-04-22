from .population import Population
from .individual import Individual


def global_discrete_recombination(population: Population) -> Individual:
    return population.global_discrete_recombination()


def global_intermediate_recombination(population: Population) -> Individual:
    return population.global_intermediate_recombination()


def discrete_recombination_random_parent_selection(population: Population) -> Individual:
    parent1, parent2 = population.random_selection(), population.random_selection()
    offspring = parent1.discrete_recombination(parent2)
    return offspring


def discrete_recombination_tournament_parent_selection(population: Population) -> Individual:
    parent1, parent2 = population.k_tournament_selection(2)
    offspring = parent1.discrete_recombination(parent2)
    return offspring


def discrete_recombination_roulette_parent_selection(population: Population) -> Individual:
    parent1, parent2 = population.roulette_selection(), population.roulette_selection()
    offspring = parent1.discrete_recombination(parent2)
    return offspring


def intermediate_recombination_random_parent_selection(population: Population) -> Individual:
    parent1, parent2 = population.random_selection(), population.random_selection()
    offspring = parent1.intermediate_recombination(parent2)
    return offspring


def intermediate_recombination_tournament_parent_selection(population: Population) -> Individual:
    parent1, parent2 = population.k_tournament_selection(2)
    offspring = parent1.intermediate_recombination(parent2)
    return offspring


def intermediate_recombination_roulette_parent_selection(population: Population) -> Individual:
    parent1, parent2 = population.roulette_selection(), population.roulette_selection()
    offspring = parent1.intermediate_recombination(parent2)
    return offspring


def global_intermediate_recombination(population: Population) -> Individual:
    return population.global_intermediate_recombination()


def discrete_recombination_random_parent_selection(population: Population) -> Individual:
    parent1, parent2 = population.random_selection(), population.random_selection()
    offspring = parent1.discrete_recombination(parent2)
    return offspring


def discrete_recombination_tournament_parent_selection(population: Population) -> Individual:
    parent1, parent2 = population.k_tournament_selection(2)
    offspring = parent1.discrete_recombination(parent2)
    return offspring


def discrete_recombination_roulette_parent_selection(population: Population) -> Individual:
    parent1, parent2 = population.roulette_selection(), population.roulette_selection()
    offspring = parent1.discrete_recombination(parent2)
    return offspring


def intermediate_recombination_random_parent_selection(population: Population) -> Individual:
    parent1, parent2 = population.random_selection(), population.random_selection()
    offspring = parent1.intermediate_recombination(parent2)
    return offspring


def intermediate_recombination_tournament_parent_selection(population: Population) -> Individual:
    parent1, parent2 = population.k_tournament_selection(2)
    offspring = parent1.intermediate_recombination(parent2)
    return offspring


def intermediate_recombination_roulette_parent_selection(population: Population) -> Individual:
    parent1, parent2 = population.roulette_selection(), population.roulette_selection()
    offspring = parent1.intermediate_recombination(parent2)
    return offspring

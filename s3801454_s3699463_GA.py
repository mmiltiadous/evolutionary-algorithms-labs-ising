import numpy as np
# you need to install this package `ioh`. Please see documentations here: 
# https://iohprofiler.github.io/IOHexp/ and
# https://pypi.org/project/ioh/
from ioh import get_problem, logger, ProblemClass
import sys
import itertools
import random


# budget = 5000
dimension = 50

# Uniform Crossover
def single_point_crossover(p1,p2,x):
    p1_new=np.append(p1[:x],p2[x:])
    p2_new=np.append(p2[:x],p1[x:])
    return p1_new,p2_new


def uniform_crossover(p1, p2, crossover_probability):
    if cross_type == 'uniform':
        if np.random.uniform(0, 1) < crossover_probability:
            for i in range(len(p1)):
                if np.random.uniform(0, 1) < 0.5:
                    t = p1[i]
                    p1[i] = p2[i]
                    p2[i] = t

def npoints_crossover(p1, p2, crossover_probability, npoints):
    if np.random.uniform(0, 1) < crossover_probability:
        cross_points = list(np.random.choice(range(1, 50), npoints, replace=False))
        for i in cross_points:
            p1, p2 = single_point_crossover(p1.copy(), p2.copy(), i) 
    return p1, p2
            

# Standard bit mutation using mutation rate p
def mutation(p, mutation_rate):
    for i in range(len(p)) :
        if np.random.uniform(0,1) < mutation_rate:
            p[i] = 1 - p[i]

def binomial_mutation(individual, mutation_probability, mutation_strength):
    mutated_individual = individual.copy()

    for i in range(len(mutated_individual)):
        if np.random.rand() < mutation_probability:
            # Add a random value from a binomial distribution
            mutation_value = np.random.binomial(1, mutation_strength)
            mutated_individual[i] = (mutated_individual[i] + mutation_value) % 2

    return mutated_individual
  

def proportional_selection(parent, parent_f):
    # Plusing 0.001 to avoid dividing 0
    f_min = min(parent_f)
    f_sum = sum(parent_f) - (f_min - 0.001) * len(parent_f)
    
    rw = [(parent_f[0] - f_min + 0.001)/f_sum]
    for i in range(1,len(parent_f)):
        rw.append(rw[i-1] + (parent_f[i] - f_min + 0.001) / f_sum)
    
    select_parent = []
    for i in range(len(parent)) :
        r = np.random.uniform(0,1)
        index = 0
        # print(rw,r)
        while(r > rw[index]) :
            index = index + 1
        select_parent.append(parent[index].copy())
    return select_parent


def tournamentk_selection(parent, parent_f, tournament_k): 
    select_parent = []
    tournament_k = min(tournament_k, len(parent_f))
    pre_select = np.random.choice(len(parent_f), tournament_k, replace=False)
    index = 0 
    for i in range(len(parent)) :
        pre_select = np.random.choice(len(parent_f),tournament_k,replace = False)
        max_f = sys.float_info.min
        for p in pre_select:
            if parent_f[p] > max_f:
                index = p
                max_f = parent_f[p]
        select_parent.append(parent[index].copy())
    return select_parent



def s3801454_s3699463_GA(problem,  pop_size, budget = None):
    # initial_pop = ... make sure you randomly create the first population
    # `problem.state.evaluations` counts the number of function evaluation automatically,
    # which is incremented by 1 whenever you call `problem(x)`.
    # You could also maintain a counter of function evaluations if you prefer.
    if problem.meta_data.problem_id == 18:
        optimum=8
    if problem.meta_data.problem_id == 19:
        optimum=50
    if budget is None:
        budget = 5000
    
    f_opt = sys.float_info.min
    x_opt = None
    parent = []
    parent_f = []
    for i in range(pop_size):

        # Initialization
        parent.append(np.random.randint(2, size = problem.meta_data.n_variables))
        parent_f.append(problem(parent[i]))
        #budget = budget - 1


    while problem.state.evaluations < budget :
        # please implement the mutation, crossover, selection here
        # .....
        # this is how you evaluate one solution `x`
        # f = problem(x)
        # Evaluate fitness for each individual in the population
    # no return value needed 
        if seletype == 'proportional':
            offspring = proportional_selection(parent,parent_f)
        elif seletype == 'tournamentk':
            offspring = tournamentk_selection(parent,parent_f,tournament_k)

        if cross_type=='npoints':
            for i in range(0,pop_size - (pop_size%2),2) :
                offspring[i], offspring[i+1]  =  npoints_crossover(offspring[i], offspring[i+1], crossover_probability, npoints) 
        elif cross_type=='uniform':
            for i in range(0,pop_size - (pop_size%2),2) :
                uniform_crossover(offspring[i], offspring[i+1], crossover_probability) 

        if mutatype == 'bitflip':
            for i in range(pop_size):
                mutation(offspring[i], mutation_rate)
        elif mutatype == 'binomial':
            for i in range(pop_size):
                offspring[i] = binomial_mutation(offspring[i], mutation_rate, mutation_strength)

        

        parent = offspring.copy()
        for i in range(pop_size) : 
            parent_f[i] = problem(parent[i])
            # budget = budget - 1
            if parent_f[i] > f_opt:
                    f_opt = parent_f[i]
                    x_opt = parent[i].copy()
            if f_opt >= optimum or problem.state.evaluations >= budget:
                break
    
    print(f_opt,x_opt)
    return f_opt

def create_problem(fid: int):
    # Declaration of problems to be tested.
  
    problem = get_problem(fid, dimension=dimension, instance=1, problem_class=ProblemClass.PBO)

    # Create default logger compatible with IOHanalyzer
    # `root` indicates where the output files are stored.
    # `folder_name` is the name of the folder containing all output. You should compress the folder 'run' and upload it to IOHanalyzer.
    l = logger.Analyzer(
        root=f"dataf{fid}",  # the working directory in which a folder named `folder_name` (the next argument) will be created to store data
        folder_name=f"experiment{i+1}",  # the folder name to which the raw performance data will be stored
        algorithm_name=f"genetic_algorithm problem f{fid} exp{i+1}",  # name of your algorithm
        algorithm_info="Practical assignment of the EA course",
    )
    # attach the logger to the problem
    problem.attach_logger(l)
    return problem, l


# Top 5 Combinations based on F18 Fitness:
# #bit flip
# Combination 1: {'npoints:': 10, 'tournament_k': 35, 'pop_size': 30, 'crossover_prob': 0.5, 'mutation_rate': 0.05, 'seed': 42, 'f_opt_f18': 4.378066451902746, 'f_opt_f19': 47.1}
# binomial
# Combination 2: {'npoints:': 5, 'tournament_k': 20, 'pop_size': 10, 'crossover_prob': 0.5, 'mutation_rate': 0.05, 'seed': 42, 'mutation_strength': 0.5, 'f_opt_f18': 4.369956857115103, 'f_opt_f19': 47.4}
# Combination 3: {'npoints:': 10, 'tournament_k': 5, 'pop_size': 10, 'crossover_prob': 0.8, 'mutation_rate': 0.05, 'seed': 42, 'mutation_strength': 0.5, 'f_opt_f18': 4.361577323640678, 'f_opt_f19': 47.7}
# Combination 4: {'npoints:': 20, 'tournament_k': 5, 'pop_size': 10, 'crossover_prob': 0.2, 'mutation_rate': 0.02, 'seed': 42, 'mutation_strength': 1.0, 'f_opt_f18': 4.34541494189218, 'f_opt_f19': 47.3}
# Combination 5: {'npoints:': 20, 'tournament_k': 10, 'pop_size': 10, 'crossover_prob': 0.5, 'mutation_rate': 0.05, 'seed': 42, 'mutation_strength': 0.5, 'f_opt_f18': 4.343026972608767, 'f_opt_f19': 47.8}

# Top 5 Combinations based on F19 Fitness: 
# #binomial
# Combination 1: {'npoints:': 20, 'tournament_k': 5, 'pop_size': 10, 'crossover_prob': 0.2, 'mutation_rate': 0.05, 'seed': 42, 'mutation_strength': 0.5, 'f_opt_f18': 4.289510891446778, 'f_opt_f19': 48.2}
# Combination 2: {'npoints:': 20, 'tournament_k': 10, 'pop_size': 10, 'crossover_prob': 0.8, 'mutation_rate': 0.05, 'seed': 42, 'mutation_strength': 0.5, 'f_opt_f18': 4.290196090650573, 'f_opt_f19': 48.0}
# Combination 3: {'npoints:': 10, 'tournament_k': 10, 'pop_size': 30, 'crossover_prob': 0.8, 'mutation_rate': 0.05, 'seed': 42, 'mutation_strength': 1.0, 'f_opt_f18': 4.076731756159349, 'f_opt_f19': 48.0}
# Combination 4: {'npoints:': 20, 'tournament_k': 5, 'pop_size': 10, 'crossover_prob': 0.8, 'mutation_rate': 0.02, 'seed': 42, 'mutation_strength': 1.0, 'f_opt_f18': 4.113778465113955, 'f_opt_f19': 47.9}
# Combination 5: {'npoints:': 20, 'tournament_k': 10, 'pop_size': 10, 'crossover_prob': 0.5, 'mutation_rate': 0.05, 'seed': 42, 'mutation_strength': 0.5, 'f_opt_f18': 4.343026972608767, 'f_opt_f19': 47.8}



if __name__ == "__main__":
    


    # best parameter configurations for each problem
    npointss = [10,20]
    tournament_ks=[35,5]
    pop_sizes=[30,10]
    crossover_probabilities=[0.5,0.2]
    mutation_rates=[0.05,0.05]
    seed=42
    mutation_strength= 0.5
    

    for i in range(2): #running best configuration for each of the f18 and f19 problems
        seletype = 'tournamentk' #'proportional'
        cross_type = 'npoints' #'uniform'


        crossover_probability = crossover_probabilities[i]
        mutation_rate =mutation_rates[i]
        pop_size = pop_sizes[i]

        tournament_k = tournament_ks[i]
        npoints = npointss[i]
        

        if i>0:
            mutatype='binomial'
        else: 
            mutatype = 'bitflip' 
            

        

        # this how you run your algorithm with 20 repetitions/independent run
        if i<1:
            np.random.seed(seed)

            F18, _logger = create_problem(18)
            #optimum=15
            s_f_opt=0
            for run in range(20):
                print(f'F18, Run:{run}')
                f_opt = s3801454_s3699463_GA(F18, pop_size)
                s_f_opt=s_f_opt+f_opt
                F18.reset() # it is necessary to reset the problem after each independent run
            _logger.close() # after all runs, it is necessary to close the logger to make sure all data are written to the folder
            print('F18 fitness average:',s_f_opt/20)
        
        else:
            np.random.seed(seed)

            F19, _logger = create_problem(19)
            #optimum=50
            s_f_opt2=0
            for run in range(20): 
                print(f'F19, Run:{run}')
                f_opt2=s3801454_s3699463_GA(F19, pop_size)
                s_f_opt2=s_f_opt2+f_opt2
                F19.reset()
            _logger.close()
            print('F19 fitness average:',s_f_opt2/20)

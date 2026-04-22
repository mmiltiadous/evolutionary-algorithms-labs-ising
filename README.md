# evolutionary-optimization
 
Implementation and tuning of a **Genetic Algorithm (GA)** and **Evolution Strategy (ES)** to solve two combinatorial optimization problems, the LABS (F18) and Ising Model (F19), as part of the Evolutionary Algorithms course (2023). Full report is also provided (`ea2023_practical_assignment_report.pdf`).
 
Hyperparameters were tuned using **Grid Search** (GA) and **Sequential Model-Based Optimization** (ES), exploring variants of selection, crossover, and mutation operators.
 
 
## Problems
 
### F18: Low Autocorrelation Binary Sequences (LABS)
Maximizes the reciprocal of autocorrelation energy over a binary sequence of length 50. The theoretical optimum approaches ~12.32 as n → ∞.
 
### F19: Ising Model (1D Ring)
Maximizes the energy of a one-dimensional Ising spin system. The optimum for dimension 50 is 50.
 
Both problems are evaluated using the [IOH Profiler](https://iohprofiler.github.io/) framework with a budget of **5000 function evaluations** and **20 independent runs**.
 
 
## Algorithms
 
### Genetic Algorithm (`s3801454_s3699463_GA.py`)
 
**Best configuration for F18** (avg. fitness 4.38):
- Tournament-k selection (k=35), n-point crossover (n=10), bit-flip mutation
- pop_size=30, crossover_prob=0.5, mutation_rate=0.05
**Best configuration for F19** (avg. fitness 48.2):
- Tournament-k selection (k=5), n-point crossover (n=20), binomial mutation
- pop_size=10, crossover_prob=0.2, mutation_rate=0.05, mutation_strength=0.5
- 
### Evolution Strategy (`s3801454_s3699463_ES.py`)
 
**Best configuration for F18** (avg. fitness 3.86):
- μ=10, λ=112, intermediate recombination + tournament parent selection
**Best configuration for F19** (avg. fitness 45.8):
- μ=18, λ=111, discrete recombination + tournament parent selection
### Hyperparameter Tuning
 
- **GA**: Grid search over population size, crossover probability, mutation rate, tournament size, and number of crossover points — see `grid_search_ga_f18_f19.ipynb`
- **ES**: Sequential Model-Based Optimization (Bayesian optimization via `scikit-optimize`) over μ, λ, and recombination function — see `smbo_search_ES.py`
 
## Requirements
 
```
ioh
scikit-optimize
numpy
```
 
Install:
```bash
pip install ioh scikit-optimize numpy
```
 
## Usage
 
**Run GA** (best configuration):
```bash
python s3801454_s3699463_GA.py
```
 
**Run ES** (best configuration):
```bash
python s3801454_s3699463_ES.py
```
 
**Run SMBO search for ES** on a given problem:
```bash
python smbo_search_ES.py --problem 18 --iter 50
python smbo_search_ES.py --problem 19 --iter 50
```
 
Output data is saved to `data/` (ES) and `dataf18/` / `dataf19/` (GA) in IOH Analyzer format.

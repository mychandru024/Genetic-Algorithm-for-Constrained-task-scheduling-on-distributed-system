
# coding: utf-8

# In[122]:

#    example which maximizes the sum of a list of integers
#    each of which can be 0 or 1

import random
import sys

from deap import base
from deap import creator
from deap import tools

import time
start_time = time.time()

print("\n\n\n\nTest Running ")
print("============================================================================")
stats=[]

param = sys.argv
IND_SIZE = int(param[1])
__gen =    int(param[2])
__pop =  int(param[3])


# Problem Size
# IND_SIZE = 150
# __gen = 50
# __pop = 450

print("\n\n- Problem Size ",IND_SIZE)
print("- Generation  ",__gen)
print("- Population Size  ",__pop)

# In[123]:

creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

toolbox = base.Toolbox()

toolbox.register("attr_bool", random.randint, 0, 1)
toolbox.register("individual", tools.initRepeat, creator.Individual,
    toolbox.attr_bool, IND_SIZE)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def evalOneMax(individual):
    return sum(individual),

toolbox.register("evaluate", evalOneMax)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)


# In[124]:
from datetime import datetime
startTime = datetime.now()

def geneticAlgo(NGEN,POP_SIZE):
    pop_fitNess = []
    random.seed(64)
    pop = toolbox.population(n=POP_SIZE)
    CXPB, MUTPB, NGEN = 0.5, 0.4, NGEN
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit
    for g in range(NGEN):
        offspring = toolbox.select(pop, len(pop))
        offspring = list(map(toolbox.clone, offspring))
        for child1, child2 in zip(offspring[::2], offspring[1::2]):
            if random.random() < CXPB:
                toolbox.mate(child1, child2)
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit
        pop[:] = offspring
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x*x for x in fits)
        std = abs(sum2 / length - mean**2)**0.5
        pop_fitNess.append(max(fits))
        if g == NGEN-1:
            stats.append(pop_fitNess)

    best_ind = tools.selBest(pop, 1)[0]
    # print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))



# In[125]:

# geneticAlgo(NGen,PopSize)
# problem size = 100
print("--- completed in %s seconds ---" % (time.time() - start_time))
geneticAlgo(__gen,__pop)
print("Each Generation Fitness:")
print(stats[0])

print("\n\nTest Completed ")
print("----------------------------------------------------------------------------")
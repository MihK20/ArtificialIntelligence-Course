import math
import random

POPULATION_SIZE = 200
ELITE_SIZE = 2 

# def population_generation(n):
#     population = []
#     for i in range(POPULATION_SIZE):
#         individual=[random.randint(0, 1) for i in range(n)]
#         population.append(individual)

#     return population

def population_generation(n, m, items):
    population = []

    for _ in range(POPULATION_SIZE):
        individual = [0] * n

        places = list(range(n))
        random.shuffle(places)

        total_weight = 0

        for i in places:
            weight, value = items[i]

            if total_weight + weight <= m and random.random() < 0.5:
                individual[i] = 1
                total_weight += weight

        population.append(individual)

    return population

def fitness_function(m, n, population, items):
    scores = []
    for individual in population:
        weight = 0
        sum1 = 0
        for i in range(n):
            if individual[i] == 1:
                mi, ci = items[i]
                weight+=mi
                sum1+=ci

        if weight>m:
            sum1 = 0
        scores.append(sum1)
    return scores

def selection(population, scores):
    traction = int(0.5 * POPULATION_SIZE)

    ranked = sorted(zip(population, scores), key=lambda x: x[1], reverse=True)

    cut = max(2, traction)
    selected = ranked[:cut]

    parents = [ random.choice(selected)[0][:] for i in range(POPULATION_SIZE)]
    return parents


def crossover(parent1, parent2):
    child = [parent1[i] if random.choice([False, True]) else parent2[i] for i in range(len(parent1))]
    return child

def repair(individual, m, items):
    sum1 = sum(items[i][0] for i in range(len(individual)) if individual[i] == 1)

    while sum1 > m:
        selected = [i for i in range(len(individual)) if individual[i] == 1]

        worst = min(selected, key=lambda i: items[i][1] / items[i][0])

        individual[worst] = 0
        sum1-= items[worst][0]

    return individual

def reproduction(parents, n):
    parentsLen = len(parents)

    children = []
    for i in range(0, parentsLen, 2):
        parent1 = parents[i]
        parent2 = parents[(i+1)%parentsLen]
        child = crossover(parent1, parent2)
        children.append(child)
        i+=1

    return children[:POPULATION_SIZE]


def mutation(children, n):
    rate = 1/n
    for individual in children:
        for i in range(n):
            if random.random() < rate:
                individual[i] = 1- individual[i]

    return children


def new_generation(population, children, m, n, items):
    scores = fitness_function(m, n, population, items)

    ranked = sorted(zip(population, scores), key=lambda x: x[1], reverse=True)
    elites = [individual for individual, score in ranked[:ELITE_SIZE]]

    new_population = elites + children
    new_scores = fitness_function(m, n, new_population, items)
    ranked = sorted(zip(new_population, new_scores), key=lambda x: x[1], reverse=True)

    return [individual for individual, score in ranked[:POPULATION_SIZE]]


def genetic_algorithm(m, n, items):
    population = population_generation(n, m, items)
    scores = fitness_function(m, n, population, items)
    
    best_values = []
    generations = 150

    for generation in range(generations + 1):
        best_value = max(scores)
        best_values.append(best_value)

        if generation == generations:
            break

        parents = selection(population, scores)

        children = reproduction(parents, n)

        children = mutation(children, n)

        children = [repair(child, m, items) for child in children]

        population = new_generation(population, children, m, n, items)

        scores = fitness_function(m, n, population, items)


    return max(scores), best_values


mn = input()
mn = mn.split(" ")
m = int(mn[0])
n = int(mn[1])

items = []
for i in range(n):
    mici = input()
    mici = mici.split(" ")
    mi = int(mici[0])
    ci = int(mici[1])
    items.append((mi, ci))

pop = genetic_algorithm(m, n , items)

for i, value in enumerate(pop[1]):
    if i % 10 == 0 or i == len(pop[1]) - 1:
        print(value)

print()
print(pop[0])

import math
import random

POPULATION_SIZE = 10000

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
            weight, _ = items[i]

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

    parents = [selected[i][0][:] for i in range(cut)]
    return parents


def crossover(parent1, parent2):
    child = [parent1[i] if random.choice([False, True]) else parent2[i] for i in range(len(parent1))]
    return child

# def crossover(parent1, parent2):
#     l = len(parent1)//3
#     r = 2 *l
#     child1 = parent1[:l]+parent2[l:r]+parent1[r:]
#     child2 = parent2[:l]+parent1[l:r]+parent2[r:]
#     return [child1, child2]

def repair(individual, m, items):
    totalWeight = sum(items[i][0] for i in range(len(individual)) if individual[i] == 1)

    while totalWeight > m:
        selected = [i for i in range(len(individual)) if individual[i] == 1]

        worst = min(selected, key=lambda i: items[i][1] / items[i][0])

        individual[worst] = 0
        totalWeight-= items[worst][0]

    return individual

def reproduction(parents, m, items):
    parentsLen = len(parents)

    children = []
    for i in range(parentsLen//2):
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)
        child = crossover(parent1, parent2)
        child = repair(child, m, items)
        children.append(child)

    return children


def mutation(children, n):
    rate = 0.2
    for individual in children:
        if random.random() < rate:
            i = random.choice(range(n))
            individual[i] = 1- individual[i]

    return children


def genetic_algorithm(m, n, items):
    population = population_generation(n, m, items)
    scores = fitness_function(m, n, population, items)
    
    best_values = []
    generations = 25

    for generation in range(generations + 1):
        best_value = max(scores)
        best_values.append(best_value)

        if generation == generations:
            break

        parents = selection(population, scores)

        children = reproduction(parents, m, items)

        children = mutation(children, n)
        parentL = len(parents)//2
        population = parents[:parentL] + children + children[:parentL]

        scores = fitness_function(m, n, population, items)


    return best_values


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

for i, value in enumerate(pop):
    if i % 3 == 0 or i == len(pop) - 1:
        print(value)

print()
print(pop[-1])

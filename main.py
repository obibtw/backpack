import random

items = [
    (5, 10), (3, 7), (2, 4), (3, 6), (1, 3),
    (4, 8), (6, 12), (2, 5), (3, 6), (4, 9)
]

capacity = 20
num_items = len(items)

POPULATION_SIZE = 100
GENERATIONS = 200
MUTATION_RATE = 0.1
CROSSOVER_RATE = 0.8
TOURNAMENT_SIZE = 3

def fitness_ga(individual):
    total_weight = 0
    total_value = 0
    for i in range(num_items):
        if individual[i] == 1:
            total_weight += items[i][0]
            total_value += items[i][1]
    if total_weight > capacity:
        return 0
    return total_value

def create_individual():
    return [random.randint(0, 1) for _ in range(num_items)]

def tournament_selection(population, fitnesses):
    tournament_indices = random.sample(range(len(population)), TOURNAMENT_SIZE)
    best_idx = max(tournament_indices, key=lambda idx: fitnesses[idx])
    return population[best_idx][:]

def crossover(parent1, parent2):
    if random.random() < CROSSOVER_RATE:
        point = random.randint(1, num_items - 1)
        child1 = parent1[:point] + parent2[point:]
        child2 = parent2[:point] + parent1[point:]
        return child1, child2
    return parent1[:], parent2[:]

def mutate(individual):
    for i in range(num_items):
        if random.random() < MUTATION_RATE:
            individual[i] = 1 - individual[i]
    return individual

def genetic_algorithm():
    print("\n[GENETIC ALGORITHM]")
    print("Iteration | Best Fitness | Avg Fitness")
    print("-" * 40)

    population = [create_individual() for _ in range(POPULATION_SIZE)]
    best_individual = None
    best_fitness = 0

    for generation in range(GENERATIONS):
        fitnesses = [fitness_ga(ind) for ind in population]

        current_best_idx = max(range(len(fitnesses)), key=lambda i: fitnesses[i])
        current_best_fitness = fitnesses[current_best_idx]

        if current_best_fitness > best_fitness:
            best_fitness = current_best_fitness
            best_individual = population[current_best_idx][:]

        if generation % 20 == 0:
            avg_fitness = sum(fitnesses) / POPULATION_SIZE
            print(f"   {generation:5d}   |     {best_fitness:5d}     |   {avg_fitness:.2f}")

        new_population = [best_individual[:]]

        while len(new_population) < POPULATION_SIZE:
            parent1 = tournament_selection(population, fitnesses)
            parent2 = tournament_selection(population, fitnesses)
            child1, child2 = crossover(parent1, parent2)
            child1 = mutate(child1)
            child2 = mutate(child2)
            new_population.append(child1)
            if len(new_population) < POPULATION_SIZE:
                new_population.append(child2)

        population = new_population

    return best_individual, best_fitness

NUM_ANTS = 30
ITERATIONS = 100
ALPHA = 1.0
BETA = 2.0
EVAPORATION = 0.5
Q = 100

pheromones = [1.0 for _ in range(num_items)]

def heuristic(i):
    weight, value = items[i]
    if weight == 0:
        return 0
    return value / weight

def ant_solution():
    solution = [0] * num_items
    total_weight = 0
    for i in range(num_items):
        if total_weight + items[i][0] <= capacity:
            attract = (pheromones[i] ** ALPHA) * (heuristic(i) ** BETA)
            prob = attract / (1 + attract)
            if random.random() < prob:
                solution[i] = 1
                total_weight += items[i][0]
    return solution

def fitness_aco(individual):
    total_weight = 0
    total_value = 0
    for i in range(num_items):
        if individual[i] == 1:
            total_weight += items[i][0]
            total_value += items[i][1]
    if total_weight > capacity:
        return 0
    return total_value

def update_pheromones(ants_solutions, ants_values):
    global pheromones
    for i in range(num_items):
        pheromones[i] *= (1 - EVAPORATION)
    for ant_sol, ant_val in zip(ants_solutions, ants_values):
        for i in range(num_items):
            if ant_sol[i] == 1:
                pheromones[i] += Q * (ant_val / capacity)

def ant_colony_algorithm():
    print("\n[ANT COLONY ALGORITHM]")
    print("Iteration | Best Value | Avg Value")
    print("-" * 40)

    best_solution = None
    best_value = 0

    for iteration in range(ITERATIONS):
        ant_solutions = []
        ant_values = []

        for _ in range(NUM_ANTS):
            solution = ant_solution()
            value = fitness_aco(solution)
            ant_solutions.append(solution)
            ant_values.append(value)
            if value > best_value:
                best_value = value
                best_solution = solution[:]

        update_pheromones(ant_solutions, ant_values)

        if iteration % 20 == 0:
            avg_value = sum(ant_values) / NUM_ANTS
            print(f"   {iteration:5d}   |     {best_value:5d}     |   {avg_value:.2f}")

    return best_solution, best_value

def print_solution(individual, total_value, algorithm_name):
    print("\n[RESULT: " + algorithm_name + "]")

    total_weight = 0
    selected_items = []

    for i in range(len(individual)):
        if individual[i] == 1:
            total_weight += items[i][0]
            selected_items.append((i + 1, items[i][0], items[i][1]))

    print("Items count: " + str(len(selected_items)))
    print("Total weight: " + str(total_weight) + " kg")
    print("Total value: " + str(total_value))
    print("Free space: " + str(capacity - total_weight) + " kg")
    print("")
    print("Selected items (index: weight, value):")
    for idx, weight, value in selected_items:
        print("  " + str(idx) + ": " + str(weight) + " kg, " + str(value) + " value")

def main():
    print("\n[KNAPSACK PROBLEM]")
    print("Items: " + str(num_items))
    print("Capacity: " + str(capacity) + " kg")
    print("")

    best_individual_ga, best_value_ga = genetic_algorithm()
    print_solution(best_individual_ga, best_value_ga, "GENETIC ALGORITHM")

    best_individual_ant, best_value_ant = ant_colony_algorithm()
    print_solution(best_individual_ant, best_value_ant, "ANT COLONY ALGORITHM")

    print("\n[COMPARISON]")
    print("Genetic Algorithm value: " + str(best_value_ga))
    print("Ant Colony Algorithm value: " + str(best_value_ant))

    if best_value_ga > best_value_ant:
        print("Winner: GENETIC ALGORITHM")
    elif best_value_ant > best_value_ga:
        print("Winner: ANT COLONY ALGORITHM")
    else:
        print("Draw")

if __name__ == "__main__":
    main()
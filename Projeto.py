import numpy as np
import random
from numpy.random import choice
import matplotlib.pyplot as plt

SERV = 4  # numero de servidores
TASKS = 5  # numero de tarefas
POPULATION = 100  # Size of Population
CROSS_RATE = 0.8  # CrossOver Chance
MUTATION_RATE = 0.03  # Mutation Rate
N_GENERATIONS = 100  # Number of Generations


def organizar(population, tempototal):
    for population, tempototal in zip(tempototal, np.array(population)[np.argsort(tempototal)]):
        print((population, tempototal))
    pass


def fitness(elemento, matcusto):
    elemento = np.squeeze(np.asarray(elemento))
    result = elemento * matcusto
    custo_total = np.sum(result)  # Soma o total de tempo que demora a concluir as taref

    return custo_total


def aceitaRejeita(population, tempototal, matcusto):
    end = 0

    while True:

        solucao = []

        solution = population[
            random.randint(0, len(population) - 1)]
        solucao.append(fitness(solution, matcusto))

        maxFit = choice(tempototal)

        if (maxFit < solucao):
            return solution
        end = end + 1

        if end > 1000:
            return None


def crossover(solution1, solution2):
    corta1 = solution1[:, 1:3]
    print(" Corta coluna 1 e 2 da primeira solução", "\n\n", corta1, "\n\n")

    corta2 = solution2[:, 0:1]
    corta3 = solution2[:, 3:5]

    print(" Corte 2 - primeira task da segunda solução", "\n\n", corta2, "\n\n",
          "Corte 3 - últimas duas tasks da segunda solução", "\n\n", corta3, "\n\n")

    filho = np.hstack([corta2, corta1, corta3])

    print(" Matriz Filho com 2 colunas da solução 1 e o resto da solução 2", "\n\n",
          filho, "\n\n")

    return filho


def mutacao(novo_filho):
    crianca = np.matrix(novo_filho)
    aux = crianca[:, [1, 3]]
    crianca[:, [1, 3]] = crianca[:, [3, 1]]
    crianca[:, [3, 1]] = aux

    return crianca


def main():
    # Criar Matriz com custos

    matcusto = np.random.rand(SERV, TASKS)

    # inicializar populacao

    population = []
    for w in range(POPULATION):
        elemento = np.zeros((SERV, TASKS), dtype=np.int)
        for i in range(TASKS):
            elemento[random.randint(0, SERV - 1)][i] = 1
        population.append(elemento)

    # avalia o fitness

    tempototal = []
    for j in range(POPULATION):
        tempototal.append(fitness(population[j], matcusto))

    best_solution = []
    best_fitness = 0
    gen_count = 0
    crossover_count = 0
    mutation_count = 0




    for g in range(N_GENERATIONS):

        gen_count += 1

        solution1 = aceitaRejeita(population, tempototal, matcusto)
        solution2 = aceitaRejeita(population, tempototal, matcusto)

        print(" Solução 1", "\n\n", solution1, "\n\n", "Solução 2", "\n\n", solution2, "\n\n")

        # crossover

        novo_filho = []

        for _ in range(POPULATION):
            novo_filho.append(crossover(solution1, solution2))
            crossover_count += 1

        # mutacao

        crianca = []

        for _ in range(POPULATION):
            if np.random.rand() < MUTATION_RATE:
                crianca.append(mutacao(novo_filho[_]))
                mutation_count += 1
            else:
                crianca.append(novo_filho[_])

        # vereficar se a solucao e boa

        population = crianca

        for f in range(POPULATION):
            fitcrianca = fitness(population[f], matcusto)
            if best_fitness < fitcrianca:
                best_fitness = fitcrianca
                best_solution = population[f]

    print("\n\n", "Número de Gerações:", gen_count, "\n\n", "Número de Crossovers:", crossover_count, "\n\n",
          "Número de Mutações:", mutation_count, "\n\n", "MELHOR SOLUCAO:", "\n\n", best_solution, "\n\n", "Fiteness tempo total", best_fitness)

    # cria um grafico para o melhor fitness x geracoes

    plt.plot(tempototal)
    plt.xlabel('nr. de geracoes')
    plt.ylabel('melhor fitness')
    plt.title('Curva de fitness')
    plt.show()


if __name__ == '__main__':
    main()

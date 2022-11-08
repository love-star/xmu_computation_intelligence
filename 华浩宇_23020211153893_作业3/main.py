import numpy as np
import random
import copy
import matplotlib.pyplot as plt


class City:
    def __init__(self, idx, x, y):
        self.idx = idx
        self.x = x
        self.y = y

    def __repr__(self):
        return str(self.idx)


def distance(ca, cb):
    dx = abs(ca.x - cb.x)
    dy = abs(ca.y - cb.y)
    distance = int(np.sqrt((dx ** 2) + (dy ** 2)))
    return distance


def init_pop(city_list, popSize):
    pop = []
    for i in range(popSize):
        new_city_list = random.sample(city_list, len(city_list))
        pop.append(new_city_list)

    return pop


def fitness(pop):
    dis_citys = distance_citys(pop)
    return 1.0 / dis_citys


def distance_citys(pop):
    temp_dis = 0
    for i in range(len(pop) - 1):
        temp_dis += distance(pop[i], pop[i + 1])
    temp_dis += distance(pop[len(pop) - 1], pop[0])

    return temp_dis


def rank(poplulation):
    rankPop_dic = {}
    for i in range(len(poplulation)):
        fit = fitness(poplulation[i])
        rankPop_dic[i] = fit

    return sorted(rankPop_dic.items(), key=lambda x: x[1], reverse=True)


def select(pop, pop_rank, eliteSize):
    select_pop = []
    for i in range(eliteSize):
        select_pop.append(pop[pop_rank[i][0]])

    cumsum = 0
    cumsum_list = []
    temp_pop = copy.deepcopy(pop_rank)
    for i in range(len(temp_pop)):
        cumsum += temp_pop[i][1]
        cumsum_list.append(cumsum)
    for i in range(len(temp_pop)):
        cumsum_list[i] /= cumsum

    for i in range(len(temp_pop) - eliteSize):
        rate = random.random()
        for j in range(len(temp_pop)):
            if cumsum_list[j] > rate:
                select_pop.append(pop[pop_rank[i][0]])
                break

    return select_pop


def breed(pop, eliteSize):
    breed_pop = []
    for i in range(eliteSize):
        breed_pop.append(pop[i])

    i = 0
    while i < (len(pop) - eliteSize):
        a = random.randint(0, len(pop) - 1)
        b = random.randint(0, len(pop) - 1)
        if a != b:
            fa, fb = pop[a], pop[b]
            genea, geneb = random.randint(0, len(pop[a]) - 1), random.randint(0, len(pop[b]) - 1)
            startgene = min(genea, geneb)
            endgene = max(genea, geneb)
            child1 = []
            for j in range(startgene, endgene):
                child1.append(fa[j])
            child2 = []
            for j in fb:
                if j not in child1:
                    child2.append(j)
            breed_pop.append(child1 + child2)
            i = i + 1

    return breed_pop


def mutate(pop, mutationRate):
    mutation_pop = []
    for i in range(len(pop)):
        for j in range(len(pop[i])):
            rate = random.random()
            if rate < mutationRate:
                a = random.randint(0, len(pop[i]) - 1)
                pop[i][a], pop[i][j] = pop[i][j], pop[i][a]
        mutation_pop.append(pop[i])

    return mutation_pop


def next_pop(population, eliteSize, mutationRate):
    pop_rank = rank(population)  # 按照适应度排序
    select_pop = select(population, pop_rank, eliteSize)  # 精英选择策略，加上轮盘赌选择
    breed_pop = breed(select_pop, eliteSize)  # 繁殖
    next_generation = mutate(breed_pop, mutationRate)  # 变异

    return next_generation


# 画出路线图的动态变化
def GA_plot_dynamic(city_list, popSize, eliteSize, mutationRate, generations):
    plt.figure('Map')
    plt.ion()
    population = init_pop(city_list, popSize)

    print("initial distance:{}".format(1.0 / (rank(population)[0][1])))
    for i in range(generations):
        plt.cla()
        population = next_pop(population, eliteSize, mutationRate)
        idx_rank_pop = rank(population)[0][0]
        best_route = population[idx_rank_pop]
        city_x = []
        city_y = []
        for j in range(len(best_route)):
            city = best_route[j]
            city_x.append(city.x)
            city_y.append(city.y)
        city_x.append(best_route[0].x)
        city_y.append(best_route[0].y)
        plt.scatter(city_x, city_y, c='r', marker='*', s=200, alpha=0.5)
        plt.plot(city_x, city_y, "b", ms=20)
        plt.pause(0.1)

    plt.ioff()
    plt.show()

    print("final distance:{}".format(1.0 / (rank(population)[0][1])))
    bestRouteIndex = rank(population)[0][0]
    bestRoute = population[bestRouteIndex]
    return bestRoute


def GA(city_list, popSize, eliteSize, mutationRate, generations):
    population = init_pop(city_list, popSize)  # 初始化种群
    process = []

    print("initial distance:{}".format(1.0 / (rank(population)[0][1])))
    for i in range(generations):
        population = next_pop(population, eliteSize, mutationRate)  # 产生下一代种群
        process.append(1.0 / (rank(population)[0][1]))

    plt.figure(1)
    print("final distance:{}".format(1.0 / (rank(population)[0][1])))
    plt.plot(process)
    plt.ylabel('Distance')
    plt.xlabel('Generation')
    plt.savefig(str(generations) + '_' + str(1.0 / (rank(population)[0][1])) + '_' + str(mutationRate) + '_process.jpg')

    plt.figure(2)
    idx_rank_pop = rank(population)[0][0]
    best_route = population[idx_rank_pop]
    print(best_route)
    city_x = []
    city_y = []
    for j in range(len(best_route)):
        city = best_route[j]
        city_x.append(city.x)
        city_y.append(city.y)
    city_x.append(best_route[0].x)
    city_y.append(best_route[0].y)
    plt.scatter(city_x, city_y, c='r', marker='*', s=200, alpha=0.5)
    plt.plot(city_x, city_y, "b", ms=20)
    for i in range(len(coordinates)):
        plt.text(coordinates[i][0], coordinates[i][1], r'  ' + str(i + 1))
    plt.savefig(str(generations) + '_' + str(mutationRate) + '_route.jpg')
    plt.show()


num_city = 15
city_list = []

coordinates = np.array([[-0.0000000400893815, 0.0000000358808126],
                        [-28.8732862244731230, -0.0000008724121069],
                        [-79.2915791686897506, 21.4033307581457670],
                        [-14.6577381710829471, 43.3895496964974043],
                        [-64.7472605264735108, -21.8981713360336698],
                        [-29.0584693142401171, 43.2167287683090606],
                        [-72.0785319657452987, -0.1815834632498404],
                        [-36.0366489745023770, 21.6135482886620949],
                        [-50.4808382862985496, -7.3744722432402208],
                        [-50.5859026832315024, 21.5881966132975371],
                        [-0.1358203773809326, 28.7292896751977480],
                        [-65.0865638413727368, 36.0624693073746769],
                        [-21.4983260706612533, -7.3194159498090388],
                        [-57.5687244704708050, 43.2505562436354225],
                        [-43.0700258454450875, -14.5548396888330487]])

for i in range(0, num_city):
    city_list.append(City(i + 1, coordinates[i][0], coordinates[i][1]))

GA(city_list, 100, 20, 0.01, 500)

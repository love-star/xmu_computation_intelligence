import random

import matplotlib.pyplot as plt

from MAEPSO import *
plt.rcParams['font.sans-serif'] = ['SimHei']


iter_num = 1500  # 迭代次数


class Particle:
    def __init__(self, Vmax, maxSpeed, dim, func=lambda x:np.sum(np.square(x), axis=1)):
        self.pos = [random.uniform(-Vmax, Vmax) for i in range(dim)]  # 粒子的位置
        self.speed = [random.uniform(-maxSpeed, maxSpeed) for i in range(dim)]  # 粒子的速度
        self.bestPos = [0.0 for i in range(dim)]  # 粒子最好的位置
        self.func = func
        self.fitnessValue = self.func(self.pos)  # 适应度函数值

    def set_pos(self, i, value):
        self.pos[i] = value

    def get_pos(self):
        return self.pos

    def set_best_pos(self, i, value):
        self.bestPos[i] = value

    def get_best_pos(self):
        return self.bestPos

    def set_speed(self, i, value):
        self.speed[i] = value

    def get_speed(self):
        return self.speed

    def set_fitness_value(self, value):
        self.fitnessValue = value

    def get_fitness_value(self):
        return self.fitnessValue


class PSO:
    def __init__(self, iter_num, func=lambda x:np.sum(np.square(x), axis=1), bestFitnessValue=float('Inf')):
        self.C1 = 1.2
        self.C2 = 1.2
        self.W = 1
        self.dim = 30  # 粒子的维度
        self.n = 20  # 粒子个数
        self.iter_num = iter_num  # 迭代次数
        self.Vmax = 10
        self.maxSpeed = 0.5  # 粒子最大速度
        self.bestFitnessValue = bestFitnessValue
        self.bestPosition = [0.0 for i in range(self.dim)]  # 种群最优位置
        self.bestFitnessList = []  # 每次迭代最优适应值
        self.func = func  # 适应度函数

        # 对种群进行初始化
        self.ParticleList = [Particle(self.Vmax, self.maxSpeed, self.dim, self.func) for i in range(self.n)]

    def set_bestFitnessValue(self, value):
        self.bestFitnessValue = value

    def get_bestFitnessValue(self):
        return self.bestFitnessValue

    def set_bestPosition(self, i, value):
        self.bestPosition[i] = value

    def get_bestPosition(self):
        return self.bestPosition

    # 按照公式更新速度
    def update_speed(self, part):
        for i in range(self.dim):
            speed_value = self.W * part.get_speed()[i] + self.C1 * random.random() * (part.get_best_pos()[i] - part.get_pos()[i]) \
                        + self.C2 * random.random() * (self.get_bestPosition()[i] - part.get_pos()[i])
            if speed_value > self.maxSpeed:
                speed_value = self.maxSpeed
            elif speed_value < -self.maxSpeed:
                speed_value = -self.maxSpeed
            part.set_speed(i, speed_value)

    # 按照公式更新位置
    def update_pos(self, part):
        for i in range(self.dim):
            pos_value = part.get_pos()[i] + part.get_speed()[i]
            part.set_pos(i, pos_value)
        value = self.func(part.get_pos())
        if value < part.get_fitness_value():
            part.set_fitness_value(value)
            for i in range(self.dim):
                part.set_best_pos(i, part.get_pos()[i])
        if value < self.get_bestFitnessValue():
            self.set_bestFitnessValue(value)
            for i in range(self.dim):
                self.set_bestPosition(i, part.get_pos()[i])

    def update(self):
        for i in range(self.iter_num):
            for part in self.ParticleList:
                self.update_speed(part)  # 更新速度
                self.update_pos(part)  # 更新位置
            self.bestFitnessList.append(self.get_bestFitnessValue())  # 每次迭代完把当前的最好适应度保存
        return self.bestFitnessList


if __name__ == "__main__":
    pso1 = PSO(iter_num, func=Rosenbrock)
    bestFitnessList1 = pso1.update()
    pso2 = MAEPSO(func=Rosenbrock, methods='MAEPSO')
    bestFitnessList2 = pso2.evolve(iter_num, 1)
    x = np.linspace(400, iter_num, iter_num-400)
    plt.figure()
    plt.plot(x, bestFitnessList1[400:], c="r")
    plt.plot(x, bestFitnessList2[400:], c="b")
    plt.title("PSO(red)+MAEPSO(blue)")
    plt.xlabel("迭代次数")
    plt.ylabel("最优解")
    plt.show()
import math


def Tablet(X):
    sum = 0
    for i in range(1, len(X)):
        sum = sum + X[i] ** 2
    return sum + (X[0] ** 2) * 100000


def Quadratic(X):
    sum = 0
    for i in range(0, len(X)):
        tmp = 0
        for j in range(0, i + 1):
            tmp += X[j]
        sum += tmp ** 2
    return sum


def Rosenbrock(X):
    sum = 0
    for i in range(0, len(X) - 1):
        sum += 100 * (X[i + 1] - X[i] * X[i]) ** 2 + (X[i] - 1) ** 2
    return sum


def Griewank(X):
    sum1 = 0
    sum2 = 1
    for i in range(0, len(X)):
        sum1 += X[i] * X[i] / 4000
        sum2 *= math.cos(X[i] / math.sqrt(i + 1))
    return sum1 - sum2 + 1


def Rastrigin(X):
    sum = 0
    for i in range(0, len(X)):
        sum += (X[i] ** 2 - 10 * math.cos(2 * math.pi * X[i]) + 10)
    return sum


def Schaffer(X):
    sum = 0
    for i in range(0, len(X) - 1):
        si = pow(X[i] ** 2 + X[i + 1] ** 2, 1 / 4)
        sum += si * (math.sin(50 * pow(si, 1 / 10)) + 1.0)
    return sum

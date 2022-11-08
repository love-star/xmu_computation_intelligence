import matplotlib.pyplot as plt
import numpy as np
import copy

# the number of city
cityCount = 15

# 旅行商问题 ( TSP , Traveling Salesman Problem )
data_xy = np.array([[-0.0000000400893815, 0.0000000358808126],
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


# 得到距离矩阵的函数
def get_distance_matrix(data_xy):
    num = data_xy.shape[0]  # 15个坐标点
    distmat = np.zeros((15, 15))  # 15X15距离矩阵
    for i in range(num):
        for j in range(i, num):
            distmat[i][j] = distmat[j][i] = round(np.linalg.norm(data_xy[i] - data_xy[j]))
    return distmat



# 计算路径的长度
def cal_distance(distance, route):
    dis = 0
    length = len(route)
    for i in range(length - 1):
        dis += distance[route[i]][route[i + 1]]
    dis += distance[route[length - 1]][route[0]]
    return dis


# 画出最优路径
def draw_best_path(bestRoute, data_xy):
    plt.figure(2)
    x = []
    y = []
    for i in bestRoute:
        x.append(data_xy[i - 1][0])
        y.append(data_xy[i - 1][1])
    plt.scatter(x, y)
    plt.plot(x, y)
    for i in range(len(data_xy)):
        plt.text(data_xy[i][0], data_xy[i][1], r'  ' + str(i + 1))
    plt.xlabel('x')
    plt.ylabel('y')
    plt.show()


# 画出解的能量变化
def draw_energy(energys):
    plt.figure(1)
    plt.plot(np.arange(0, len(energys), 1), energys, color='b')
    plt.xlabel("L")
    plt.ylabel("energy")
    plt.show()


# 动态方程计算微分方程du
def cal_du(V, distance):
    sum_col = np.sum(V, axis=0) - 1  # 列之和
    sum_row = np.sum(V, axis=1) - 1  # 行之和
    temp1 = np.zeros((cityCount, cityCount))
    temp2 = np.zeros((cityCount, cityCount))
    for i in range(cityCount):
        for j in range(cityCount):
            temp1[i, j] = sum_col[j]
    for i in range(cityCount):
        for j in range(cityCount):
            temp2[j, i] = sum_row[j]
    # 将第一列移动到最后一列
    c_1 = V[:, 1:cityCount]
    c_0 = np.zeros((cityCount, 1))
    c_0[:, 0] = V[:, 0]
    c = np.concatenate((c_1, c_0), axis=1)
    c = np.dot(distance, c)
    return -A * (temp1 + temp2) - D * c


# 更新神经网络的输入电压U
def cal_U(U, du, step):
    return U + du * step


# 更新神经网络的输出电压V
def cal_V(U, U0):
    return 1 / 2 * (1 + np.tanh(U / U0))


# 计算当前网络的能量
def cal_energy(V, distance):
    t1 = np.sum(np.power(np.sum(V, axis=0) - 1, 2))
    t2 = np.sum(np.power(np.sum(V, axis=1) - 1, 2))
    idx = [i for i in range(1, cityCount)]
    idx = idx + [0]
    Vt = V[:, idx]
    t3 = distance * Vt
    t3 = np.sum(np.sum(np.multiply(V, t3)))
    e = 0.5 * (A * (t1 + t2) + D * t3)
    return e


# 生成路径
def generate_route(V):
    newV = np.zeros([cityCount, cityCount])
    route = []
    for i in range(cityCount):
        mm = np.max(V[:, i])
        for j in range(cityCount):
            if V[j, i] == mm:
                newV[j, i] = 1
                route += [j]
                break
    return route, newV


if __name__ == '__main__':
    A = cityCount ** 2
    D = cityCount / 2
    U0 = 0.0001  # 初始电压
    step = 0.001  # 步长
    L = 100000  # 迭代次数
    flag = False

    distance = get_distance_matrix(data_xy)  # 获取城市的距离矩阵

    # 初始化神经网络的输入状态（电路的输入电压U）
    U = 1 / 2 * U0 * np.log(cityCount - 1) + (2 * (np.random.random((cityCount, cityCount))) - 1)
    # 初始化神经网络的输出状态（电路的输出电压V）
    V = cal_V(U, U0)

    energys = np.array([0.0 for x in range(L)])  # 每次迭代的能量
    best_distance = np.inf  # 最优距离
    best_route = []  # 最优路线
    distances = []  # 每个路径解的距离

    # 迭代训练网络
    for i in range(L):
        # 利用动态方程计算du
        du = cal_du(V, distance)
        # 由一阶欧拉法更新下一个时间的输入状态（电路的输入电压U）
        U = cal_U(U, du, step)
        # 由sigmoid函数更新下一个时间的输出状态（电路的输出电压V）
        V = cal_V(U, U0)
        # 计算当前网络的能量E
        energys[i] = cal_energy(V, distance)
        # 检查路径的合法性
        route, newV = generate_route(V)
        if len(np.unique(route)) == cityCount:
            route.append(route[0])
            dis = cal_distance(distance, route)
            distances.append(dis)
            print('第{}次迭代找到的符合条件的当前距离为：{}，能量为：{}，路径为：{}'.format(i, dis, energys[i], route))
            if dis <= best_distance:
                best_distance = dis
                best_route = copy.deepcopy(route)
                flag = True
    if flag:
        draw_energy(energys)  # 画出能量变化
        draw_best_path(best_route, data_xy)
        print('神经网络找到的最优解距离为：{}，路径为：{}'.format(best_distance, best_route))
    else:
        print('没有找到最优解')

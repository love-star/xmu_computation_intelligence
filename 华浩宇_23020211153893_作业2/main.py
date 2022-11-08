import numpy as np
import matplotlib.pyplot as plt

# 旅行商问题 ( TSP , Traveling Salesman Problem )
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


# 得到距离矩阵的函数
def get_distance_matrix(coordinates):
    num = coordinates.shape[0]  # 15个坐标点
    distmat = np.zeros((15, 15))  # 15X15距离矩阵
    for i in range(num):
        for j in range(i, num):
            distmat[i][j] = distmat[j][i] = round(np.linalg.norm(coordinates[i] - coordinates[j]))
    return distmat


def init_parameter():
    alpha = 0.99
    t = (1, 100)
    epoch = 1000
    return alpha, t, epoch


num = coordinates.shape[0]
distmat = get_distance_matrix(coordinates)  # 得到距离矩阵

new_solution = np.arange(num)

PATH_MAX_LENGTH = 999999
current_solution = new_solution.copy()
current_length = PATH_MAX_LENGTH

best_solution = new_solution.copy()
best_length = PATH_MAX_LENGTH

alpha, t2, epoch = init_parameter()
t = t2[1]

result = []  # 记录迭代过程中的最优解
while t > t2[0]:
    for i in np.arange(epoch):
        while True:  # 产生两个不同的随机数
            loc1 = int(np.ceil(np.random.rand() * (num - 1)))
            loc2 = int(np.ceil(np.random.rand() * (num - 1)))

            if loc1 != loc2:
                break
        new_solution[loc1], new_solution[loc2] = new_solution[loc2], new_solution[loc1]

        new_length = 0
        for i in range(num - 1):
            new_length += distmat[new_solution[i]][new_solution[i + 1]]
        new_length += distmat[new_solution[14]][new_solution[0]]
        if new_length < current_length:  # 接受该解
            # 更新current_solution
            current_length = new_length
            current_solution = new_solution.copy()
            # 更新 best_solution
            if new_length < best_length:
                best_length = new_length
                best_solution = new_solution.copy()
        else:  # 按一定的概率接受该解
            if np.random.rand() < np.exp(-(new_length - current_length) / t):
                current_length = new_length
                current_solution = new_solution.copy()
            else:
                new_solution = current_solution.copy()
    t = alpha * t
    result.append(best_length)
# 用来显示结果
solution = np.append(best_solution, 0)
solution = solution + np.ones(solution.shape)
solution = solution.astype(int)
print(solution)

plt.subplot(1, 2, 1)
plt.plot(np.array(result))
plt.ylabel("best_length")
plt.xlabel("t")
plt.subplot(1, 2, 2)
x, y = [], []
for i in np.nditer(solution):
    x.append(coordinates[i - 1][0])
    y.append(coordinates[i - 1][1])
plt.scatter(x, y)
plt.plot(x, y)
plt.title("Epoch: {}   t:{:.2f}".format(epoch, t))
for i in range(len(coordinates)):
    plt.text(coordinates[i][0], coordinates[i][1], r'  ' + str(i + 1))
plt.xlabel('x')
plt.ylabel('y')
plt.show()

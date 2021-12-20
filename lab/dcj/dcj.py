import pulp


# pulp 的一个小 demo
def demoSolution():
    model = pulp.LpProblem("Demo", pulp.LpMaximize)

    # 变量
    A = pulp.LpVariable('A', lowBound=0, cat='Integer')
    B = pulp.LpVariable('B', lowBound=0, cat='Integer')
    C = pulp.LpVariable('C', lowBound=0, cat='Integer')

    # 目标函数
    model += 3 * A + 4 * B + 5 * C

    # 约束
    model += A + 2 * B <= 20
    model += B + 3 * C <= 40

    # 求解
    model.solve()
    print(pulp.LpStatus[model.status])

    # 打印目标函数的最大值
    print(pulp.value(model.objective))
    # 打印目标函数取得最大值时各变量的值（最优解）
    print(A.varValue, B.varValue, C.varValue)


# 需解决的问题
def solution():
    model = pulp.LpProblem("", pulp.LpMaximize)

    # 变量
    x_set, y_set, z_set = [[]], [0], [0]
    for i in range(1, 11):
        x_set.append([])
        for j in range(11, 21):
            # x[i][j] ∈ {0, 1}, 1 <= i <= 10 (S_1), 11 <= j <= 20 (S_2)
            x_set[i].append(pulp.LpVariable(f"x{i}.{j}", lowBound=0, upBound=1, cat=pulp.LpInteger))
    for i in range(1, 21):
        # 0 <= y[i] <= i, 1 <= i <= 20, y[i] is integer
        y_set.append(pulp.LpVariable(f"y{i}", lowBound=0, upBound=i, cat=pulp.LpInteger))
        # i * z[i] <= y[i], 1 <= i <= 20, z[i] is positive integer
        z_set.append(pulp.LpVariable(f"z{i}", lowBound=0, cat=pulp.LpInteger))
    print(y_set, z_set)

    # 目标函数
    objective = 0
    for z in z_set:
        objective += z
    model += objective

    # 约束
    # 1. 关于 x 的约束
    # for i in range(1, 11):
    #     for j in range(11, 21):
    #         model += x_set[i][j - 10] == 1
    # 2. 关于 y 的约束
    edges = [
        (1, 2), (3, 4), (5, 6), (7, 8), (9, 10),
        (11, 12), (13, 14), (15, 16), (17, 18), (19, 20)
    ]

    # 3. 关于 z 的约束：i * z[i] <= y[i]
    for i in range(1, 21):
        model += i * z_set[i] <= y_set[i]

    # 打印目标函数
    print(model.objective)
    print(model.constraints)


solution()

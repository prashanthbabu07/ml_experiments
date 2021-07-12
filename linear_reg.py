# %%
import numpy as np
from numpy.core.fromnumeric import transpose
from numpy.lib.function_base import gradient
# %%
# x0, x1, y
exp_sal = [[1, 2, 12], [1, 6, 11], [1, 5, 10], [
    1, 7, 9], [1, 10, 8], [1, 11, 6], [1, 12, 1]]
m = len(exp_sal)
# %%


def hypothesis(t0, t1, x):
    return t0 + t1 * x

# %%


nparray = np.asarray(exp_sal)
# %%

features = nparray[:, [0, 1]]
# %%

features_t = features.transpose()
# %%
thetas = [0, 0]


# %%

# sum([(predictions[i] - exp_sal[i][2])**2 for i in range(m)]) * 1 / (2 * m)

# %%
# training rate
a = 0.01

costs = []
for steps in range(1000):
    predictions = np.matmul(thetas, features_t)
    cost = sum([(predictions[i] - exp_sal[i][2]) **
               2 for i in range(m)]) * 1 / (2 * m)
    for j in range(len(thetas)):
        # temp = 0
        temp = thetas[j] - (a / m) * sum([(predictions[i] -
                                           exp_sal[i][2]) * features_t[j][i] for i in range(m)])
        thetas[j] = temp
        # print(temp)
    costs.append([thetas[0], thetas[1], cost])
# print(costs)

# %%
import matplotlib.pyplot as plt

linear_reg = [[x, hypothesis(thetas[0], thetas[1], x)] for x in range(20)]
plt.plot(nparray[:, [1, 1]], nparray[:, [2, 2]])
plt.plot([l[0] for l in linear_reg], [l[1] for l in linear_reg])

plt.plot([c[0] for c in costs], [c[2] for c in costs], '.', color="r")

plt.plot()
plt.ylabel('sal')
plt.xlabel('exp')
plt.show()
# %%


# %%

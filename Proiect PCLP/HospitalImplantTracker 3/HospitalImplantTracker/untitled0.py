import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

rng = np.random.RandomState(1)
x = 10 * rng.rand(50)
y = 2 * x - 5 + rng.randn(50)

fig, ax = plt.subplots()
ax.plot(x, y, 'ro')
ax.set_xlabel('x')
ax.set_ylabel('y')
plt.show()

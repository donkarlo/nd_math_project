import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# داده‌ها
x1 = [1, 2, 3, 4]
y1 = [1, 4, 9, 16]
z1 = [1, 1, 2, 3]

x2 = [1, 2, 3, 4]
y2 = [2, 3, 5, 7]
z2 = [2, 3, 3, 4]

# ساخت figure و axis سه‌بعدی
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# رسم
ax.scatter(x1, y1, z1)
ax.scatter(x2, y2, z2)

plt.show()
import matplotlib.pyplot as plt

# داده‌ها
x1 = [1, 2, 3, 4]
y1 = [1, 4, 9, 16]

x2 = [1, 2, 3, 4]
y2 = [2, 3, 5, 7]

fig = plt.figure()
ax = fig.add_subplot(111)

ax.scatter(x1, y1)
ax.scatter(x2, y2)

plt.show()
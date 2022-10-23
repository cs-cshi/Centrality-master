import matplotlib.pyplot as plt


def plot_2(x1, y1, x2, y2, label1, label2, x_label, y_label):
    plt.plot(x1, y1, color='r', linestyle='-', marker='^', linewidth=1, label=label1)
    plt.plot(x2, y2, color='b', linestyle='-', marker='s', linewidth=1, label=label2)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(color="k", linestyle=":")
    plt.legend([label1, label2])
    plt.show()


def plot_4(x1, y1, x2, y2, x3, y3, x4, y4, label1, label2, label3, label4, x_label, y_label):
    plt.plot(x1, y1, color='r', linestyle='-', marker='^', linewidth=1, label=label1)
    plt.plot(x2, y2, color='b', linestyle='-', marker='s', linewidth=1, label=label2)
    plt.plot(x3, y3, color='m', linestyle='-', marker='d', linewidth=1, label=label3)
    plt.plot(x4, y4, color='y', linestyle='-', marker='x', linewidth=1, label=label4)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.grid(color="k", linestyle=":")
    plt.legend([label1, label2, label3, label4])
    plt.show()
# import numpy as np
#
# x = np.arange(-1, 1, 0.1)
# y1 = np.exp(x)
# y2 = np.exp(2 * x)
# print(x)
# print(y1)
# print(y2)
#
# show(x, y1, x, y2, '3', '1', '1', '2')
#
# plt.show()

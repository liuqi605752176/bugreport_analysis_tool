import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import datetime

fig = plt.figure()
ax1 = fig.add_subplot(1, 1, 1)
plt.ylim(0, 22803616)


def animate(i):
    pullData = open("dump_meminfo.txt", "r").read()
    dataArray = pullData.split('\n')
    xar = []
    yar = []
    for eachLine in dataArray:
        if len(eachLine) > 1:
            x_time, y_total, y_free, y_cached = eachLine.split()
            if str(x_time).startswith("##"):
                continue
            xar.append(datetime.datetime.now())
            yar.append(y_free)
    ax1.clear()
    ax1.plot(xar, yar)


ani = animation.FuncAnimation(fig, animate, interval=500)
plt.show()

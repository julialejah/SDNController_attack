#https://towardsdatascience.com/plotting-live-data-with-matplotlib-d871fac7500b
#https://stackoverflow.com/questions/474528/what-is-the-best-way-to-repeatedly-execute-a-function-every-x-seconds
#Creates PDF file with performance graph of CPU and RAM
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import psutil
import collections
import sched, time
from datetime import datetime

s= sched.scheduler(time.time, time.sleep)

def my_function():
    #print("*entra*")
    #get data
    cpu.popleft()
    cpu.append(psutil.cpu_percent(interval=1))    
    ram.popleft()
    ram.append(psutil.virtual_memory().percent)
    #clear axis
    ax.cla()
    ax1.cla()
    #plot cpu
    ax.plot(cpu)
    ax.scatter(len(cpu)-1,cpu[-1]) 
    ax.text(len(cpu)-1,cpu[-1]+2, "{}%".format(cpu[-1]))   
    ax.set_ylim(0,100)
    #plot memory
    ax1.plot(ram)
    ax1.scatter(len(ram)-1,ram[-1])
    ax1.text(len(ram)-1,ram[-1]+2,"{}%".format(ram[-1]))
    ax1.set_ylim(0,100)
    s.enter(3,1,my_function)
    plt.savefig("fig_performance/fig"+str(datetime.timestamp(datetime.now()))+".pdf")




cpu = collections.deque(np.zeros(100))
ram = collections.deque(np.zeros(100))
#print("CPU: {}".format(cpu))
#print("Memory: {}".format(ram))
#my_function()
#my_function()
#my_function()
#print("CPU: {}".format(cpu))
#print("Memory: {}".format(ram))
# define and adjust figure
fig = plt.figure(figsize=(12,6), facecolor='#DEDEDE')
ax = plt.subplot(121)
ax1 = plt.subplot(122)
ax.set_facecolor('#DEDEDE')
ax1.set_facecolor('#DEDEDE')
# test
s.enter(3,1,my_function)

s.run()

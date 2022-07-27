import random
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

def plot(data):
    sns.distplot(data)
    plt.title('Mean: ' + str(np.mean(data)) + '\n' +
              'Min: ' + str(np.min(data)) + '\n' +
              'Max: ' + str(np.max(data)) + '\n' +
              '50%: ' + str(sorted(data)[len(data)//2]) + '\n' +
              '90%: ' + str(sorted(data)[int(len(data)*0.9)]))
    plt.show()

if __name__ == '__main__':
    with open('./hbase/v2/year_2001_bloom_cache.txt', 'r') as file:
        time_list = file.readline()
    plot(eval(time_list))
import json
import matplotlib.pyplot as plt
from scipy import misc
from pylab import *
from os import listdir
from os.path import isfile, join


def draw_picture(json_name_1,json_name_2):
    json_file_1 = open(json_name_1)
    datas_1 = json.load(json_file_1)    # 第一个文件数据
    json_file_2 = open(json_name_2)
    datas_2 = json.load(json_file_2)    # 第二个文件数据
    types = []
    for data in datas_1:
        if not data['type'] in types:
            types.append(data['type'])
    for type in types:  # 对文件中按type作图
        draw_point(datas_1, datas_2, type)

def draw_point(datas_1, datas_2, type):
    plt.figure()
    num_total = []
    time_total = []
    for data in datas_1:
        if data['type'] == type:
            num = data['num']
            time = data['time']
            new_num = num / 10000
            num_total.append(new_num)
            time_total.append(time)
    plt.plot(num_total, time_total, label='Mongodb Test', linewidth=3, color='k', marker='o',
                 markerfacecolor='red', markersize=8)
    plt.grid(axis='y')
    # 设置数字标签
    for a, b in zip(num_total, time_total):
        plt.text(a, b + 0.001, '%.4f' % b, ha='center', va='bottom', fontsize=9)

    num_total = []
    time_total = []
    for data in datas_2:
        if data['type'] == type:
            num = data['num']
            time = data['time']
            new_num = num / 10000
            num_total.append(new_num)
            time_total.append(time)
    plt.plot(num_total, time_total, label='Mysql Test', linewidth=3, color='r', marker='s',
             markerfacecolor='blue', markersize=8)
    plt.grid(axis='y')
    # 设置数字标签
    for a, b in zip(num_total, time_total):
        plt.text(a, b + 0.001, '%.4f' % b, ha='center', va='bottom', fontsize=9)

    plt.title(type) # 标题
    plt.xlabel("Data Size") # 横轴
    plt.ylabel("Time(s)")  # 纵轴
    plt.axis([0,10,0,8])  # 设置区间
    scale_x = range(1,11)
    index_x = ['10k', '20k', '30k', '40k', '50k', '60k', '70k','80k','90k','100k']
    plt.xticks(scale_x, index_x)
    # 第一个参数是点的位置，第二个参数是点的文字提示
    plt.yticks([0, 2, 4, 6, 8])
    plt.legend()

    plt.savefig(type+'.png')
    plt.show()


if __name__ == '__main__':
    # 测试数据
    json_name_1 = 'mongodb.json'
    json_name_2 = 'mysql.json'
    draw_picture(json_name_1,json_name_2)

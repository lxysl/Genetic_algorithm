from PIL import Image
import os
import math
import random
import pickle
from copy import deepcopy
from matplotlib import pyplot as plt


# 读取图像
def GetImage(ori_img):
    img = Image.open(ori_img)
    color = []
    width, height = img.size
    for j in range(height):
        temp = []
        for i in range(width):
            r, g, b = img.getpixel((i, j))[:3]
            temp.append([r, g, b, r + g + b])
        color.append(temp)
    # color：三维数组，第一维列表包含r,g,b,r+g+b四个值，第二维表示行，第三维表示列
    return color, img.size


# 初始化
def RandGenes(size, target):
    width, height = size
    genes = []
    for i in range(100):
        gene = []
        for j in range(height):
            temp = []
            for k in range(width):
                t_r, t_g, t_b, t_a = target[j][k]
                r = random.randint(0, 255)
                g = random.randint(0, 255)
                b = random.randint(0, 255)
                a = abs(t_r - r) + abs(t_g - g) + abs(t_b - b)
                temp.append([r, g, b, a])
            gene.append(temp)
        genes.append([gene, 0])
    # genes：三维数组，[[基因],适应度]，基因：[[每行]]，每行：[[每列]]，每列：[r,g,b,rgb总差值]
    return genes


# 计算适应度
def CalcFitness(genes, target):
    total = 0
    for k, gene in enumerate(genes):
        count = 0
        for i, row in enumerate(gene[0]):
            for j, col in enumerate(row):
                t_r, t_g, t_b, t_a = target[i][j]
                r, g, b, a = col
                a = abs(t_r - r) + abs(t_g - g) + abs(t_b - b)
                count += a
        genes[k][1] = count
        total += count
    genes.sort(key=lambda x: x[1])
    return genes


# 总体变异
def Variation(genes, target):
    for k, gene in enumerate(genes):
        genes[k] = AltOffspring(genes[k], target)
    return genes


# 个体变异
def SelfVariation(parent, t_r, t_g, t_b):
    # 较大变异，概率较小
    max_mutate_rate = 0.05
    mid_mutate_rate = 0.2
    # 较小变异，概率较大
    min_mutate_rate = 0.5
    offspring = deepcopy(parent)
    if random.random() < max_mutate_rate:
        offspring[0] = random.randint(0, 255)
    if random.random() < max_mutate_rate:
        offspring[1] = random.randint(0, 255)
    if random.random() < max_mutate_rate:
        offspring[2] = random.randint(0, 255)

    if random.random() < mid_mutate_rate:
        offspring[0] = min(max(0, offspring[0] + random.randint(-30, 30)), 255)
    if random.random() < mid_mutate_rate:
        offspring[1] = min(max(0, offspring[1] + random.randint(-30, 30)), 255)
    if random.random() < mid_mutate_rate:
        offspring[2] = min(max(0, offspring[2] + random.randint(-30, 30)), 255)

    if random.random() < min_mutate_rate:
        offspring[0] = min(max(0, offspring[0] + random.randint(-10, 10)), 255)
    if random.random() < min_mutate_rate:
        offspring[1] = min(max(0, offspring[1] + random.randint(-10, 10)), 255)
    if random.random() < min_mutate_rate:
        offspring[2] = min(max(0, offspring[2] + random.randint(-10, 10)), 255)

    offspring[3] = abs(offspring[2] - t_b) + abs(offspring[1] - t_g) + abs(offspring[0] - t_r)
    return offspring


# 子代父代最优取代
def AltOffspring(gene, target):
    for i, row in enumerate(gene[0]):
        for j, parent in enumerate(row):
            p_r, p_g, p_b, p_a = parent
            t_r, t_g, t_b, t_a = target[i][j]
            offsprings = []
            for k in range(5):
                offsprings.append(SelfVariation(parent, t_r, t_g, t_b))
            offsprings.sort(key=lambda x: x[3])
            gene[0][i][j] = offsprings[0] if offsprings[0][3] < p_a else parent
    return gene


# # 交叉
# def Merge(gene1, gene2, size):
#     width, height = size
#     y = random.randint(0, width - 1)
#     x = random.randint(0, height - 1)
#     new_gene = deepcopy(gene1[0][:x])
#     new_gene = [new_gene, 0]
#     new_gene[0][x:] = deepcopy(gene2[0][x:])
#     new_gene[0][x][:y] = deepcopy(gene1[0][x][:y])
#     return new_gene


# # 自然选择
# def Select(genes, size):
#     seek = len(genes) * 2 // 3
#     i = 0
#     j = seek + 1
#     # 将后1/3的基因替换为前2/3基因的两两交叉
#     while i < seek:
#         genes[j] = Merge(genes[i], genes[i + 1], size)
#         j += 1
#         i += 2
#     return genes


# 保存生成的图片
def SavePic(genes, generation, ori_img):
    evaluation = ['优', '中', '差']
    for k, genek in enumerate(genes):
        gene = genek[0]
        img = Image.open(ori_img)
        for j, row in enumerate(gene):
            for i, col in enumerate(row):
                r, g, b, _ = col
                img.putpixel((i, j), (r, g, b))
        img.save("{}.png".format(str(generation) + evaluation[k]))


def SavePlotData(genes, generation, plotdata):
    fitnessSum = 0
    for i in range(100):
        fitnessSum += genes[i][1]
    plotdata[0].append(genes[0][1])
    plotdata[1].append(genes[99][1])
    plotdata[2].append(fitnessSum / 100)
    plotdata[3].append(generation)
    plt.plot(plotdata[3], plotdata[0], color='red', label='best')
    plt.plot(plotdata[3], plotdata[1], color='green', label='worst')
    plt.plot(plotdata[3], plotdata[2], color='blue', linestyle='--', label='average')
    plt.xlabel('generation')
    plt.ylabel('fitness')
    plt.savefig('{}.png'.format('fitness' + str(generation)))
    plt.show()


# 备份
def SaveData(data, backup):
    print('[INFO]: Save data to {}...'.format(backup))
    with open(backup, 'wb') as f:
        pickle.dump(data, f)
    f.close()


# 读取备份
def ReadData(backup):
    print('[INFO]: Read data from {}...'.format(backup))
    with open(backup, 'rb') as f:
        data = pickle.load(f)
        genes = data['genes']
        generation = data['generation']
    f.close()
    return genes, generation


# 运行
def run(ori_img, backup, plotdata, resume=False):
    data, size = GetImage(ori_img)
    if resume:
        genes, generation = ReadData(backup)
    else:
        genes = RandGenes(size, data)
        generation = 0
    while True:
        genes = Variation(genes, data)
        genes = CalcFitness(genes, data)
        # genes = Select(genes, size)
        generation += 1
        if generation % 10 == 0:
            SaveData({'genes': genes, 'generation': generation}, backup)
            SavePic([genes[0], genes[50], genes[99]], generation, ori_img)
            SavePlotData(genes, generation, plotdata)
        print('<Generation>: {}, <Select3>: {:.4f} {:.4f} {:.4f}'.format(generation, genes[0][1], genes[50][1],
                                                                         genes[99][1]))


if __name__ == '__main__':
    # 备份
    backup = 'backup.tmp'
    # 原始图像
    ori_img = './test.png'
    # 折线图数据[优，差，均，代]
    plotdata = [[], [], [], []]
    # resume为True则读取备份文件，在其基础上进行自然选择和变异
    run(ori_img, backup, plotdata, resume=False)

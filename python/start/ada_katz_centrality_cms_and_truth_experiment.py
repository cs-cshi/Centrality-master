import sys

sys.path.append('..')
from simulator.graph_simulator import *
from experiments.experiments import *
from experiments.experiments import AdaWithCountMinAndMemoryDictCompareExperiment
from experiments.experiments import AdaWithCountSketchAndMemoryDictCompareExperiment
from experiments.experiments import MinHeapTopKExperiment
from experiments.experiments import TemporalTimeAdaKatzCompareExperiment

# norm，beta，base共同决定了时间衰减幅度
# base = 1.1
# norm = 0.00000001，即时间窗口，太大会math error
# 对于tennis.csv而言，1495576813-1497570221,norm 取 0.00001~0.0001时有意义
# cm_sketch_size = 1024
# beta需小于最大特征值的倒数，不同数据集对应最佳取值均不同，详情见论文


beta = 0.01
# base = 2.718281828459
# base = 1.015
# base = 1.115 最佳
base = 1.115
# 1994个时间切片，较细粒度
norm = 0.000001
k = 100
sketch_size = 8192
ada_exp = True

# cm
ex = AdaWithCountMinAndMemoryDictCompareExperiment(k, beta, base, norm, sketch_size, ada_exp)

# cs
# ex = AdaWithCountSketchAndMemoryDictCompareExperiment(k, beta, base, norm, sketch_size)

# k = 200
# beta = 0.2
# base = 2.0
# norm = 0.0001
# output_path = '../../data/rg17_data/centrality_measures/'
# 不用sketch 观察使用了加权/去加权后的效果
# ex = MinHeapTopKExperiment(k, beta, base, norm)

data_path = '../../data/rg17_data/raw/rg17_mentions.csv'
# data_path = '../../data/maccdc2012_00000——.flows'
# data_path = '../../data/botnet-capture-20110815-fast-flux-2.flows'
# data_path = '../../data/equinix-chicago.dirA.20160121-125911.UTC.anon3_test.flows'
# data_path = 'equinix-chicago.dirA.20160121-125911.UTC.anon1.flows'

simulator = OnlineGraphSimulator(data_path)
simulator.simulate(ex)

# 目前实验结果比较好的一组数据
# jaccard similarity: 0.941747572815534
# 相对误差也很小
# k = 100
# beta = 0.01
# base = 2.7
# norm = 0.1
# cm_sketch_size = 1024

# 求矩阵的最大特征值
# import numpy as np
# A = np.array([],[])
# lamda = np.linalg.eig(A)
# index = np.argmax(lamda[0])
# lamda_max = np.real(lamda[0][index])

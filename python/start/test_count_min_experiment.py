from sketch_utils.sketches import *
from plot_util.plot_utils import *
import random

data = []
for i in range(10000):
    data.append(random.randint(0, 1000))

data_set = set(data)
print(len(data))
print(len(data_set))

truth_count = {}
for i in range(len(data)):
    value = truth_count.get(data[i], 0)
    truth_count[data[i]] = value + 1

truth_res = []
for k in data_set:
    truth_res.append((k, truth_count[k]))

cms = CountMinSketch(256)

for i in range(len(data)):
    cms.set_value(data[i], 1)

cms_res = []
for k in data_set:
    cms_res.append((k, cms.get_value(k)))

print('truth_res:')
print(truth_res)
print('cms_res:')
print(cms_res)
truth_res = sorted(truth_res, key=lambda x: x[1], reverse=True)
cms_res = sorted(cms_res, key=lambda x: x[1], reverse=True)
truth_x = [x for x in range(len(truth_res))]
truth_y = [x[1] for x in truth_res]
cms_x = [x for x in range(len(truth_res))]
cms_y = [x[1] for x in cms_res]
plot_2(truth_x, truth_y, cms_x, cms_y, 'truth', 'cms', 'item', 'count')

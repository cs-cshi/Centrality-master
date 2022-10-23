from data_process.data_process import *

data_path = '../../data/SAT-03-11-2018_0.flows'
new_data_path = '../../data/SAT-03-11-2018_0_cleaned.flows.flows'
clean_ipv6(data_path, new_data_path)
# copy(data_path, new_data_path)
print('ok')

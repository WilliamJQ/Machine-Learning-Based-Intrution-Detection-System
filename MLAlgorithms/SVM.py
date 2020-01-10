import DataProcessor as dp
from multiprocessing import Process



# 文件夹路径
data_loc_path = '/Users/zhongwentao/Desktop/毕业设计/训练数据'
file_name = 'kddcup_10_percent'
# file_name = 'debug_used_data'
# 转换数据
# p = Process(target=dp.read_file_to_csv, args=[data_loc_path, '{}.txt'.format(file_name), '{}.csv'.format(file_name)])
dp.read_file_to_csv(data_loc_path, '{}.txt'.format(file_name), '{}.csv'.format(file_name))
# p.start()
# p.join()
print("读取成功")

# process data
file_path = dp.get_file_path(data_loc_path, file_name, 'txt')
data = dp.process_data(file_path)

# 通过特征选择删除多余特征
data, feature_new = dp.recursive_feature_elimination(data)
data.to_csv('{}/debug_data_output.csv'.format(data_loc_path), columns=None, index=False)
print("完成")















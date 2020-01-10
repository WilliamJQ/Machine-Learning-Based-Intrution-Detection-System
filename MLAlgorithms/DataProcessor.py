import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.feature_selection import RFECV
from sklearn.model_selection import StratifiedKFold
from sklearn.svm import SVC

col_names = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", "land",
    "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in", "num_compromised",
    "root_shell", "su_attempted", "num_root", "num_file_creations", "num_shells", "num_access_files",
    "num_outbound_cmds", "is_host_login", "is_guest_login", "count", "srv_count", "serror_rate",
    "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate", "diff_srv_rate",
    "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate",
    "dst_host_diff_srv_rate", "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate",
    "dst_host_serror_rate", "dst_host_srv_serror_rate", "dst_host_rerror_rate", "dst_host_srv_rerror_rate", "label"]
protocol_type_list = ['tcp', 'udp', 'icmp']
service_list = ['aol', 'auth', 'bgp', 'courier', 'csnet_ns', 'ctf', 'daytime', 'discard', 'domain', 'domain_u',
                'echo', 'eco_i', 'ecr_i', 'efs', 'exec', 'finger', 'ftp', 'ftp_data', 'gopher', 'harvest',
                'hostnames','http', 'http_2784', 'http_443', 'http_8001', 'imap4', 'IRC', 'iso_tsap', 'klogin', 'kshell',
                'ldap', 'link', 'login', 'mtp', 'name', 'netbios_dgm', 'netbios_ns', 'netbios_ssn', 'netstat', 'nnsp',
                'nntp', 'ntp_u', 'other', 'pm_dump', 'pop_2', 'pop_3', 'printer', 'private', 'red_i', 'remote_job', 'rje',
                'shell', 'smtp', 'sql_net', 'ssh', 'sunrpc', 'supdup', 'systat', 'telnet', 'tftp_u', 'tim_i', 'time',
                'urh_i', 'urp_i', 'uucp', 'uucp_path', 'vmnet', 'whois', 'X11', 'Z39_50']
flag_list = ['OTH', 'REJ', 'RSTO', 'RSTOS0', 'RSTR', 'S0', 'S1', 'S2', 'S3', 'SF', 'SH']
label_list = ['normal.', 'buffer_overflow.', 'loadmodule.', 'perl.', 'neptune.', 'smurf.',
              'guess_passwd.', 'pod.', 'teardrop.', 'portsweep.', 'ipsweep.', 'land.', 'ftp_write.',
              'back.', 'imap.', 'satan.', 'phf.', 'nmap.', 'multihop.', 'warezmaster.', 'warezclient.',
              'spy.', 'rootkit.']


# 获取文件路径
def get_file_path(data_loc_path, file_name, file_type):
    return '{}/{}.{}'.format(data_loc_path, file_name, file_type)


# 将读入的数据存取为csv文件
def read_file_to_csv(data_loc_path, from_file_name, to_file_name):
    from_path = data_loc_path + '/{}'.format(from_file_name)
    to_path = data_loc_path + '/{}'.format(to_file_name)
    print("# 开始读取文件")
    data = pd.read_csv(from_path, header=None, names=col_names)
    print(data[:2])
    print("# 成功读取文件，开始转换为CSV")
    data.to_csv(to_path, columns=None, index=False)
    print("# 转换完成")


# 查找字符串在数组中的下标
def find_index(string, array):
    for i in range(len(array)):
        if string == array[i]:
            return i


# 数据标准化计算
def compute_regression_value(val, std, mean):
    if std == 0 or mean == 0:
        return 0
    return (val - mean) / std


# 数据归一化计算
def compute_normalization_value(val, min_val, max_val):
    if min_val == max_val or val == min_val:
        return 0
    return (val - min_val) / (max_val - min_val)


# 数据处理
def process_data(file_path):
    # 读取数据
    data_frame = pd.read_csv(file_path)
    data_num = data_frame.shape[0]
    # 将dataFrame转换为list
    print("# 准备开始数据无量纲化")
    data_list = data_frame.values.tolist()
    '''
        1.数据无量纲化：
        将数据类型统一以便后续操作
    '''
    print("# 准备完成, 开始数据无量纲化")
    # 遍历数组将字符改为数值
    for idx in range(len(data_list)):
        row = data_list[idx]
        # 将数据中字符转化为数字
        row[1] = find_index(row[1], protocol_type_list)
        row[2] = find_index(row[2], service_list)
        row[3] = find_index(row[3], flag_list)
        row[41] = find_index(row[41], label_list)
        print("## 已完成{}%".format((idx / data_num) * 100))

    print("# 数据无量纲化完成, 正在处理数据...")
    # 转化为DataFrame
    data_frame = pd.DataFrame(data_list, columns=col_names)
    print("# 数据处理完成")
    print(data_list[:3])

    '''
        2.数据标准化
        x' = [x-mean(x)] / std(x)
        
        ** 此处理需要将最后一列排除 **
    '''
    print("# 准备开始数据标准化")
    # 计算每一列的标准差
    std = data_frame.std(axis='rows').tolist()
    # 计算每一列的均值
    mean = data_frame.mean(axis='rows').tolist()
    # 将dataFrame转换为list
    data_list = data_frame.values.tolist()
    print("# 准备完成, 开始数据标准化")
    # 遍历数组并计算
    for idx in range(len(data_list)):
        row = data_list[idx]
        for col_idx in range(len(row)-1):
            row[col_idx] = abs(compute_regression_value(row[col_idx], std[col_idx], mean[col_idx]))
        print("## 已完成{}%".format((idx / data_num) * 100))

    print("# 数据标准化完成, 正在处理数据...")
    data_frame = pd.DataFrame(data_list, columns=col_names)
    print("# 处理完成")
    '''
        3.数据归一化
        x' = (x-x_min) / (x_max-x_min)
        
        ** 此处理需要将最后一列排除 **
    '''
    # 计算每一列的最小值和最大值
    print("# 准备开始数据归一化")
    min_val = data_frame.min(axis='rows').tolist()
    max_val = data_frame.max(axis='rows').tolist()
    data_list = data_frame.values.tolist()
    print("# 准备完成, 开始数据归一化")
    for idx in range(len(data_list)):
        row = data_list[idx]
        for col_idx in range(len(row)-1):
            row[col_idx] = compute_normalization_value(row[col_idx], min_val[col_idx], max_val[col_idx])
        print("## 已完成{}%".format((idx / data_num) * 100))
    print("# 数据归一化完成, 正在处理数据...")
    data_frame = pd.DataFrame(data_list, columns=col_names)
    print("# 处理完成")
    return data_frame


# 特征选择(递归消除法)
def recursive__feature_elimination(data_frame):
    # 获取X和y的特征名
    x_col_names = col_names
    x_col_names.remove("label")
    y_col_name = "label"
    # 把data分割成X和y
    X = data_frame[x_col_names]
    y = data_frame[y_col_name]
    model = SVC(kernel="linear")
    rfe = RFECV(estimator=model, step=1, cv=StratifiedKFold(3))
    rfe = rfe.fit(X, y)
    print(rfe.ranking_)



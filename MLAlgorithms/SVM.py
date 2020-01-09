import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
global label_list
global data_num

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
service_list=['aol', 'auth', 'bgp', 'courier', 'csnet_ns', 'ctf', 'daytime', 'discard', 'domain', 'domain_u',
                 'echo', 'eco_i', 'ecr_i', 'efs', 'exec', 'finger', 'ftp', 'ftp_data', 'gopher', 'harvest', 'hostnames',
                 'http', 'http_2784', 'http_443', 'http_8001', 'imap4', 'IRC', 'iso_tsap', 'klogin', 'kshell', 'ldap',
                 'link', 'login', 'mtp', 'name', 'netbios_dgm', 'netbios_ns', 'netbios_ssn', 'netstat', 'nnsp', 'nntp',
                 'ntp_u', 'other', 'pm_dump', 'pop_2', 'pop_3', 'printer', 'private', 'red_i', 'remote_job', 'rje', 'shell',
                 'smtp', 'sql_net', 'ssh', 'sunrpc', 'supdup', 'systat', 'telnet', 'tftp_u', 'tim_i', 'time', 'urh_i', 'urp_i',
                 'uucp', 'uucp_path', 'vmnet', 'whois', 'X11', 'Z39_50']
flag_list=['OTH', 'REJ', 'RSTO', 'RSTOS0', 'RSTR', 'S0', 'S1', 'S2', 'S3', 'SF', 'SH']
label_list=['normal.', 'buffer_overflow.', 'loadmodule.', 'perl.', 'neptune.', 'smurf.',
    'guess_passwd.', 'pod.', 'teardrop.', 'portsweep.', 'ipsweep.', 'land.', 'ftp_write.',
    'back.', 'imap.', 'satan.', 'phf.', 'nmap.', 'multihop.', 'warezmaster.', 'warezclient.',
    'spy.', 'rootkit.']


# 将读入的数据存取为csv文件
def read_file_to_csv(read_path, to_path):
    print("# 开始读取文件")
    data = pd.read_csv(read_path)
    print(data[:2])
    print("# 成功读取文件，开始转换为CSV")
    data.to_csv(to_path)
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


# 数据处理
def process_data(data):
    # 将dataFrame转换为list
    data_list = data.values.tolist()
    '''
        1.数据无量纲化：
        将数据类型统一以便后续操作
    '''
    print("#开始数据无量纲化")
    # 遍历数组将字符改为数值
    for row in data_list:
        # 将数据中字符转化为数字
        row[1] = find_index(row[1], protocol_type_list)
        row[2] = find_index(row[2], service_list)
        row[3] = find_index(row[3], flag_list)
        row[41] = find_index(row[41], label_list)

    # 转化为DataFrame
    df = pd.DataFrame(data_list, columns=col_names)
    print(data_list[:3])
    print("# 数据无量纲化完成")

    '''
        2.数据标准化
        x' = [x-mean(x)] / std(x)
    '''
    print("# 开始数据标准化")
    # 计算每一列的标准差
    std = df.std(axis='rows').tolist()
    # 计算每一列的均值
    mean = df.mean(axis='rows').tolist()
    # 将dataFrame转换为list
    data_list = df.values.tolist()
    # 遍历数组并计算
    for idx in range(len(data_list)):
        row = data_list[idx]
        for col_idx in range(len(row)):
            row[col_idx] = abs(compute_regression_value(row[col_idx], std[col_idx], mean[col_idx]))
        print("## 已完成{}%".format((idx/data_num) * 100))

    print("# 数据标准化完成")
    df = pd.DataFrame(data_list, columns=col_names)
    return df


# load data
data = pd.read_csv('training_datas/kddcup_data.csv')
data_num = data.shape[0]
# print(data_num)
# 处理数据
data = process_data(data)










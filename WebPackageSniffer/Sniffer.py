import pcap
import dpkt
import socket


def inet_to_str(inet):
    try:
        return socket.inet_ntop(socket.AF_INET, inet)
    except ValueError:
        return socket.inet_ntop(socket.AF_INET6, inet)


# 解析IP数据包
def resolve_ip_packet():
    eth = dpkt.ethernet.Ethernet(buffer)
    # 分离出IP数据包
    ip = eth.data
    # 解析IP数据包
    do_not_fragment = bool(ip.off & dpkt.ip.IP_DF)
    more_fragments = bool(ip.off & dpkt.ip.IP_MF)
    fragment_offset = ip.off & dpkt.ip.IP_OFFMASK
    # 打印数据包信息
    print("IP: %s -> %s (len=%d, ttl=%d, DF=%d, MF=%d, offset=%d)\n" % (
        inet_to_str(ip.src),
        inet_to_str(ip.dst),
        ip.len,
        ip.ttl,
        do_not_fragment,
        more_fragments,
        fragment_offset))
    # 服务类型(Type Of Service)
    print(ip.tos)
    # 协议类型(Protocol）
    print(ip.p)
    # help(ip)
    print(ip.data.data)


sniffer = pcap.pcap(name=None, promisc=True, immediate=True, timeout_ms=50)
for (time_stamp, buffer) in sniffer:
    try:
        resolve_ip_packet()

    except:
        print("--------------")
        llc = dpkt.llc.LLC(buffer)
        print(llc)

        pass






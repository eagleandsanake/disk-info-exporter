from prometheus_client import Gauge
import psutil

# Create Prometheus Gauges
disk_usage_gauge = Gauge('disk_usage_bytes', 'Disk usage in bytes', ['device', 'mount_point', 'type'])

used_info_index = ["total", "used", "free", "percent"]


# 获取所有的磁盘信息
def get_all_disk_partitions():
    return psutil.disk_partitions(all=True)


# 获取各个分区的使用量
def get_disk_usage(partition) -> map:
    usage = psutil.disk_usage(partition.mountpoint)
    return {
        "device": partition.device,
        "mount_point": partition.mountpoint,
        used_info_index[0]: usage.total,
        used_info_index[1]: usage.used,
        used_info_index[2]: usage.free,
        used_info_index[3]: usage.percent
    }


def do_collect():
    # 磁盘使用信息
    disk_all = get_all_disk_partitions()
    for disk in disk_all:
        used_info = dict(get_disk_usage(disk))
        for index in used_info_index:
            disk_usage_gauge.labels(
                device=disk.device,
                mount_point=disk.mountpoint,
                type=index
            ).set(used_info.get(index))


if __name__ == "__main__":
    print(list(map(lambda ele: get_disk_usage(ele), get_all_disk_partitions())))
    # do_collect()
    # print(disk_usage_gauge)
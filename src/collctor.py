from prometheus_client import Gauge
import psutil

# Create Prometheus Gauges
disk_usage_gauge = Gauge('disk_usage_bytes', 'Disk usage in bytes', ['device', 'mount_point', 'type'])
io_disk_usage_gauge = Gauge('io_disk_usage_bytes', 'Disk usage in bytes', ['device', 'type'])

used_info_index = ["total", "used", "free", "percent"]
io_used_info_index = ["read_count", "write_count", "read_bytes", "write_bytes", "read_time", "write_time"]


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
        try:
            used_info = dict(get_disk_usage(disk))
            for index in used_info_index:
                disk_usage_gauge.labels(
                    device=disk.device,
                    mount_point=disk.mountpoint,
                    type=index
                ).set(used_info.get(index))
        except PermissionError:
            print(f"当前设备无权限获取{disk.device}")
            continue
    # 获取写入写出量
    io_used_info = psutil.disk_io_counters(perdisk=True)
    for disk_mame, used_info in io_used_info.items():
        for index in io_used_info_index:
            io_disk_usage_gauge.labels(
                device=disk_mame,
                type=index
            ).set(getattr(used_info, index))


if __name__ == "__main__":
    print(list(map(lambda ele: get_disk_usage(ele), get_all_disk_partitions())))
    # print(psutil.disk_io_counters(perdisk=True))
    # do_collect()
    # print(disk_usage_gauge)

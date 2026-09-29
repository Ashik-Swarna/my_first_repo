
import shutil
import subprocess

THRESHOLD = 80


def get_cpu_usage():
    result = subprocess.run(
        ["top", "-bn2", "-d", "1"],
        capture_output=True,
        text=True,
        check=True
    )

    cpu_lines = [
        line for line in result.stdout.splitlines()
        if "Cpu(s)" in line
    ]

    idle = float(
        cpu_lines[-1].split("id")[0].split(",")[-1].strip()
    )
    return 100 - idle


def get_memory_usage():
    with open("/proc/meminfo") as file:
        memory = {}
        for line in file:
            key, value = line.split(":")
            memory[key] = int(value.strip().split()[0])

    total = memory["MemTotal"]
    available = memory["MemAvailable"]

    return (total - available) / total * 100


def get_disk_usage():
    disk = shutil.disk_usage("/")
    return disk.used / disk.total * 100


def check_health(name, usage):
    print(f"{name}: {usage:.2f}%")

    if usage > THRESHOLD:
        print(f"WARNING: High {name} usage!")
    else:
        print(f"{name} is healthy.")


print("===== SERVER HEALTH REPORT =====")

check_health("CPU", get_cpu_usage())
check_health("Memory", get_memory_usage())
check_health("Disk", get_disk_usage())

print("===== MONITORING COMPLETED =====")

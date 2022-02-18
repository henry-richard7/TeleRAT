import platform
import psutil


class system_info:
    my_system = platform.uname()
    gigabyte = float(1024 * 1024 * 1024)

    mem = psutil.virtual_memory()
    mem_total = float(mem.total / gigabyte)
    mem_free = float(mem.free / gigabyte)
    mem_used = float(mem.used / gigabyte)

    hdd = psutil.disk_usage("/")
    HDD_total = hdd.total / gigabyte
    HDD_Used = hdd.used / gigabyte
    HDD_Free = hdd.free / gigabyte

    def get_system(self):
        return self.my_system.system

    def get_system_name(self):
        return self.my_system.node

    def get_system_release(self):
        return self.my_system.release

    def get_system_version(self):
        return self.my_system.version

    def get_system_machine(self):
        return self.my_system.machine

    def get_system_processor(self):
        return self.my_system.processor

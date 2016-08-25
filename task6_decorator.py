# Program which monitoring system & create system

import psutil
import schedule
import datetime
import json
import configparser

# For clean outlogs file
clear_json_file = open("outlog.json", "a")
clear_json_file.close()
clear_txt_file = open("outlog.txt", "a")
clear_txt_file.close()
clear_dec_log = open("outlog.decorator", "a")
clear_dec_log.close()

# For config file
config = configparser.ConfigParser()
config.read('conf6.ini')
output_type = config.get('common', 'type')
interval = config.get('common', 'interval')
decorswitch = config.getboolean('common', 'decorswitch')


# Create decorator
def tracer (dec_func):
    def wrapper(*args, **kwargs):
        print("Decarator work before")
        func = open('outlog.decorator', "a")
        func.write('Entered:{0}, {1}, {2}\n'.format(dec_func.__name__, str(args), str(kwargs)))
        func.write('snapshot:{}\n'.format(GetStat.snapshot))
        dec_func(*args, **kwargs)
        func.write('Exit:{}\n'.format(dec_func.__name__))
        func.write("\n")
        func.close()
        # dec_func()
        print("Decarator work after")
    return wrapper if decorswitch else dec_func


# Parrent class which collected statistics
class GetStat:
    snapshot = 1  # counter of snapshots
    def __init__(self):
        self.time = datetime.datetime.strftime(datetime.datetime.now(),	'%Y-%m-%d-%H:%M:%S')
        self.cpu_st = psutil.cpu_percent(interval=1, percpu=True)
        self.memory_total_st = (psutil.disk_usage('/')[0] / 1048576).__round__(2)
        self.memory_pers_st = psutil.disk_usage('/')[3]
        self.ram_pers_st = psutil.virtual_memory()[2]
        self.hdd_read_st = (psutil.disk_io_counters()[2] / 1048576).__round__(2)
        self.hdd_write_st = (psutil.disk_io_counters()[3] / 1048576).__round__(2)
        self.net_sent_st = (psutil.net_io_counters()[0] / 1048576).__round__(2)
        self.net_rec_st = (psutil.net_io_counters()[1] / 1048576).__round__(2)


# Class for writing statistics to outlog.txt
class WriteTxt(GetStat):
    @tracer
    def write_txt(self):
        file_var = open('outlog.txt', "a")
        file_var.write("Snapshot{0}:{1}\n".format(GetStat.snapshot, self.time))
        # cpu_st
        file_var.write('CPU usage:{}%\n'.format(self.cpu_st))
        # memory_total_st
        file_var.write('Memory usage: Total:{}Mb\n'.format(self.memory_total_st))
        # memory_pers_st
        file_var.write('Memory usage: Percent free:{}%\n'.format(self.memory_pers_st))
        # ram_pers_st
        file_var.write('RAM usage: Percent free:{}%\n'.format(self.ram_pers_st))
        # hdd_read_st
        file_var.write('Disk IO usage: read: {}Mb\n'.format(self.hdd_read_st))
        # hdd_write_st
        file_var.write('Disk IO usage: write:{}Mb\n'.format(self.hdd_write_st))
        # net_sent_st
        file_var.write('Network usage: sent:{}Mb\n'.format(self.net_sent_st))
        # net_rec_st
        file_var.write('Network usage: receive:{}Mb\n'.format(self.net_rec_st))
        file_var.write("\n")
        file_var.close()
        GetStat.snapshot += 1


# Class for writing statistics to outlog.json
class WriteJson(GetStat):
    @tracer
    def write_json(self):
        # global snapshot
        self.time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H:%M:%S')
        snap_create = {
            'CPU usage:': self.cpu_st,
            'Memory usage: Total:': str(self.memory_total_st) + "Mb",
            'Memory usage: Percent free:': str(self.memory_pers_st) + "%",
            'RAM usage: Percent free:': str(self.ram_pers_st) + "%",
            'Disk IO usage: read:': str(self.hdd_read_st) + "Mb",
            'Disk IO usage: write:': str(self.hdd_write_st) + "Mb",
            'Network usage: sent:': str(self.net_sent_st) + "Mb",
            'Network usage: receive:': str(self.net_rec_st) + "Mb"
            }
        data = ('SNAPSHOT' + str(GetStat.snapshot) + ": " + str(self.time) + ": ", snap_create)
        with open("outlog.json", "a") as file_var:
            json.dump(data, file_var, indent=3, sort_keys=True)
            GetStat.snapshot += 1


def rtxt():
    objt = WriteTxt()
    objt.write_txt()
def rjson():
    objj = WriteJson()
    objj.write_json()

#def running():
    #objt = WriteTxt()
    #objj = WriteJson()
    #objt.write_txt()
    #objj.write_json()

# Section for checking & scheduled work
if output_type == "txt":
    schedule.every(int(interval)).seconds.do(rtxt)
elif output_type == "json":
    schedule.every(int(interval)).seconds.do(rjson)
else:
    print("Checked your file, or permission")
while True:
    schedule.run_pending()
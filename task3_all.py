#Program which monitoring system

import psutil, schedule, datetime, json, configparser, time

#For clean outlogs file
clearjson_file = open("outlog.json", "a")
clearjson_file.close()
cleartxt_file=open("outlog.txt", "a")
cleartxt_file.close()


snapshot = 1 #counter of snapshots

#For config file
config = configparser.ConfigParser()
config.read('conf.ini')
output_type = config.get('common', 'type')
interval = config.get('common', 'interval')

#Function for writing statistics to outlog.txt
def writetxt():
    global snapshot
    file_var = open('outlog.txt', "a")
    time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H:%M:%S')
    file_var.write("Snapshot{0}:{1}\n".format(snapshot, time))
    file_var.write('CPU usage:{}%\n'.format(psutil.cpu_percent(interval=1, percpu=True)))
    file_var.write('Memory usage: Total:{}Mb\n'.format((psutil.disk_usage('/')[0] / 1048576).__round__(2)))
    file_var.write('Memory usage: Percent free:{}%\n'.format(psutil.disk_usage('/')[3]))
    file_var.write('RAM usage: Percent free:{}%\n'.format(psutil.virtual_memory()[2]))
    file_var.write('Disk IO usage: read: {}Mb\n'.format((psutil.disk_io_counters()[2] / 1048576).__round__(2)))
    file_var.write('Disk IO usage: write:{}Mb\n'.format((psutil.disk_io_counters()[3] / 1048576).__round__(2)))
    file_var.write('Network usage: sent:{}Mb\n'.format((psutil.net_io_counters()[0] / 1048576).__round__(2)))
    file_var.write('Network usage: recieve:{}Mb\n'.format((psutil.net_io_counters()[1] / 1048576).__round__(2)))
    file_var.write("\n")
    file_var.close()
    snapshot += 1

#Function for writing statistics to outlog.json
def writejson():
    global snapshot
    time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d-%H:%M:%S')
    snapcreate = {
     'CPU usage:': psutil.cpu_percent(interval=1, percpu=True),
     'Memory usage: Total:': str((psutil.disk_usage('/')[0] / 1048576).__round__(2)) + "Mb",
     'Memory usage: Percent free:': str(psutil.disk_usage('/')[3]) + "%",
     'RAM usage: Percent free:': str(psutil.virtual_memory()[2]) + "%",
     'Disk IO usage: read:': str((psutil.disk_io_counters()[2] / 1048576).__round__(2)) + "Mb",
     'Disk IO usage: write:': str((psutil.disk_io_counters()[3] / 1048576).__round__(2)) + "Mb",
     'Network usage: sent:': str((psutil.net_io_counters()[0] / 1048576).__round__(2)) + "Mb",
     'Network usage: recv:': str((psutil.net_io_counters()[1] / 1048576).__round__(2)) +"Mb"
    }
    data = ('SNAPSHOT' + str(snapshot) + ": " + str(time) + ": ", snapcreate)
    with open("outlog.json", "a") as file_var:
     json.dump(data, file_var, indent=3, sort_keys=True)
     snapshot += 1

#Section for checking & scheduled work
if output_type == "txt":
    schedule.every(int(interval)).seconds.do(writetxt)
elif output_type == "json":
    schedule.every(int(interval)).seconds.do(writejson)
else:
    print("Checked your file, or permission")
while True:
    schedule.run_pending()
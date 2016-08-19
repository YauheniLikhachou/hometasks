import re
from collections import Counter
try:
    ip_file = open("access.log" , "r")
except NameError:
        print("File not found")

def ip_serch(n, access_log="access.log"):

    ip_pattern = re.compile("^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    s_ip = Counter()

    with open(access_log, "r") as file:
        for line in file:
            if line not in ["\n", "\r\n"]:
                i = line.split(maxsplit=1)[0]

                if ip_pattern.match(i):
                    s_ip[i] += 1

    return s_ip.most_common(n)
print(ip_serch(10))
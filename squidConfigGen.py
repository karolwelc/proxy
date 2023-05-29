from random import sample
import subprocess
import time
input_subnet = input("Enter Subnet: ")
port = int(input("Enter port: "))
print("1. ip range 1-127")
print("2. ip range 128-254")
print("3. ip range 1-254")
ip_range = input("ip range: ")
def clear_file(file_path):
    with open(file_path, 'w') as file:
        file.truncate()
squidID = input("Input squid config id: ")
file_path = 'passwd'+squidID
try:
    clear_file(file_path)   
except:
    print("no password file found")
    time.sleep(0.3)
with open(f"proxies{squidID}.txt","w") as proxies_file:
    with open(f"squid{squidID}.conf","w") as file:
        file.write(f"auth_param basic program /usr/lib/squid/basic_ncsa_auth /etc/squid/passwd{squidID}\n")
        file.write(f"\n")
        if ip_range == "1":
            start = 1
            end = 128
        if ip_range == "2":
            start = 128
            end = 255
        if ip_range == "3":
            start = 1
            end = 255
        for i in range(start, end):
            
            username = "".join(map(str, sample(range(0, 9), 8)))
            password = "".join(map(str, sample(range(0, 9), 8)))
            port +=1 
            auth_ip_id = f"auth_ip{i}"
            specyfic_ip = input_subnet.rsplit(".", 1)[0] + "." + f"{i}"
            file.write(f"### ip:{specyfic_ip} port: {port} ###" + "\n")
            file.write(f"http_port {specyfic_ip}:{port}\n")
            file.write(f"acl port_{port} localport {port}\n")
            file.write(f"tcp_outgoing_address {specyfic_ip} port_{port}\n")
            file.write(f"acl {auth_ip_id} proxy_auth {username}\n")
            file.write(f"http_access allow {auth_ip_id} port_{port}\n")
            file.write(f"\n")

            command = f'htpasswd -b passwd {username} {password}'
            subprocess.run(command, shell=True, check=True)
            proxies_file.write(f"{specyfic_ip}:{port}:{username}:{password}" + "\n")
        file.write("forwarded_for delete\n")
        file.write("request_header_access Via deny all\n")
        file.write("http_access deny all\n")
        file.write("dns_v4_first on\n")
        file.write("forwarded_for delete\n")
        file.write("via off\n")
        file.write("cache deny all\n")
        file.write("quick_abort_min 0 KB\n")
        file.write("quick_abort_max 0 KB\n")
        file.write("shutdown_lifetime 0 seconds\n")
        file.write("quick_abort_pct 70\n")
        file.write("max_filedesc 65535\n")
        file.write("cache_mem 200 MB\n")
        file.write("icp_port 0\n")
        file.write("htcp_port 0\n")
        file.write("icp_access deny all\n")
        file.write("htcp_access deny all\n")
        file.write("snmp_port 0\n")
        file.write("snmp_access deny all\n")
        file.write("pipeline_prefetch on\n")
        file.write("memory_pools on\n")
        file.write("memory_pools_limit 80 MB\n")
        file.write("maximum_object_size 2048 KB\n")
        file.write("maximum_object_size_in_memory 1024 KB\n")
        file.write("ipcache_size 4096\n")
        file.write("ipcache_low 90\n")
        file.write("ipcache_high 95\n")
        file.write("maximum_object_size_in_memory 50 KB\n")
        file.write("cache_store_log none\n")
        file.write("half_closed_clients off\n")
        file.write("pid_filename /var/run/squid/kierylo.pid\n")
        file.write("cache_dir ufs /var/spool/squid/kierylo 7000 16 256\n")
        file.write("cache_effective_user proxy\n")

        command = f'systemctl restart squid'
        subprocess.run(command, shell=True, check=True)
import subprocess

def cpu_utilization(ip_address):
    '''
        OID value: 1.3.6.1.4.1.9.2.1.56.0
        OID description:
        This is the current CPU utilization for cisco routers. Works on c7200 router.
        https://www.alvestrand.no/objectid/1.3.6.1.4.1.9.2.1.56.0.html
    '''
    proc = subprocess.Popen("snmpwalk -v3 -u user1 -A authpass -X encpassword -l authpriv " + ip_address + " .1.3.6.1.4.1.9.2.1.56.0", stdout=subprocess.PIPE, shell=True)
    proc.wait()

    return int(proc.communicate()[0].decode('utf-8').split("INTEGER: ")[1])

def write_dns_file():
    '''
       Write DNS file changes.
    '''
    
    for router in routers:
        line = 10 

        f = open(routers[router]["zone_file"], "r")
        lines = f.readlines()
        f.close()

        lines[line-1] = "    IN A " + routers[router]["datacenter_ip"] + "\n"

        f = open(routers[router]["zone_file"], "w")
        lines = "".join(lines)
        f.write(lines)
        f.close()

if __name__ == '__main__':
    routers = {
        "aveiro": {
            "cpu_value": 0,
            "router_ip": "10.0.0.42",
            "datacenter_ip": "192.100.3.2",
            "zone_file": "/etc/bind/aracdn.com-aveiro.db"
        },
        "faro": {
            "cpu_value": 0,
            "router_ip": "10.0.0.48",
            "datacenter_ip": "192.100.4.2",
            "zone_file": "/etc/bind/aracdn.com-faro.db",
        },
        "lisboa": {
            "cpu_value": 0,
            "router_ip": "10.0.0.41",
            "datacenter_ip": "192.100.2.2",
            "zone_file": "/etc/bind/aracdn.com-other.db"
        }
    }

    for router in routers:
        routers[router]["cpu_value"] = cpu_utilization(routers[router]["router_ip"])

    cpu_limit = 5

    min_busy = sorted(routers, key=lambda x: routers[x]["cpu_value"])[0]
    
    for router in routers:
        if routers[router]["cpu_value"] > cpu_limit:
            routers[router]["datacenter_ip"] = routers[min_busy]["datacenter_ip"]
    
    # write_dns_file()

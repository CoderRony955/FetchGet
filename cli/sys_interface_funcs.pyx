import psutil
import os
from ping3 import ping
import time
import platform
import socket
import whois
import speedtest
from datetime import datetime
from rich.console import Console
import  requests
import logging
import statistics
from rich.traceback import install
from typing import Any

install()
console = Console()

logging.basicConfig(level=logging.INFO,
                    filename="fetchget.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger(__name__)

def sys_info(args) -> None:
    cdef list info = []
    for i in platform.uname():
        info.append(i)
    if os.name != 'nt':
        console.print(info[0], style='gray')
    else:
        console.print(f' OS: {info[0]}', style='blue')
    console.print(f' Node: {info[1]}', style='green')
    console.print(f' Release: {info[3]}', style='yellow')
    console.print(f' Version: {info[4]}', style='cyan')
    console.print(f' Machine: {info[5]}', style='cyan')
    
#-----------------------------------------------------------------

def my_ips(args) -> None:
    try:
        hostname = socket.gethostname()
        get = socket.gethostbyname_ex(hostname)[2]
        console.print(f'Private IPs:\n', style='blue')
        for i in get:
            console.print(i, style='blue')
        print()
        public_ip = requests.get('https://api.ipify.org')
        console.print(f'Public IP: {public_ip.text}', style='blue')
    except(requests.ConnectionError, requests.HTTPError, KeyboardInterrupt) as e:
        console.print(str(e), style='red')
        logger.error(e)


#-----------------------------------------------------------------

def count_cpu(args) -> None:
    cdef int total_count = psutil.cpu_count()
    try:
        if total_count >= 8:
            console.print(f' Total CPU: {total_count}', style='green')
        elif total_count <= 7 and total_count >= 4:
            console.print(f' Total CPU: {total_count}', style='blue')
        elif total_count <= 3:
            console.print(f' Total CPU: {total_count}', style='gray')
    except (psutil.Error, KeyboardInterrupt) as e:
        logger.error(e)

#-----------------------------------------------------------------

def ram_info(args) -> None:
    cdef float ram 
    cdef float used_ram
    try:
        ram = psutil.virtual_memory().total / (1024 ** 3)  # Convert to GB
        used_ram = psutil.virtual_memory().used / (1024 ** 3)  # Convert to GB
        if ram < 8:
            console.print(f' Total RAM: {ram:.2f} GB', style='gray')
            console.print(f' Used RAM: {used_ram:.2f} GB\n', style='yellow')
            console.print('Hmm.. It seems like you have less amount RAM because at this you must need to have a atleast 8GB or more RAM. My advice is to please upgrade your RAM', style='bold')
            return

        console.print(f' Total RAM: {ram:.2f} GB', style='cyan')
        console.print(f' Used RAM: {used_ram:.2f} GB\n', style='yellow')
        console.print(f' Great! You have {ram:.2f} Giga Bytes of RAM in your system it sounds \'Woaaaa..\'', style='bold')
    except (psutil.Error, Exception) as e:
        logger.error(e)

#-----------------------------------------------------------------

def cpu_utilization(args) -> None:
    cdef int usage
    try:
        console.print("[bold cyan]Press 'Ctrl + C' to quit[/bold cyan]\n")
        console.print(f"{'CPU USAGE':<20}{'STATUS':<30}{'SUGGESTION'}")

        while True:
            usage = psutil.cpu_percent(interval=1)

            if usage > 70:
                color = "yellow"
                status = "High Utilization"
                suggestion = "Close unnecessary apps to avoid overheating issue"
            else:
                color = "green"
                status = "Normal"
                suggestion = "All good"

            console.print(f"{str(usage)+' %':<20}{status:<30}{suggestion}", style=color)
            time.sleep(0.5)
    except KeyboardInterrupt as e:
        logger.error(e)

#-----------------------------------------------------------------

def users(args) -> None:
    cdef list[Any] info
    try:
        info = []
        for i in psutil.users()[0]:
            info.append(i)
            
        console.print(f' Users: {info[0]}', style='cyan')
        console.print(f' Terminal: {info[1]}', style='cyan')
        console.print(f' Host: {info[2]}', style='cyan')
        console.print(f' Started: {info[3]}', style='cyan')
        console.print(f' Pid: {info[4]}', style='cyan')
    except (Exception, psutil.Error) as e:
        logger.error(e)

#-----------------------------------------------------------------

def io_interface(args) -> None:
    cdef list[Any] net_io
    try:
        console.print(' press \'ctrl + c\' to quit')
        while True:
            net_io = []
            for i in psutil.net_io_counters(pernic=False):
                net_io.append(i)
                
            console.print(f' Bytes sent -> {net_io[0]}', style='blue')
            console.print(f' Bytes received <- {net_io[1]}', style='green')
            time.sleep(1)
    except (Exception, psutil.Error) as e:
        logger.error(e)

#-----------------------------------------------------------------

def process_ids(args) -> None:
    try:
        for ids in psutil.pids():
            console.print(ids, end=' ', style='blue')
    except (Exception, psutil.Error) as e:
        logger.error(e)

#-----------------------------------------------------------------

def net_conn_info(args) -> None:
    try:
        with console.status("[bold green]checking...[/]", spinner="dots"):
            time.sleep(1)
        for conn in psutil.net_connections(kind=args.connection):
            console.print(f"PID: {conn.pid}, Local: {conn.laddr}, Remote: {conn.raddr}, Status: {conn.status}")
    except (psutil.Error, Exception) as e:
        logger.error(e)

#-----------------------------------------------------------------

def net_inter_info(args) -> None:
    cdef dict[Any] stats
    try:
        stats = psutil.net_if_stats()
        with console.status("[bold green]checking...[/]", spinner="dots"):
            time.sleep(1)
        for interface, info in stats.items():
            console.print(f"\nInterface: {interface}")
            console.print(f"  Is Up: {info.isup}")
            console.print(f"  Duplex: {info.duplex}")
            console.print(f"  Speed: {info.speed} Mbps")
            console.print(f"  MTU: {info.mtu}")
    except (Exception, psutil.Error) as e:
        logger.error(e)
    
#-----------------------------------------------------------------

def net_add(args) -> None:
    cdef dict[Any] interfaces
    try:
        interfaces = psutil.net_if_addrs()
        with console.status("[bold green]checking...[/]", spinner="dots"):
            time.sleep(1)
        for interface, addrs in interfaces.items():
            console.print(f"\nInterface: {interface}", style='blue')
            for addr in addrs:
                console.print(f" Address Family: {addr.family}")
                console.print(f" Address: {addr.address}")
                console.print(f" Netmask: {addr.netmask}")
                console.print(f" Broadcast: {addr.broadcast}")
    except (Exception, psutil.Error) as e:
        logger.error(e)

#-----------------------------------------------------------------

def cpu_stats(args) -> None:
    cdef stats = psutil.cpu_stats()
    try:
        console.print(f" Context switches: {stats.ctx_switches}")
        console.print(f" Interrupts: {stats.interrupts}")
        console.print(f" Soft interrupts: {stats.soft_interrupts}")
        console.print(f" System calls: {stats.syscalls}")
    except (Exception, psutil.Error) as e:
        logger.error(e)

#-----------------------------------------------------------------

def swap_ram_info(args) -> None:
    cdef swap = psutil.swap_memory()
    try:
        console.print(f" Total Swap: {swap.total / (1024**2):.2f} MB")
        console.print(f" Used Swap: {swap.used / (1024**2):.2f} MB")
        console.print(f" Free Swap: {swap.free / (1024**2):.2f} MB")
        console.print(f" Swap Usage: {swap.percent:.2f}%")
        console.print(f" Swapped In: {swap.sin / (1024**2):.2f} MB")
        console.print(f" Swapped Out: {swap.sout / (1024**2):.2f} MB")
    except (Exception, psutil.Error) as e:
        logger.error(e)
        
#-----------------------------------------------------------------

def whois_lookup(args) -> None:
    cdef str domain_name
    try:
        domain_name = args.hostname

        info = whois.whois(domain_name)

        def normalize_date(d):
            if isinstance(d, list):
                console.print(d[0].strftime('%Y-%m-%d %H:%M:%S') if isinstance(d[0], datetime) else d[0])
            elif isinstance(d, datetime):
                console.print(d.strftime('%Y-%m-%d %H:%M:%S'))
            else:
                console.print(d)
        with console.status("[bold green]getting info...[/]", spinner="dots"):
            time.sleep(2)
        for key, value in info.items():
            if 'date' in key and value is not None:
                console.print(f' {key} -> {normalize_date(value)}')
            else:
                console.print(f' {key} -> {value}')
    except Exception as e:
        logger.error(e)

#-----------------------------------------------------------------

def host_ip(args) -> None:
    cdef str hostname
    try:
        hostname = args.hostname
        console.print( f'Hostname: {hostname}\nIPv4:    {socket.gethostbyname(hostname)}')
    except (socket.error, Exception) as e:
        console.print(e)
        logger.error(e)

#-----------------------------------------------------------------

def pingg(args) -> None:
    cdef list hosts = [
        '1.1.1.1',
        '8.8.8.8',
        '9.9.9.9',
        '208.67.222.222',
        '94.140.14.14',
        '76.76.2.0',
        '185.228.168.9',
        '185.222.222.222'
    ]

    try:
        samples = 5

        for host in hosts:
            delays = []
            for i in range(samples):
                delay = ping(host)
                if delay is not None:
                    delays.append(delay * 1000)  #
                else:
                    console.print(f"Ping {i+1} to {host} failed")

            # Calculate and print average
            if delays:
                avg_ping = statistics.mean(delays)
                console.print(
                    f"\n✅ Average ping to {host} over {len(delays)} responses: {avg_ping:.2f} ms")
                console.print(f"Minimum: {min(delays):.2f} ms, Maximum: {max(delays):.2f} ms")
            else:
                console.print(f"\n❌ All ping attempts to {host} failed.")
    except Exception as e:
        logger.info(e)
    
#-----------------------------------------------------------------

def internet_speedtest(args) -> None:
    console.print("Please wait a while because it just take some seconds to check :)")
    st = speedtest.Speedtest()

    # Get best server (based on ping)
    st.get_best_server()

    # Perform download and upload tests
    download_speed = st.download()
    upload_speed = st.upload()
    ping_result = st.results.ping
    

    # Convert bits per second to Mbps
    download_speed_mbps = download_speed / 1_000_000
    upload_speed_mbps = upload_speed / 1_000_000
    with console.status("[bold green]getting info...[/]", spinner="dots"):
            time.sleep(2)

    try:
        console.print(f"Download Speed: {download_speed_mbps:.2f} Mbps")
        console.print(f"Upload Speed: {upload_speed_mbps:.2f} Mbps")
        console.print(f"Ping: {ping_result:.2f} ms") 
    except (KeyboardInterrupt, speedtest.ConfigRetrievalError, speedtest.SpeedtestServersError, speedtest.ServersRetrievalError) as e:
        console.print(f"An error occurred while running this command for more info please check logs ;-;", style="red")
        logger.error(e)



import asyncio
import argparse
import sys_interface_funcs
import others
import logging

logging.basicConfig(level=logging.INFO,
                    filename="fetchget.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger(__name__)

about = '\033[3mA free and open-source tool that help you to gather information of your system utilities and performing networking related tasks!\033[0m'


def main():
    parser = argparse.ArgumentParser(
        description=f"""\
\033[1m\033[92mFetch\033[96mGet\033[0m 1.1\n\n{about}\n\n
Available Commands:
    \033[92msysinfo                                      Get system information\033[0m
    \033[93mips                                          Get your public and private IPs\033[0m
    \033[94mmyipinfo                                     Get your IP information\033[0m
    \033[95mipinfo     -ip {{valid ip address}}            Get information of any valid specific IP address\033[0m
    \033[96mraminfo                                      Get your physical RAM information\033[0m
    \033[33mswapinfo                                     See the information of you system's swap memory\033[0m
    livecpu                                      Get your live CPU utilization
    \033[34mcpustats                                     See the status of CPU since boot time\033[0m
    \033[36musers                                        Get total users that are logged in the system\033[0m
    \033[31mnetio                                        Catch the live bytes send or received\033[0m
    \033[34mpids                                         See all process ids\033[0m
    \033[32mnetinter                                     See all network interfaces information\033[0m
    \033[36mnetadd                                       See all network interfaces addresses\033[0m
    \033[95mconninfo   -connection {{all,inet4,inet6,tcp,udp}}   Get network connections information by giving connections names\033[0m
    
    \033[92mGET        -url {{valid url}}                  Make HTTP GET requests\033[0m
    \033[93mPOST       url -k1 key -v1 value             Make HTTP POST request\033[0m
              {{four more optional key values pairs available}}
                 
    \033[94mPUT       url -k1 key -v1 value              Make HTTP PUT request\033[0m
              {{four more optional key values pairs available}}   
              
    \033[33mPATCH     url -k1 key -v1 value              Make HTTP PATCH request\033[0m
              {{four more optional key values pairs available}}   
    
    \033[91mDELETE    url                                Make HTTP DELETE requests\033[0m
              {{five optional payloads in form of key and value pair are available e.g. DELETE url -k1 user_id -v1 1234}}
    
    \033[35mwhois     -hostname {{xyz.com}}                Perform WHOIS lookup on any domain / hostname\033[0m
    \033[36mhostip    -hostname {{xyz.com}}                See IPv4 address of any particular hostname\033[0m
    \033[32mdnslookup    -domain {{xyz.com}}               See all records including ('A (IPv4)', 'AAAA (IPv6)', 'NS (name servers)', 'SOA (metadata about domain)' etc.)  of any particular hostname / domain\033[0m
    
    \033[94mverify    -target {{domain, url}}              Check url, domain if it is suspicious or not\033[0m
    \033[95mabuseip   -ip {{target ip}}                    Check any IP if it is abusive or not (abusive means if any IP is responsible to perform malicious tasks on the internet then that IP is abusive)\033[0m
    \033[93mping                                         Perform ping command on all public DNS servers just using single command\033[0m
    \033[92mnetspeed                                     Use this command to check your internet speed, it will check and returns your internet \'Download speed\', \'Upload speed\' and \'How much ping your are getting\033[0m
    \033[96mfind      -username {{target username}}        Perform username lookup on over 20+ social networks to find user\033[0m
    
    
        """,
        formatter_class=argparse.RawTextHelpFormatter
    )
    subparsers = parser.add_subparsers(
        title="Available subcommands", dest="Available Commands")

    parser_sysinfo = subparsers.add_parser(
        "sysinfo", help="Get system information")
    parser_sysinfo.set_defaults(func=sys_interface_funcs.sys_info)

    parser_ips = subparsers.add_parser(
        "ips", help="Get your public and private IP")
    parser_ips.set_defaults(func=sys_interface_funcs.my_ips)

    parser_myipinfo = subparsers.add_parser(
        "myipinfo", help="Get your IP information")
    parser_myipinfo.set_defaults(func=others.my_ip_info)

    parser_raminfo = subparsers.add_parser(
        "raminfo", help="Get your physical RAM information")
    parser_raminfo.set_defaults(func=sys_interface_funcs.ram_info)

    parser_swap_mem_info = subparsers.add_parser(
        "swapinfo", help="See the information of you system's swap memory")
    parser_swap_mem_info.set_defaults(func=sys_interface_funcs.swap_ram_info)

    parser_livecpu = subparsers.add_parser(
        "livecpu", help="Get your live CPU utilization")
    parser_livecpu.set_defaults(func=sys_interface_funcs.cpu_utilization)

    parser_cpustats = subparsers.add_parser(
        "cpustats", help="See the status of CPU since boot time")
    parser_cpustats.set_defaults(func=sys_interface_funcs.cpu_stats)

    parser_users = subparsers.add_parser(
        "users", help="Get total users that are logged in the system")
    parser_users.set_defaults(func=sys_interface_funcs.users)

    parser_netio = subparsers.add_parser(
        "netio", help="Catch the live bytes send or received")
    parser_netio.set_defaults(func=sys_interface_funcs.io_interface)

    parser_pids = subparsers.add_parser(
        "pids", help="See all process ids")
    parser_pids.set_defaults(func=sys_interface_funcs.process_ids)

    parser_netinter = subparsers.add_parser(
        "netinter", help="See all network interfaces information")
    parser_netinter.set_defaults(func=sys_interface_funcs.net_inter_info)

    parser_netadd = subparsers.add_parser(
        "netadd", help="See all network interfaces addresses")
    parser_netadd.set_defaults(func=sys_interface_funcs.net_add)

    parser_ipinfo = subparsers.add_parser(
        "ipinfo", help="Get information of any valid specific IP address")
    parser_ipinfo.add_argument(
        "-ip", help="Valid ip address to get information", required=True)
    parser_ipinfo.set_defaults(func=others.ip_info)


    parser_conninfo = subparsers.add_parser(
        "conninfo", help="Get network connections information by giving connections names")
    parser_conninfo.add_argument(
        "-connection", help="connection e.g. all, inet4, inet6, tcp, udp etc.", required=True,
        choices=["all", "inet4", "inet6", "tcp", "udp"],
    )
    parser_conninfo.set_defaults(func=sys_interface_funcs.net_conn_info)


    parser_GET_req = subparsers.add_parser(
        "GET", help="Make HTTP GET requests")
    parser_GET_req.add_argument(
        "-url", required=True
    )
    parser_GET_req.set_defaults(func=others.GET)


    def handle_post(args):
        post = others.post_req(args)
        asyncio.run(post.POST(args))

    parser_POST_req = subparsers.add_parser(
        "POST", help="Make HTTP POST requests")
    parser_POST_req.add_argument("url", help="Target URL")
    parser_POST_req.add_argument("-k1", required=True)
    parser_POST_req.add_argument("-v1", required=True)
    parser_POST_req.add_argument("-k2")
    parser_POST_req.add_argument("-v2")
    parser_POST_req.add_argument("-k3")
    parser_POST_req.add_argument("-v3")
    parser_POST_req.add_argument("-k4")
    parser_POST_req.add_argument("-v4")
    parser_POST_req.add_argument("-k5")
    parser_POST_req.add_argument("-v5")
    parser_POST_req.set_defaults(func=handle_post)


    def handle_patch(args):
        patch = others.patch_req(args)
        asyncio.run(patch.PATCH(args))

    parser_PATCH_req = subparsers.add_parser(
        "PATCH", help="Make HTTP PATCH requests")
    parser_PATCH_req.add_argument("url", help="Target URL")
    parser_PATCH_req.add_argument("-k1", required=True)
    parser_PATCH_req.add_argument("-v1", required=True)
    parser_PATCH_req.add_argument("-k2")
    parser_PATCH_req.add_argument("-v2")
    parser_PATCH_req.add_argument("-k3")
    parser_PATCH_req.add_argument("-v3")
    parser_PATCH_req.add_argument("-k4")
    parser_PATCH_req.add_argument("-v4")
    parser_PATCH_req.add_argument("-k5")
    parser_PATCH_req.add_argument("-v5")
    parser_PATCH_req.set_defaults(func=handle_patch)


    def handle_put(args):
        put = others.put_req(args)
        asyncio.run(put.PUT(args))

    parser_PUT_req = subparsers.add_parser(
        "PUT", help="Make HTTP PUT requests")
    parser_PUT_req.add_argument("url", help="Target URL")
    parser_PUT_req.add_argument("-k1", required=True)
    parser_PUT_req.add_argument("-v1", required=True)
    parser_PUT_req.add_argument("-k2")
    parser_PUT_req.add_argument("-v2")
    parser_PUT_req.add_argument("-k3")
    parser_PUT_req.add_argument("-v3")
    parser_PUT_req.add_argument("-k4")
    parser_PUT_req.add_argument("-v4")
    parser_PUT_req.add_argument("-k5")
    parser_PUT_req.add_argument("-v5")
    parser_PUT_req.set_defaults(func=handle_put)


    def handle_delete(args):
        delete = others.del_req(args)
        asyncio.run(delete.DELETE(args))

    parser_DELETE_req = subparsers.add_parser(
        "DELETE", help="Make DELETE PUT requests")
    parser_DELETE_req.add_argument("url", help="Target URL")
    parser_DELETE_req.add_argument("-k1")
    parser_DELETE_req.add_argument("-v1")
    parser_DELETE_req.add_argument("-k2")
    parser_DELETE_req.add_argument("-v2")
    parser_DELETE_req.add_argument("-k3")
    parser_DELETE_req.add_argument("-v3")
    parser_DELETE_req.add_argument("-k4")
    parser_DELETE_req.add_argument("-v4")
    parser_DELETE_req.add_argument("-k5")
    parser_DELETE_req.add_argument("-v5")
    parser_DELETE_req.set_defaults(func=handle_delete)


    parser_whois = subparsers.add_parser(
        "whois", help="Perform WHOIS lookup on any domain / hostname")
    parser_whois.add_argument(
        "-hostname", help="Hostname / Domain to target", required=True)
    parser_whois.set_defaults(func=sys_interface_funcs.whois_lookup)


    parser_hostip = subparsers.add_parser(
        "hostip", help="See IPv4 address of any particular hostname")
    parser_hostip.add_argument(
        "-hostname", help="Hostname / Domain to target", required=True)
    parser_hostip.set_defaults(func=sys_interface_funcs.host_ip)


    parser_dns_lookup = subparsers.add_parser(
        "dnslookup", help="See all records including ('A (IPv4)', 'AAAA (IPv6)', 'NS (name servers)', 'SOA (metadata about domain)' etc.)  of any particular hostname / domain")
    parser_dns_lookup.add_argument(
        "-domain", help="Hostname / Domain to target", required=True)
    parser_dns_lookup.set_defaults(func=others.dns_lookup)


    parser_verify = subparsers.add_parser(
        "verify", help="Check url, domain if it is suspicious or not")
    parser_verify.add_argument(
        "-target", help="Domain, url to target", required=True)
    parser_verify.set_defaults(func=others.verify_url_)
    
    
    parser_abuse_ip_check = subparsers.add_parser(
        "abuseip", help="Check any IP if it is abusive or not (abusive means if any IP is responsible to perform malicious tasks on the internet then that IP is abusive)")
    parser_abuse_ip_check.add_argument(
        "-ip", help="ip to target", required=True)
    parser_abuse_ip_check.set_defaults(func=others.abuse_ip_check)
    
    
    parser_ping_all = subparsers.add_parser(
        "ping", help="Perform ping command on all public DNS servers just using single command")
    parser_ping_all.set_defaults(func=sys_interface_funcs.pingg)
    
    
    parser_check_internet_speed = subparsers.add_parser(
        "netspeed", help="Use this command to check your internet speed, it will check and returns your internet \'Download speed\', \'Upload speed\' and \'How much ping your are getting\'")
    parser_check_internet_speed.set_defaults(func=sys_interface_funcs.internet_speedtest)

    parser_find_user = subparsers.add_parser(
        "find", help="Perform username lookup on over 20+ social networks to find user")
    parser_find_user.add_argument(
        "-username", help="username to target", required=True)
    parser_find_user.set_defaults(func=others.find_user)


    # Parse and call the appropriate function
    args = parser.parse_args()
    if asyncio.iscoroutinefunction(args.func):
        asyncio.run(args.func(args))
    else:
        args.func(args)


if __name__ == "__main__":
    main()

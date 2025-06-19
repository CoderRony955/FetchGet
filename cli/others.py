import httpx
import json
from rich.console import Console
from rich.traceback import install
import logging
import time
import vt
from dotenv import load_dotenv
import os
import dns.resolver
from typing import Optional, Any

install()
console = Console()

load_dotenv()

logging.basicConfig(level=logging.INFO,
                    filename="fetchget.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger(__name__)


async def my_ip_info(args):
    try:
        async with httpx.AsyncClient() as client:
            ip = await client.get('https://api.ipify.org')
            get_info = await client.get(f'https://ipinfo.io/{ip.text}/json')

            with console.status("[bold green]Loading...[/]", spinner="dots"):
                time.sleep(2)
            logger.info(f'user IP -> {ip.text.strip()}')

            to_dict = json.loads(get_info.text)
            for i, j in to_dict.items():
                console.print(f'{i} -> {j}')
            logger.info('operation successfull')
    except (httpx.ProxyError, httpx.NetworkError, httpx.ConnectError, Exception) as e:
        console.print(f"Error: {e}", style="red")
        logger.error(f"Error: {e}")

# -----------------------------------------------------------------


async def ip_info(args):
    try:
        async with httpx.AsyncClient() as client:
            get_info = await client.get(f'https://ipinfo.io/{args.ip}/json')
            logger.info(f'target IP -> {args.ip}')
            with console.status("[bold green]Loading...[/]", spinner="dots"):
                time.sleep(2)
            to_dict = json.loads(get_info.text)
            for i, j in to_dict.items():
                console.print(f'{i} -> {j}')
            logger.info('operation successfull')
    except (httpx.ProxyError, httpx.NetworkError, httpx.ConnectError, Exception) as e:
        console.print(f"Error: {e}", style="red")
        logger.error(f"Error: {e}")

# -----------------------------------------------------------------
# HTTP requests methods
# -----------------------------------------------------------------


async def GET(args):
    try:
        async with httpx.AsyncClient() as client:
            req = await client.get(str(args.url))
            with console.status("[bold green]getting output...[/]", spinner="dots"):
                time.sleep(2)
            console.print(req.text)
    except (httpx.ProxyError, httpx.NetworkError, httpx.ConnectError, KeyboardInterrupt) as e:
        console.print(f"Network error: {e}", style="red")
        logger.error(f"Network error: {e}")

# -----------------------------------------------------------------


class post_req:

    def __init__(self, args):
        self.url = str(args.url)

        self.k1, self.v1 = str(args.k1), args.v1
        self.k2, self.v2 = str(args.k2), args.v2
        self.k3, self.v3 = args.k3, args.v3
        self.k4, self.v4 = args.k4, args.v4
        self.k5, self.v5 = args.k5, args.v5

    async def POST(self, args):
        try:
            async with httpx.AsyncClient() as client:
                data = {
                    k: v for k, v in [
                        (self.k1, self.v1),
                        (self.k2, self.v2),
                        (self.k3, self.v3),
                        (self.k4, self.v4),
                        (self.k5, self.v5)
                    ] if k is not None and v is not None
                }

                output = await client.post(url=self.url, data=data)
                with console.status("[bold green]getting output...[/]", spinner="dots"):
                    time.sleep(2)
                console.print(output.text)
        except (httpx.ProxyError, httpx.NetworkError, httpx.ConnectError, KeyboardInterrupt) as e:
            console.print(f"Network error: {e}", style="red")
            logger.error(f"Network error: {e}")

# -----------------------------------------------------------------


class patch_req:

    def __init__(self, args):
        self.url = str(args.url)

        self.k1, self.v1 = str(args.k1), args.v1
        self.k2, self.v2 = str(args.k2), args.v2
        self.k3, self.v3 = args.k3, args.v3
        self.k4, self.v4 = args.k4, args.v4
        self.k5, self.v5 = args.k5, args.v5

    async def PATCH(self, args):
        try:
            async with httpx.AsyncClient() as client:
                data = {
                    k: v for k, v in [
                        (self.k1, self.v1),
                        (self.k2, self.v2),
                        (self.k3, self.v3),
                        (self.k4, self.v4),
                        (self.k5, self.v5)
                    ] if k is not None and v is not None
                }

                output = await client.patch(url=self.url, data=data)
                with console.status("[bold green]getting output...[/]", spinner="dots"):
                    time.sleep(2)
                console.print(output.text)
        except (httpx.ProxyError, httpx.NetworkError, httpx.ConnectError, KeyboardInterrupt) as e:
            console.print(f"Network error: {e}", style="red")
            logger.error(f"Network error: {e}")
# -----------------------------------------------------------------


class put_req:

    def __init__(self, args):
        self.url = str(args.url)

        self.k1, self.v1 = str(args.k1), args.v1
        self.k2, self.v2 = str(args.k2), args.v2
        self.k3, self.v3 = args.k3, args.v3
        self.k4, self.v4 = args.k4, args.v4
        self.k5, self.v5 = args.k5, args.v5

    async def PUT(self, args):
        try:
            async with httpx.AsyncClient() as client:
                data = {
                    k: v for k, v in [
                        (self.k1, self.v1),
                        (self.k2, self.v2),
                        (self.k3, self.v3),
                        (self.k4, self.v4),
                        (self.k5, self.v5)
                    ] if k is not None and v is not None
                }

                output = await client.put(url=self.url, data=data)
                with console.status("[bold green]getting output...[/]", spinner="dots"):
                    time.sleep(2)
                console.print(output.text)
        except (httpx.ProxyError, httpx.NetworkError, httpx.ConnectError, KeyboardInterrupt) as e:
            console.print(f"Network error: {e}", style="red")
            logger.error(f"Network error: {e}")

# -----------------------------------------------------------------


class del_req:
    def __init__(self, args):
        self.url = str(args.url)

        self.k1, self.v1 = str(args.k1), args.v1
        self.k2, self.v2 = str(args.k2), args.v2
        self.k3, self.v3 = args.k3, args.v3
        self.k4, self.v4 = args.k4, args.v4
        self.k5, self.v5 = args.k5, args.v5

    async def DELETE(self, args):
        try:
            payload = {
                k: v for k, v in [
                    (self.k1, self.v1),
                    (self.k2, self.v2),
                    (self.k3, self.v3),
                    (self.k4, self.v4),
                    (self.k5, self.v5)
                ] if k is not None and v is not None
            }

            async with httpx.AsyncClient() as client:
                request = httpx.Request(
                    method="DELETE",
                    url=self.url,
                    headers={"Content-Type": "application/json"},
                    content=json.dumps(payload)
                )
                response = await client.send(request)

                with console.status("[bold green]Getting output...[/]", spinner="dots"):
                    time.sleep(2)
                console.print(response.text)

        except (httpx.ProxyError, httpx.NetworkError, httpx.ConnectError, KeyboardInterrupt) as e:
            console.print(f"Network error: {e}", style="red")
            logger.error(f"Network error: {e}")

# -----------------------------------------------------------------
# -----------------------------------------------------------------


def dns_lookup(args) -> None:
    record_types = [
        "A", "AAAA", "MX", "NS", "TXT", "CNAME", "SOA",
        "SRV", "CAA", "DNSKEY", "DS", "RRSIG", "TLSA",
        "NAPTR", "SPF"
    ]
    resolver = dns.resolver.Resolver()
    resolver.nameservers = ["1.1.1.1", "8.8.8.8"]
    resolver.timeout = 3
    resolver.lifetime = 5
    with console.status(f" [bold green]getting records...[/]", spinner="dots"):
        time.sleep(1)  # Cosmetic delay for status animation
    for record_type in record_types:
        try:
            answers = resolver.resolve(args.domain, record_type)
            for rdata in answers:
                console.print(f" [cyan]{record_type}[/] → {rdata.to_text()}")
        except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.NoNameservers, dns.resolver.Timeout, KeyboardInterrupt) as e:
            console.print(f" [red]{record_type}[/] → [italic]{str(e)}[/]")

# -----------------------------------------------------------------


def verify_url_(args):
    api_key = os.getenv('VIRUSTOTAL_APIKEY')
    try:

        with vt.Client(apikey=api_key) as client:
            # Step 1: Submit the URL for scanning
            analysis = client.scan_url(args.target)
            console.print(f"Submitted URL: {args.target}")
            console.print("Waiting for analysis to complete...\n")

            # Step 2: Wait for analysis to finish
            while True:
                analysis = client.get_object(f"/analyses/{analysis.id}")
                if analysis.status == "completed":
                    break
            with console.status(f" [bold green]getting report...[/]", spinner="dots"):
                time.sleep(1)  # Cosmetic delay for status animation

            # Step 3: Retrieve full report using encoded URL ID
            url_id = vt.url_id(args.target)
            url_obj = client.get_object(f"/urls/{url_id}")

            # Step 4: Access stats safely using .get()
            stats = url_obj.get("last_analysis_stats", {})

            if not stats:
                console.print(
                    "❌ No analysis stats found. Try scanning again later.")
                return

            # Step 5: Display result
            console.print(f"🧾 Scan Summary for: {args.target}")
            console.print(f"✅ Harmless:   {stats.get('harmless', 0)}")
            console.print(f"⚠️ Suspicious: {stats.get('suspicious', 0)}")
            console.print(f"❌ Malicious:  {stats.get('malicious', 0)}")
            console.print(f"🧐 Undetected: {stats.get('undetected', 0)}")

            if stats.get('malicious', 0) > 0 or stats.get('suspicious', 0) > 0:
                console.print("⚠️ This URL may be phishing or malicious.")
            else:
                console.print("✅ This URL appears clean.")
    except (vt.APIError, vt.error, Exception) as e:
        logger.error(e)
        console.print(e)

# -----------------------------------------------------------------


async def abuse_ip_check(args):
    api_key = os.getenv('ABUSE_IPDB_APIKEY')
    try:

        url = "https://api.abuseipdb.com/api/v2/check"
        headers = {
            "Accept": "application/json",
            "Key": api_key
        }
        params = {
            "ipAddress": args.ip,
            "maxAgeInDays": 90
        }

        async with httpx.AsyncClient() as client:
            response = await client.get(url=url, headers=headers, params=params)
            with console.status(f" [bold green]getting record...[/]", spinner="dots"):
                time.sleep(1)

            if response.status_code == 200:
                decodedResponse = response.json().get("data", {})
                
                for key, value in decodedResponse.items():
                    console.print(f" {key} → {value}")
            else:
                console.print(f" Error {response.status_code}: {response.text}")

    except (httpx.ProxyError, httpx.NetworkError, httpx.ConnectError, Exception) as e:
        console.print(f" Network error: {e}", style="red")
        logger.error(f"Network error: {e}")

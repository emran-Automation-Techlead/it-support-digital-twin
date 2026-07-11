import platform
import re
import socket
import subprocess

import psutil

import ui
from logger import log_action

VPN_KEYWORDS = ["tun", "tap", "vpn", "cisco", "globalprotect", "nordlynx", "wg", "utun"]


def _ping_host(host: str = "8.8.8.8", timeout_s: int = 5):
    system = platform.system()
    if system == "Windows":
        cmd = ["ping", "-n", "4", host]
    else:
        cmd = ["ping", "-c", "4", host]

    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout_s
        )
    except (subprocess.TimeoutExpired, OSError):
        return False, None

    if result.returncode != 0:
        return False, None

    match = re.search(r"(?:time|tempo)[=<]([\d.]+)\s*ms", result.stdout, re.IGNORECASE)
    latency = float(match.group(1)) if match else None
    return True, latency


def _dns_resolves(host: str = "google.com") -> bool:
    try:
        socket.gethostbyname(host)
        return True
    except socket.gaierror:
        return False


def _detect_vpn_adapter():
    try:
        interfaces = psutil.net_if_addrs().keys()
    except Exception:
        return None

    for name in interfaces:
        lowered = name.lower()
        for keyword in VPN_KEYWORDS:
            if keyword in lowered:
                return name
    return None


def check_vpn():
    with ui.spinner("Pinging 8.8.8.8..."):
        reachable, latency = _ping_host()

    with ui.spinner("Resolving DNS (google.com)..."):
        dns_ok = _dns_resolves()

    with ui.spinner("Scanning network interfaces for VPN adapters..."):
        vpn_adapter = _detect_vpn_adapter()

    rows = [
        ["Internet reachable", "[green]Yes[/green]" if reachable else "[red]No[/red]"],
        ["Latency", f"{latency:.1f} ms" if latency is not None else "unknown"],
        ["DNS resolution", "[green]OK[/green]" if dns_ok else "[red]FAILED[/red]"],
        [
            "VPN adapter detected",
            f"[green]{vpn_adapter}[/green]" if vpn_adapter else "[yellow]None found[/yellow]",
        ],
    ]
    ui.render_table("VPN / Connectivity Check", ["Metric", "Result"], rows)

    if reachable and dns_ok:
        ui.print_success("Network connectivity looks healthy.")
        outcome = "SUCCESS" if vpn_adapter else "SUCCESS_NO_VPN_ADAPTER"
    elif reachable and not dns_ok:
        ui.print_warning("Internet is reachable but DNS resolution is failing.")
        outcome = "DEGRADED_DNS"
    else:
        ui.print_error("No internet connectivity detected.")
        outcome = "FAILED_UNREACHABLE"

    log_action("VPN_CHECK", "system", outcome)
    return {
        "reachable": reachable,
        "latency": latency,
        "dns_ok": dns_ok,
        "vpn_adapter": vpn_adapter,
    }

from pathlib import Path

import psutil

import ui
from actions.vpn import check_vpn
from logger import log_action


def _outlook_process():
    for proc in psutil.process_iter(["pid", "name"]):
        try:
            name = (proc.info["name"] or "").lower()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
        if "outlook" in name:
            return proc
    return None


def _flow_no_internet():
    ui.print_info("Step 1/3: Checking network interfaces and connectivity...")
    result = check_vpn()

    if not result["reachable"]:
        ui.print_error("Step 2/3: No internet connectivity detected.")
        ui.print_info(
            "Suggested actions: check the physical/Wi-Fi connection, restart the "
            "network adapter, or contact IT if the outage is site-wide."
        )
        return "FAILED_NO_CONNECTIVITY"

    if not result["dns_ok"]:
        ui.print_warning("Step 2/3: Connectivity is fine but DNS resolution failed.")
        ui.print_info("Suggested action: flush DNS cache or switch to 8.8.8.8 / 1.1.1.1.")
        return "DEGRADED_DNS"

    ui.print_success("Step 2/3: Connectivity and DNS both look healthy.")
    ui.print_info("Step 3/3: If the issue persists, it may be app-specific - try a different app or browser.")
    return "RESOLVED_NO_ISSUE_FOUND"


def _flow_outlook():
    ui.print_info("Step 1/2: Checking whether Outlook is currently running...")
    proc = _outlook_process()

    if proc is None:
        ui.print_warning("Outlook does not appear to be running.")
        ui.print_info("Suggested action: try launching Outlook again. If it still fails, try Outlook Safe Mode.")
        return "NOT_RUNNING"

    ui.print_success(f"Outlook is running (PID {proc.pid}).")
    if ui.confirm("Outlook appears unresponsive. Terminate and suggest a restart?"):
        try:
            proc.terminate()
            ui.print_success("Outlook process terminated. Please relaunch Outlook.")
            return "RESTARTED"
        except (psutil.NoSuchProcess, psutil.AccessDenied) as e:
            ui.print_error(f"Could not terminate Outlook: {e}")
            return "FAILED_TERMINATE"

    ui.print_info("No action taken.")
    return "NO_ACTION"


def _flow_slow_computer():
    ui.print_info("Step 1/3: Checking memory usage...")
    mem = psutil.virtual_memory()
    ui.render_table(
        "Memory Usage",
        ["Metric", "Value"],
        [
            ["Total", f"{mem.total / (1024 ** 3):.1f} GB"],
            ["Used", f"{mem.percent}%"],
            ["Available", f"{mem.available / (1024 ** 3):.1f} GB"],
        ],
    )

    ui.print_info("Step 2/3: Checking disk usage...")
    disk = psutil.disk_usage(str(Path.home().anchor))
    ui.render_table(
        "Disk Usage",
        ["Metric", "Value"],
        [
            ["Total", f"{disk.total / (1024 ** 3):.1f} GB"],
            ["Used", f"{disk.percent}%"],
            ["Free", f"{disk.free / (1024 ** 3):.1f} GB"],
        ],
    )

    ui.print_info("Step 3/3: Top 5 processes by memory usage...")
    procs = sorted(
        psutil.process_iter(["pid", "name", "memory_percent"]),
        key=lambda p: p.info.get("memory_percent") or 0,
        reverse=True,
    )[:5]
    rows = [
        [str(p.info["pid"]), p.info["name"] or "?", f"{(p.info['memory_percent'] or 0):.1f}%"]
        for p in procs
    ]
    ui.render_table("Top Processes (by memory)", ["PID", "Name", "Memory %"], rows)

    if mem.percent > 85 or disk.percent > 90:
        ui.print_warning("System resources are under heavy load - this likely explains the slowness.")
        return "HIGH_RESOURCE_USAGE"

    ui.print_info("Resource usage looks normal - the slowness may be app-specific or hardware-related.")
    return "NORMAL_USAGE"


def _flow_shared_drive():
    ui.print_info("Step 1/2: Checking network connectivity (shared drives require network access)...")
    result = check_vpn()

    if not result["reachable"]:
        ui.print_error("No network connectivity - this is likely why the shared drive is unreachable.")
        return "FAILED_NO_CONNECTIVITY"

    ui.print_success("Network connectivity looks fine.")
    ui.print_info("Step 2/2: Shared drive access often requires re-authentication.")
    username = ui.prompt("Enter your username to verify credentials: ").strip()
    if username:
        ui.print_info(f"Suggested action: reconnect the drive using credentials for '{username}', or contact IT if access was recently revoked.")
    return "GUIDED_CREDENTIAL_CHECK"


_FLOWS = {
    "no_internet": ("Can't connect to internet", _flow_no_internet),
    "outlook": ("Outlook not opening", _flow_outlook),
    "slow": ("Slow computer", _flow_slow_computer),
    "shared_drive": ("Can't access shared drive", _flow_shared_drive),
}


def troubleshoot(topic: str):
    if topic not in _FLOWS:
        ui.print_error(f"No guided flow found for '{topic}'.")
        log_action("TROUBLESHOOT", "system", f"FAILED_UNKNOWN_TOPIC:{topic}")
        return None

    title, flow_fn = _FLOWS[topic]
    ui.print_info(f"Starting guided troubleshooting: {title}")
    outcome = flow_fn()
    log_action("TROUBLESHOOT", "system", f"{topic}:{outcome}")
    return outcome

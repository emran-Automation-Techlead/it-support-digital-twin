import os
import platform
from pathlib import Path

import ui
from logger import log_action


def _temp_dirs() -> list[Path]:
    system = platform.system()
    dirs = []

    if system == "Windows":
        temp = os.environ.get("TEMP")
        if temp:
            dirs.append(Path(temp))
        windows_temp = Path(os.environ.get("SystemRoot", "C:\\Windows")) / "Temp"
        dirs.append(windows_temp)
    else:
        dirs.append(Path("/tmp"))
        dirs.append(Path.home() / ".cache")

    return [d for d in dirs if d.exists()]


def _dir_size_and_files(path: Path):
    total_size = 0
    files = []
    for root, _, filenames in os.walk(path):
        for name in filenames:
            file_path = Path(root) / name
            try:
                size = file_path.stat().st_size
            except (OSError, PermissionError):
                continue
            total_size += size
            files.append(file_path)
    return total_size, files


def scan_temp_dirs():
    dirs = _temp_dirs()
    report = {}

    with ui.spinner("Scanning temp directories..."):
        for d in dirs:
            size, files = _dir_size_and_files(d)
            report[d] = {"size": size, "files": files}

    rows = [
        [str(d), f"{info['size'] / (1024 * 1024):.2f} MB", str(len(info["files"]))]
        for d, info in report.items()
    ]
    ui.render_table("Temp File Report", ["Path", "Size", "File Count"], rows)
    return report


def cleanup():
    report = scan_temp_dirs()
    total_size = sum(info["size"] for info in report.values())

    if total_size == 0:
        ui.print_info("No temp files found to clean up.")
        log_action("DISK_CLEANUP", "system", "NOOP_EMPTY")
        return

    if not ui.confirm(
        f"Delete temp files across {len(report)} director(y/ies) "
        f"(~{total_size / (1024 * 1024):.2f} MB)?"
    ):
        ui.print_warning("Disk cleanup cancelled.")
        log_action("DISK_CLEANUP", "system", "CANCELLED")
        return

    reclaimed = 0
    skipped = 0

    with ui.spinner("Deleting temp files..."):
        for d, info in report.items():
            for file_path in info["files"]:
                try:
                    size = file_path.stat().st_size
                    file_path.unlink()
                    reclaimed += size
                except (PermissionError, OSError):
                    skipped += 1
                    continue

    ui.print_success(f"Reclaimed {reclaimed / (1024 * 1024):.2f} MB.")
    if skipped:
        ui.print_warning(f"Skipped {skipped} file(s) in use or permission-denied.")

    log_action(
        "DISK_CLEANUP",
        "system",
        f"SUCCESS:{reclaimed / (1024 * 1024):.2f}MB_reclaimed,{skipped}_skipped",
    )

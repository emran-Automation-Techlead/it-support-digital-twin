import data_store
import ui
from logger import log_action

_STATUS_COLOR = {
    "active": "green",
    "locked": "red",
    "inactive": "yellow",
    "expired": "red",
}


def check_status(username: str):
    with ui.spinner(f"Querying account status for '{username}'..."):
        user = data_store.find_user(username)

    if user is None:
        ui.print_error(f"User '{username}' not found.")
        log_action("ACCOUNT_STATUS", username, "FAILED_NOT_FOUND")
        return

    color = _STATUS_COLOR.get(user["status"], "white")
    ui.render_table(
        f"Account Status - {user['full_name']}",
        ["Field", "Value"],
        [
            ["Username", user["username"]],
            ["Email", user["email"]],
            ["Status", f"[{color}]{user['status']}[/{color}]"],
            ["Department", user["department"]],
            ["Password Expires", user["password_expires"]],
            ["Last Login", user["last_login"]],
        ],
    )
    log_action("ACCOUNT_STATUS", username, "SUCCESS")


def unlock_account(username: str):
    with ui.spinner(f"Checking lock status for '{username}'..."):
        user = data_store.find_user(username)

    if user is None:
        ui.print_error(f"User '{username}' not found.")
        log_action("ACCOUNT_UNLOCK", username, "FAILED_NOT_FOUND")
        return

    if user["status"] != "locked":
        ui.print_info(
            f"{user['full_name']} ({user['username']}) is not locked "
            f"(current status: {user['status']})."
        )
        log_action("ACCOUNT_UNLOCK", username, "NOOP_NOT_LOCKED")
        return

    if not ui.confirm(f"Unlock account for {user['full_name']} ({user['username']})?"):
        ui.print_warning("Account unlock cancelled.")
        log_action("ACCOUNT_UNLOCK", username, "CANCELLED")
        return

    with ui.spinner("Unlocking account..."):
        data_store.update_user(username, status="active")

    ui.print_success(f"Account unlocked for {user['full_name']} ({user['username']}).")
    log_action("ACCOUNT_UNLOCK", username, "SUCCESS")

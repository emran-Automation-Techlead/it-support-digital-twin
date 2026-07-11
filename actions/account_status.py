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

import secrets
import string

import data_store
import ui
from logger import log_action


def _generate_temp_password(length: int = 12) -> str:
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
    return "".join(secrets.choice(alphabet) for _ in range(length))


def reset_password(username: str):
    with ui.spinner(f"Looking up '{username}' in AD/LDAP..."):
        user = data_store.find_user(username)

    if user is None:
        ui.print_error(f"User '{username}' not found.")
        log_action("PASSWORD_RESET", username, "FAILED_NOT_FOUND")
        return

    if not ui.confirm(f"Reset password for {user['full_name']} ({user['username']})?"):
        ui.print_warning("Password reset cancelled.")
        log_action("PASSWORD_RESET", username, "CANCELLED")
        return

    with ui.spinner("Generating temporary password..."):
        temp_password = _generate_temp_password()
        data_store.update_user(username, status="active")

    ui.print_success(f"Password reset for {user['full_name']} ({user['username']}).")
    ui.print_info(f"Temporary password: [bold]{temp_password}[/bold]")
    ui.print_warning("User must change this password on next login.")
    log_action("PASSWORD_RESET", username, "SUCCESS")

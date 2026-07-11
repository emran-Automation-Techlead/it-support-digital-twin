from datetime import datetime

import data_store
import ui
from logger import log_action

VALID_PRIORITIES = ["Low", "Medium", "High", "Critical"]
VALID_CATEGORIES = ["Network", "Hardware", "Software", "Account", "Other"]


def _next_ticket_id() -> str:
    today = datetime.now().strftime("%Y%m%d")
    tickets = data_store.load_tickets()
    prefix = f"IT-{today}-"
    todays_count = sum(1 for t in tickets if t["ticket_id"].startswith(prefix))
    return f"{prefix}{todays_count + 1:04d}"


def _prompt_choice(label: str, options: list[str]) -> str:
    options_str = "/".join(options)
    while True:
        answer = ui.prompt(f"{label} ({options_str}): ").strip()
        for opt in options:
            if answer.lower() == opt.lower():
                return opt
        ui.print_warning(f"Please choose one of: {options_str}")


def create_ticket(reported_by: str, description: str | None = None):
    ui.print_info("Let's create an IT support ticket.")

    if not description:
        description = ui.prompt("Describe the issue: ").strip()
        while not description:
            ui.print_warning("Description cannot be empty.")
            description = ui.prompt("Describe the issue: ").strip()

    priority = _prompt_choice("Priority", VALID_PRIORITIES)
    category = _prompt_choice("Category", VALID_CATEGORIES)

    user = data_store.find_user(reported_by)
    email = user["email"] if user else ui.prompt("Your email: ").strip()

    with ui.spinner("Filing ticket..."):
        ticket = {
            "ticket_id": _next_ticket_id(),
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "reported_by": reported_by,
            "email": email,
            "category": category,
            "priority": priority,
            "description": description,
            "status": "Open",
        }
        data_store.add_ticket(ticket)

    ui.print_success(f"Ticket created: {ticket['ticket_id']}")
    ui.render_table(
        "Ticket Summary",
        ["Field", "Value"],
        [
            ["Ticket ID", ticket["ticket_id"]],
            ["Reported By", reported_by],
            ["Email", email],
            ["Category", category],
            ["Priority", priority],
            ["Description", description],
            ["Status", ticket["status"]],
        ],
    )
    log_action("CREATE_TICKET", reported_by, f"SUCCESS:{ticket['ticket_id']}")
    return ticket

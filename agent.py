import re
from enum import Enum

import ui
from actions import account, disk, password, tickets, troubleshoot, vpn
from supervisor import detect_trigger


class Intent(Enum):
    PASSWORD_RESET = "PASSWORD_RESET"
    ACCOUNT_UNLOCK = "ACCOUNT_UNLOCK"
    ACCOUNT_STATUS = "ACCOUNT_STATUS"
    VPN_CHECK = "VPN_CHECK"
    DISK_CLEANUP = "DISK_CLEANUP"
    CREATE_TICKET = "CREATE_TICKET"
    TROUBLESHOOT = "TROUBLESHOOT"
    UNKNOWN = "UNKNOWN"


# Ordered most-specific-first: multi-word phrases before single keywords,
# so "unlock my vpn" doesn't get misrouted to ACCOUNT_UNLOCK.
_RULES: list[tuple[Intent, list[str]]] = [
    (Intent.TROUBLESHOOT, [
        "can't connect to internet", "cant connect to internet", "no internet",
        "outlook not opening", "outlook won't open", "outlook wont open",
        "slow computer", "computer is slow", "pc is slow",
        "can't access shared drive", "cant access shared drive", "shared drive",
    ]),
    (Intent.VPN_CHECK, ["vpn", "connectivity", "ping", "network connection"]),
    (Intent.PASSWORD_RESET, ["reset password", "forgot password", "password reset", "new password"]),
    (Intent.ACCOUNT_UNLOCK, ["unlock account", "unlock my account", "account locked", "unlock user"]),
    (Intent.ACCOUNT_STATUS, ["account status", "status of", "check account", "is my account"]),
    (Intent.DISK_CLEANUP, ["clean up temp", "disk cleanup", "clean temp files", "free up space", "temp files"]),
    (Intent.CREATE_TICKET, ["create a ticket", "create ticket", "open a ticket", "file a ticket", "submit a ticket"]),
]

_TROUBLESHOOT_TOPIC = {
    "can't connect to internet": "no_internet",
    "cant connect to internet": "no_internet",
    "no internet": "no_internet",
    "outlook not opening": "outlook",
    "outlook won't open": "outlook",
    "outlook wont open": "outlook",
    "slow computer": "slow",
    "computer is slow": "slow",
    "pc is slow": "slow",
    "can't access shared drive": "shared_drive",
    "cant access shared drive": "shared_drive",
    "shared drive": "shared_drive",
}


def detect_intent(text: str) -> tuple[Intent, str | None]:
    lowered = text.lower().strip()
    for intent, phrases in _RULES:
        for phrase in phrases:
            if phrase in lowered:
                matched_topic = _TROUBLESHOOT_TOPIC.get(phrase)
                return intent, matched_topic
    return Intent.UNKNOWN, None


def _extract_username(text: str) -> str | None:
    match = re.search(r"\bfor\s+(\w+)", text, re.IGNORECASE)
    if match:
        return match.group(1)
    match = re.search(r"\bof\s+(\w+)", text, re.IGNORECASE)
    if match:
        return match.group(1)
    words = text.strip().split()
    if words:
        return words[-1]
    return None


class Agent:
    def handle(self, text: str):
        response = detect_trigger(text)
        if response:
            ui.print_info(response)

        intent, topic = detect_intent(text)

        if intent == Intent.PASSWORD_RESET:
            username = ui.prompt("Username to reset: ").strip()
            return password.reset_password(username)

        if intent == Intent.ACCOUNT_UNLOCK:
            username = ui.prompt("Username to unlock: ").strip()
            return account.unlock_account(username)

        if intent == Intent.ACCOUNT_STATUS:
            username = _extract_username(text) or ui.prompt("Username to check: ").strip()
            return account.check_status(username)

        if intent == Intent.VPN_CHECK:
            return vpn.check_vpn()

        if intent == Intent.DISK_CLEANUP:
            return disk.cleanup()

        if intent == Intent.CREATE_TICKET:
            reported_by = ui.prompt("Your username: ").strip()
            return tickets.create_ticket(reported_by)

        if intent == Intent.TROUBLESHOOT:
            return troubleshoot.troubleshoot(topic)

        ui.print_warning("I didn't understand that - let's file a support ticket instead.")
        reported_by = ui.prompt("Your username: ").strip()
        return tickets.create_ticket(reported_by, description=text)

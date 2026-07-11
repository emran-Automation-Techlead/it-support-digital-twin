# IT Support Digital Twin

A terminal-based, offline IT support agent. Type an issue in plain English and it
routes to the right action: password reset, account unlock, VPN/connectivity
check, disk cleanup, ticket creation, or a guided troubleshooting flow.

No external APIs, no database — everything runs locally against mock JSON data.

## Setup

```bash
pip install -r requirements.txt
python main.py
```

Requires Python 3.10+.

## Example session

```
You: check if my VPN is connected
You: what's the status of jsmith
You: clean up temp files
You: I can't open Outlook
You: create a ticket
You: exit
```

## Features

- **Natural language intent detection** — keyword/pattern based, no LLM calls
- **Password reset** — mock AD/LDAP lookup, generates a temp password
- **Account unlock** — checks and clears locked status
- **Account status** — full health summary (status, department, password expiry, last login)
- **VPN / connectivity check** — real `ping` to 8.8.8.8, DNS resolution, scans
  network interfaces for VPN adapter names (tun, tap, vpn, cisco, globalprotect, etc.)
- **Disk cleanup** — scans temp directories (`%TEMP%`, `C:\Windows\Temp` on
  Windows; `/tmp`, `~/.cache` on Linux/macOS), reports size, deletes on
  confirmation, reports space reclaimed
- **Ticket creation** — collects description/priority/category, generates an
  `IT-YYYYMMDD-XXXX` ticket ID, saved to `data/tickets.json`
- **Guided troubleshooting** — step-by-step flows for: can't connect to
  internet, Outlook not opening, slow computer, can't access shared drive

## Project structure

```
main.py                   entry point / input loop
agent.py                  intent detection + routing
ui.py                     rich UI helpers (panels, tables, spinners, colors)
logger.py                 logging setup -> logs/it_support.log
data_store.py             JSON read/write for users & tickets
actions/
  password.py
  unlock.py
  account_status.py
  vpn.py
  disk.py
  ticket.py
  troubleshoot.py
data/
  users.json               10 mock users (active/locked/inactive/expired)
  tickets.json              ticket store, starts empty
logs/
  it_support.log            action log (timestamp | action | username | outcome)
```

## Notes

- All destructive actions (unlock account, reset password, delete temp files)
  require an explicit `y/N` confirmation before executing.
- Every action is logged to `logs/it_support.log`.
- Unrecognized input falls back to ticket creation with the original text
  pre-filled as the description.

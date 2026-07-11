# IT Support Digital Twin

A terminal-based, offline-first IT support agent with two interfaces:

- **Text Mode** — type an issue in plain English, routed by keyword-based
  intent detection to the right action.
- **Voice Mode** — talk to "Alex," an ElevenLabs Conversational AI agent,
  via the ElevenLabs web widget opened in your browser.

Password resets, account unlocks, VPN/connectivity checks, disk cleanup,
ticket creation, and guided troubleshooting all run locally against mock
JSON data — no external APIs required except for Voice Mode.

## Setup

```bash
git clone https://github.com/emran-Automation-Techlead/it-support-digital-twin.git
cd it-support-digital-twin
pip install -r requirements.txt
cp .env.example .env
```

Then open `.env` and add your ElevenLabs agent ID:

```
ELEVENLABS_AGENT_ID=your_elevenlabs_agent_id_here
```

`ELEVENLABS_API_KEY` is optional — the web widget only needs the agent ID.

Run it:

```bash
python main.py
```

Requires Python 3.10+. Voice Mode opens a local HTML file in your default
browser; the widget itself handles microphone/speaker access.

## Startup menu

```
╔══════════════════════════════════╗
║   IT Support Digital Twin        ║
║   Powered by ElevenLabs          ║
╚══════════════════════════════════╝

[1] Text Mode
[2] Voice Mode (Alex - ElevenLabs)
```

If `ELEVENLABS_AGENT_ID` is missing from `.env`, Voice Mode prints a warning
and exits back cleanly instead of crashing — it never fails silently or
partially connects.

## Features

- **Natural language intent detection** — keyword/pattern based, no LLM calls
- **Password reset** — mock AD/LDAP lookup, generates a temp password
- **Account status & unlock** — health summary plus locked-account clearing
- **VPN / connectivity check** — real `ping` to 8.8.8.8, DNS resolution, scans
  network interfaces for VPN adapter names (tun, tap, vpn, cisco, globalprotect, etc.)
- **Disk cleanup** — scans temp directories (`%TEMP%`, `C:\Windows\Temp` on
  Windows; `/tmp`, `~/.cache` on Linux/macOS), reports size, deletes on
  confirmation, reports space reclaimed
- **Ticket creation** — collects description/priority/category, generates an
  `IT-YYYYMMDD-XXXX` ticket ID, saved to `data/tickets.json`
- **Guided troubleshooting** — step-by-step flows for: can't connect to
  internet, Outlook not opening, slow computer, can't access shared drive
- **Voice Mode** — opens the ElevenLabs Conversational AI web widget in your
  default browser for a full-duplex voice conversation with "Alex"

## Project structure

```
main.py                   entry point, mode selector
agent.py                  intent detection + routing (text mode)
ui.py                     rich UI helpers (panels, tables, spinners, colors)
logger.py                 logging setup -> logs/it_support.log
data_store.py             JSON read/write for users & tickets
voice/
  elevenlabs_agent.py      loads .env, renders widget.html, opens it in the browser
  widget.html               ElevenLabs web widget template (placeholder agent-id)
  widget_rendered.html      generated at runtime with your real agent-id (gitignored)
actions/
  password.py
  account.py               status check + unlock
  vpn.py
  disk.py
  tickets.py
  troubleshoot.py
data/
  users.json               10 mock users (active/locked/inactive/expired)
  tickets.json              ticket store (gitignored, generated locally)
logs/                       action log (gitignored)
.env.example                 placeholder credentials, safe to commit
.env                         your real credentials, gitignored — never commit
```

## Security notes

- **Never commit `.env`.** It's excluded via `.gitignore` from the very
  first commit. Only `.env.example` (empty placeholders) is tracked.
- **No API key required for Voice Mode.** The web widget authenticates
  with just the public agent ID, so there's no server-side secret to
  protect for this feature.
- All destructive actions (unlock account, reset password, delete temp
  files) require an explicit `y/N` confirmation before executing.
- Every state-changing action is logged to `logs/it_support.log`
  (timestamp | action | username | outcome).
- Unrecognized text input falls back to ticket creation with the original
  text pre-filled as the description — nothing is silently dropped.

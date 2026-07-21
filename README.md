# 🤖 IT Support Digital Twin — Powered by ElevenLabs & AI

## Overview

A fully functional AI-powered IT Support agent named **Imran** that handles
real IT support tasks via voice and text. Built with Python and ElevenLabs
Conversational AI.

## ✅ Features

- Voice mode powered by ElevenLabs (Imran - AI IT Support Agent)
- Text mode for terminal-based interaction
- Supervisor-debate trigger detection — recognizes impossible timelines,
  repeated unresolved issues, security-bypass requests, system-blame
  language, and users abandoning the conversation, and responds with an
  appropriate acknowledgment before continuing
- Password reset workflow (mock AD/LDAP lookup, generates a temp password)
- Account unlock and status check
- VPN connectivity diagnostics — real `ping` to 8.8.8.8, DNS resolution,
  scans network interfaces for VPN adapter names (tun, tap, vpn, cisco,
  globalprotect, etc.)
- Disk cleanup and temp file removal — scans temp directories, reports size,
  deletes on confirmation, reports space reclaimed
- IT ticket creation with auto-generated ticket IDs (`IT-YYYYMMDD-XXXX`)
- Step-by-step guided troubleshooting — no internet, Outlook not opening,
  slow computer, can't access shared drive
- Full audit logging of all actions
- Mock user directory with realistic data (10 users: active/locked/inactive/expired)

## 🏗️ Architecture

```
user
  -> main.py                (entry point, mode selector)
       -> agent.py           (supervisor triggers + intent detection, Text Mode)
            -> actions/*.py  (password, account, vpn, disk, tickets, troubleshoot)
                 -> data_store.py (JSON read/write)
                      -> data/*.json
            -> logger.py     -> logs/it_support.log
       -> voice/elevenlabs_agent.py (Voice Mode: opens ElevenLabs widget)
```

## 🚀 Quick Start

1. `git clone https://github.com/emran-Automation-Techlead/it-support-digital-twin.git`
2. `cd it-support-digital-twin`
3. `pip install -r requirements.txt`
4. `cp .env.example .env`
5. Add your ElevenLabs API key and Agent ID to `.env`
6. `python main.py`
7. Choose Text Mode or Voice Mode

## 📁 Project Structure

```
main.py                   entry point, mode selector
agent.py                  supervisor triggers + intent detection/routing (text mode)
supervisor.py             regex-based trigger detection for difficult conversational patterns
ui.py                     rich UI helpers (panels, tables, spinners, colors)
logger.py                 logging setup -> logs/it_support.log
data_store.py             JSON read/write for users & tickets
voice/
  elevenlabs_agent.py      loads .env, renders widget.html, opens it in the browser
  widget.html               ElevenLabs web widget template (placeholder agent-id)
  widget_rendered.html      generated at runtime with your real agent-id (gitignored)
actions/
  password.py              password reset
  account.py                status check + unlock
  vpn.py                    connectivity diagnostics
  disk.py                   temp file scan + cleanup
  tickets.py                ticket creation
  troubleshoot.py           guided troubleshooting flows
data/
  users.json               10 mock users (active/locked/inactive/expired)
  tickets.json              ticket store (gitignored, generated locally)
logs/                       action log (gitignored)
.env.example                 placeholder credentials, safe to commit
.env                         your real credentials, gitignored — never commit
```

## 🎙️ Voice Agent (Imran)

- Powered by ElevenLabs Conversational AI
- Handles: password resets, account unlocks, VPN checks,
  disk cleanup, ticket creation, troubleshooting
- Natural conversation flow with confirmation steps
- Escalates to a senior technician after 2 failed attempts (configured in
  Imran's ElevenLabs system prompt)

## 🔒 Security

- All credentials loaded from `.env` file
- `.env` is gitignored — never committed, from the very first commit
- No API key required for Voice Mode — the web widget authenticates with
  just the public agent ID
- Destructive actions (unlock account, reset password, delete temp files)
  require explicit `y/N` confirmation before executing
- Full audit trail in `logs/` (timestamp | action | username | outcome)

## 🛠️ Tech Stack

- Python 3.10+
- ElevenLabs Conversational AI
- rich (terminal UI)
- psutil (system diagnostics)
- python-dotenv

## 📸 Screenshots

[Screenshot of text mode]

[Screenshot of voice mode]

## 🎬 Demo Video

[▶️ Watch the demo](assets/videos/imran-voice-agent-demo.mp4) — Imran handling
IT support requests via voice.

## 📊 Presentation

[📑 Project overview deck](assets/IT_Support_Digital_Twin_Overview.pptx) —
title, features, architecture, voice agent, tech stack, security, and demo.

## 📄 License

MIT

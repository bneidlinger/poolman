# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Poolman is a Bitcoin mining operations dashboard ("TangNet Mining Ops") — a Flask app that aggregates live stats from two mining pools (CKPool and Public Pool) and displays them in a terminal-style web UI. Designed to run as a kiosk on a Raspberry Pi 5 with a small dedicated screen.

## Running the App

```bash
pip install -r requirements.txt
BTC_ADDRESS="your_btc_address" python app.py
```

The server starts on `http://0.0.0.0:5000`. The dashboard auto-refreshes via AJAX every 30 seconds.

## Architecture

```
app.py              — Flask backend: serves the page + JSON API endpoints
templates/
  index.html        — Dashboard HTML/CSS/JS (Jinja2 template, AJAX polling)
requirements.txt    — Python dependencies
poolman.service     — systemd unit file for auto-start on Pi boot
start-kiosk.sh      — Script to launch Chromium in kiosk mode
```

- **Framework**: Flask with `render_template` (template in `templates/index.html`)
- **Config**: `BTC_ADDRESS` loaded from environment variable, falls back to `"YOUR_ADDRESS"`
- **Data sources** (queried via JSON API routes, proxied through Flask):
  - CKPool (solo mining): `https://solo.ckpool.org/users/{BTC_ADDRESS}` — may return NDJSON
  - Public Pool (NerdMiners/Bitaxe): `https://public-pool.io:40557/api/client/{BTC_ADDRESS}`
  - Public Pool network info: `https://public-pool.io:40557/api/network`
- **API routes**: `GET /api/ckpool`, `GET /api/publicpool`, `GET /api/network`
- **Frontend**: Dark terminal aesthetic (green-on-black monospace), vanilla JS AJAX polling, responsive down to 480px

## Pi Deployment

1. Copy files to the Pi
2. Edit `poolman.service`: set `BTC_ADDRESS`, `User`, and `WorkingDirectory`
3. `sudo cp poolman.service /etc/systemd/system/ && sudo systemctl enable --now poolman`
4. Add `start-kiosk.sh` to autostart (e.g., via desktop autostart or systemd)

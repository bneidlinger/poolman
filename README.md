# POOLMAN

### `OPERATION TANGNET` // CLASSIFIED: DIMENSION C-137

> *"Listen Morty, mining Bitcoin solo is like trying to find a specific grain of sand on every beach in the multiverse. But we're doing it anyway because we're not cowards."*
> — Rick Sanchez, C-137

A Bitcoin solo mining dashboard for the beautifully delusional. Aggregates live stats from [CKPool](https://solo.ckpool.org) and [Public Pool](https://public-pool.io) into a terminal-style command center that makes your mass of 500 GH/s miners feel like an interdimensional covert operation.

## Dashboards

### `/` — Pi Dashboard (Kiosk Mode)

The original. Green-on-black terminal aesthetic designed for a Raspberry Pi 5 with a small screen. Tabbed interface (All / CKPool / Public Pool), auto-refreshes every 30 seconds, responsive down to 480px. No frills. Just numbers.

### `/lab` — Lab Dashboard (Operation TangNet)

The fun one. A three-panel command center themed as a mashup of *Rick and Morty*'s chaotic lab and *The Patriot*'s dry spy humor. Designed for a 16" monitor on a mini PC.

**Features:**
- **Mission Briefing** — Network difficulty, block height, combined hashrate, pool source cards
- **Field Operatives** — Worker "dossier" cards with codenames (Pickle Rick, Evil Morty, Lakeman, etc.), pool badges, ACTIVE/DARK status, clearance levels
- **Interdimensional Odds Calculator** — Calculates your probability of finding a block, converts expected time to years, maps it to a historical era, and roasts you with a Rick quote
- **Portal Timeline** — A snake-pattern visualization mapping your expected wait across 20 milestones from the Big Bang to present day, with a spinning portal marker showing where you'd land. Spoiler: it's usually somewhere between the Pyramids and the invention of fire

## Quick Start

```bash
pip install -r requirements.txt
```

Create a `.env` file:
```
BTC_ADDRESS=your_btc_address_here
```

Run:
```bash
python app.py
```

Open `http://localhost:5000` (Pi dashboard) or `http://localhost:5000/lab` (lab dashboard).

## Architecture

```
app.py              — Flask backend: API proxy + page routes
templates/
  index.html        — Pi dashboard (inline CSS/JS)
  lab.html          — Lab dashboard (inline CSS/JS)
requirements.txt    — Python dependencies (Flask, requests)
poolman.service     — systemd unit for Pi auto-start
start-kiosk.sh      — Chromium kiosk launcher
.env                — BTC_ADDRESS (not committed, obviously)
```

**Data sources** (proxied through Flask):
- CKPool: `https://solo.ckpool.org/users/{BTC_ADDRESS}`
- Public Pool: `https://public-pool.io:40557/api/client/{BTC_ADDRESS}`
- Network info: `https://public-pool.io:40557/api/network`

**API routes:** `GET /api/ckpool` `GET /api/publicpool` `GET /api/network`

No database. No auth. No WebSockets. Just three fetch calls on a 30-second loop and a mass of CSS that would make a design system engineer cry.

## Pi Deployment

1. Copy files to the Pi
2. Create `.env` with your `BTC_ADDRESS`
3. Edit `poolman.service` — set `User` and `WorkingDirectory`
4. ```bash
   sudo cp poolman.service /etc/systemd/system/
   sudo systemctl enable --now poolman
   ```
5. Add `start-kiosk.sh` to autostart for Chromium kiosk mode

## The Math (Odds Calculator)

```
expected_seconds = (network_difficulty * 2^32) / your_hashrate
```

With ~2.35 TH/s against ~113T difficulty, you're looking at roughly 4,500 years. The dashboard helpfully informs you that if you started mining when the Mesopotamians were building their first cities, you *might* have a block by now.

Each era on the timeline comes with a Rick Sanchez quote calibrated to maximize existential despair about your hashrate.

## Why

Because solo mining Bitcoin with consumer hardware is objectively irrational, and if you're going to do something irrational, you should at least have a cool dashboard for it.

---

*Built with mass delusion and mass electricity by the TangNet Mining Command.*

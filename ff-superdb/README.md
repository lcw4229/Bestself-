# 🏈 FF SuperDB — Fantasy Football Super Database

A single-file PWA that **syncs and unifies all your fantasy football leagues**
(Sleeper + ESPN) into one offline-capable database on your device. No server, no
account, no API key — everything runs in your browser and is stored locally.

## What "sync" means here

Yes — you sync your leagues into the app. Here's exactly how:

1. **Sleeper (primary).** Open **Settings**, type your Sleeper username, and tap
   **Connect & load my leagues**. The app calls Sleeper's public read API, finds
   every league on your account for the current season, and lets you pick which
   ones to track (your 3). Once tracked, it pulls **standings, rosters, matchups,
   records, and points** for each league.
2. **ESPN (your 4th league).** Add it in Settings by League ID + season.
   - *Public* ESPN leagues sync automatically.
   - *Private* ESPN leagues can't be read directly by any browser app (ESPN
     doesn't send its login cookies to other websites — a browser security
     rule, not a bug). For those, use **Import JSON**: the app gives you a URL to
     open while logged into espn.com, and you paste the resulting JSON in once.
     It's then stored on-device like everything else.
3. **Refresh = re-sync.** Data is fetched live each time you open a view, so
   scores and standings stay current. Tap a view again (or **Refresh player
   database** in Settings) to pull the latest. Nothing is stale-cached except the
   app shell (so it opens offline).

The player database (~11k NFL players) is synced once and cached in IndexedDB,
then refreshed roughly daily.

## Features

- **Dashboard** — cross-league "super" view: combined W-L, win rate, all your
  teams, this week's matchups, and **player exposure** (who you roster across
  multiple leagues).
- **Leagues** — standings, full rosters (starters + bench), and weekly matchups
  for every synced league.
- **Players** — searchable/filterable database of every NFL player with
  position, team, injury status, depth chart, age, experience, and which of your
  teams roster them.
- **Trending** — most-added / most-dropped players across Sleeper (24h waiver
  signal).

## Data sources

- **Sleeper** — `https://api.sleeper.app/v1` (public, CORS-enabled, no key).
- **ESPN** — `https://lm-api-reads.fantasy.espn.com` (public leagues) or manual
  JSON import (private leagues).

All league data lives only in your browser (`localStorage` + `IndexedDB`).
Nothing is transmitted to any third party beyond the official Sleeper/ESPN APIs.

## Running it

It's a static site — no build step.

```bash
# from the ff-superdb/ folder
python3 -m http.server 8080
# then open http://localhost:8080
```

Or deploy the `ff-superdb/` folder to any static host (GitHub Pages, Netlify,
etc.) and "Add to Home Screen" on your phone to install it as an app.

> Note: this project is intentionally separate from the "Best Self" tracker that
> also lives in this repo. FF SuperDB is entirely self-contained in this folder.

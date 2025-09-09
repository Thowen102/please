# PuffQuest Advance (GBA)
A Kirby‑like **infinite, procedurally generated** side‑scrolling platformer for **Game Boy Advance**. Built with **Butano** + **devkitARM**. One‑click build via GitHub Actions.


## Zero‑setup build (GitHub)
1. Create a new public or private repo.
2. Copy all files from this README into matching paths.
3. Push to `main`. Open **Actions** → **Build GBA ROM** → download artifact `PuffQuestAdvance.gba`.
4. Run in **mGBA** or on hardware (flashcart).


## Local build (optional, advanced)
- Install devkitPro/devkitARM, clone Butano, set `LIBBUTANO` env pointing to `.../butano/butano`, then `make`.


## Controls
- D‑Pad: Move / Aim
- A: Jump (hold for variable height)
- B: Attack (power‑up alters attack)
- L: Dash (if Dash power‑up active)
- Start: Pause/Resume (Options: Music/SFX toggle, FPS, Quit)
- Select: Seed reset (on Title)


## Gameplay
- Endless auto‑scroll to the right. Survive, collect **coins**, defeat **enemies**, avoid **spikes**.
- **Power‑ups** (timed): *Dash*, *Fire* (projectile), *Spark* (short‑range arc), *Stone* (ground‑slam).
- **Score**: distance + coins + enemy streak multipliers. **High score** saved to SRAM.


## Assets & Licenses (auto‑fetched by script)
- Player: **ExplorerHero (32x32)** — CC0.
- Enemies: **Assorted 32x32 creatures** — CC0.
- Tiles/coins: **Grass tiles 32x32** — CC0.
- SFX: **512 8‑bit style SFX** — CC0 (subset used: jump, collect, hit, pause).


Credits are compiled in `CREDITS.md`. All third‑party art/audio remain under their original licenses; code is MIT.


## Tech
- Engine: **Butano** (C++ GBA engine). See docs on importing assets & audio.
- CI: **devkitPro Docker** for reproducible builds.


## Extending
- Add BMP+JSON under `graphics/` and WAV under `audio/`. See `tools/fetch_assets.py` for examples.

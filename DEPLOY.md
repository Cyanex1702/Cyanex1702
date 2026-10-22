# CYANEX1702 / CATHODE GHOST — Deploy

This is a drop-in **GitHub profile README** built with animated GIFs and Markdown-compatible HTML. It does NOT contain featured project cards. Project details belong exclusively in GitHub's native Repositories tab, not this profile.

## Safest install: clone, copy, push

1. Back up your existing profile repository or create a new branch before copying files.
2. Clone your profile repo:

   ```bash
   git clone https://github.com/Cyanex1702/Cyanex1702.git
   cd Cyanex1702
   ```
3. Copy **README.md** and the **contents** of **assets/** from this archive into your cloned repository root. Keep `.git/` untouched. This replaces the displayed profile without touching any of your other repositories.
4. To keep the real contribution snake refreshing, also copy `.github/workflows/snake.yml` (if your existing workflow is configured differently, compare rather than overwrite).
5. Commit and push:

   ```bash
   git add README.md assets .github/workflows/snake.yml
   git commit -m "style: restore animated cathode-ray personal profile"
   git push origin main
   ```
6. Visit `https://github.com/Cyanex1702`.
7. Optionally go to **Actions -> Generate Matrix Contribution Snake -> Run workflow**. GitHub Actions might need enabling. The workflow needs **Settings -> Actions -> General -> Workflow permissions -> Read and write permissions** to commit the generated snake SVG files.

## How animation works

- The right-side radar in `crt-boot.gif` now displays your **uploaded winged emblem** instead of the original `C` glyph. The source artwork is `assets/cyanex-winged-emblem.png`; it is preserved in the ZIP.
- Four locally rendered GIFs drive the main visual experience: `crt-boot.gif`, `whoami-console.gif`, `neural-topology.gif`, and `specs-rack.gif`.
- Four small original animations add CRT ambience: `packet-bus-v3.gif`, `analog-sync-v3.gif`, `signal-rack-v3.gif`, `carrier-sync.gif`.
- `snake-daemon.gif` is the local decorative snake; `github-snake*.svg` are the GitHub contribution snake assets, refreshed by a workflow.
- GitHub sanitizes active HTML/JS. The pre-rendered GIF approach is intentional and works on GitHub profile READMEs. The external typing header and shields are optional extras.
- **No live fictional skill values:** the animated bars in `specs-rack.gif` represent moving channel signal, not scores or proficiency percentages.

## Updating details

Edit the text under `> 00 / WHOAMI`, the `> 02 / LSHW` skills block, and the operator manual in `README.md`. Image text is baked into GIFs. A reproducible (optional) renderer is in `scripts/render_crt.py`, using Pillow, NumPy, and locally installed Inter and DejaVu Sans Mono fonts. To regenerate the GIFs, run `pip install pillow numpy` then `python scripts/render_crt.py` in an environment with those fonts. The rendered GIFs are already included: you do not need Python just to deploy.

Avoid re-adding project listings here; the native Repositories tab is there when visitors want to explore.

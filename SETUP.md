# CYANEX1702 // SIGNAL NOIR — PERSONAL EDITION

This is a **GitHub profile README about the person behind the code**, not a portfolio of individual repositories. It includes an animated identity hero, an illustrated operator file, a skill constellation, a technical-specification panel, an engineering philosophy display, and an optional contribution snake.

**No individual projects, project links, cards, or repository data panels appear in the README.** The only repository navigation is one subtle footer link to GitHub's dedicated repositories tab.

## Install

1. Back up the contents of your current `Cyanex1702/Cyanex1702` profile repository.
2. Copy `README.md`, `assets/`, and `.github/workflows/snake.yml` from this package to the matching locations in your profile repository. You may also keep the script and the local `PREVIEW.html` for maintenance.
3. Remove the **old README's project showcase**, obsolete `assets/project-*.svg` artwork, and the old `live-assets.yml` workflow and live telemetry generator if you no longer use them; this package deliberately excludes them.
4. Commit and push. Open `https://github.com/Cyanex1702` in a browser to check appearance in both dark and light modes.
5. To refresh the contribution snake, run the `Generate Matrix Contribution Snake` action once from the Actions tab. Scheduled refreshes will continue. This workflow uses `contents: write` to commit updated SVGs; ensure your repository permits that workflow to push.

## Personalizing the content

- All personal claims are based on the previously supplied README's skills and philosophy. No biography, years of experience, location, employer, hardware specifications, or credentials have been invented.
- Edit `README.md` to update the introduction, preferences, or technical stack.
- Artwork is SVG stored in `assets/` and can be regenerated with `python scripts/build_identity_art.py` (standard-library only).
- `assets/operator-spec.svg`, `assets/hero-signal.gif`, and `assets/final-signal.svg` are reused from the earlier SIGNAL NOIR build. Edit these manually if your stack or message changes.
- `README-STATIC.md` is an optional motion-reduced alternative. To use it, copy its contents over `README.md` (it replaces the animated intro with the static poster). The contribution snake still animates in supporting browsers; remove that section if you want fully static imagery.

## Notes

The local `PREVIEW.html` approximates GitHub's Markdown and dark colors. GitHub may render some HTML, spacing, badges or SVG text slightly differently; always check the real profile after publication.

The GitHub Actions snake can show cached contribution values until a workflow successfully runs. No private data is requested or embedded.

# CYANEX1702 MATRIX-ANALOG // ULTIMATE

This is the full terminal-artifact edition.

## Included

- custom animated CRT / Matrix hero
- packet bus ticker
- GEN-AI / VISION / RAG signal rack
- custom NEOFETCH terminal panel
- custom live GitHub telemetry panel
- dynamic LAST_PACKET public event panel
- hardware-style LSHW stack inventory
- local SNAKE.DAEMON animation
- real GitHub contribution snake
- live Matrix-style contribution calendar
- animated system topology / packet-routing map
- MAN CYANEX1702 easter egg
- carrier / tape sync effects
- uppercase terminal typography system

## Automated workflows

### `Generate Matrix Contribution Snake`
Creates:
- `assets/github-snake.svg`
- `assets/github-snake-dark.svg`

### `Refresh Live Terminal Assets`
Refreshes every 6 hours:
- `assets/terminal-telemetry.svg`
- `assets/neofetch.svg`
- `assets/last-packet.svg`
- `assets/matrix-contributions.svg`

The live asset generator reads only GitHub public profile/repository/event/contribution information.

## Deploy

Create the public profile repository:

`Cyanex1702/Cyanex1702`

Push this package's contents to the root of that repo.

Then:

1. Open **Actions**.
2. Run **Generate Matrix Contribution Snake** once.
3. Run **Refresh Live Terminal Assets** once.
4. Reload the public profile.

After that both workflows refresh themselves automatically.

No personal access token needs to be stored in the repository.
The workflows use GitHub's repository-provided `GITHUB_TOKEN`.
